import requests
import json

url='http://localhost:3000/data'
post_data = {"hashtag": "Trump", "user":"Jane Doedoe", "sa_type": "positive", "sa_score": "10"}

res = requests.post(url, json=post_data)
	

if res.status_code != 200:
  print("Error:", res.status_code)

data = res.json()

print(data)