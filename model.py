import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy.lib.function_base import vectorize

vectorizer = TfidfVectorizer()

# data source
product_data = pd.read_csv('./amazon.csv')

# selecting columns
selected_col = ['product_id', 'product_name', 'category', 'discounted_price', 'rating', 'about_product', 'rating_count']

# deleting all null fields from selected colunms
for col in selected_col:
    product_data[col] = product_data[col].fillna('')

# fixing some price symbol issue
# update_matches = [price.replace('₹', '') for price in partial_matches]
# print(update_matches)

# making selected cols into a single string
combined_col = product_data['product_id'] + ' ' + product_data['product_name'] + ' ' + product_data['category'] + ' ' + \
               product_data['discounted_price'].str.replace('₹', '') + ' ' + product_data['rating'] + ' ' + \
               product_data['about_product'] + ' ' + product_data['rating_count']

# print(combined_col[0])

col_vectors = vectorizer.fit_transform(combined_col)

# Finding the similar product (index, score) for each product
similar = cosine_similarity(col_vectors)

recommend_products = []


# Taking the user input
def get_recommendations(search):
    recommend_products.clear()
    product_search = search

    # comined cols
    all_cols = list(combined_col)

    # finding the close match to the searched prouct name
    # matched_product = difflib.get_close_matches(product_search, name_list)
    partial_matches = list(set(product for product in combined_col if product_search in product.lower()))

    # print(partial_matches)

    # close match all most same to user input
    close_match = partial_matches[0]  # taking the first value of the list

    # print(close_match)

    pid = close_match.split()[0]
    index_of_the_product = product_data[product_data.product_id == pid]['index'].values[0]
    # print(index_of_the_product)

    # similarity score
    similarity_score = list(enumerate(similar[index_of_the_product]))

    # sorted similar product
    sorted_product = sorted(similarity_score, key=lambda pro: pro[1], reverse=True)

    # suggest some product based on product name
    # print("Product you may like: \n")

    i = 1
    for product in sorted_product:
        idx = product[0]
        if i <= 10:  # similar 10 product
            recommend_products.append(idx)
            i += 1

    return recommend_products
