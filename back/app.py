import http.server
import socketserver
import pymongo
from pymongo import MongoClient
from flask import Flask, appcontext_popped, render_template, request, redirect, url_for
from os import path

#connection mongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]

try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print("MongoDB connection is successful.")
except pymongo.errors.ConnectionFailure as error:
    print(f"Could not connect to MongoDB: {error}")

 #connection html
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    
#find data
@appcontext_popped.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    cars = collection.find({'$or': [{'car_mark': {'$regex': keyword, '$options': 'i'}}, 
                                      {'car_model': {'$regex': keyword, '$options': 'i'}},
                                      {'year': {'$regex': keyword, '$options': 'i'}},
                                      {'color': {'$regex': keyword, '$options': 'i'}},
                                      {'engine': {'$regex': keyword, '$options': 'i'}}
                                     ]})
    results = []
    for car in cars:
        results.append({'car_mark': car['car_mark'], 'car_model': car['car_model'], 'year': car['year'],
                        'color': car['color'], 'engine': car['engine']})
    return render_template('result.html', results=results)


#contacts
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         name = request.form["name"]
#         email = request.form["email"]
#         password = request.form["password"]
#         collection.insert_one({
#             "name": name,
#             "email": email,
#             "password": password
#         })
#         return redirect(url_for("index.html"))
#     return render_template("contact.html")