from flask import Flask, render_template, request, jsonify
import pickle
from model import RestaurantRecommender  # Assuming your model is saved as model.py

app = Flask(__name__)

# Load the pickle file with the restaurant recommender model
with open('restaurant_recommender.pkl', 'rb') as file:
    recommender = pickle.load(file)

def get_unique_values(column):
    return recommender.df[column].unique().tolist()

@app.route('/')
def index():
    cities = get_unique_values('City')
    return render_template('index.html', cities=cities)

@app.route('/get_places')
def get_places():
    city = request.args.get('city')
    places = recommender.df[recommender.df['City'] == city]['Place Name'].unique().tolist()
    return jsonify(places=places)

@app.route('/get_items')
def get_items():
    place = request.args.get('place')
    items = recommender.df[recommender.df['Place Name'] == place]['Item Name'].unique().tolist()
    return jsonify(items=items)

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    city = request.form['city']
    place = request.form['place']
    item = request.form['item']
    recommendations = recommender.recommend(city, place, item)
    return render_template('recommendations.html', recommendations=recommendations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
