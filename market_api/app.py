from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from config import user_name, p_word
import pandas as pd

from flask import Flask, jsonify
from flask_cors import CORS


# Database Setup
engine = create_engine(f'postgresql://{user_name}:{p_word}@localhost:5432/marketing')



# Flask Setup

app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

# Flask Routes

@app.route("/")
def welcome():
    # add some information about the api here
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )


base_query = f'''
        select a.name as agency_name, a.city, amr.ranking_category, pc.name as product_category, amr.year, amr.points
            from agency as a
            join agency_market_rank amr on
                a.id = amr.agency_id
            join agency_product_category apc on
                a.id = apc.agency_id
            join product_category pc on
                apc.product_category_id = pc.id
            '''
order_by = "order by a.name, amr.year, amr.ranking_category, amr.points desc"

@app.route("/agencies")
def names():
    
    my_record = pd.read_sql(base_query + order_by, engine)
    
    print(my_record.columns)
    return my_record.to_json(orient="records")


@app.route("/agencies/<my_city>/<my_rank_cat>/<my_prod_cat>")
def filtered(my_city=None, my_rank_cat=None, my_prod_cat=None):
    print(my_city, my_rank_cat, my_prod_cat)

    filters = []    
    if my_city != "all":
        filters.append(f"a.city = '{my_city}'")
    if my_rank_cat != "all":
        filters.append(f"amr.ranking_category = '{my_rank_cat}'")
    if my_prod_cat != "all":
        filters.append(f"pc.name = '{my_prod_cat}'")
    

    if filters:
        where = " and ".join(filters)

        my_record = pd.read_sql(f'{base_query} where {where} {order_by}', engine)
        print(my_record.columns)
        return my_record.to_json(orient="records")
    else:
        my_record = pd.read_sql(base_query + order_by, engine)
    
        print(my_record.columns)
        return my_record.to_json(orient="records")

if __name__ == '__main__':
    app.run(debug=True)