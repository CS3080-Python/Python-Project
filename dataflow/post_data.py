import requests
import json

# Add document to CouchDB containing data retrieved from Twitter API
def post_tweet(db_object):
    url='http://localhost:3000/data'
    
    input_data = {}
    input_data['topic'] = db_object.topic
    input_data['sa_type'] = db_object.sa_type
    input_data['sa_score'] = db_object.sa_score   

    res = requests.post(url, json=input_data)

    if res.status_code != 200:
      print("Error: ", res.status_code)
