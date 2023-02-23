from flask import Flask, request, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

#connection mongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get from html
        name = request.form["name"]
        email = request.form["email"]
        car = request.form["car"]

        # insert
        collection.insert_one({
            "name": name,
            "email": email,
            "car": car
        })

        return "Order placed successfully!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
