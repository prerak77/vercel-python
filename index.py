# All of the imports need to run the server
#
# the flask library is used to create the server and host the REST API
# They include the MySQL connect to MySQL database to store all the user details.
# the azure cosmos library allow connectivity to the microsoft azure database
# flsak cors is used help with cross cors compatibilty

from flask import Flask, json, request, Response, render_template, redirect, send_file, make_response
import bcrypt
from flask_cors import CORS, cross_origin
import mysql.connector as mys
import pymongo
from fpdf import FPDF

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


@app.route("/pdf", methods=['POST', "GET"])
@cross_origin()
def downloade_data():
    data = (request.json)['content']
    CIN = list(data.values())[0]
    # create a new PDF object
    pdf = FPDF()
    pdf.add_page()

    # set some properties of the PDF file
    pdf.set_title('BRSR Report')
    pdf.set_author('Vertois')
    pdf.set_subject('pdf document for BRSR report')

    # add some text to the PDF file
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'VERTOIS', ln=1)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(40, 10, 'Business Responsibility & Sustainability Report', ln=1)

    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, 'I. Details of the listed entity', ln=1)

    pdf.set_font('Arial', "B", 8)
    pdf.cell(
        80, 5, '1)     Corporate Identity Number (CIN) of the Listed Entity:', ln=0)
    pdf.set_font('Arial', "", 8)
    pdf.cell(
        10, 5, CIN, ln=1)

    pdf.cell(
        40, 5, '2)     Name of the Listed Entity: The Tata Power Company Limited', ln=1)
    pdf.cell(40, 5, '3)     Year of incorporation: 1919', ln=1)
    pdf.cell(40, 5, '4)     Registered office address: Bombay House, 24, Homi Mody Street, Mumbai - 400 001, Maharashtra, India', ln=1)
    pdf.cell(40, 5, '5)     Corporate address: Corporate Center, 34 Sant Tukaram Road, Carnac Bunder, Mumbai - 400 009, Maharashtra, India', ln=1)
    pdf.cell(40, 5, '6)     E-mail: tatapower@tatapower.com', ln=1)
    pdf.cell(40, 5, '7)     Telephone: 022-6665 8282', ln=1)
    pdf.cell(40, 5, '8)     Website: www.tatapower.com', ln=1)
    pdf.cell(40, 5, '9)     Financial year for which reporting is being done: April 2021 - March 2022', ln=1)
    pdf.cell(40, 5, '10)     Name of the Stock Exchange(s) where shares are listed: BSE Limited and National Stock Exchange of India Limited ', ln=1)
    pdf.cell(40, 5, '11)     Paid-up Capital: INR 319.56 crore', ln=1)
    pdf.cell(40, 5, '12)     Name and contact details (telephone, email address) of the person who may be contacted in case of any queries on the BRSR report: ', ln=1)
    pdf.cell(40, 5, '           Ms. Jyoti Kumar Bansal, Chief-Branding, Corp Communication, CSR & Sustainability', ln=1)
    pdf.cell(40, 5, '           Email - jyotikumar.bansal@tatapower.com', ln=1)
    pdf.cell(40, 5, '           Contact Number: 022-6717 1666', ln=1)
    pdf.cell(40, 5, '13)     Reporting boundary - Are the disclosures under this report made on a standalone basis (i.e. only for the entity) or on a consolidated basis (i.e. for the entity and all the entities which form a part of its consolidated financial statements, taken together): Consolidated basis', ln=1)

    # create a response with the PDF file
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers.set('Content-Disposition',
                         'attachment', filename='example.pdf')
    response.headers.set('Content-Type', 'application/pdf')

    return response


@ app.route("/data", methods=['POST'])
@ cross_origin()
def members():
    # To retieve the data recieved from the frontend and using the json.load function
    request_data = json.loads(request.data)
    CREATE_DATABASE()
    ADDING_NEW_ELEMENT(request_data)

    return (" ")


@ app.route("/signup", methods=['POST'])
@ cross_origin()
def Signup_Data():
    request_data = json.loads(request.data)
    create_table_user()
    insert_table_user(request_data)

    return (" ")


@ app.route("/login_add", methods=['POST', "GET"])
@ cross_origin()
def Login_Data():
    global check_user
    check_user = False
    request_data = request.get_json()
    check_user = get_data(request_data)

    return {"state_type": [str(check_user)]}


# Azure code
CONNECTION_STRING = 'mongodb://acb84250-0ee0-4-231-b9ee:nBOe35HkdIxwSM5n7buO3au0wIPT7kIrkfqFdR2roCaTDfRaI7UcixtqvC0J5i2DGfnC86MFnxDyACDbmptjEQ==@acb84250-0ee0-4-231-b9ee.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@acb84250-0ee0-4-231-b9ee@'


DB_NAME = "Vertois"
COLLECTION_NAME = "Vertois"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client[DB_NAME]


def CREATE_DATABASE():
    # Create collection if it doesn't exist
    collection = db[COLLECTION_NAME]
    if COLLECTION_NAME not in db.list_collection_names():
        # Creates a unsharded collection that uses the DBs shared throughput
        db.command(
            {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
        )
        print("Created collection '{}'.\n".format(COLLECTION_NAME))


def ADDING_NEW_ELEMENT(data):

    KEYS = list(data["content"].keys())
    VALUES = list(data["content"].values())

    new_item = {
        "CIN":     VALUES[0],
        KEYS[1]: VALUES[1],
        KEYS[2]: VALUES[2],
        KEYS[3]: VALUES[3],
        KEYS[4]: VALUES[4],
        KEYS[5]: VALUES[5],
        KEYS[6]: VALUES[6],
        KEYS[7]: VALUES[7],

    }
    collection = db[COLLECTION_NAME]

    result = collection.update_one(
        {"id": new_item["CIN"]}, {"$set": new_item}, upsert=True
    )


def GET_VALUES(id):
    ID = list(id["content"].values())
    collection = db[COLLECTION_NAME]
    doc = collection.find_one({"id": ID[0]})
    return doc


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


# to generate a pdf of the data


if __name__ == '__main__':
    app.run(debug=True)
