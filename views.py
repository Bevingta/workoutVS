from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import asyncio


views = Blueprint(__name__, "views")

leaderboard_data = {
    'Drew': 5,
    'Kevin': 7,
    'Sophia': 3,
    'Brady': 0,
    'Sawyer': 0
}


#uses the block stuff in HTML to change the website view
names = ["Drew", "Kevin", "Sophia", "Sawyer", "Brady", "Trevor"]
totals = {}

async def count_name_occurrences(database_name, collection_name, target_name, loop):
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://bevingtonan:1234@cluster0.m2wnxuj.mongodb.net/?retryWrites=true&w=majority')

    # Access the specified database and collection
    db = client[database_name]
    collection = db[collection_name]

    # Use count_documents to efficiently count occurrences of the target name
    count = await loop.run_in_executor(None, collection.count_documents, {"name": target_name})

    if count > 0:
        print(f"The name '{target_name}' appears {count} times in the collection.")
        totals[target_name] = count
    else:
        print(f"The name '{target_name}' does not exist in the collection.")

    # Close the MongoDB connection
    client.close()


#uses the block stuff in HTML to change the website view
@views.route("/")
async def profile():
    # Replace these values with your actual MongoDB connection details and collection information
    database_name = "workout"
    collection_name = "people"

    # Create tasks for each name
    tasks = [count_name_occurrences(database_name, collection_name, name, asyncio.get_event_loop()) for name in names]

    # Run tasks concurrently
    await asyncio.gather(*tasks)
    return render_template('scratch.html', leaderboard=totals)
