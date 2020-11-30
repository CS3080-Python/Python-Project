import couchdb
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import datetime

import sys  
sys.path.append('C:\CS3080\Python-Project\sentiment_analysis')  
from get_sentiment import SentimentAnalysis # Get tweet/set analysis
from get_data import get_topic_data

# GLOBAL VALUES #
SERVER_HOST_NAME = "localhost"
SERVER_PORT = 3000

ADMIN_UN = "admin"
ADMIN_PW = "**CS-3080**"
DB_ADDRESS = "http://" + ADMIN_UN + ":" + ADMIN_PW + "@" + SERVER_HOST_NAME + ":5984/"
DB_NAME = "py-project-db"

VIEWS_LIST = ["topics", "sa_types"]                # List of views in the database
REQUIRED_PARAMS = ["topic", "sa_type", "sa_score"] # Key values that must be present in POST requests to the server

# SETUP COUCHDB #
# Get a reference to our CouchDB server + database
couch = couchdb.Server(DB_ADDRESS) 
db = couch[DB_NAME]


# FLASK REST API #
app = Flask(__name__)

# WEB FORM HANDLING #
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/status", methods=["GET"])
def status():
    return render_template('status.html', status='OK', updatetime=datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"))

@app.route('/search')
def searchForm():
    return render_template('search.html')

@app.route('/database')
def dbForm():
    return render_template('database.html')


# Handle Search Form data
@app.route('/search-form-handler', methods=['POST'])
def handleSearchData():
    
    # Run sentiment analysis on the topic provided in the Search form
    db_obj = SentimentAnalysis(request.values['topic'])
    return render_template('meter.html', topic=db_obj.topic, sa_type=db_obj.sa_type, sa_score=db_obj.sa_score, source="Sentiment Analysis")


# Handle Database Query Form data
@app.route('/db-form-handler', methods=['POST'])
def handleDBQuery():
    
    # Check to see if there is a document for the requested topic currently in the database, take user to an error page if not
    try:
        doc_data = get_topic_data(request.values['topic'])['1']
        return render_template('meter.html', topic=doc_data['topic'], sa_type=doc_data['sa_type'], sa_score=doc_data['sa_score'], source="database")
    except:
        return render_template('database_error.html', topic=request.values['topic'])


# DATABASE INTERACTION #

# GET - Retrieve data for the specified design document and view (pass "all" to view_name to see all documents)
@app.route("/design/<ddoc_name>/<view_name>", methods=["GET"])
def getDesignDoc(ddoc_name, view_name):
   
    try:
        # Ensure the view exists
        db.view(name=ddoc_name + "/" + view_name, include_docs=True).rows

        return_json = {}
        row_num = 1

        # Add all rows in the view to a JSON return value, where each row is identified by a numerical key
        for item in db.view(name=ddoc_name + "/" + view_name, include_docs=True):
            return_json[str(row_num)] = item.doc["article_data"]
            row_num += 1
        return return_json

    # View is not valid
    except:
        return "The specified " + ddoc_name + " could not be found in the database.", 200


# POST - Add a document to database using data received from Twitter API
@app.route("/data", methods=["POST"])
def receivedTwitterData():

    # Make sure POST request body includes the required parameters
    for param in REQUIRED_PARAMS:
        if not param in request.json:
            return "POST request data MUST contain a \'" + param + "\' key!", 400

    # Check whether a view already exists for each of the parameters. If so, update the document. Otherwise, create a new one
    for i, view in enumerate(VIEWS_LIST):
        try:
            db.view(name=view + "/" + request.json[REQUIRED_PARAMS[i]]).rows
        except:
            createNewView(view, request.json[REQUIRED_PARAMS[i]], REQUIRED_PARAMS[i]) 

    # Check whether document already exists under this view, and if so, update it
    if len(db.view(name="topics" + "/" + request.json["topic"], include_docs=True).rows) > 0:
        for item in db.view(name="topics" + "/" + request.json["topic"], include_docs=True):
            for param in REQUIRED_PARAMS:
                item.doc["article_data"][param] = request.json[param]
                item.doc["article_data"][param] = request.json[param]
           
            doc_id, doc_rev = db.save(item.doc)
            print("Updated document with ID " + doc_id + "@" + doc_rev + ".")

    # If no existing document, create a new one
    else:
        createDoc(request.json)

    # Add document containing the Twitter data to database
    return "Received Twitter data and successfully added it to the database.", 200


# Add a new view to the specified design document, so we can filter docs by the specified field name
def createNewView(ddoc_id, view_name, field_name):

    # @params
    # ddoc_id: The name of the design document (i.e. the part after "_design/")
    # view_name: The name of the view to create
    # field_name: The name of the field to filter docuemnts by
    
    doc = db["_design/" + ddoc_id]
    doc["views"][view_name] = {"map": "function (doc) { if (doc.article_data." + field_name + " == \"" + view_name + "\") { emit(doc._id, 1); } }"}
    db.save(doc)

    return "Successfully created new view \'" + view_name + "\' in design document \'" + ddoc_id + "\'", 200


# Create a new document based on data received from Twitter API
def createDoc(json_data):

    # Set initial document data
    doc_data = { "article_data": { } }

    # Add all required parameters to document
    for param in REQUIRED_PARAMS:
        doc_data["article_data"][param] = json_data[param]

    doc_id, doc_rev = db.save(doc_data)

    return "Successfully created new document. ID: " + doc_id + ", REV: " + doc_rev, 200


# Start Flask server
if __name__ == "__main__":
    app.run(host=SERVER_HOST_NAME, port=SERVER_PORT, debug=False)
