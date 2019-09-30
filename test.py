import json

str = '{"name": "Alenka", "type": "confectionery", "length": 15, "width": 7, "height": 2}'
obj = json.loads(str)
print(obj['name'])