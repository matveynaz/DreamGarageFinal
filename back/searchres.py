from flask import Flask, render_template, appcontext_popped, request
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
#connection mongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]

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

@app.route("/", methods=["GET", "POST"])
@app.route("/search")
def search():
   if request.method == "POST":
        table_name = request.form.get("table_name")

        # Execute the query
        results = collection.find({})

        # Render the results in an HTML template
        return render_template("results.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)