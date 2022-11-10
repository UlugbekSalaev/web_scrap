import time
import mysql.connector
import requests
from bs4 import BeautifulSoup
import lxml

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="corpus"
)

cursor = mydb.cursor()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def get_text(url, i):
    print(i, "Pr:", url)
    # time.sleep(5)
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    if not soup.find(class_="docBody__content-em"):
        return
    if soup.find(class_='ACT_FORM'):
        category = soup.find(class_='ACT_FORM').text
    else:
        category = ""
    title = soup.find(class_="ACT_TITLE").text
    date = soup.find(class_="docHeader__item-value d-flex").text.strip()
    # text = soup.find(class_='pg-article__text mb-5').text
    text = ""
    for p in soup.find(class_='docBody__content-em').find_all(class_='ACT_TEXT lx_elem_comment'):
        text += p.text + "\n"

    # write to db
    sql = "INSERT IGNORE INTO lexuz (title, text, date, url, category) VALUES (%s, %s, %s, %s, %s)"
    val = (title, text, date, url, category)
    cursor.execute(sql, val)
    mydb.commit()
    # print(date, category, title, text)

i = 0
with open("lexuz.txt") as file:
    for line in file:
        i = i + 1
        if i>1716:
            get_text(line.rstrip(), i)