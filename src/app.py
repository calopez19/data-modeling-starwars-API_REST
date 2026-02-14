"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorite_people, Favorite_planets
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()

    if not body.get("email") or not body.get("password") or not body.get("username"):
        return jsonify({"msg": "Email, password y username son requeridos"}), 400

    user_email_exists = User.query.filter_by(email=body['email']).first()
    user_name_exists = User.query.filter_by(email=body['username']).first()
    if user_email_exists or user_name_exists:
        return jsonify({"msg": "Ese correo electrónico o el usurio ya está registrado"}), 409

    user = User()
    user.username = body.get('username')
    user.email = body.get('email')
    user.password = body.get('password')
    user.is_active = True

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 200


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": f"Usuario {user_id} eliminado"}), 200


@app.route('/users', methods=['GET'])
def users_list():

    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    response_body = {
        "msg": "Lista de Usuarios",
        "users": users
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def people_list():
    people = People.query.all()
    people = list(map(lambda people: people.serialize(), people))

    response_body = {
        "msg": "Lista de Personajes",
        "personajes": people
    }

    return jsonify(response_body), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def people(people_id):
    people = User.query.get(people_id)
    if people is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404

    people_exist = User.query.filter_by(id=people_id).first()
    response_body = {
        "personajes": people_exist
    }
    return jsonify(response_body), 200


@app.route('/planet', methods=['GET'])
def planet_list():
    planet = Planets.query.all()
    planet = list(map(lambda planet: planet.serialize(), planet))

    response_body = {
        "msg": "Lista de Planetas",
        "Planetas": planet
    }

    return jsonify(response_body), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()

    if not body or "name" not in body:
        return jsonify({"msg": "El nombre del planeta es obligatorio"}), 400

    planet_exists = Planets.query.filter_by(name=body['name']).first()
    if planet_exists:
        return jsonify({"msg": "Este planeta ya está registrado"}), 400

    new_planet = Planets()
    new_planet.name = body.get("name"),
    new_planet.rotation_period = body.get("rotation_period"),
    new_planet.orbital_period = body.get("orbital_period"),
    new_planet.diameter = body.get("diameter"),
    new_planet.climate = body.get("climate"),
    new_planet.gravity = body.get("gravity"),
    new_planet.terrain = body.get("terrain"),
    new_planet.surface_water = body.get("surface_water"),
    new_planet.population = body.get("population")

    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201


@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def user_favorite(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "usuario no encontrado"}), 404

    favorites = Favorite_people.query.get(user_id)
    if favorites is None:
        return jsonify({"msg": "usuario sin favoritos"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
