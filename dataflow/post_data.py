import requests
import json

def post_tweet(db_object):
    url='http://localhost:3000/data'
    
    input_data = {}
    input_data['topic'] = db_object.topic
    input_data['sa_type'] = db_object.sa_type
    input_data['sa_score'] = db_object.sa_score   
       
    # Save for a rainy day...
    #input_data['user'] = db_object.user
    #input_data['text'] = db_object.text
    #input_data['hashtag_list'] = db_object.hashtag_list

    res = requests.post(url, json=input_data)
        

    if res.status_code != 200:
      print("Error:", res.status_code)

    data = res.json()

    print(data)
