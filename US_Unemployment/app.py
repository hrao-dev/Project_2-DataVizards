# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,send_file,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

import sys
print(sys.path)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///static/assets/data/us_unemployment.db"

# # Remove tracking modifications
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# from .models import census
try:
    # Assume we're a sub-module in a package.
    from .models import *
except ImportError:
     from models import *


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/demographics/")
def demographics():
    return render_template("demographics.html")

@app.route("/industry_stats/")
def industry_stats():
    return render_template("industry_stats.html")

@app.route("/references/")
def datasources():
    return render_template("references.html")

@app.route("/census_data/")
def census_data():
    results = db.session.query(census.state, census.variable, census.value).order_by(census.state,census.variable).all()
    census_data = []
    for result in results:
        census_data.append({
            'state': result[0],
            'year':result[1],
            'value':result[2]
        })
   
    # print(jsonify(census_data))
    return jsonify(census_data)

@app.route("/unemployment_claims/")
def unemploymentClaimsdata():
    results = db.session.query(claims.state, claims.year_month, claims.year, claims.initial_claim,claims.average_insured_unemployment_rate).order_by(claims.state,claims.year_month).all()
    claims_data = []
    for result in results:
        claims_data.append({
            'state':result[0],
            'year_month': result[1],
            'year':result[2],
            'initial_claim':result[3],
            'unemployment_rate':result[4]
        })
    return jsonify(claims_data)

# @app.route("/api/states")
# def states_json():
#     print("hello")
#     return send_file('/static/js/us-states.geojson',mimetype='application/json')    

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True    
    app.run()

