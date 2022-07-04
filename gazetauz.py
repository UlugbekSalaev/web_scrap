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

def get_text(url, cat, date):
    print("Pr:" + url)
    # time.sleep(5)
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    # category = soup.find(class_='itemCat').text
    title = soup.find(id="article_title").text
    # date = soup.find(class_="articleDateTime").text.strip()
    # text = soup.find(class_='pg-article__text mb-5').text
    text = ""
    for p in soup.find(class_='article-text').find_all('p'):
        text += p.text + "\n"

    # write to db
    sql = "INSERT INTO gazetauz (title, text, date, url, category) VALUES (%s, %s, %s, %s, %s)"
    val = (title, text, date, url, cat)
    cursor.execute(sql, val)
    mydb.commit()

def get_urls(url, cat):
    print("Cat url: " +url)
    time.sleep(5)
    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, "lxml")
    try:
        for c in soup.find_all(class_="nblock"):
            url1 = c.find('h3').find('a', href=True)['href']
            url1 = "https://www.gazeta.uz" + url1
            date = c.find(class_="ndt").text
            try:
                get_text(url1, cat, date)
            except:
                print("Error in get text")

    except Exception:
        print("Error in get URL")

cats = ["Jamiyat", "Siyosat", "Iqtisodiyot", "Sport", "Kolumnist", "Koronavirus"]
catsid = ["society", "politics", "economy", "sport", "column", "coronavirus"]
catscnt = [690, 245, 226, 81, 5, 98,]

ind = 0
for i in range(56, catscnt[ind]+1):
    print("Page:" + cats[ind] + ": " + str(i))
    get_urls("https://gazeta.uz/oz/"+catsid[ind]+"?page=" + str(i), cats[ind])