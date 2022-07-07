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

def get_text(url, cat):
    print("Pr:" + url)
    # time.sleep(5)
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    # category = soup.find(class_='itemCat').text
    title = soup.find(class_="single-title").text
    date = soup.find(class_="post-date").text.strip()
    # text = soup.find(class_='pg-article__text mb-5').text
    text = ""
    for p in soup.find(class_='single-content-self').find_all('p'):
        if p.text.startswith("Facebook:") or p.text.startswith("Reklama hu"):
            continue
        text += p.text + "\n"

    # write to db
    sql = "INSERT IGNORE INTO zirauz (title, text, date, url, category) VALUES (%s, %s, %s, %s, %s)"
    val = (title, text, date, url, cat)
    cursor.execute(sql, val)

def get_urls(url, cat):
    print("Cat url: " +url)
    # time.sleep(5)
    get_text("https://zira.uz/uz/recipe/videoretsept-chumoli-uyi-muraveynik-pishirig-i/", cat)

    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, "lxml")
    try:
        for c in soup.find_all(class_="masonry-item"):
            url1 = c.find('h3').find('a', href=True)['href']
            # date = c.find(class_="ndt").text
            try:
                get_text(url1, cat)
            except:
                print("Error in get text")
        mydb.commit()

    except Exception:
        print("Error in get URL")

cats = ["shirinliklar", "quyuq-taomlar", "suyuq-taomlar", "qaylalar", "nonushtalar", "ichimliklar"]
# catsid = ["society", "politics", "economy", "sport", "column", "coronavirus"]
catscnt = [16, 20, 4, 2, 6, 3,]

ind = 5
for i in range(1, catscnt[ind]+1):
    print("Page:" + cats[ind] + ": " + str(i))
    get_urls("https://zira.uz/uz/s/"+cats[ind]+"/page/" + str(i), cats[ind])

finish