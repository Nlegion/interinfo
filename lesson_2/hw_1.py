import requests
from bs4 import BeautifulSoup
from pprint import pprint

# work = input()
work = 'python'
base_url = 'https://hh.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}
params = {'area': '1', 'fromSearchLine': 'true', 'text': work, 'from': 'suggest_post'}
# querystring = {"area": 1, "search_field": "description", "experience": "between1And3", "text": search_text,
#                "clusters": "true", "ored_clusters": "true", "enable_snippets": "true", "from": "suggest_post",
#                "industry": 43,}
positions_list = []

url = f'{base_url}search/vacancy'
response = requests.get(url, headers=headers, params=params)

if response.ok:
    dom = BeautifulSoup(response.text, "html.parser")
    expected_items = int(dom.find("h1", {"class": "bloko-header-section-3"}).getText().split(" ", 1)[0])
    expected_last_page = expected_items // 50 + 1
    print(f'страниц с данными: {expected_last_page}')

    for x in range(expected_last_page + 1):
        response = requests.request("GET", base_url, headers=headers, params=params)
        params["page"] = x
        dom = BeautifulSoup(response.text, "html.parser")
        positions = dom.find_all("div", {"class": "vacancy-serp-item"})
        for position in positions:
            position_data = {}
            position_name_data = position.find('a', {"data-qa": "vacancy-serp__vacancy-title"})
            position_name = position_name_data.getText()
            position_link = position_name_data["href"].split("?", 1)[0]
            position_compensation = position.find('span', {"data-qa": "vacancy-serp__vacancy-compensation"})
            if position_compensation is None:
                min_compensation = "Not Indicated"
                max_compensation = "Not Indicated"
                currency = "Not Indicated"
            else:
                position_compensation = position_compensation.getText()
                currency = position_compensation[position_compensation.rindex(' ') + 1:]
                if "от" in position_compensation:
                    min_compensation = int(''.join(filter(str.isdigit, position_compensation)))
                    max_compensation = "Not Indicated"
                elif "до" in position_compensation:
                    min_compensation = "Not Indicated"
                    max_compensation = int(''.join(filter(str.isdigit, position_compensation)))
                elif "–" in position_compensation:
                    min_compensation = int(''.join(filter(str.isdigit, position_compensation.split("–", 1)[0])))
                    max_compensation = int(''.join(filter(str.isdigit, position_compensation.split("–", 1)[1])))
            position_data["position_source"] = base_url
            position_data["position_name"] = position_name
            position_data["position_link"] = position_link
            position_data["min_compensation"] = min_compensation
            position_data["max_compensation"] = max_compensation
            position_data["currency"] = currency
            positions_list.append(position_data)

print(f'всего позиций: {len(positions_list)}')
pprint(positions_list)
