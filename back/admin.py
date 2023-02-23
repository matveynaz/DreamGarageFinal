import pymongo
import hashlib
from flask import Flask, render_template

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
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)


#send articles
def send_articles(user, articles):
    # Check if the user exists in the database
    if not collection.find_one({'username': user}):
        return 'User does not exist'

    # Insert the articles into the orders collection
    for article in articles:
        collection.insert_one({'user': user, 'article': article})

    return 'Articles sent successfully'


#show the table of orders
def show_orders():
    # Get the orders from the database
    orders = collection.find()

    # Create a table of orders
    table = []
    for order in orders:
        article = collection.find_one({'name': order['article']})
        table.append([article['car'], article['name'], article['price'], order['user']])

    return table


# Send articles to a user
send_articles('john', ['Article 1', 'Article 2'])

# Show the table of orders
table = show_orders()
for row in table:
    print(row)

# Send articles to a user
send_articles('john', ['Article 1', 'Article 2'])

# Show the table of orders
table = show_orders()
for row in table:
    print(row)
