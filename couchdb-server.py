import couchdb
from flask import Flask
from flask import request

# GLOBAL VALUES #
SERVER_HOST_NAME = "localhost"
SERVER_PORT = 3000

ADMIN_UN = "admin"
ADMIN_PW = "password"
DB_ADDRESS = "http://" + ADMIN_UN + ":" + ADMIN_PW + "@" + SERVER_HOST_NAME + ":5984/"
DB_NAME = "py-project-db"


# SETUP COUCHDB #
# Get a reference to our CouchDB server + database
couch = couchdb.Server(DB_ADDRESS) 
db = couch[DB_NAME]


# FLASK REST API #
app = Flask(__name__)

# GET Design Doc Rows
@app.route("/design/<doc_name>/<index_name>", methods=["GET"])
def getDesignDoc(doc_name, index_name):
    for row in db.view(name=doc_name + "/" + index_name).rows:
        return row.value

# POST a new document (payload should be in JSON format)
@app.route("/create_doc", methods=["POST"])
def createDoc():
    doc_id, doc_rev = db.save({"key1": request.json["value1"], "key2": request.json["value2"]})
    return "Successfully created new document. ID: " + doc_id + ", REV: " + doc_rev


# Start Flask server
if __name__ == "__main__":
    app.run(host=SERVER_HOST_NAME, port=SERVER_PORT, debug=False) # Set "debug" to True for console logs
