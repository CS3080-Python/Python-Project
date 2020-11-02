import requests
import json

# Define functions for each view type
def get_topic_data(topic):
  url = 'http://localhost:3000/design/topics/' + topic
  get_data(url)

def get_saType_data(sa_type):
  url='http://localhost:3000/design/sa_types/' + sa_type
  get_data(url)

# General function to retrieve data from database given a valid URL
def get_data(url):
  res = requests.get(url)
  
  if res.status_code != 200:
    print("Error:", res.status_code)

  data = res.json()
  return data