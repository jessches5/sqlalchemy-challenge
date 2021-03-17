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
        f"/api/v1.0/tobs"
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
    results = session.query(ST.station, ST.name).all()

    session.close()

    # Create a list of all_stations
    all_stations = []
    for station, name in results:
        st_dict = {}
        st_dict["station"] = station
        st_dict["name"] = name
        all_stations.append(st_dict)
        
        return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)

