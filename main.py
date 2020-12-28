from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
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


    def to_dict(self):

        result = {}

        for column in self.__table__.columns:
            result[column.name] = getattr(self,column.name)

        return result



@app.route("/")
def home():
    return render_template("index.html")



@app.route('/add',methods=['POST'])
def add():

    name = request.form['name']
    map_url = request.form['map_url']
    img_url = request.form['img_url']
    location = request.form['location']
    seats = request.form['seats']
    has_toilet = request.form['toilet']
    has_wifi = request.form['wifi']
    has_sockets = request.form['sockets']
    can_take_calls = request.form['calls']
    coffee_price = request.form['price']




    new_cafe = Cafe(name=name,map_url=map_url,img_url=img_url,location=location,seats=seats,has_toilet=has_toilet,has_wifi=has_wifi,has_sockets=has_sockets,can_take_calls=can_take_calls,coffee_price=coffee_price)

    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/random")
def random_cafe():

    cafes = Cafe.query.all()
    cafe = random.choice(cafes)

    return jsonify(cafe=cafe.to_dict())

@app.route("/all")
def all_cafes():

    cafes = Cafe.query.all()


    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

@app.route("/search")
def search():

    location = request.args.get('loc')

    location = location.title()


    cafe = Cafe.query.filter_by(location=location).first()


    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={'Not Found': 'Sorry, we don\'t have a cafe at that location.'}),404

@app.route('/update/<int:cafe_id>',methods=['PATCH'])
def update_price(cafe_id):

    new_price = request.args.get('new_price')


    cafe = Cafe.query.get(cafe_id)

    if cafe:
        cafe.coffee_price = new_price

        db.session.commit()

    
        return jsonify(success='Successfully updated the price.'),200
    else:
        return jsonify(error={'Not Found': 'Sorry a cafe with that id was not found in the database.'}),404


@app.route('/report-closed/<int:cafe_id>',methods=['DELETE'])
def delete_cafe(cafe_id):

    
    correct_api_key = 'TopSecretAPIKey'
    api_key = request.args.get('api-key')
    cafe = Cafe.query.get(cafe_id)


    if cafe:

        if api_key == correct_api_key:
            db.session.delete(cafe)

            db.session.commit()
            return jsonify(success='Successfully deleted cafe.'),200
        else:
            return jsonify(error={'Invalid Key': 'Sorry, your API key is not valid'}),403

    
    else:
        return jsonify(error={'Not Found': 'Sorry a cafe with that id was not found in the database.'}),404









## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
