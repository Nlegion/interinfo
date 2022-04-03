import time

from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service

s = Service('./chromedriver')
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

browser = webdriver.Chrome(service=s, options=chrome_options)
browser.implicitly_wait(5)

browser.get('https://account.mail.ru/login')

login_elem = browser.find_element(By.NAME, 'username')
login_elem.send_keys('study.ai_172')
login_elem.send_keys(Keys.ENTER)

pass_elem = browser.find_element(By.NAME, 'password')
pass_elem.send_keys('NextPassword172#')
pass_elem.send_keys(Keys.ENTER)

settings_elem = browser.find_element(By.CLASS_NAME, 'settings')
settings_elem.click()

try:
    settings_column_elem = browser.find_element(By.XPATH, '//div[@data-test-id="3pane-disabled"]')
    settings_column_elem.click()
except NoSuchElementException:
    pass

webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
mail_qty_menu = browser.find_element(By.CLASS_NAME, "portal-menu-element_deselect")
mail_qty_item = int(mail_qty_menu.find_element(By.CLASS_NAME, 'button2__txt').text)

webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

mail_list = []

for i in range(mail_qty_item):
    webdriver.ActionChains(browser).send_keys(Keys.ARROW_DOWN).perform()

    mail_item_dict = {}

    time.sleep(1)

    try:

        mail_title = browser.find_element(By.CLASS_NAME, 'thread-subject').text
        mail_sender = browser.find_element(By.CLASS_NAME, 'letter-contact').text
        mail_date = browser.find_element(By.CLASS_NAME, 'letter__date').text
        mail_contents = browser.find_element(By.CLASS_NAME, 'letter-body__body-content').get_attribute('innerHTML')

        print(f"reading mail {i + 1} of {mail_qty_item}: {mail_title}")

        mail_item_dict["mail_title"] = mail_title
        mail_item_dict["mail_sender"] = mail_sender
        mail_item_dict["mail_date"] = mail_date
        mail_item_dict["mail_contents"] = mail_contents

        mail_list.append(mail_item_dict)

    except NoSuchElementException:
        continue

client = MongoClient('localhost', 27017)
data_base = client["mail_database"]

mail_collection = data_base.mail_collection

try:
    for mail_item in mail_list:
        mail_collection.insert_one(mail_item)

except DuplicateKeyError:
    print(f'Duplicate key error, item with id {mail_item.get("_id")} skipped')

print("данные добавлены в базу данных")
print(f'всего позиций: {len(mail_list)}')
