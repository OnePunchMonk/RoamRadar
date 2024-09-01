from flask import Flask, jsonify
from flask_cors import CORS
import os
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)


MONGODB_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGODB_URI)

db = client['itinerariesDB']
reviews_collection = db['reviews']


@app.route('/')
def home():
    """
    Home page of the API.
    Returns a welcome message.
    """
    return "Welcome to the Review Visualisation API for ChartsJs!"


@app.route('/ratings', methods=['GET'])
def get_ratings():
    pipeline = [
        {"$group": {"_id": "$ratings", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    ratings = list(reviews_collection.aggregate(pipeline))
    return jsonify(ratings)



@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    # Fetch the top 5 reviews sorted by rating and most recent (_id)
    reviews = reviews_collection.find().sort([("ratings", -1), ("_id", -1)]).limit(5)
    reviews_text = [review['review'] for review in reviews]
    
    return jsonify(reviews_text)
if __name__ == '__main__':
    app.run(debug=True)
