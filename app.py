import os
import click

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

@app.route("/")
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

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

