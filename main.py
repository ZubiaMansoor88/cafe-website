from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()

#Create Form
class CafeForm(FlaskForm):
    name = StringField(label='Cafe Name', validators=[DataRequired()])
    location = StringField(label='Location', validators=[DataRequired()])
    map_url = StringField(label='Location on Google Map', validators=[DataRequired(), URL()])
    img_url = StringField(label='Cafe Image', validators=[DataRequired(), URL()])
    seats = StringField(label='Number of Seats', validators=[DataRequired()])
    coffee_price = StringField(label='Cafe Price', validators=[DataRequired()])
    sockets = BooleanField('The cafe have socckets available.')
    toilets = BooleanField('The cafe have toilets available.')
    wifi = BooleanField('The cafe have free wifi available.')
    take_calls = BooleanField('The cafe take calls for order booking.')
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all_cafe")
def all_cafe():
    data=[]
    with app.app_context():
        all_cafe = Cafe.query.order_by(Cafe.id).all()
    for coffee in all_cafe:
        data.append(coffee)
    return render_template("cafe_list.html", cafes=data)

@app.route('/cafe/<cafe_id>')
def show_cafe(cafe_id):
    with app.app_context():
        requested_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    return render_template("cafe_detail.html", cafe=requested_cafe)

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = {
            'name': form.name.data,
            'map_url': form.map_url.data,
            'img_url': form.img_url.data,
            'location': form.location.data,
            'has_sockets': form.sockets.data,
            'has_toilet': form.toilets.data,
            'has_wifi': form.wifi.data,
            'can_take_calls': form.take_calls.data,
            'seats': form.seats.data,
            'coffee_price': form.coffee_price.data
        }
        with app.app_context():
            cafe = Cafe(
                name = new_cafe['name'],
                map_url = new_cafe['map_url'],
                img_url = new_cafe['img_url'],
                location = new_cafe['location'],
                has_sockets = new_cafe['has_sockets'],
                has_toilet = new_cafe['has_toilet'],
                has_wifi = new_cafe['has_wifi'],
                can_take_calls = new_cafe['can_take_calls'],
                seats = new_cafe['seats'],
                coffee_price = new_cafe['coffee_price']
            )
            db.session.add(cafe)
            db.session.commit()
        return redirect(url_for('all_cafe'))
    return render_template('add.html', form=form)

@app.route('/delete/<cafe_id>')
def delete_cafe(cafe_id):
    with app.app_context():
        cafe_to_delete = db.session.query(Cafe).filter_by(id=cafe_id).first()
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return redirect(url_for('all_cafe'))
        else:
            return "Post not found", 404


if __name__ == '__main__':
    app.run(debug=True)