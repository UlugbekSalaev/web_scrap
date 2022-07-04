import mysql.connector
import requests
from bs4 import BeautifulSoup
import lxml
import time

start_time = time.time()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="corpus"
)

cursor = mydb.cursor()


def write_in_file(self, text):
    file = open(str(self.path) + '/' + str(self.filename), mode="w")
    file.write(text)
    file.close()


def get_text(url, category):
    print("Start: " + url)
    try:
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        if "Not Found" in r:
            print(url + " : not found")
            return

        # category = soup.find(class_='itemCat').text
        title = soup.find(class_='post-title').text
        date = soup.find(class_='date').text
        text = ''

        # table = soup.find_all('div', attrs={"class": "postContent"})
        # for x in table:
        #     text += x.find('p').text + '\n\n'

        parag = soup.find_all('p')
        for x in parag:
            if 'Foto:' in x.text:
                continue
            text += x.text + '\n\n'

        # write to db
        sql = "INSERT IGNORE INTO kunuz (title, text, date, url, category) VALUES (%s, %s, %s, %s, %s)"
        val = (title, text, date, url, category)
        cursor.execute(sql, val)
        print("Success:" + url)
    except:
        print("Error:" + url)
    time.sleep(5)

def get_urls(url):
    '''Returns data specifically from kun.uz/uz.'''
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    if "Sahifa topilmadi" in page:
        print(url + " : not found")
        return
    i = 0
    for p in soup.find_all(class_="post-body"):
        i += 1
        if i < 4:
            continue
        url1 = p.find('a')['href']
        url1 = "https://m.kun.uz" + url1
        # caturl = p.find(class_="data").find('a')['href']
        category = p.find(class_="data").find('a').text.strip()
        get_text(url1, category)
    mydb.commit()


for i in range(7403, 11582):
    print("Page:" + str(i))
    get_urls("https://m.kun.uz/uz?q=%2Fuz&page=" + str(i))
    print("--- %s minutes ---" % ((time.time() - start_time) / 60))
