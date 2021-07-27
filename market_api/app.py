import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from config import user_name, p_word
import pandas as pd

from flask import Flask, jsonify
from flask_cors import CORS


#################################################
# Database Setup
#################################################
engine = create_engine(f'postgresql://{user_name}:{p_word}@localhost:5432/marketing')


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    # add some information about the api here
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )


@app.route("/agencies")
def names():
    
    #find my own record
    my_city = 'New York'
    my_rank_cat = 'media'
    my_product_cat = 'Retail'

    my_query = f'''
        select a.name as agency_name, a.city, amr.ranking_category, pc.name as product_category, amr.year, amr.points
            from agency as a
            join agency_market_rank amr on
                a.id = amr.agency_id
            join agency_product_category apc on
                a.id = apc.agency_id
            join product_category pc on
                apc.product_category_id = pc.id
            '''

        # where a.city = '{my_city}' and amr.ranking_category = '{my_rank_cat}' and pc.name = '{my_product_cat}'
        # order by a.name, amr.year, amr.ranking_category, amr.points desc
    
    my_record = pd.read_sql(my_query, engine)
    
    print(my_record.columns)
    return my_record.to_json(orient="records")


# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)