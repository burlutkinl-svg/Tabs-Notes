import requests
import json

print(requests.get('http://localhost:8000/api/say-hello').json())
