# Population_Guinea_2014

# ETL_population_guinea
This code reads population data for Guinea from an Excel file and shapefile data for Guinea from a shapefile. It performs some data cleaning and manipulation, including reprojecting the shapefile to a projected coordinate system and calculating population density. It then creates a choropleth map of population density in Guinea and another choropleth map of population by prefecture, with prefecture names as labels. Finally, it sends the data to a PostgreSQL database.


# API

This is a Flask application that defines two endpoints to interact with a PostgreSQL database. The database stores population data for different prefectures in Guinea. The application uses the Flask framework along with SQLAlchemy to interact with the database. The SQLAlchemy ORM is used to define a data model that matches the database schema and to execute CRUD operations on the data.

The first endpoint, /populations/<Prefecture>, is a GET endpoint that retrieves the population data for a single prefecture specified in the URL. It queries the database for a row with a matching primary key (Prefecture) and returns the result as a JSON object.

The second endpoint, /populations, is also a GET endpoint that retrieves all the population data from the table. It queries the database for all rows in the table, removes the SQLAlchemy-specific '_sa_instance_state' attribute from each object, and returns the results as a JSON object.

The application runs in debug mode and listens on all available network interfaces. It uses the database connection details provided in the DB_CONFIG dictionary to connect to the PostgreSQL server.

# DB_pop_guinea

This is a SQL script that creates a table called gin_adm2 in the public schema with the following columns:
Prefecture: a text column representing the name of a prefecture.
geometry: a geometry column that stores geometries in EPSG 31528 projection.
area: a double precision column representing the area of a prefecture in square meters.
Status: a text column representing the status of a prefecture.
Population_2014: a bigint column representing the population of a prefecture in 2014.
density_2014: a double precision column representing the population density of a prefecture in 2014.
The script also creates an index called idx_gin_adm2_geometry on the geometry column using a GiST (Generalized Search Tree) index. The purpose of this index is to speed up queries that involve spatial data, such as finding all the prefectures that intersect a given polygon.
