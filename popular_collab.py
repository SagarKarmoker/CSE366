import pandas as pd
import numpy as np
from datetime import datetime

def popular_product(rating: int):
    products = pd.read_json('./Dataset_new/products.json')
    customers = pd.read_json('./Dataset_new/customers.json')
    ratings = pd.read_json('./Dataset_new/ratings.json')

    # Drop the 'CreateDate' column from the ratings DataFrame
    ratings.drop(columns=["CreateDate"], inplace=True)

    # Rename the 'Id' column in the products DataFrame to 'ProductID'
    products.rename(columns={'Id': 'ProductID'}, inplace=True)

    # Merge ratings with products on 'ProductID' to get product names
    ratings_with_name = ratings.merge(products, on='ProductID')

    # Group by product name and count the number of ratings
    num_rating_df = ratings_with_name.groupby('Name').count()['Rate'].reset_index()
    num_rating_df.rename(columns={'Rate': 'nums-ratings'}, inplace=True)

    # Group by product name and calculate the average rating
    avg_rating_df = ratings_with_name.groupby('Name').mean()['Rate'].reset_index()
    avg_rating_df.rename(columns={'Rate': 'avg-ratings'}, inplace=True)

    # Merge the two dataframes to get 'nums-ratings' and 'avg-ratings'
    popular_df = num_rating_df.merge(avg_rating_df, on='Name')

    # Filter products with a minimum number of ratings (rating) and sort by 'avg-ratings' in descending order
    popular_df = popular_df[popular_df['nums-ratings'] >= rating].sort_values('avg-ratings', ascending=False)

    # Take the top 5 products
    popular_df = popular_df.head(10)

    return popular_df[['Name', 'nums-ratings', 'avg-ratings']]

# # Usage example:
# popular_products = popular_product(50)  # Example rating threshold
# print(popular_products)
