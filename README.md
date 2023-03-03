# Population_Guinea_2014

# ETL_population_guinea
This code reads population data for Guinea from an Excel file and shapefile data for Guinea from a shapefile. It performs some data cleaning and manipulation, including reprojecting the shapefile to a projected coordinate system and calculating population density. It then creates a choropleth map of population density in Guinea and another choropleth map of population by prefecture, with prefecture names as labels. Finally, it sends the data to a PostgreSQL database.


# API

This is a Flask application that defines two endpoints to interact with a PostgreSQL database. The database stores population data for different prefectures in Guinea. The application uses the Flask framework along with SQLAlchemy to interact with the database. The SQLAlchemy ORM is used to define a data model that matches the database schema and to execute CRUD operations on the data.

The first endpoint, /populations/<Prefecture>, is a GET endpoint that retrieves the population data for a single prefecture specified in the URL. It queries the database for a row with a matching primary key (Prefecture) and returns the result as a JSON object.

The second endpoint, /populations, is also a GET endpoint that retrieves all the population data from the table. It queries the database for all rows in the table, removes the SQLAlchemy-specific '_sa_instance_state' attribute from each object, and returns the results as a JSON object.

The application runs in debug mode and listens on all available network interfaces. It uses the database connection details provided in the DB_CONFIG dictionary to connect to the PostgreSQL server.
This code defines a Flask application and connects it to a PostgreSQL database using SQLAlchemy. It then defines a data model object called "Population" that maps to a PostgreSQL table called "gin_adm2". The code provides two REST/CRUD endpoints - one to retrieve a single population record by Prefecture name, and another to retrieve all population records. The code also sets up the app configuration and starts the Flask application in debug mode.
This code is a Python program that uses the Flask web framework to create a web application that accesses and displays data about the population of Guinea. It defines a SQLAlchemy database model for the population data and has routes to initialize the database and retrieve population data by prefecture. The code also defines routes to retrieve data about all countries in a SQLite database and to render a template for a web page.
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
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
    # geometry = db.Column(db.Float()) 
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






# DB1_pop_guinea

This is a SQL script that creates a table called gin_adm2 in the public schema with the following columns:
Prefecture: a text column representing the name of a prefecture.
geometry: a geometry column that stores geometries in EPSG 31528 projection.
area: a double precision column representing the area of a prefecture in square meters.
Status: a text column representing the status of a prefecture.
Population_2014: a bigint column representing the population of a prefecture in 2014.
density_2014: a double precision column representing the population density of a prefecture in 2014.
The script also creates an index called idx_gin_adm2_geometry on the geometry column using a GiST (Generalized Search Tree) index. The purpose of this index is to speed up queries that involve spatial data, such as finding all the prefectures that intersect a given polygon.

Script:
-- Table: public.gin_adm2

-- DROP TABLE IF EXISTS public.gin_adm2;

CREATE TABLE IF NOT EXISTS public.gin_adm2
(
    "Prefecture" text COLLATE pg_catalog."default",
    geometry geometry(Geometry,31528),
    area double precision,
    "Status" text COLLATE pg_catalog."default",
    "Population_2014" bigint,
    density_2014 double precision
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.gin_adm2
    OWNER to postgres;
-- Index: idx_gin_adm2_geometry

-- DROP INDEX IF EXISTS public.idx_gin_adm2_geometry;

CREATE INDEX IF NOT EXISTS idx_gin_adm2_geometry
    ON public.gin_adm2 USING gist
    (geometry)
    TABLESPACE pg_default;
# Requirements
These are Python packages/libraries:

geopandas: a library to work with geospatial data, particularly geospatial data in GeoJSON format.
pandas: a library for data manipulation and analysis.
ipykernel: a kernel for Jupyter notebooks, used to execute Python code in Jupyter notebooks.
requests: a library for sending HTTP requests and handling HTTP responses.
SQLAlchemy: a library for working with databases using Python, particularly for creating SQL queries and connecting to a database server.
psycopg2: a library for working with PostgreSQL databases using Python.
GeoAlchemy2: a library for working with geospatial data in SQL databases using SQLAlchemy.
numpy: a library for numerical computing in Python.
jsonify: a method for serializing JSON data in Flask.
flask-sqlalchemy: a Flask extension for working with SQL databases using SQLAlchemy.

# Map density population
This code block creates a choropleth map of population density by prefecture in Guinea using the density_2014 column previously created. It also adds prefecture name labels and sets the title and axis labels. The resulting map will show the relative population densities of each prefecture in Guinea.
# Create a new figure and axis
fig, ax = plt.subplots(figsize=(10,10))

# Plot the density choropleth
gin_prefectures.plot(column='density_2014', legend= True, cmap='nipy_spectral_r', ax=ax)

# Add prefecture name labels
gin_prefectures.apply(lambda x: ax.annotate(s=x.Prefecture, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)

# Set the title and axis labels
ax.set_title('Population by Prefecture in Guinea (2014)')  
ax.set_xlabel('Longitude') 
ax.set_ylabel('Latitude')

# Show the plot
plt.show()
# Map population
This code plots a choropleth map of Guinea showing the population of each prefecture in 2014. The code uses the plot method of a GeoDataFrame, passing in the column to use for coloring the map (Population_2014), the color map (nipy_spectral_r), and the axis to use (ax). The apply method is used to add labels to each prefecture using the prefecture name and the centroid of the geometry. Finally, the title and axis labels are set using the set_title, set_xlabel, and set_ylabel methods of the axis object.
# Create a new figure and axis
fig, ax = plt.subplots(figsize=(10,10))

# Plot the density choropleth
gin_prefectures.plot(column='Population_2014', legend= True, cmap='nipy_spectral_r', ax=ax)

# Add prefecture name labels
gin_prefectures.apply(lambda x: ax.annotate(s=x.Prefecture, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)

# Set the title and axis labels
ax.set_title('Population by Prefecture in Guinea (2014)')  
ax.set_xlabel('Longitude') 
ax.set_ylabel('Latitude')

# Show the plot
plt.show()
# Map area
This code plots the choropleth map for the column 'area'. This means that the map is showing the spatial distribution of the area of the prefectures in Guinea.
# Create a new figure and axis
fig, ax = plt.subplots(figsize=(10,10))

# Plot the density choropleth
gin_prefectures.plot(column='area', legend= True, cmap='nipy_spectral', ax=ax)

# Add prefecture name labels
gin_prefectures.apply(lambda x: ax.annotate(s=x.Prefecture, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)

# Set the title and axis labels
ax.set_title('Population by Prefecture in Guinea (2014)')  
ax.set_xlabel('Longitude') 
ax.set_ylabel('Latitude')

# Show the plot
plt.show()
