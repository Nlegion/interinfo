import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}
vacancy_source = "hh.ru"
base_url = "https://hh.ru/search/vacancy"
work = "Python"
page_number = 0
items_on_page = 20

querystring = {"area": 1,
               "search_field": "description",
               "experience": "between1And3",
               "text": work,
               "clusters": "true",
               "ored_clusters": "true",
               "enable_snippets": "true",
               "from": "suggest_post",
               "industry": 7,
               "professional_role": 96,
               "page": page_number
               }

positions_list = []

response = requests.request("GET", base_url, headers=headers, params=querystring)

if response.ok:
    dom = BeautifulSoup(response.text, "html.parser")
    expected_items = int(dom.find("h1", {"class": "bloko-header-section-3"}).getText().split(" ", 1)[0])
    expected_last_page = expected_items // items_on_page + 1
    print(f'страниц с данными: {expected_last_page}')

    for x in range(expected_last_page + 1):
        response = requests.request("GET", base_url, headers=headers, params=querystring)
        querystring["page"] = x
        dom = BeautifulSoup(response.text, "html.parser")
        positions = dom.find_all("div", {"class": "vacancy-serp-item"})

        for position in positions:
            position_data = {}

            position_name_data = position.find('a', {"data-qa": "vacancy-serp__vacancy-title"})
            position_name = position_name_data.getText()
            position_link = position_name_data["href"].split("?", 1)[0]
            position_id = position_link.split("/")[4]

            position_compensation = position.find('span', {"data-qa": "vacancy-serp__vacancy-compensation"})
            if position_compensation is None:
                min_compensation = None
                max_compensation = None
                currency = None

            else:
                position_compensation = position_compensation.getText()
                currency = position_compensation[position_compensation.rindex(' ') + 1:]
                if "от" in position_compensation:
                    min_compensation = int(''.join(filter(str.isdigit, position_compensation)))
                    max_compensation = None
                elif "до" in position_compensation:
                    min_compensation = None
                    max_compensation = int(''.join(filter(str.isdigit, position_compensation)))
                elif "–" in position_compensation:
                    min_compensation = int(''.join(filter(str.isdigit, position_compensation.split("–", 1)[0])))
                    max_compensation = int(''.join(filter(str.isdigit, position_compensation.split("–", 1)[1])))

            position_data["position_source"] = vacancy_source
            position_data["position_name"] = position_name
            position_data["position_link"] = position_link
            position_data["min_compensation"] = min_compensation
            position_data["max_compensation"] = max_compensation
            position_data["currency"] = currency

            positions_list.append(position_data)

client = MongoClient('localhost', 27017)
data_base = client["positions_database"]

positions_collection = data_base.positions_collection

try:
    for position in positions_list:
        positions_collection.insert_one(position)

except DuplicateKeyError:
    print(f'Duplicate key error, item with id {position.get("_id")} skipped')

print("данные добавлены в базу данных")
print(f'всего позиций: {len(positions_list)}')
