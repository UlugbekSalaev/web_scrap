import mysql.connector
import requests
from bs4 import BeautifulSoup
import lxml
from time import sleep
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="corpus"
)

cursor = mydb.cursor()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def write_in_file(self, text):
    file = open(str(self.path) + '/' + str(self.filename), mode="w")
    file.write(text)
    file.close()

def get_text(url):
    r = requests.get(url, timeout=5, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    category = soup.find(class_='itemCat').text
    title = soup.find(class_='title-1').text
    date = soup.find(class_='itemDatas').text
    text = ''

    # table = soup.find_all('div', attrs={"class": "postContent"})
    # for x in table:
    #     text += x.find('p').text + '\n\n'

    parag = soup.find_all('p')
    for x in parag:
        if 'Foto:' in x.text:
            continue
        text += x.text + '\n\n'

    #write to db
    sql = "INSERT IGNORE INTO daryouz_sport (title, text, date, url, category) VALUES (%s, %s, %s, %s, %s)"
    val = (title, text, date, url, category)
    cursor.execute(sql, val)
    # mydb.commit()
    # sleep(5)

def get_urls(url):
    '''Returns urls from daryo.uz/uz.'''
    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, "lxml")

    count = 0
    for a in soup.find_all('a', href=True):
        count += 1
        if count > 12:
            break
        if count > 2 and count < 13:
            url1 = a['href']
            url1 = "https://m.daryo.uz" + url1

            try:
                get_text(url1)
                print("Success:"+url1)
            except Exception:
                print("Error processing URL")

for i in range(3185, 3185):
    print("Page:" + str(i))
    get_urls("https://m.daryo.uz/category/sport/page/" + str(i) + "/")
    mydb.commit()
finish