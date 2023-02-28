from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
import psycopg2
DB_CONFIG = {
    "database": "pop_guinea",
    "username": "postgres",
    "password": "Diallo10",
    "host": "localhost",
    "port": "5432"}

# Notice, normally this is set with environment variables on the server
# machine do avoid exposing the credentials. Something like
# DB_CONFIG = {}
# DB_CONFIG['database'] = os.environ.get('DATABASE')
# DB_CONFIG['username'] = os.environ.get('USERNAME')
# ...

# Create a flask application
app = Flask(__name__)

# # Set the database connection URI in the app configuration

username = DB_CONFIG['username']
password = DB_CONFIG['password']
host = DB_CONFIG['host']
port = DB_CONFIG['port']
database = DB_CONFIG['database']

# database_uri = {f"postgresql://username:password@host:port/database"} 
database_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # Create object to control SQLAlchemy from the Flask app
db = SQLAlchemy(app)

# # Create a data model object that matches our database
# Matches rides_geojson view 

# Matches sa.rides table 
class Population(db.Model):
    __tablename__ = "gin_adm2"
    __table_args__ = {"schema": "public"}
    Prefecture = db.Column(db.Text(20), primary_key=True)
    geometry = db.Column(db.Float()) 
    area = db.Column(db.Float()) 
    Status = db.Column(db.Text(20))
    Population_2014 = db.Column(db.Integer)
    density_2014 = db.Column(db.Float())   
# Create the REST/CRUD endpoints
# GET method to get a single ride using it's id from the rides_geojson view
    

@app.route('/populations/<Prefecture>', methods=['GET'])
def get_pop(Prefecture):
    pop = Population.query.get(Prefecture) 
    del pop.__dict__['_sa_instance_state']
    return jsonify(pop.__dict__)

# GET method to get all rides from the rides_geojson view
@app.route('/populations', methods=['GET'])
def get_populations():
    populations = []
    for population in db.session.query(Population).all():
        del population.__dict__['_sa_instance_state']
        populations.append(population.__dict__)
    return jsonify(populations) 
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) 

# import requests

# response = requests.get('http://127.0.0.1:5000/')
# print(response.text) 
# if __name__ == '__main__':
#       app.run(debug=True, port=8443)
# if __name__ == '__main__':
#     app.run(debug=True, port = 5432)