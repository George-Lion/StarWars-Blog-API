"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Vehicles, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

#CHARACTERS [GET] /people

@app.route("/characters", methods=["GET"])
def get_characters():
    users = Characters.query.all()
    character_1_serialized = list(map(lambda people: people.serialize(), users))
    return jsonify({"result": character_1_serialized}), 200

@app.route("/character/<int:oneCharacter_id>", methods=["GET"])
def get_oneCharacter(oneCharacter_id):
    character = Characters.query.filter_by(id=oneCharacter_id).first()
    return jsonify({"result": character.serialize()}), 200

#PLANETS [GET] /planets

@app.route("/planets", methods=["GET"])
def get_planets():
    users = Planets.query.all()
    planets_serialized = list(map(lambda planet: planet.serialize(), users))
    return jsonify({"result": planets_serialized}), 200

@app.route("/planet/<int:onePlanet_id>", methods=["GET"])
def get_onePlanet(onePlanet_id):
    planets = Planets.query.filter_by(id=onePlanet_id).first()
    return jsonify({"result": planets.serialize()}), 200

#VEHICLES [GET] /vehicles

@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    users = Vehicles.query.all()
    vehicles_serialized = list(map(lambda vehicle: vehicle.serialize(), users))
    return jsonify({"result": vehicles_serialized}), 200

@app.route("/vehicle/<int:oneVehicle_id>", methods=["GET"])
def get_onevehicle(oneVehicle_id):
    vehicles = Vehicles.query.filter_by(id=oneVehicle_id).first()
    return jsonify({"result": vehicles.serialize()}), 200

#USERS [GET] /user
    
@app.route("/users", methods=["GET"])
def get_user():
    users = User.query.all()
    users_serialized = list(map(lambda people: people.serialize(), users))
    return jsonify({"result": users_serialized}), 200

@app.route("/user/favorites", methods=["GET"])
def get_oneUser(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify({"result": user.favorites}), 200

# POST

@app.route("/users", methods=["POST"])
def create_user():
    body_username = request.json.get("username") 
    body_email = request.json.get("email")
    user = User(username = body_username, email = body_email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"created": True, "user": user.username}), 200

@app.route("/users/<int:us_id>/favorite/character/<int:ch_id>", methods=["POST"])
def favorite_people(ch_id, us_id):
    user = User.query.get(us_id)
    new_fav = Favorites(user_id = us_id, character_id = ch_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"created": True, "people": new_fav.serialize()}), 200

#DELETE

@app.route("/characters/<int:people_id>", methods=["DELETE"])
def delete_characters(people_id):
    people = Characters.query.filter_by(id=people_id).first()
    db.session.delete(people)
    db.session.commit()
    return jsonify({"deleted": True}), 200

@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planets(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"deleted": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)