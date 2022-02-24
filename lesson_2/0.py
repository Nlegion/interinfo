from pprint import pprint

from bs4 import BeautifulSoup
import requests

response = requests.get('')
dom = BeautifulSoup(response.text, 'html.parser')
tag_a = dom.find('a')

parent_a = tag_a.parent
parent2_a = tag_a.parent.parent
print(parent2_a)

children_div = parent2_a.findChildren(recursive=False)
print(list(children_div))

tag_p = dom.find('p', {'id': 'clickable'})
pprint(tag_p)

tags_p = dom.find_all('p', {'class': ['red', 'paragraph']})
pprint(tags_p)

tags2_p = dom.select('p.paragraph.red')
pprint(tags2_p)
