# import os
# import google.generativeai as palm
# import numpy as np
# import pandas as pd
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# import pymongo
# from flask_cors import CORS

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Configure Gemini API with environment variables
# api_key = os.getenv('GEMINI_API_KEY')
# model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

# palm.configure(api_key=api_key)
# model = palm.GenerativeModel(model_name)

# # MongoDB client setup
# mongo_uri = os.getenv('MONGO_URI')
# client = pymongo.MongoClient(mongo_uri)
# db = client.itinerariesDB
# collection = db.itineraries
# collection_insert=db.UserItineraries

# # Define price ranges for budget categories
# # price_ranges = {
# #     'Low': (100, 500),
# #     'Mid': (501, 1500),
# #     'High': (1501, 5000)
# # }

# # Define possible values
# durations = np.arange(2, 6)
# interests = ["Art & Culture", "Food & Shopping", "Romantic", "Family"]

# # Function to map price to budget category
# # def get_budget_category(price):
# #     if price_ranges['Low'][0] <= price <= price_ranges['Low'][1]:
# #         return 'Low'
# #     elif price_ranges['Mid'][0] <= price <= price_ranges['Mid'][1]:
# #         return 'Mid'
# #     elif price_ranges['High'][0] <= price <= price_ranges['High'][1]:
# #         return 'High'
# #     else:
# #         return 'Unknown'


# @app.route('/')
# def home():
#     """
#     Home page of the API.
#     Returns a welcome message.

#     Returns:
#         str: Welcome message
#     """
#     return "Welcome to the Itinerary Prediction API using Gemini!"




# # Function to generate an itinerary using Gemini's API
# def generate_itinerary(budget, duration, interests):
#     try:
#         response = model.generate_content(
#             f"Generate a travel itinerary for Paris with a {budget} budget for {duration} days including these interests: {', '.join(interests)}."
#         )
#         extracted_text = response.candidates[0].content.parts[0].text
#         return extracted_text
#     except Exception as e:
#         print(f"Error generating itinerary: {e}")
#         return None

# # Function to save entry to MongoDB
# def save_to_mongo(entry):
#     collection.insert_one(entry)
#     # collection_insert.insert_one(entry)


# def save_for_user(entry2):
#     collection_insert.insert_one(entry2)



# # Endpoint to generate and save itinerary
# @app.route('/generate_itinerary', methods=['POST'])
# def generate_itinerary_endpoint():
#     data = request.json
#     budget = data.get('budget')
#     duration = data.get('duration')
#     interests = data.get('interests', [])

#     # Generate itinerary using Gemini API
#     itinerary_details = generate_itinerary(budget, duration, interests)
    
#     if not itinerary_details:
#         return jsonify({'error': 'Failed to generate itinerary'}), 500
    
#     # Prepare and save the entry
#     entry = {
#         'Days': duration,
#         'Itinerary': itinerary_details,
#         'Price_High': budget == 'High',
#         'Price_Low': budget == 'Low',
#         'Price_Mid': budget == 'Mid',
#     }
#     for interest in interests:
#         entry[interest] = 1
#     all_interests = ["Romantic", "Family", "Food & Shopping", "Art & Culture"]
#     for interest in all_interests:
#         if interest not in interests:
#             entry[interest] = 0




#     save_to_mongo(entry)
#     save_for_user(entry)
#     return jsonify(entry), 200

# if __name__ == "__main__":
#     app.run(debug=True)





            #                               Create a personalized travel itinerary for Paris based on the following preferences: Duration: 
            #   We will be visiting Paris for {duration} days ,  
            #   Our Total Budget for the trip is : {price_ranges[budget]} in USD ,
            #   You may assume upto 70 percent of it for  food, activities, and accommodation?  
            #   We'd love to engage in activities around :  {', '.join(interests)} .
            #   Please ensure the itinerary reflects my interests and budget, and includes recommendations that suit the specified duration.



####################################Most recent deployment to rollback (not working ) ###################################

"""
import os
import google.generativeai as palm
import numpy as np
import pymongo
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import ObjectId


# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure Gemini API with environment variables
api_key = os.getenv('GEMINI_API_KEY')
model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

palm.configure(api_key=api_key)
model = palm.GenerativeModel(model_name)

# MongoDB client 
mongo_uri = os.getenv('MONGO_URI')
client = pymongo.MongoClient(mongo_uri)
db = client.itinerariesDB
collection = db.itineraries
user_collection = db.userItineraries  # Separate collection for user-specific itineraries

# Define possible values
durations = np.arange(2, 6)
interests = ["Art & Culture", "Food & Shopping", "Romantic", "Family"]


# Define price ranges for budget categories
price_ranges = {
    'Low': (100, 500),
    'Mid': (501, 1500),
    'High': (1501, 5000)
}


@app.route('/')
def home():
    # """
    # Home page of the API.
    # Returns a welcome message.

    # Returns:
    #     str: Welcome message
    # """
    # return "Welcome to the Itinerary Prediction API using Gemini!"

