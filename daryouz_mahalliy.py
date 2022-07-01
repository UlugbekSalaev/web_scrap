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

def write_in_file(self, text):
    file = open(str(self.path) + '/' + str(self.filename), mode="w")
    file.write(text)
    file.close()

def get_text(url):
    r = requests.get(url).text
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
    sql = "INSERT IGNORE INTO daryouz_mahalliy (title, text, date, url, category) VALUES (%s, %s, %s, %s, %s)"
    val = (title, text, date, url, category)
    cursor.execute(sql, val)
    # mydb.commit()

def get_urls(url):
    '''Returns urls from daryo.uz/uz.'''
    page = requests.get(url).text
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

for i in range(21, 9044):
    print("Page:" + str(i))
    get_urls("https://m.daryo.uz/category/mahalliy/page/" + str(i) + "/")
    mydb.commit()