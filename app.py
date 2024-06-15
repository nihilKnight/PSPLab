import os
import click

from flask import Flask, request, flash, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sk-f3e4a18e1d7834127f2add7d4ce85169d34de28e91eb24c1b82586bb001e55a1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    account = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10))  # 'Customer' or 'Saler'

class Customer(User):
    __mapper_args__ = {
        'polymorphic_identity': 'Customer',
    }

class Saler(User):
    __mapper_args__ = {
        'polymorphic_identity': 'Saler',
    }
    products = db.relationship('Product', back_populates='manager', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manager = db.relationship('Saler', back_populates='products')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer, nullable=False)

    agent = db.relationship('Saler', foreign_keys=[agent_id])
    buyer = db.relationship('Customer', foreign_keys=[buyer_id])



@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        user = User(name=title+year)
        if len(User.query.filter(User.name==user.name).all()) > 0:
            flash('Name has been registered!')
            return redirect(url_for('index'))

        db.session.add(user)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    users = User.query.all()
    return render_template('index.html', users=users)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')

        user = User.query.filter_by(account=account).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful.')
            return redirect(url_for('index'))
        else:
            flash('Invalid account or password.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        account = request.form.get('account')
        password = request.form.get('password')
        user_type = request.form.get('type')

        if user_type == 'Customer':
            user = Customer(name=name, account=account, password=generate_password_hash(password), type=user_type)
        elif user_type == 'Saler':
            user = Saler(name=name, account=account, password=generate_password_hash(password), type=user_type)

        if User.query.filter_by(account=account).first():
            flash('Account has been registered!')
            return redirect(url_for('register'))

        db.session.add(user)
        db.session.commit()

        flash('Registration successful.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        name = request.form.get('name')
        account = request.form.get('account')
        password = request.form.get('password')

        current_user.name = name
        current_user.account = account
        if password:
            current_user.password = generate_password_hash(password)
        
        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('index'))

    return render_template('edit.html')


@app.route("/products")
@login_required
def products():
    if current_user.type != 'Saler':
        flash('You do not have access to this page.')
        return redirect(url_for('index'))
    products = Product.query.filter_by(manager_id=current_user.id).all()
    return render_template('products.html', products=products)


@app.route("/product/new", methods=['GET', 'POST'])
@login_required
def new_product():
    if current_user.type != 'Saler':
        flash('You do not have access to this page.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        origin = request.form.get('origin')
        inventory = request.form.get('inventory')
        
        product = Product(name=name, price=price, origin=origin, inventory=inventory, manager_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.')
        return redirect(url_for('products'))

    return render_template('new_product.html')


@app.route("/product/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if product.manager_id != current_user.id:
        flash('You do not have access to this page.')
        return redirect(url_for('products'))

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.origin = request.form.get('origin')
        product.inventory = request.form.get('inventory')

        db.session.commit()
        flash('Product updated successfully.')
        return redirect(url_for('products'))

    return render_template('edit_product.html', product=product)


@app.route("/product/delete/<int:id>")
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    if product.manager_id != current_user.id:
        flash('You do not have access to this page.')
        return redirect(url_for('products'))

    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.')
    return redirect(url_for('products'))


@app.route("/salers")
@login_required
def salers():
    if current_user.type != 'Customer':
        flash('You do not have access to this page.')
        return redirect(url_for('index'))
    salers = Saler.query.filter_by(type='Saler').all()
    return render_template('salers.html', salers=salers)


@app.route("/saler/<int:id>")
@login_required
def saler_detail(id):
    saler = Saler.query.get_or_404(id)
    products = Product.query.filter_by(manager_id=saler.id).all()
    return render_template('saler_detail.html', saler=saler, products=products)


@app.route("/buy/<int:product_id>", methods=['GET', 'POST'])
@login_required
def buy(product_id):
    if current_user.type != 'Customer':
        flash('You do not have access to this page.')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        amount = int(request.form.get('amount'))
        if amount > product.inventory:
            flash('Not enough inventory.')
            return redirect(url_for('buy', product_id=product_id))

        product.inventory -= amount
        order = Order(agent_id=product.manager_id, buyer_id=current_user.id, amount=amount)
        db.session.add(order)
        db.session.commit()
        flash('Purchase successful.')
        return redirect(url_for('saler_detail', id=product.manager_id))

    return render_template('buy.html', product=product)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
        click.echo('Dropped previous database.')
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    names = ['Alice', 'Bob', 'Eve', 'David']

    for name in names:
        db.session.add(User(name=name))
    db.session.commit()
    click.echo('Done.')

