import json
from types import resolve_bases
import requests

response = requests.post('http://127.0.0.1:5555/commands',data={
    'func': 'cmd',
    'info': json.dumps({
        'id': '98.57.252.204',
        'input': 'disconnect'
    })
})

print(response.status_code)
print(response.json())