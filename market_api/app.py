from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from config import user_name, p_word
import pandas as pd

from flask import Flask, jsonify, render_template
from flask_cors import CORS


# Database Setup
engine = create_engine(f'postgresql://{user_name}:{p_word}@localhost:5432/marketing')

# sql queries
select_agency = f'''
    select a.name, a.city, a.country, amr.ranking_category, pc.name as product_category, amr.year, amr.points
	from agency as a
	join agency_market_rank amr on
		a.id = amr.agency_id
	join agency_product_category apc on
		a.id = apc.agency_id
	join product_category pc on
		apc.product_category_id = pc.id
    '''
order_by_agency = "order by amr.year desc, amr.ranking_category, amr.points desc, a.name"

select_brand = f'''
    select bmr.brand, bmr.ranking_category, pc.name as product_category, bmr.year, bmr.points
	from brand_market_rank as bmr
	join brand_product_categories bpc on
		bmr.brand = bpc.brand
	join product_category pc on
		bpc.product_category_id = pc.id
'''
order_by_brand = "order by bmr.year desc, bmr.ranking_category, bmr.points desc, bmr.brand"

# Flask Setup
app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)


# Flask Routes

# index.html route
@app.route("/")
def index():
    return render_template("index.html")

# agencies_data.html route
@app.route("/agencies_data")
def agencies_data():
    return render_template("index.html")

# brands_data.html route
@app.route("/brands_data")
def brands_data():
    return render_template("brands.html")

# agencies api route returns json agencies data
@app.route("/agencies")
def agencies():
    
    my_record = pd.read_sql(select_agency + order_by_agency, engine)
    
    print(my_record.columns)
    return my_record.to_json(orient="records")

# agencies api filters the data based on user selections returns json
@app.route("/agencies/<my_city>/<my_country>/<my_rank_cat>/<my_prod_cat>")
def a_filtered(my_city=None, my_country=None, my_rank_cat=None, my_prod_cat=None):
    print(my_city, my_rank_cat, my_prod_cat)

    filters = []    
    if my_city != "all":
        filters.append(f"a.city = '{my_city}'")
    if my_country != "all":
        filters.append(f"a.country = '{my_country}'")
    if my_rank_cat != "all":
        filters.append(f"amr.ranking_category = '{my_rank_cat}'")
    if my_prod_cat != "all":
        filters.append(f"pc.name = '{my_prod_cat}'")
    

    if filters:
        where = " and ".join(filters)

        my_record = pd.read_sql(f'{select_agency} where {where} {order_by_agency}', engine)
        print(my_record.columns)
        return my_record.to_json(orient="records")
    else:
        my_record = pd.read_sql(select_agency + order_by_agency, engine)
    
        print(my_record.columns)
        return my_record.to_json(orient="records")



# api brands route returns all agencies - initial json data
@app.route("/brands")
def brands():
    
    my_record = pd.read_sql(select_brand + order_by_brand, engine)
    
    print(my_record.columns)
    return my_record.to_json(orient="records")

# agencies filters the data based on user selections
@app.route("/brands/<my_brand>/<my_rank_cat>/<my_prod_cat>")
def b_filtered(my_brand=None, my_rank_cat=None, my_prod_cat=None):
    print(my_brand, my_rank_cat, my_prod_cat)

    filters = []    
    if my_brand != "all":
        filters.append(f"bmr.brand = '{my_brand}'")
    if my_rank_cat != "all":
        filters.append(f"bmr.ranking_category = '{my_rank_cat}'")
    if my_prod_cat != "all":
        filters.append(f"pc.name = '{my_prod_cat}'")
    

    if filters:
        where = " and ".join(filters)

        my_record = pd.read_sql(f'{select_brand} where {where} {order_by_brand}', engine)
        print(my_record.columns)
        return my_record.to_json(orient="records")
    else:
        my_record = pd.read_sql(select_brand + order_by_brand, engine)
    
        print(my_record.columns)
        return my_record.to_json(orient="records")

if __name__ == '__main__':
    app.run(debug=True)

