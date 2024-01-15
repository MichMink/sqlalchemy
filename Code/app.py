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
Base.prepare(autoload_with=engine)

# Save reference to the table
M=Base.classes.measurement
S=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h2>Available routes:</h2>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0[start]<br>"
        f"/api/v1.0/[start]/[end]"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    results=session.query(M.date, M.prcp).filter(M.date>="2016-08-23").all()

    return {d:p for d,p in results}

@app.route('/api/v1.0/stations')
def stations():
    session=Session(engine)
    results=session.query(S.station, S.name).all()
    return {s:l for s,l in results}


@app.route('/api/v1.0/tobs')
def station():
    session=Session(engine)
    results=session.query( M.date, M.tobs).filter((M.date>="2016-08-23")&(M.station=="USC00519281")).all()
    return {t:s for t,s in results}

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def date_range(start,end='2017-08-23'):
    session=Session(engine)
    join=session.query(func.min(M.tobs),func.avg(M.tobs),func.max(M.tobs)).filter((M.date>=start)&(M.date<=end)).first()

    print("data:",join)
    return {"min":join[0],"avg":join[1],"max": join[2]}

if __name__ == '__main__':
    app.run(debug=True)
