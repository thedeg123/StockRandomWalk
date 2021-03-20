import json
with open('../static/profile.json') as f:
    data = json.load(f)
    print(data)
