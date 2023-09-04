from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from model import get_recommendations
from popular_collab import popular_product
from collab import recProduct

app = Flask(__name__)

data = pd.read_csv("./amazon.csv")
products = pd.read_json('/workspaces/CSE366/Dataset_new/products.json')

recommend_products = []  # Initialize an empty list to store recommended indices
popular_products = []
collab_products = []

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = None
    search_results = None
    user_input = None  # Initialize user_input here

    if request.method == "POST":
        user_input = request.form.get("user_input")
        
        # Clear the list of recommended products before getting new recommendations
        recommend_products.clear()
        
        recommendations = get_recommendations(user_input)
        recommend_products.extend(recommendations)  # Add new recommendations to the list
        
        recommended_rows = data.loc[recommendations]

        search_results = f"You searched result for: {user_input}"
        return render_template("index.html", user_input=user_input, random_sample=recommended_rows, search_results=search_results, data=data)
    else:
        random_sample = data.sample(n=10)  # Get a random sample of 10 rows
        return render_template("index.html", random_sample=random_sample)


@app.route("/content-based", methods=["GET", "POST"])
def content():
    recommendations = None
    search_results = None
    user_input = None  # Initialize user_input here

    if request.method == "POST":
        user_input = request.form.get("user_input")
        
        # Clear the list of recommended products before getting new recommendations
        recommend_products.clear()
        
        recommendations = get_recommendations(user_input)
        recommend_products.extend(recommendations)  # Add new recommendations to the list
        
        recommended_rows = data.loc[recommendations]

        search_results = f"You searched result for: {user_input}"
        return render_template("index.html", user_input=user_input, random_sample=recommended_rows, search_results=search_results, data=data)
    else:
        random_sample = data.sample(n=10)  # Get a random sample of 10 rows
        return render_template("index.html", user_input=user_input, search_results=search_results, random_sample=random_sample)
    
@app.route("/collaborative-filtering", methods=["GET", "POST"])
def collab():
    recommendations = None
    search_results = []  # Initialize search_results as an empty list
    user_input = None

    if request.method == "POST":
        user_input = request.form.get("user_input")

        # Clear the list of recommended products before getting new recommendations
        collab_products.clear()

        recommendations = recProduct(user_input)
        collab_products.extend(recommendations)  # Add new recommendations to the list

        if recommendations:
            search_results = recommendations

    return render_template("collab.html", user_input=user_input, random_sample=recommendations, search_results=search_results, data=data)


    
@app.route("/popularity-based", methods=["GET", "POST"])
def popular():
    recommendations = None
    search_results = None
    user_input = None
    result_dict = {}  # Initialize result_dict here

    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input.isdigit():
            # Assuming user_input is a valid integer
            recommendations = popular_product(int(user_input))
            # Store the recommendations in the global popular_products list
            popular_products.extend(recommendations)
            result_dict = recommendations.to_dict(orient='records')

    return render_template("popular.html", search_results=result_dict, user_input=user_input)


if __name__ == "__main__":
    app.run(debug=True)
