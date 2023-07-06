#!/usr/bin/env python3

# server/app.py
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db revision --autogenerate -m 'Create tables' 
# flask db upgrade 
# Standard imports/boilerplate setup
import os
from dotenv import load_dotenv
import psycopg2

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Pet, Owner

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->
# Load the environment variables from the .env file:
load_dotenv()  # take environment variables from .env.

# Get the environment variables:
user = os.getenv('POSTGRESQL_USER')
password = os.getenv('POSTGRESQL_PASSWORD')
host = os.getenv('POSTGRESQL_HOST')
port = os.getenv('POSTGRESQL_PORT')
database = os.getenv('POSTGRESQL_DB')

# Create the connection string:
connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

#------------------------------------------------------------------>

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Restful setup
api = Api(app)

@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    return response

@app.route('/hello', methods=['GET','POST'])
def hello():
    method = request.method
    if method == "GET":
        return {"Hello":True}
    elif method == "POST":
        return {"Hello":False}

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if not pet:
        response_body = '<h1>404 pet not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''
    
    response = make_response(response_body, 200)

    return response

@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()

    if not owner:
        response_body = '<h1>404 owner not found</h1>'
        response = make_response(response_body, 404)
        return response

    response_body = f'<h1>Information for {owner.name}</h1>'
    
    pets = [pet for pet in owner.pets]
    
    if not pets:
        response_body += f'<h2>Has no pets at this time.</h2>'

    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    response = make_response(response_body, 200)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)