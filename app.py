import os
import click
import random
import string

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from flask import (
        Flask, request, flash, render_template,
        redirect, url_for, session, send_file)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
        LoginManager, login_user, logout_user,
        login_required, current_user, UserMixin)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


######################
#     Setting Up     #
######################


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sk-f3e4a18e1d7834127f2add7d4ce85169d34de28e91eb24c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'\
        + os.path.join(app.root_path, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
# max upload size: 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#################
#     Utils     #
#################


def generate_captcha():
    characters = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choice(characters) for _ in range(6))
    session['captcha'] = captcha_text

    image = Image.new('RGB', (180, 60), 'white')
    font = ImageFont.truetype("static/fonts/arial.ttf", 40)
    draw = ImageDraw.Draw(image)

    draw.text((10, 10), captcha_text, font=font, fill='black')

    buffer = BytesIO()
    image.save(buffer, 'jpeg')
    buffer.seek(0)

    return buffer


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()\
            in ALLOWED_EXTENSIONS


#####################
#     DB Models     #
#####################


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
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manager = db.relationship('Saler', back_populates='products')
    image = db.Column(db.String(200))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    name = db.Column(db.String(100), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer, nullable=False)

    agent = db.relationship('Saler', foreign_keys=[agent_id])
    buyer = db.relationship('Customer', foreign_keys=[buyer_id])


###########################
#     Routing Methods     #
###########################


@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        user = User(name=title+year)
        if len(User.query.filter(User.name == user.name).all()) > 0:
            flash('Name has been registered!')
            return redirect(url_for('index'))

        db.session.add(user)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        captcha = request.form.get('captcha')

        if captcha.lower() != session.get('captcha', '').lower():
            flash('Invalid captcha', 'error')
            return redirect(url_for('login'))

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
            user = Customer(
                    name=name,
                    account=account,
                    password=generate_password_hash(password),
                    type=user_type
                )
        elif user_type == 'Saler':
            user = Saler(
                    name=name,
                    account=account,
                    password=generate_password_hash(password),
                    type=user_type
                )

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

        product = Product(
                name=name,
                price=price,
                origin=origin,
                inventory=inventory,
                manager_id=current_user.id
            )
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


@app.route("/upload_image/<int:product_id>", methods=['POST'])
@login_required
def upload_image(product_id):
    product = Product.query.get_or_404(product_id)
    if product.manager_id != current_user.id:
        flash('You do not have access to this page.')
        return redirect(url_for('products'))

    if 'image' not in request.files:
        flash('No file part')
        return redirect(url_for('products'))

    file = request.files['image']

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('products'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        product.image = filename
        db.session.commit()

        flash('Image uploaded successfully.')
        return redirect(url_for('products'))
    else:
        flash('File type not allowed.')
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
        order = Order(
                name=product.name,
                agent_id=product.manager_id,
                buyer_id=current_user.id,
                amount=amount
            )
        db.session.add(order)
        db.session.commit()
        flash('Purchase successful.')
        return redirect(url_for('saler_detail', id=product.manager_id))

    return render_template('buy.html', product=product)


@app.route("/orders/<int:id>")
@login_required
def orders(id):
    if current_user.type == 'Customer':
        orders = Order.query.filter_by(buyer_id=id).all()
    else:
        orders = Order.query.filter_by(agent_id=id).all()
    return render_template('orders.html', orders=orders)


@app.route('/captcha')
def captcha():
    buffer = generate_captcha()
    return send_file(buffer, mimetype='image/jpeg')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


################################
#     Customed cli command     #
################################


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

    customer = Customer(
            name='Alice',
            account='Alice',
            password=generate_password_hash('Alice'),
            type='Customer'
        )

    saler1 = Saler(
            name='Bob',
            account='Bob',
            password=generate_password_hash('Bob'),
            type='Saler'
        )

    saler2 = Saler(
            name='Eve',
            account='Eve',
            password=generate_password_hash('Eve'),
            type='Saler'
        )

    db.session.add(customer)
    db.session.add(saler1)
    db.session.add(saler2)

    db.session.commit()

    products = [
            Product(
                name='SpongeBob',
                price=100,
                origin='Pineapple House',
                inventory=30,
                manager_id=saler1.id,
                image='spongeBob.jpeg'
            ),
            Product(
                name='Patrick Star ',
                price=80,
                origin='Pineapple House',
                inventory=50,
                manager_id=saler1.id,
                image='patrickStar.jpeg'
            ),
            Product(
                name='Squidward Tentacles',
                price=120,
                origin='Pineapple House',
                inventory=20,
                manager_id=saler1.id,
                image='squidwardTentacles.jpeg'
            ),
            Product(
                name='Mr. Krabs',
                price=85,
                origin='Pineapple House',
                inventory=28,
                manager_id=saler2.id,
                image='MrKrabs.jpeg'
            ),
        ]

    for product in products:
        db.session.add(product)
    db.session.commit()

    orders = [
            Order(
                name=product.name,
                agent_id=product.manager_id,
                buyer_id=customer.id,
                amount=product.inventory//4
            ) for product in products
        ]

    for order in orders:
        db.session.add(order)
    db.session.commit()

    click.echo('Done.')
