import requests
import json

url='http://localhost:3000/design/users/all'
get_data = {}

res = requests.get(url, params={"hashtag": "Trump"})
	

if res.status_code != 200:
  print("Error:", res.status_code)

data = res.json()

print(data)