# All of the imports need to run the server
#
# the flask library is used to create the server and host the REST API
# They include the MySQL connect to MySQL database to store all the user details.
# flsak cors is used help with cross cors compatibilty

from flask import Flask, json, request, Response, render_template, redirect, send_file, make_response
import bcrypt
from flask_cors import CORS, cross_origin
import mysql.connector as mys
import pymongo
from fpdf import FPDF

# to initialize the flask framwork
app = Flask(__name__)
CORS(app)


# This is the code for all the routes

# this is the loaidng page rout that is used as a starting point for the API
# Remove later


@app.route("/")
def home():
    return "Hello world"

#                                 API ENDPOINT ROUTING

# This is the API route that recieves the login details from the login page from the frontend and then
# checks if the email id and password are vaild and present in the database by passing the retrieved
# data to the GET_VALUES_OF_SPECIFIC_USER() which is defined in the MySQL sections. The function then
# returns True or Flase to the frontned


# API route is "/user" which allows POST and GET HTTPS Requests
# cross_origin() function is used to prevent cross origin error


@app.route("/user", methods=['POST', "GET"])
@cross_origin()
def user_data_entries():

    # request.get_json() functions retrieves the data from the frontend and is in the
    # format {"content":["email@gmail.com","passwrd"]}
    data = request.get_json()

    # The data must be parsed and a list of email and password is sent as the arrgument in
    # GET_VALUES_OF_SPECIFIC_USER() function which returns True or False
    current_user = GET_VALUES_OF_SPECIFIC_USER(data['content'])
    print(current_user)
    # names = {}
    # for i in range(0,len(current_user)):
    #     names[str(i)] = current_user[i]

    # This function returns JSON data to the frontend and return True or False
    # The JSON data is of the fromat :- {"current_user": 'True'/'False'}
    return {"current_user": current_user}


# This is the API route that recieves the CIN number details from the PDF page from the frontend and then
# by passing the retrieved data to the GET_VALUES() which is defined in the MongoDB sections. The function then
# returns a dictionary of data with key value pair of company information


