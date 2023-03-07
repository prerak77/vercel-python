import mysql.connector as mys
from azure.cosmos import CosmosClient, PartitionKey
from flask_cors import CORS, cross_origin
import json
import os
from flask import Flask, json, request, jsonify
app = Flask(__name__, static_folder="frontend/build")
# This is the code for all the routes


@app.route("/")
def home():
    return "python world"


@app.route("/data", methods=['POST'])
@cross_origin()
def members():
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


@app.route("/login_add", methods=['POST'])
@cross_origin()
def Login_Data():
    global check_user
    check_user = False
    request_data = request.get_json()
    print(request_data.data)
    check_user = get_data(request_data)
    print(check_user)

    return ('')


@app.route("/login_send", methods=['GET'])
@cross_origin()
def Login_Data_Send():
    print({"state": [str(check_user)]})
    return {"state_type": [str(check_user)]}


# Azure code


ENDPOINT = 'https://de44a99c-0ee0-4-231-b9ee.documents.azure.com:443/'
KEY = 'dJL5ctFaJWB3YUzdl9sUQt5N1VziPj7G9KDf0z6s5zwpyYoDdvAx0GpSESCHCE5IwF072ML7FdpmACDb1hiQBA=='


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
def create_database():
    try:
        myconn = mys.connect(host="sql12.freemysqlhosting.net",
                             user="sql12602665", passwd="FAUkhKG9WP", port="3306")
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
        myconn = mys.connect(host="sql12.freemysqlhosting.net",
                             user="sql12602665", passwd="FAUkhKG9WP", database="sql12602665", port="3306")
        mycur = myconn.cursor()
        query = "CREATE TABLE user_details (name VARCHAR(255), email VARCHAR(255),password VARCHAR(255),ID VARCHAR(255))"
        mycur.execute(query)
        myconn.commit()
        print("Table successfully created")

    except Exception as e:
        print(e)


def insert_table_user(details):
    try:
        KEYS = list(details["content"].keys())
        VALUES = list(details["content"].values())

        print(VALUES)
        myconn = mys.connect(host="sql12.freemysqlhosting.net", user="sql12602665",
                             passwd="FAUkhKG9WP", database="sql12602665")
        mycur = myconn.cursor()
        query = "insert into user_details values\
                                            ('{}','{}','{}','{}')".format(VALUES[0], VALUES[1], VALUES[2], '')
        mycur.execute(query)
        myconn.commit()
    except Exception as e:
        print(e)


def get_data(id):
    try:
        VALUES = list(id["content"].values())

        print(VALUES[0])
        myconn = mys.connect(host="sql12.freemysqlhosting.net", user="sql12602665",
                             passwd="FAUkhKG9WP", database="sql12602665")
        if myconn.is_connected():
            print("Succesfully connected")
        mycur = myconn.cursor()
        query = "SELECT * FROM user_details where user_details.email = '{}' and user_details.password = '{}' ".format(
            VALUES[0], VALUES[1])
        mycur.execute(query)
        rs = mycur.fetchall()
        print(rs[0])
        if len(rs[0]) != 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)


create_table_user()

if __name__ == '__main__':
    app.run(debug=True)
