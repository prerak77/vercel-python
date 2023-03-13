# All of the imports need to run the server
#
# the flask library is used to create the server and host the REST API
# They include the MySQL connect to MySQL database to store all the user details.
# the azure cosmos library allow connectivity to the microsoft azure database
# flsak cors is used help with cross cors compatibilty

from flask import Flask, json, request, jsonify
import bcrypt
import json
from flask_cors import CORS, cross_origin
from azure.cosmos import CosmosClient, PartitionKey
import mysql.connector as mys

# to initialize the flask framwork
app = Flask(__name__)


# This is the code for all the routes

# this is the loaidng page rout that is used as a starting point for the API
# Remove later
@app.route("/")
def home():
    return "Hello world"

# This is a rout that allows to add the BRSR report data to the NoSQL data base in the azure cloud
# the entry point for the API is /data and it is using th e POST HTTP request


@app.route("/data", methods=['POST'])
@cross_origin()
def members():
    # To retieve the data recieved from the frontend and using the json.load function
    request_data = json.loads(request.data)
    CREATE_DATABASE()
    ADDING_NEW_ELEMENT(request_data)
    PRINTING_SINGLE_ITEM()

    return (" ")


@app.route("/signup", methods=['POST'])
@cross_origin()
def Signup_Data():
    request_data = json.loads(request.data)
    create_table_user()
    insert_table_user(request_data)

    return (" ")


@app.route("/login_add", methods=['POST', "GET"])
@cross_origin()
def Login_Data():
    global check_user
    check_user = False
    request_data = request.get_json()
    check_user = get_data(request_data)

    return {"state_type": [str(check_user)]}


# Azure code
ENDPOINT = 'https://vertois-nosql-database.documents.azure.com:443/'
KEY = 'FH36DyIs9Spu5PuUYEeX9mFVRlEwEsTWErjh6Y1twPFkPwGCcjY8NLclO46ONaWNqp2Dk9dzrUyZACDbBsdI0w=='


DATABASE_NAME = "Vertois"
CONTAINER_NAME = "Container1"

client = CosmosClient(url=ENDPOINT, credential=KEY)


def CREATE_DATABASE():
    global database, key_path, container
    database = client.create_database_if_not_exists(id=DATABASE_NAME)

    key_path = PartitionKey(path="/Vertois")

    container = database.create_container_if_not_exists(
        id=CONTAINER_NAME, partition_key=key_path, offer_throughput=400
    )


def ADDING_NEW_ELEMENT(data):

    KEYS = list(data["content"].keys())
    VALUES = list(data["content"].values())

    new_item = {
        "id":     VALUES[0],
        "Vertois": "section1",
        KEYS[1]: VALUES[1],
        KEYS[2]: VALUES[2],
        KEYS[3]: VALUES[3],
        KEYS[4]: VALUES[4],
        KEYS[5]: VALUES[5],
        KEYS[6]: VALUES[6],
        KEYS[7]: VALUES[7],

    }

    container.create_item(new_item)


def PRINTING_SINGLE_ITEM():
    existing_item = container.read_item(
        item='L28920MH1919PLC000567',
        partition_key="section1",
    )
    print("KEYS             VALUES")
    for i in range(7):
        print(list(existing_item.keys())[
              i], "             ", list(existing_item.values())[i])


# MySQL code


#                   To Create a Database
HOST = "bqiawzsj6cs1gnvwn9bf-mysql.services.clever-cloud.com"
USER = "ujcxzjccio6qgz9f"
PASSWORD = "XMjoPDVitq97Uz1AjNrb"
DATABASE = "bqiawzsj6cs1gnvwn9bf"


def create_database():
    try:
        myconn = mys.connect(host=HOST,
                             user=USER, passwd=PASSWORD, port="3306")
        mycur = myconn.cursor()
        query = "create database UserInfo"
        mycur.execute(query)
        myconn.commit()
        print("Database successfully created")

    except Exception as e:
        pass


#                   To create a table for CAR MODEL details
def create_table_user():
    try:
        myconn = mys.connect(host=HOST,
                             user=USER, passwd=PASSWORD, database=DATABASE, port="3306")
        mycur = myconn.cursor()
        query = "CREATE TABLE user_details (name VARCHAR(255), email VARCHAR(255),password VARCHAR(200),ID VARCHAR(255))"
        mycur.execute(query)
        myconn.commit()
        print("Table successfully created")

    except Exception as e:
        print(e)


def insert_table_user(details):
    try:
        KEYS = list(details["content"].keys())
        VALUES = list(details["content"].values())
        hashed = bcrypt.hashpw((VALUES[2]).encode("utf-8"), bcrypt.gensalt())

        myconn = mys.connect(host=HOST, user=USER,
                             passwd=PASSWORD, database=DATABASE)
        mycur = myconn.cursor()
        query = "insert into user_details values\
                                            ('{}','{}','{}','{}')".format(VALUES[0], VALUES[1], hashed.decode("utf-8"), '')
        mycur.execute(query)
        myconn.commit()
    except Exception as e:
        print(e)


def get_data(id):
    try:
        VALUES = list(id.values())

        myconn = mys.connect(host=HOST, user=USER,
                             passwd=PASSWORD, database=DATABASE)
        if myconn.is_connected():
            print("Succesfully connected")
        mycur = myconn.cursor()
        query = "SELECT * FROM user_details where user_details.email = '{}'".format(
            VALUES[0])
        mycur.execute(query)
        rs = mycur.fetchall()
        print(rs[0])
        if len(rs[0]) != 0:
            hashed_password = (rs[0][2]).encode()
            encode_value = (VALUES[1]).encode()
            if bcrypt.checkpw(encode_value, hashed_password):
                return True
            else:
                return False
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(debug=True)
