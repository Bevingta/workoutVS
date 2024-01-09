from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint
from pymongo import MongoClient
import asyncio

app = Flask(__name__)

# Create a Blueprint for views
views = Blueprint("views", __name__)

# MongoDB connection details
client = MongoClient('mongodb+srv://bevingtonan:1234@cluster0.m2wnxuj.mongodb.net/?retryWrites=true&w=majority')
db = client["workout"]
collection = db["people"]

# Names for profile view
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
        totals[target_name] = 0

    # Close the MongoDB connection
    client.close()


# Profile route
@app.route("/")
async def profile():
    # Replace these values with your actual MongoDB connection details and collection information
    database_name = "workout"
    collection_name = "people"

    # Create tasks for each name
    tasks = [count_name_occurrences(database_name, collection_name, name, asyncio.get_event_loop()) for name in names]

    # Run tasks concurrently
    await asyncio.gather(*tasks)
    sorted_totals = dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))
    return render_template('scratch.html', leaderboard=sorted_totals)


# Add data route
@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        # Get data from the form
        data_to_add = {
            'name': request.form['key1'],
            'date': request.form['key2'],
            'description': request.form['key3']
        }

        # Insert data into MongoDB
        collection.insert_one(data_to_add)

        print("Stuff added")

        return redirect(url_for('profile'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
