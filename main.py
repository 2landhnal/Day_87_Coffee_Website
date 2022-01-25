from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, URLField, IntegerField, BooleanField, validators
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL1', "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

class Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    map_url = URLField('URL Map', validators=[validators.URL(), DataRequired()])
    img_url = URLField('URL Image', validators=[validators.URL(), DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    has_toilet = BooleanField('Toilet', validators=[DataRequired()])
    has_wifi = BooleanField('Wifi', validators=[DataRequired()])
    has_sockets = BooleanField('Socket', validators=[DataRequired()])
    can_take_calls = BooleanField('Can take Calls', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

db.create_all()

@app.route('/')
def home():
    cafes = Cafe.query.all()
    c0 = cafes[0]
    cafes = cafes[1:]
    return render_template('index.html', cafes=cafes, c0=c0)

@app.route('/add', methods=['POST', 'GET'])
def add():
    form = Form()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            seats = form.seats.data,
            has_toilet = form.has_toilet.data,
            has_wifi = form.has_wifi.data,
            has_sockets = form.has_sockets.data,
            can_take_calls = form.can_take_calls.data,
            coffee_price = form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html', form=form)

@app.route("/delete/<int:id>", methods=['POST', 'GET'])
def delete(id):
    cafe_to_delete = Cafe.query.get(id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)