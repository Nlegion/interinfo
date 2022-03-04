from pprint import pprint
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lxml import html

url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

top_news_urls = list(set(dom.xpath("//div[@class='block']//@href")))  # используем set для дедубликации

news_list = []

for news_url in top_news_urls:

    news_item_dict = {}
    news_url_item = news_url
    print(news_url)
    response = requests.get(news_url, headers=headers)
    dom = html.fromstring(response.text)

    news_item_data = dom.xpath("//div[contains(@class, 'article')]")

    news_date = news_item_data[0].xpath(".//span/@datetime")[0]
    news_source = news_item_data[0].xpath(".//span[contains(@class, 'link__text')]/text()")[0]
    news_title = news_item_data[2].xpath(".//p/text()")[0].replace("\xa0", " ")

    news_item_dict["url"] = news_url
    news_item_dict["date"] = news_date
    news_item_dict["source"] = news_source
    news_item_dict["title"] = news_title

    news_list.append(news_item_dict)

pprint(news_list)

client = MongoClient('localhost', 27017)
data_base = client["news_database"]

news_collection = data_base.news_collection

try:
    for news_item in news_list:
        news_collection.insert_one(news_item)

except DuplicateKeyError:
    print(f'Ошибка ключа, id {news_item.get("_id")} ')

print("Данные добавлены")
print(f'всего: {len(news_list)}')