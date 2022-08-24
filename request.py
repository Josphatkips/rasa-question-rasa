import requests

url= "http://localhost:8000/api/"
myobj = {'category_id':1 }

x = requests.post(url+'category', json = myobj).json()

print(x['response_code'])
# print(x['questions'])
