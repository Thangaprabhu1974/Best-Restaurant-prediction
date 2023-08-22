import pandas as pd
import pickle

class RestaurantRecommender:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)

    def recommend(self, city, place_name, item_name):
        # Filter dataset based on the city, place, and item name
        filtered_df = self.df[
            (self.df['City'].str.lower() == city.lower()) &
            (self.df['Place Name'].str.lower() == place_name.lower()) &
            (self.df['Item Name'].str.lower() == item_name.lower())
            ]

        # If no data available for the given criteria, return empty DataFrame
        if filtered_df.empty:
            return pd.DataFrame()

        # Calculate average dining rating and delivery rating for each restaurant
        recommended_df = filtered_df.groupby('Restaurant Name').agg({
            'Dining Rating': 'mean', # Changed from 'Dining Votes'
            'Delivery Rating': 'mean' # Changed from 'Delivery Votes'
        }).reset_index()

        # Sort by the highest average dining rating and delivery rating
        recommended_df = recommended_df.sort_values(by=['Dining Rating', 'Delivery Rating'], ascending=False)

        return recommended_df

def save_model(model, filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

def load_model(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

if __name__ == '__main__':
    dataset_path = 'zomato_dataset.csv'
    recommender = RestaurantRecommender(dataset_path)

    # Save the recommender model
    save_model(recommender, 'restaurant_recommender.pkl')

    # Load the recommender model
    loaded_recommender = load_model('restaurant_recommender.pkl')

    # Make recommendations
    city = 'New York'
    place_name = 'Manhattan'
    item_name = 'Pizza'
    recommendations = loaded_recommender.recommend(city, place_name, item_name)

    print("Recommended Restaurants:")
    print(recommendations)
