# Note: This ran correctly and worked at least once and then broke. Unsure what broke based on bug fixing.
# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine= create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes"""
    return (
        f"This is the Hawaii Climate Analysis API.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """This is the precipitation analysis of the last 12 months"""
    
    #This is the link from Python to the database    
    session = Session(engine)
    
    #Querying the db for rainfall data    
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.date <= "2017-08-23").all()

    #Creating a dict for the rainfall results
    precip_list = []
    for date,prcp in precip_data:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_list.append(precip_dict)

    #Return the rainfall data in a json
    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    """This is a list of all the stations"""
    
    #This is the link from Python to the database    
    session = Session(engine)

    #Creating a list of all the stations
    all_Stations = session.query(Station.Station).all()
    all_Stations_list = list(np.ravel(all_Stations))

    #Return the station data in a json
    return jsonify(all_Stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """This is a list of temperature observations from the most active station from the last year of data"""
    
    #This is the link from Python to the database    
    session = Session(engine)

    #Creating query
    most_active = 'USC00519281'
    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.Station == most_active).all()
    
    most_active_Station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").filter(Measurement.Station == most_active)

    #Creating a list for the tobs info
    station_tobs = []

    for date,tobs in most_active_Station:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        station_tobs.append(tobs_dict)

    #Return the station results in a json
    return jsonify(station_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    """This is the lowest, highest, and average temperature from a specific start date"""

    #This is the link from Python to the database    
    session = Session(engine)

    #This is the query for min, max, avg rainfall
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    #Creating list to store the rainfall query    
    start_tobs = []
    for min,max,avg in results:
        start_tobs_dict = {}
        start_tobs_dict["Min"] = min
        start_tobs_dict["Max"] = max
        start_tobs_dict["Avg"] = avg
        start_tobs.append(start_tobs_dict)
    
    #Return the rainfall results in a json
    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """This is the lowest, highest, and average temperature between specific start and end dates"""
    
    #This is the link from Python to the database    
    session = Session(engine)

    #This is the query for min, max, avg rainfall for a date span
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    #Creating list to store the rainfall and date query    
    start_end_tobs = []
    for min,max,avg in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["Min"] = min
        start_end_tobs_dict["Max"] = max
        start_end_tobs_dict["Avg"] = avg
        start_end_tobs.append(start_end_tobs_dict)

    #Return the rainfall results in a json
    return jsonify(start_end_tobs)