# API route is "/pdf" which allows POST and GET HTTPS Requests
# cross_origin() function is used to prevent cross origin error
@app.route("/pdf", methods=['POST', "GET"])
@cross_origin()
def downloade_data():

    # request.get_json() functions retrieves the data from the frontend and is in the
    # format {"content":{"CIN" : "1234567890"}}
    data = (request.json)['content']
    print(data)

    # Since data is a dictionary of CIN data we have to extract the CIN number to do so we get the
    # values using values() function which then retuen the values in dict_values format which is then
    # converted to a list using the list() function and the first value in this list in the CIN number
    # we need and hence we get [0]the value
    CIN = list(data.values())[0]

    # After extracting the CIN number we pass it into the GET_VALUES() function as the argument
    # which returns a dictionary of key values pair with all the specific company information
    VALUES = GET_VALUES(CIN)

    # create a new PDF object
    pdf = FPDF()
    pdf.add_page()  # add a new page

    # set some properties of the PDF file
    pdf.set_title('BRSR Report')
    pdf.set_author('Vertois')
    pdf.set_subject('pdf document for BRSR report')

    # Cells are blocks in the pdf document that are used to enter text data into

    # add some text to the PDF file
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'VERTOIS', ln=1)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(40, 10, 'Business Responsibility & Sustainability Report', ln=1)

    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, 'I. Details of the listed entity', ln=1)

    # The 1st entry is CIN this the hending of the main cin number but the input will come after
    # the 9th entry to maintain conitnuty in the display
    pdf.set_font('Arial', "B", 8)
    pdf.cell(
        87, 5, '1)     Corporate Identity Number (CIN) of the Listed Entity:', ln=0)

    # the entry is the financial year but this the 9th input but since there must be 2 columns the next
    # entry in the code is the 9th entry
    pdf.set_font('Arial', "B", 8)
    pdf.cell(73, 5, '9)     Financial year for which reporting is being done: ',
             ln=0, )
    pdf.set_font('Arial', "", 8)
    pdf.cell(40, 5, 'April 2021 - March 2022', ln=1, )

    # since the output for the CIN entry must be below the the entry heading just the input is the next
    # code in order to match the input to be be just below the title
    pdf.set_font('Arial', "", 8)
    pdf.cell(10, 5, "          "+CIN, ln=1)

    # the next part of the code is the title for the 2nd entry which is the name of the counrty
    pdf.set_font('Arial', "B", 8)
    pdf.cell(
        42, 5, '2)     Name of the Listed Entity: ', ln=0)

    pdf.set_font('Arial', "", 8)
    pdf.cell(
        45, 5, VALUES['Name'], ln=0,)

    # The 3dh entry is the next entry which is beside the 2nd entry
    pdf.set_font('Arial', "B", 8)
    pdf.cell(37, 5, '3)     Year of incorporation: ', ln=0)
    pdf.set_font('Arial', "", 8)
    pdf.cell(
        10, 5, VALUES['Year'], ln=1)

    # The next entry is 4th which is below the 2nd entry
    pdf.set_font('Arial', "B", 8)
    pdf.multi_cell(80, 5, '4)    Registered office address:')
    pdf.set_font('Arial', "", 8)

    # Here we use a multi_cell instead of a normal cell since the lenght of the address can vary and
    # hence the cell must adjust its length according to lenght of address in order to maintain
    # continuity. The extra space is adjusted to the space for the title
    # "4)    Registered office address:"
    pdf.set_xy(15, 55)
    pdf.multi_cell(
        80, 5, "                                           "+VALUES['office Address'])

    # the next entry is the 5th entry which is below the 4th entry
    pdf.set_font('Arial', "B", 8)
    pdf.cell(35, 5, '5)     Corporate address:')

    # since the corperate address can vary in lenght hence a multi cell must be used but a multi cell
    # cannot be placed next to another cell and hence the position must be manually added and hence
    # to maintian contunity the next entry which is the 11th entry
    pdf.set_xy(96, 55)
    pdf.set_font('Arial', "B", 8)
    pdf.cell(40, 5, '11)     Paid-up Capital: ', ln=1)
    pdf.set_font('Arial', "", 8)
    pdf.set_xy(127, 55)
    pdf.cell(
        10, 5, 'INR 319.56 crore')

    # to maintian the continuty the mutli cell coorperate address is added next
    pdf.set_font('Arial', "", 8)
    pdf.set_xy(15, 65)
    pdf.multi_cell(
        80, 5, "                                "+VALUES['Corporate Address'])

    # The next entry is Email
    pdf.set_font('Arial', "B", 8)
    pdf.cell(17, 5, '6)     E-mail:', ln=0)
    pdf.set_font('Arial', "", 8)
    pdf.cell(
        40, 5, VALUES['Email'], ln=1)

    # The next entry is telephone
    pdf.set_font('Arial', "B", 8)
    pdf.cell(22, 5, '7)     Telephone:', ln=0)
    pdf.set_font('Arial', "", 8)
    pdf.cell(
        40, 5, VALUES['telephone'], ln=1)

    # The next entry is Website
    pdf.set_font('Arial', "B", 8)
    pdf.cell(20, 5, '8)     Website:', ln=0)
    pdf.set_font('Arial', "", 8)
    pdf.cell(40, 5, VALUES['website'], ln=1)

    # The next entry is contact details that must align with the 4th entry and hence the position
    # is adjusted using the set_xy() function
    pdf.set_xy(96, 60)
    pdf.set_font('Arial', "B", 8)
    pdf.multi_cell(
        95, 5, '12)  Name and contact details (telephone, email address) of the person who may be contacted in case of any queries on the BRSR report: ')
    pdf.set_font('Arial', "", 8)
    pdf.set_xy(97, 70)
    pdf.multi_cell(
        95, 5, '           Ms. Jyoti Kumar Bansal, Chief-Branding, Corp Communication, CSR & Sustainability')
    pdf.set_xy(88, 80)
    pdf.cell(40, 5, '           Email - jyotikumar.bansal@tatapower.com', ln=1)

    pdf.set_xy(88, 85)
    pdf.cell(40, 5, '           Contact Number: 022-6717 1666', ln=1)

    # The next entry is Reporting boundary details that must align with the 5th entry and hence the position
    # is adjusted using the set_xy() function
    pdf.set_font('Arial', "B", 8)
    pdf.set_xy(97, 90)
    pdf.multi_cell(95, 5, '13) Reporting boundary - Are the disclosures under this report made on a standalone basis (i.e. only for the entity) or on a consolidated basis (i.e. for the entity and all the entities which form a part of its consolidated financial statements, taken together): ')
    pdf.set_font('Arial', "", 8)
    pdf.set_xy(157, 105)
    pdf.cell(40, 5, '           Consolidated basis', ln=1)

    # create a response with the PDF file
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers.set('Content-Disposition',
                         'attachment', filename='example.pdf')
    response.headers.set('Content-Type', 'application/pdf')

    return response


# This is a rout that allows to add the BRSR report data to the MongoDB database in the MongoDB cloud
# storage provider the entry point for the API is /data and it is using the POST HTTP request


@ app.route("/data", methods=['POST'])
@ cross_origin()
def members():
    # To retieve the data recieved from the frontend and using the json.load function and
    request_data = json.loads(request.data)

    # This function is used to create a MongoDB database that makes adding all the BRSR data
    CREATE_DATABASE()

    # The requested data is then sent to the ADDING_NEW_ELEMENT() function as argument to add the data
    # into the MongoDB database
    ADDING_NEW_ELEMENT(request_data)

    return (" ")


# This is a route that allows users to create a profile to store thier company details and store the
# details in a MySQL database and the entry point for the API is /signup and it is using
# the POST HTTP request


