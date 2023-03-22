# All of the imports need to run the server
#
# the flask library is used to create the server and host the REST API
# They include the MySQL connect to MySQL database to store all the user details.
# the azure cosmos library allow connectivity to the microsoft azure database
# flsak cors is used help with cross cors compatibilty

from flask import Flask, json, request, Response, render_template, redirect, send_file, make_response
import bcrypt
import json
from flask_cors import CORS, cross_origin
from azure.cosmos import CosmosClient, PartitionKey
import mysql.connector as mys
import pdfkit
import pymongo
from flask_weasyprint import HTML, render_pdf
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table
import PyPDF2
from io import BytesIO
from docx import Document


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

    # Render the HTML template
    html = render_template('file.html')

    # Generate the PDF
    pdf = render_pdf(HTML(string=html))

    # Create a response object with the PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=my_pdf.pdf'
    return response

    # Create a new PDF using ReportLab
    pdf = canvas.Canvas('example.pdf')

    # Add content to the PDF
    pdf.setFont('Helvetica', 12)
    pdf.drawString(1 * inch, 10.5 * inch, "old")

    # Add a table to the PDF
    data = [['Name', 'Age', 'Gender'], [
        'John', '35', 'Male'], ['Jane', '28', 'Female']]
    table = Table(data)
    table.wrapOn(pdf, 0, 0)
    table.drawOn(pdf, 1 * inch, 6 * inch)

    # Save the PDF
    pdf.save()

    # Return the PDF as a response
    response = make_response(open('example.pdf', 'rb').read())
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition',
                         'attachment', filename='example.pdf')
    return response

    rendered_html = render_template('file.html', CIN='cin')
    html = HTML(string=rendered_html)
    pdf_file = 'file.pdf'
    css = CSS(string='@page { size: legal landscape; }')
    html.write_pdf(pdf_file, stylesheets=[css])
    return send_file(pdf_file, as_attachment=True)

    # out = render_template('file.html', CIN='cin')

    options = {
        "orientation": "landscape",
        "page-size": 'Legal',
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
        "enable-local-file-access": ""
    }

    # # Build PDF from HTML
    pdf = pdfkit.from_string(out, options=options)
    # pdf = pdfkit.from_string(out, options=options,configuration = config)

    # #  Download the PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    return out


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