# Helper function to convert MongoDB documents to JSON serializable format
# def serialize_document(doc):
#     if isinstance(doc, dict):
#         return {k: serialize_document(v) for k, v in doc.items()}
#     elif isinstance(doc, list):
#         return [serialize_document(i) for i in doc]
#     elif isinstance(doc, ObjectId):
#         return str(doc)
#     else:
#         return doc

# # Function to generate an itinerary using Gemini's API
# def generate_itinerary(budget, duration, interests):
#     try:
#         response = model.generate_content(f'''Hey there! I'm planning a trip to Paris for {duration} days. My budget is around {price_ranges[budget]} USD. I'm really into {', '.join(interests)}.Can you whip up a fun-filled itinerary that fits my style and budget? I'm looking for recommendations that'll make my trip unforgettable. and not ask any further questions.''')
        
#         extracted_text = response.candidates[0].content.parts[0].text
#         return extracted_text
    
#     except Exception as e:
#         print(f"Error generating itinerary: {e}")
#         return jsonify({'error': 'Internal server error'}), 500



# # Function to save entry to MongoDB
# def save_to_mongo(entry):
#     collection.insert_one(entry)

# # Function to save user-specific entry to MongoDB
# def save_for_user(entry2):
#     user_collection.insert_one(entry2)

# # Endpoint to generate and save itinerary
# @app.route('/generate_itinerary', methods=['POST'])
# def generate_itinerary_endpoint():
#     data = request.json
#     budget = data.get('Price')
#     duration = data.get('Days')
#     interests = data.get('Categories', [])
#     # user_id = data.get('UserId')  # Expect user_id from the request

#     # Generate itinerary using Gemini API
#     itinerary_details = generate_itinerary(budget, duration, interests)
    
#     if not itinerary_details:
#         return jsonify({'error': 'Failed to generate itinerary'}), 500
    
#     # Prepare and save the entry
#     entry = {
#         'Days': duration,
#         'Itinerary': itinerary_details,
#         'Price_High': budget == 'High',
#         'Price_Low': budget == 'Low',
#         'Price_Mid': budget == 'Mid',
#     }
#     for interest in interests:
#         entry[interest] = 1
#     all_interests = ["Romantic", "Family", "Food & Shopping", "Art & Culture"]
#     for interest in all_interests:
#         if interest not in interests:
#             entry[interest] = 0

#     save_to_mongo(entry)

#     # Save user-specific entry if user_id is provided
#     # if user_id:
#     #     entry2 = entry.copy()
#     #     entry2['UserId'] = user_id
#     #     save_for_user(entry2)
    
#     serialized_entry = serialize_document(entry)
#     return jsonify(serialized_entry), 200

# if __name__ == "__main__":
#     app.run(debug=True)




"""










########################################
"""

# import os
# import google.generativeai as palm
# import numpy as np
# import pandas as pd
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# import pymongo
# from flask_cors import CORS

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Configure Gemini API with environment variables
# api_key = os.getenv('GEMINI_API_KEY')
# model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

# palm.configure(api_key=api_key)
# model = palm.GenerativeModel(model_name)

# # MongoDB client setup
# mongo_uri = os.getenv('MONGO_URI')
# client = pymongo.MongoClient(mongo_uri)
# db = client.itinerariesDB
# collection = db.itineraries
# user_collection = db.userItineraries  # Separate collection for user-specific itineraries

# # Define possible values
# durations = np.arange(2, 6)
# interests = ["Art & Culture", "Food & Shopping", "Romantic", "Family"]

# # Function to generate an itinerary using Gemini's API
# def generate_itinerary(budget, duration, interests):
#     try:
#         response = model.generate_content(
#             f"Generate a travel itinerary for Paris with a {budget} budget for {duration} days including these interests: {', '.join(interests)}."
#         )
#         extracted_text = response.candidates[0].content.parts[0].text
#         return extracted_text
#     except Exception as e:
#         print(f"Error generating itinerary: {e}")
#         return None

# # Function to save entry to MongoDB
# def save_to_mongo(entry):
#     collection.insert_one(entry)

# # Function to save user-specific entry to MongoDB
# def save_for_user(entry2):
#     user_collection.insert_one(entry2)

# # Endpoint to generate and save itinerary
# @app.route('/generate_itinerary', methods=['POST'])
# def generate_itinerary_endpoint():
#     data = request.json
#     budget = data.get('budget')
#     duration = data.get('duration')
#     interests = data.get('interests', [])
#     user_id = data.get('user_id')  # Expect user_id from the request

#     # Generate itinerary using Gemini API
#     itinerary_details = generate_itinerary(budget, duration, interests)
    
