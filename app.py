from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from model import get_recommendations

app = Flask(__name__)

data = pd.read_csv("./amazon.csv")
recommend_products = []  # Initialize an empty list to store recommended indices

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
        return render_template("index.html", user_input=user_input, search_results=search_results, random_sample=random_sample)

if __name__ == "__main__":
    app.run(debug=True)
