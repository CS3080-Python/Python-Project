import couchdb
from flask import Flask
from flask import request
from flask import render_template #optional, but useful
from flask import jsonify
import datetime

import sys  
sys.path.append('C:\CS3080\Python-Project\sentiment_analysis')  
from get_sentiment import SentimentAnalysis # get tweet/set analysis

# GLOBAL VALUES #
SERVER_HOST_NAME = "localhost"
SERVER_PORT = 3000

ADMIN_UN = "admin"
ADMIN_PW = "**CS-3080**"
DB_ADDRESS = "http://" + ADMIN_UN + ":" + ADMIN_PW + "@" + SERVER_HOST_NAME + ":5984/"
DB_NAME = "py-project-db"

VIEWS_LIST = ["topics", "users", "sa_types", "sa_scores", "texts", "hashtags"]               # List of views in the database
REQUIRED_PARAMS = ["topic", "user", "sa_type", "sa_score", "text", "hashtag_list"] # Key values that must be present in POST requests to the server

# SETUP COUCHDB #
# Get a reference to our CouchDB server + database
couch = couchdb.Server(DB_ADDRESS) 
db = couch[DB_NAME]


# FLASK REST API #
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/status", methods=["GET"])
def status():
    return render_template('status.html', status='OK', updatetime=datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"))
                                  
# serving form web page
@app.route("/search")
def form():
    return render_template('search.html')

# handling form data
@app.route('/form-handler', methods=['POST'])
def handle_data():
    # since we sent the data using POST, we'll use request.form
    #print('Hashtag to Search (request.form): ', request.form['hashtag'])
    
    # we can also request.values
    #print('Hashtag to Search (request.values): ', request.values['hashtag'])
    #return "Request received successfully!"
    SentimentAnalysis(request.values['topic'])
    return jsonify(request.form)

# GET - Retrieve data for the specified design document and view (pass "all" to view_name to see all documents)
@app.route("/design/<ddoc_name>/<view_name>", methods=["GET"])
def getDesignDoc(ddoc_name, view_name):
    for row in db.view(name=ddoc_name + "/" + view_name).rows:
        return row.value


# POST - Add a document to database using data received from Twitter API
@app.route("/data", methods=["POST"])
def receivedTwitterData():

    # Make sure POST request body includes the required parameters
    for param in REQUIRED_PARAMS:
        if not param in request.json:
            return {"res": "POST request data MUST contain a \'" + param + "\' key!"}, 400

    # Check whether a view already exists for each of the parameters, and if not, create a new one
    '''
    for i, view in enumerate(VIEWS_LIST):
        try:
            print('View', view)
            db.view(name=view + "/" + request.json[REQUIRED_PARAMS[i]]).rows
        except:
            createNewView(view, request.json[REQUIRED_PARAMS[i]], REQUIRED_PARAMS[i]) 
    '''
    # Add document containing the Twitter data to database
    createDoc(request.json)

    return {"res": "Received Twitter data and successfully added it to the database."}, 200


# Add a new view to the specified design document, so we can filter docs by the specified field name
def createNewView(ddoc_id, view_name, field_name):

    # @ params
    # ddoc_id: The name of the design document (i.e. the part after "_design/")
    # view_name: The name of the view to create
    # field_name: The name of the field to filter docuemnts by
    
    doc = db["_design/" + ddoc_id]
    doc["views"][view_name] = {"map": "function (doc) { if (doc.article_data." + field_name + " == \"" + view_name + "\") { emit(doc._id, 1); } }"}
    db.save(doc)

    return {"res": "Successfully created new view \'" + view_name + "\' in design document \'" + ddoc_id + "\'"}, 200


# Create a new document based on data received from Twitter API
def createDoc(json_data):
    doc_data = {
        "article_data": { 
            "topic": json_data["topic"], 
            "user": json_data["user"], 
            "sa_score": json_data["sa_score"],
            "sa_type": json_data["sa_type"],
            "text": json_data['text'],
            "hashtag": json_data['hashtag_list']
        }
    }
    doc_id, doc_rev = db.save(doc_data)

    return {"res": "Successfully created new document. ID: " + doc_id + ", REV: " + doc_rev}, 200


# Start Flask server
if __name__ == "__main__":
    app.run(host=SERVER_HOST_NAME, port=SERVER_PORT, debug=False) # Set "debug" to True for console logs

