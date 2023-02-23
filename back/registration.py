import pymongo
import hashlib
from flask import Flask, request, render_template


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

#registration
def register(username, password):
    # Hash the password
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Check if the user already exists in the database
    if collection.find_one({'username': username}):
        return 'User already exists'

    # Insert the user details into the database
    collection.insert_one({'username': username, 'password': hashed_password})
    return 'User registered successfully'

#login
def login(username, password):
    # Hash the password
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Check if the username and password are correct
    user = collection.find_one({'username': username, 'password': hashed_password})
    if user:
        return 'Login successful'
    else:
        return 'Invalid username or password'



app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    result = register(username, password)
    return render_template('result.html', result=result)

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    result = login(username, password)
    return render_template('result.html', result=result)


