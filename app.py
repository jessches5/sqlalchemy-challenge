import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
MS = Base.classes.measurement
ST = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list """
    # Query all passengers
    results = session.query(MS.date, MS.prcp).all()

    session.close()

# Create a dictionary from the row data and append to a list 
    all_prcp = []
    for date, precipitation in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = precipitation
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations """
    # Query all stations
    results = session.query(MS.station).all()

    session.close()

    # Create a list of all_stations
    all_stations = []
    for station in results:
        st_dict = {}
        st_dict["station"] = station
        all_stations.append(st_dict)
        
        return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations """
    # Query all dates and temperature observations of the most active station for the last year of data
    results = session.query(MS.date, MS.tobs).filter(MS.station == 'USC00519281').all()

    session.close()

    # Create a list of all_stations
    active_station = []
    for date, tobs in results:
        active_dict = {}
        active_dict["date"] = date
        active_dict["tobs"] = tobs
        active_station.append(active_dict)
        
        return jsonify(active_station)

if __name__ == '__main__':
    app.run(debug=True)

