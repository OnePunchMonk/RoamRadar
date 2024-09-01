from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import os
import json
from datetime import datetime
# import jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
CORS(app, resources={r"/*": {"origins": "*"}})
# MongoDB setup

MONGODB_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGODB_URI)
db = client['itinerariesDB']
signup_collection = db['signup']
reviews_collection = db['reviews']



@app.route('/')
def home():
    """
    Home page of the API.
    Returns a welcome message.
    """
    return "Welcome to the APIs for Signup,Login,Add review , fetch reviews !"


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    # Check if username or email already exists
    if signup_collection.find_one({"username": username}):
        return jsonify({'success': False, 'message': 'Username already taken'}), 400
    
    if signup_collection.find_one({"email": email}):
        return jsonify({'success': False, 'message': 'Email already registered'}), 400

    hashed_password = generate_password_hash(password)
    signup_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })
    
    return jsonify({'success': True})

# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')

#         user = signup_collection.find_one({"email": email})
#         if user and check_password_hash(user['password'], password):
#             session['user_id'] = str(user['_id'])
#             session['username'] = user['username']
#             return jsonify({'success': True, 'token': 'dummy_token', 'userID': str(user['_id'])})
#         else:
#             return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500


# @app.route('/login', methods=['POST','GET'])
# def login():
#     if request.method == 'POST':
#         data = request.get_json()
#         email = data.get('email')
#         password = data.get('password')
        
#         user = signup_collection.find_one({"email": email})
#         if user and check_password_hash(user['password'], password):
#             session['user_id'] = str(user['_id'])
#             session['username'] = user['username']
#             return jsonify({'success': True})
#         else:
#             return jsonify({'success': False, 'message': 'Invalid email or password'}), 400
#     else:
#         return render_template('login.html')
    



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = signup_collection.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 400
    else:
        return render_template('login.html')
        
# @app.route('/dashboard')
# def dashboard():
#     if 'username' in session:
#         username = session['username']
#         return render_template('dashboard.html', username=username)
#     return redirect(url_for('login'))


@app.route('/user-dashboard', methods=['GET'])
def user_dashboard():
    if 'username' in session:
        username = session.get('username')
        return jsonify({'success': True, 'username': username})
    return jsonify({'success': False, 'message': 'User not logged in'})


@app.route('/logout', methods=['POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'No user logged in'})


@app.route('/add_review', methods=['POST'])
def add_review():
    try:
        data = request.get_json()
        ratings = int(data['ratings'])
        review = data['review']
        
        reviews_collection.insert_one({
            "ratings": ratings,
            "review": review,
            "createdAt": datetime.utcnow()
        })
        
        return jsonify({'success': True})
    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500
    




# See reviews
@app.route('/see_reviews')
def see_reviews():
    if 'username' in session:
        reviews = reviews_collection.find().sort([("ratings", -1), ("createdAt", -1)]).limit(3)
        return render_template('see_reviews.html', username=session['username'], reviews=reviews)
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
