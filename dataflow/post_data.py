import requests
import json

def post_tweet(tweet):
    url='http://localhost:3000/data'
    
    input_data = {}
    input_data['topic'] = tweet.topic
    input_data['sa_type'] = tweet.sentiment
    input_data['sa_score'] = tweet.sent_score   
       
    # Save for a rainy day...
    #input_data['user'] = tweet.user
    #input_data['text'] = tweet.text
    #input_data['hashtag_list'] = tweet.hashtag_list

    res = requests.post(url, json=input_data)
        

    if res.status_code != 200:
      print("Error:", res.status_code)

    data = res.json()

    print(data)
