import pprint
import requests
import json

# requests settings
appid = ''
service = 'https://api.github.com/users/'
user_name = 'nlegion'
set = '/repos'
req = requests.get(f'{service}{user_name}{set}')
data = req.json()

# users repo
repo = []
for item in data:
    repo.append(item['name'])
print(f'Список репозиторием пользователя {user_name}:{repo}')

with open('hw_1_repos.json', 'w') as f:
    json_repo = json.dump(repo, f)
