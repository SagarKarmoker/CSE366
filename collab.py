import pandas as pd
import numpy as np

def recProduct(name):
  products = pd.read_json('/workspaces/CSE366/Dataset_new/products.json')
  customers = pd.read_json('/workspaces/CSE366/Dataset_new/customers.json')
  ratings = pd.read_json('/workspaces/CSE366/Dataset_new/ratings.json')
  ratings = ratings[['CustomerID', 'ProductID', 'Rate']]

  products.rename(columns = {'Id':'ProductID'}, inplace = True)

  """# Popularity Based System

  ## minimum 250 rating then recommned with highest avg rating
    """

  ratings_with_name = ratings.merge(products, on='ProductID')
  ratings_with_name.groupby('Name').count()['Rate']

  num_rating_df = ratings_with_name.groupby('Name').count()['Rate'].reset_index()
  num_rating_df.rename(columns={'Rate': 'nums-ratings'}, inplace=True)

  # printing the avg rating
  avg_rating_df = ratings_with_name.groupby('Name').mean()['Rate'].reset_index()
  avg_rating_df.rename(columns={'Rate': 'avg-ratings'}, inplace=True)

  #merging two dataframe
  popular_df = num_rating_df.merge(avg_rating_df, on='Name')

  #logic
  #products having rating >= 50 in total
  #top 50 products, sort based on avg rating
  popular_df = popular_df[popular_df['nums-ratings'] >= 50].sort_values('avg-ratings', ascending=False).head(50)
  # popular_df = popular_df[popular_df.merge(products, on='Name').drop_duplicates('Name')[['Name','nums-ratings', 'avg-ratings']]]
  popular_df = popular_df.merge(products, on='Name').drop_duplicates('Name')[['Name','nums-ratings', 'avg-ratings']]

  """# Collabrative Filtering Rating Based Book Recommnedation
  ##
  """

  customers.rename(columns = {'Id':'CustomerID'}, inplace = True)

  ratings_with_name.groupby('CustomerID').count()['Rate']

  notRated = ratings_with_name.groupby('CustomerID').count()['Rate'] > 200
  rated_user = notRated[notRated].index

  filter_rating = ratings_with_name[ratings_with_name['CustomerID'].isin(rated_user)]
  filter_rating[ratings_with_name['CustomerID'].isin(rated_user)]

  y = filter_rating.groupby('Name').count()['Rate']>= 50
  famous_products= y[y].index

  final_ratings = filter_rating[filter_rating['Name'].isin(famous_products)]
  # final_ratings.drop_duplicates()

  pt = final_ratings.pivot_table(index='Name', columns='CustomerID', values='Rate')

  pt.fillna(0, inplace=True)

  #distance calculation
  #each products becomes vector and we will calculate the eulicaten distance

  from sklearn.metrics.pairwise import cosine_similarity

  #distance (similarity score)
  sim_score = cosine_similarity(pt)

  #index fetch of the particular products
  index = np.where(pt.index == name)[0][0]
  #removed the 0th products which same book, so from 1 to 6 total 5 products
  similar_products = sorted(list(enumerate(sim_score[index])), key=lambda x:x[1], reverse=True)[1:6] #sorted based on similarity score

  products_list = []

  products_list.append([pt.index[i[0]] for i in similar_products])
  return products_list
#DONE