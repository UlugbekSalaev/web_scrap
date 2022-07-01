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
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def write_in_file(self, text):
    file = open(str(self.path) + '/' + str(self.filename), mode="w")
    file.write(text)
    file.close()


def get_text(url, category):
    print("Start: " + url)
    try:
        r = requests.get(url, headers=headers).text
        soup = BeautifulSoup(r, 'html.parser')
        if "Not Found" in r:
            print(url + " : not found")
            return

        # category = soup.find(class_='itemCat').text
        title = soup.find(class_='pos_0').text
        date = soup.find(class_='date').text
        text = ''

        # table = soup.find_all('div', attrs={"class": "postContent"})
        # for x in table:
        #     text += x.find('p').text + '\n\n'

        parag = soup.find(class_='fullText').find_all('p')
        for x in parag:
            if 'Foto:' in x.text:
                continue
            if x.text.strip() == '':
                continue
            text += x.text + '\n\n'

        # write to db
        sql = "INSERT IGNORE INTO normauz (title, text, date, url, category) VALUES (%s, %s, %s, %s, %s)"
        val = (title, text, date, url, category)
        cursor.execute(sql, val)
        print("Success:" + url)
    except:
        print("Error:" + url)


def get_urls(url):
    '''Returns data specifically from norma.uz/uz.'''
    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, "lxml")
    if "Sahifa topilmadi" in page:
        print(url + " : not found")
        return

    for p in soup.find(class_='categoryItems').find_all(class_="item"):
        try:
            url1 = p.find('a')['href']
            url1 = "https://www.norma.uz" + url1
            # caturl = p.find(class_="data").find('a')['href']
            category = p.find(class_="serviceInfo").find('a').text.strip()
            get_text(url1, category)
        except:
            print("Bir narsa xatolik!")
    mydb.commit()

for i in range(216, 300):
    print("Page:" + str(i))
    get_urls("https://www.norma.uz/oz/?page=" + str(i))
    print("--- %s minutes ---" % ((time.time() - start_time) / 60))
