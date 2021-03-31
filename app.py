# Dependencies and Setup
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///D:\Data Science\HW\8-SQLAlchemy\hawaii-weather-analysis\Resources\hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Calculate the date from 1 year ago
    one_year = dt.date(2017, 8, 23) - dt.datetime(days)

    # Query date and prcp
    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).all()

    # Create a dictionary from results
    precipitation_dict = {}
    for date, prcp in prcp_scores:
        precipitation_dict[date] = prcp
    
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():

    # Query stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query one year of temperature observations from the most active station
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year).all()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs=tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    
    # Query the min. max, and average tobs for a given start and start-end dates 
    sel = [func.min(Measurement.tobs),
      func.avg(Measurement.tobs),
      func.max(Measurement.tobs)]
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    results = session.query(*sel).\
        filter(Measurement.date >= start_date).all()

    # List of temp min, avg, and max
    start_tobs = list(np.ravel(results))

    return jsonify(start_tobs=start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    # Query the min. max, and average tobs for a given start and start-end dates 
    sel = [func.min(Measurement.tobs),
      func.avg(Measurement.tobs),
      func.max(Measurement.tobs)]
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    
    results = session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    # List of temp min, avg, and max
    start_end_tobs = list(np.ravel(results))

    return jsonify(start_end_tobs=start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)
