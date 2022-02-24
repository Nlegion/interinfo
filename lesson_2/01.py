import requests
from bs4 import BeautifulSoup
from pprint import pprint

base_url = 'https://www.kinopoisk.ru/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}

params = {'b': 'series'}

url = f'{base_url}/lists/movies/popular/'
response = requests.get(url, headers=headers, params=params)
dom = BeautifulSoup(response.text, 'html.parser')
serials = dom.find_all('div', {'class': 'styles_root__3a8vf'})
serials_list = []
for serials in serials:
    serial_data = {}
    print()
