import requests

url= "http://localhost:8000/api/"
myobj = {'question':" " }

x = requests.post(url+'query', json = myobj).json()

print(x)
# print(x['questions'])
