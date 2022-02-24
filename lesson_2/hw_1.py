import requests
from bs4 import BeautifulSoup
from pprint import pprint

# start params
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}
vacancy_source = "hh.ru"
url = "https://hh.ru/search/vacancy"
work = "Python"
page_number = 0

params = {"area": 1,
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
response = requests.get(url, headers=headers, params=params)

# body programm

if response.ok: # response 200
    dom = BeautifulSoup(response.text, "html.parser") # create dom
    expected_items = int(dom.find("h1", {"class": "bloko-header-section-3"}).getText().split(" ", 1)[0]) # score of pages
    expected_last_page = expected_items // 50 + 1
    print(f'страниц с данными: {expected_last_page}')

    for x in range(expected_last_page + 1): # pages view
        response = requests.get(url, headers=headers, params=params)
        params["page"] = x
        dom = BeautifulSoup(response.text, "html.parser")
        positions = dom.find_all("div", {"class": "vacancy-serp-item"})

        for position in positions: # loops for read values
            position_data = {}

            position_name_data = position.find('a', {"data-qa": "vacancy-serp__vacancy-title"})
            position_name = position_name_data.getText()
            position_link = position_name_data["href"].split("?", 1)[0]

            position_compensation = position.find('span', {"data-qa": "vacancy-serp__vacancy-compensation"})
            if position_compensation is None:
                min_compensation = "Не объявлено"
                max_compensation = "Не объявлено"
                currency = "Не объявлено"

            else:
                position_compensation = position_compensation.getText()
                currency = position_compensation[position_compensation.rindex(' ') + 1:]
                if "от" in position_compensation:
                    min_compensation = int(''.join(filter(str.isdigit, position_compensation)))
                    max_compensation = "Не объявлено"
                elif "до" in position_compensation:
                    min_compensation = "Не объявлено"
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

print(f'всего вакансий: {len(positions_list)}')
pprint(positions_list)
