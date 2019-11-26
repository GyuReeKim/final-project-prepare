# json 파일 읽기

import json

with open('director.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(len(data))