#     if not itinerary_details:
#         return jsonify({'error': 'Failed to generate itinerary'}), 500
    
#     # Prepare and save the entry
#     entry = {
#         'Days': duration,
#         'Itinerary': itinerary_details,
#         'Price_High': budget == 'High',
#         'Price_Low': budget == 'Low',
#         'Price_Mid': budget == 'Mid',
#     }
#     for interest in interests:
#         entry[interest] = 1
#     all_interests = ["Romantic", "Family", "Food & Shopping", "Art & Culture"]
#     for interest in all_interests:
#         if interest not in interests:
#             entry[interest] = 0

#     save_to_mongo(entry)

#     # Save user-specific entry if user_id is provided
#     if user_id:
#         entry2 = entry.copy()
#         entry2['UserId'] = user_id
#         save_for_user(entry2)
    
#     return jsonify(entry), 200

# if __name__ == "__main__":
#     app.run(debug=True)








############ Most Recent modifications ############


import os
import google.generativeai as palm
import numpy as np
import pymongo
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure Gemini API with environment variables
api_key = os.getenv('GEMINI_API_KEY')
model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

palm.configure(api_key=api_key)
model = palm.GenerativeModel(model_name)

# MongoDB client
mongo_uri = os.getenv('MONGO_URI')
client = pymongo.MongoClient(mongo_uri)
db = client.itinerariesDB
collection = db.itineraries
user_collection = db.UserItineraries  # Separate collection for user-specific itineraries

# Define possible values
durations = np.arange(2, 6)
interests = ["Art & Culture", "Food & Shopping", "Romantic", "Family"]

# Define price ranges for budget categories
price_ranges = {
    'Low': (100, 500),
    'Mid': (501, 1500),
    'High': (1501, 5000)
}

@app.route('/')
def home():
    """
    Home page of the API.
    Returns a welcome message.
    """
    return "Welcome to the Itinerary Prediction API using Gemini!"

# Helper function to convert MongoDB documents to JSON serializable format
def serialize_document(doc):
    if isinstance(doc, dict):
        return {k: serialize_document(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_document(i) for i in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

def validate_inputs(budget, duration, interests):

    output=""
    valid_budgets = ['Low', 'Mid', 'High']
    if budget not in valid_budgets:
        output+=(f"Invalid budget value: {budget}")
    if not isinstance(duration, int) or duration <= 0:
        output+=(f"Invalid duration value: {duration}")
    if not isinstance(interests, list) or not all(isinstance(i, str) for i in interests):
        output+=("Interests should be a list of strings")
    
    return output

# Function to generate an itinerary using Gemini's API
def generate_itinerary(budget, duration, interests):
    try:
        validate_inputs(budget, duration, interests)
        print(price_ranges[budget])
        print(duration)
        print(interests)

        response = model.generate_content(f'''Hey there! I'm planning a trip to Paris for {duration} days. My budget is around {price_ranges[budget]} USD. I'm really into {', '.join(interests)}. Can you whip up a fun-filled itinerary that fits my style and budget? I'm looking for recommendations that'll make my trip unforgettable and not ask any further questions.''')
        
        
        print(response)

        extracted_text = response.candidates[0].content.parts[0].text

        output=validate_inputs(budget, duration, interests)
        temporary=output+extracted_text
        return temporary
    
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return "Error generating itinerary"

# Function to save entry to MongoDB
def save_to_mongo(entry):
    collection.insert_one(entry)

# Function to save user-specific entry to MongoDB
def save_for_user(entry2):
    user_collection.insert_one(entry2)

# Endpoint to generate and save itinerary
@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary_endpoint():
    data = request.json
    requestData = data.get('requestData', {})
    user_id = data.get('userId')  # Expect user_id from the request

    budget = requestData.get('budget')
    duration = requestData.get('duration')
    interests = requestData.get('interests', [])

    # Generate itinerary using Gemini API
    itinerary_details = generate_itinerary(budget, duration, interests)
    
    if not itinerary_details:
        return jsonify({'error': 'Failed to generate itinerary'}), 500
    
    # Prepare and save the entry
    entry = {
        'Days': duration,
        'Itinerary': itinerary_details,
        'Price_High': budget == 'High',
        'Price_Low': budget == 'Low',
        'Price_Mid': budget == 'Mid',
    }
    for interest in interests:
        entry[interest] = 1
    all_interests = ["Romantic", "Family", "Food & Shopping", "Art & Culture"]
    for interest in all_interests:
        if interest not in interests:
            entry[interest] = 0

    save_to_mongo(entry)

    # Save user-specific entry if user_id is provided
    if user_id:
        entry2 = entry.copy()
        entry2['UserId'] = user_id
        save_for_user(entry2)
    
    serialized_entry = serialize_document(entry)
    return jsonify(serialized_entry), 200

if __name__ == "__main__":
    app.run(debug=True)
