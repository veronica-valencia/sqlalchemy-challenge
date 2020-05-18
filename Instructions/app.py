import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station= Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

"""Return a list of Dates adn precipitation information"""

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp.filter(Measurement.date>='2016-08-23').order_by(Measurement.date))
    session.close()

    precipitation_scores= []
    for s in results:
            precipitation_dict={}
            precipitation_dict["date"]= s.date
            precipitation_dict["prcp"]=s.prcp
            precipitation_scores.append(precipitation_dict)
    return jsonify(precipitation_scores)
                            

   
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations names"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))
    return jsonify(station_names)
                            
        

@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature for the previous year"""
    # Query all passengers
    results = session.query(Measurement.tobs).all()

    session.close()

 # Convert list of tuples into normal list
    temp_values = list(np.ravel(results))

    return jsonify(temp_values)


@app.route("/api/v1.0/<start>")
def temperature_start():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
             filter(Measurement.date>=start).all()


    session.close()
 # Convert list of tuples into normal list
    temperature_start = list(np.ravel(results))

    return jsonify(temperature_start)
                            

@app.route("/api/v1.0/<start>/<end>")
def temperature_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
             filter(Measurement.date>= start).\
             filter(Measurement.date<=end).all()


    session.close()
 # Convert list of tuples into normal list
    temperature_end = list(np.ravel(results))

    return jsonify(temperature_end)
                            

if __name__ == '__main__':
    app.run(debug=True)
