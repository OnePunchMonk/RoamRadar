import os
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
# Load models from file
with open('cluster_models.pkl', 'rb') as f:
    cluster_models = pickle.load(f)

# MongoDB setup
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.itinerariesDB
collection = db.itineraries
collection_insert=db.UserItineraries

@app.route('/')
def home():
    """
    Home page of the API.
    Returns a welcome message.

    Returns:
        str: Welcome message
    """
    return "Welcome to the Itinerary Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict an itinerary given the number of days, price, and categories.

    Body should contain a JSON object with the following keys:
        - Days (int): Number of days for the itinerary.
        - Price (str): Price category of the itinerary (High, Mid, or Low).
        - Categories (list[str]): List of categories for the itinerary (Romantic, Family, Food & Shopping, Art & Culture).

    Returns a JSON object with a single key 'prediction' containing the
    predicted itinerary.
    """
    data = request.json
    days = data.get('Days')
    price = data.get('Price')
    categories = data.get('Categories')

    # Prepare input data
    input_data = pd.DataFrame([{
        'Price_High': 1 if price == 'High' else 0,
        'Price_Low': 1 if price == 'Low' else 0,
        'Price_Mid': 1 if price == 'Mid' else 0,
        'Romantic': 1 if 'Romantic' in categories else 0,
        'Family': 1 if 'Family' in categories else 0,
        'Food & Shopping': 1 if 'Food & Shopping' in categories else 0,
        'Art & Culture': 1 if 'Art & Culture' in categories else 0
    }])

    if days not in cluster_models:
        return jsonify({'error': 'Invalid days parameter'}), 400

    knn_model = cluster_models[days]
    prediction = knn_model.predict(input_data)
    
    return jsonify({'prediction': prediction[0]})

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    result = collection_insert.insert_one(data)
    return jsonify({'inserted_id': str(result.inserted_id)}), 201

@app.route('/data', methods=['GET'])
def get_data():
    entries = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB `_id` field
    return jsonify(entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
