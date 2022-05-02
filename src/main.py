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
from models import db, User, Characters
#from models import Person

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

@app.route("/users", methods=["POST"])
def create_user():
    body_username = request.json.get("username") 
    body_email = request.json.get("email")
    user = User(username = body_username, email = body_email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"created": True, "user": user.username}), 200

@app.route("/characters", methods=["POST"])
def create_people():
    body_name = request.json.get("name") 
    body_height = request.json.get("height")
    body_gender = request.json.get("gender")
    people = Characters(name = body_name, height = body_height, gender = body_gender)
    db.session.add(people)
    db.session.commit()
    return jsonify({"created": True, "people": people.name}), 200

@app.route("/characters", methods=["GET"])
def get_characters():
    users = Characters.query.all()
    character_1_serialized = list(map(lambda people: people.serialize(), users))
    return jsonify({"result": character_1_serialized}), 200

@app.route("/character/<int:oneCharacter_id>", methods=["GET"])
def get_oneCharacter(oneCharacter_id):
    character = Characters.query.filter_by(id=oneCharacter_id).first()
    return jsonify({"result": character.serialize()}), 200

""" @app.route("/character/<int:oneCharacter_id>", methods=["GET"])
def get_oneCharacter(oneCharacter_id):
    users = Characters.query.get()
    oneCharacter= Characters.query.filter_by(id=oneCharacter_id).first()
    oneCharacter = Characters.query.filter(Characters.id == oneCharacter_id).first()
    return jsonify({"result": oneCharacter}), 200 """

@app.route("/characters/<string:people_name>", methods=["DELETE"])
def delete_characters(people_name):
    people = Characters.query.filter_by(name=people_name).first()
    db.session.delete(people)
    db.session.commit()
    return jsonify({"deleted": True}), 200


@app.route("/users", methods=["GET"])
def get_user():
    users = User.query.all()
    users_serialized = list(map(lambda people: people.serialize(), users))
    return jsonify({"result": users_serialized}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)