@ app.route("/signup", methods=['POST'])
@ cross_origin()
def Signup_Data():

    # Get the user signup data from the frontend
    request_data = json.loads(request.data)

    # This function is used to create a MySQL database
    create_table_user()

    # This function is used to add all the data into the MySQL database
    insert_table_user(request_data)

    return (" ")

# This is a route that allows users to Login into their profile and checks if the user is valid
#  and present in the dataase and the entry point for the API is /signup and it is using
# the POST and GET HTTPS request


@ app.route("/login_add", methods=['POST', "GET"])
@ cross_origin()
def Login_Data():
    global check_user
    check_user = False
    request_data = request.get_json()

    # The get_data() function passes the data from the frontend which is the login data and then
    # checks if the user is present in the database and returns a list of data which includes
    # a True or False if the user is valid and the user name to keep track of which account is being used
    check_user = get_data(request_data)

    # This function sends JSON data with state type which tells if th euser is valid or not
    # and user which tells the username
    return {"state_type": [str(check_user[0])], "user": [str(check_user[1])]}


#                                MONGODB DATABASE FUNCTIONS


# Azure code
CONNECTION_STRING = 'mongodb+srv://prerakjiwane:X773MuzK2EBte20t@brsrdata.s8idggf.mongodb.net/?retryWrites=true&w=majority'


DB_NAME = "BrsrData"
COLLECTION_NAME = "Vertois"

# This function allows connection to the cloud database using the unique CONNECTION KEY
client = pymongo.MongoClient(CONNECTION_STRING)

# This specifies which databse must be used which in this case is BrsrData
db = client[DB_NAME]

# This function decleration is used to create a document to store data in the database only if the
# document does not exist


def CREATE_DATABASE():
    # Create collection if it doesn't exist
    collection = db[COLLECTION_NAME]

    if COLLECTION_NAME not in db.list_collection_names():
        # Creates a unsharded collection that uses the DBs shared throughput
        db.command(
            {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
        )
        print("Created collection '{}'.\n".format(COLLECTION_NAME))


# This function is used to add the BRSR data to the document in the database
def ADDING_NEW_ELEMENT(data):
    try:
        # The data from the fronend is not organised and must be parsed to get the needed data and hence
        # new data must be reorganised into a dictonary with exact key value pairs

        # To get all the keys from data which is in the format {"content" : {.....}} and hence first we
        # extract the dictionary from data and then extract the keys from that dictionary using the
        # keys() function and which return a dict_keys type which is then converted to a list
        KEYS = list(data["content"].keys())

        # The process to getting a list of values from data is similar to the process of extracting
        # keys
        VALUES = list(data["content"].values())

        # The new data is then added to a new dictionary to easily store all the data
        new_item = {
            KEYS[0]: VALUES[0],
            KEYS[1]: VALUES[1],
            KEYS[2]: VALUES[2],
            KEYS[3]: VALUES[3],
            KEYS[4]: VALUES[4],
            KEYS[5]: VALUES[5],
            KEYS[6]: VALUES[6],
            KEYS[7]: VALUES[7],
            KEYS[8]: VALUES[8],
            KEYS[9]: VALUES[9],
            KEYS[10]: VALUES[10],
            KEYS[11]: VALUES[11],
            KEYS[12]: VALUES[12],
        }

        # Next we have to get the document to which we have to add the data
        collection = db[COLLECTION_NAME]

        # this then adds the data
        result = collection.update_one(
            {"id": new_item["CIN"]}, {"$set": new_item}, upsert=True
        )
        #
        # result = collection.insert_one(
        #     {"id": new_item["CIN"]}, {"$set": new_item}
        # )
    except Exception as e:
        print(e)


# This function is used to retrun all the data which has a specific id
def GET_VALUES(id):
    collection = db[COLLECTION_NAME]
    doc = collection.find_one({"id": id})
    return doc

# This function is used to retrun only the id, name and company cin number


def GET_VALUES_OF_SPECIFIC_USER(id):
    collection = db[COLLECTION_NAME]
    results = collection.find({"user": id})
    num = 0
    LST_COMPANY_NAME = []
    for doc in results:
        num += 1
        LST_COMPANY_NAME.append(
            {'id': num, 'name': doc['Name'], 'cin': doc['CIN']})
    return LST_COMPANY_NAME


#                             MYSQL DATABASE FUNCTIONS


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

#                   To insert the user information


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

#                   To return True or False and check if the user exists or not


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

        # if there is no user with the specific email and password then the the lsit is empty and
        # then return False
        if len(rs[0]) != 0:

            # This is used to unhash and check if the password matchs
            hashed_password = (rs[0][2]).encode()
            encode_value = (VALUES[1]).encode()
            if bcrypt.checkpw(encode_value, hashed_password):
                return [True, VALUES[0]]
            else:
                return False
    except Exception as e:
        print(e)


# to generate a pdf of the data


if __name__ == '__main__':
    app.run(debug=True)
