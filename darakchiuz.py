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


def get_text(url, cat):
    print(url)

    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    # category = soup.find(class_='itemCat').text
    title = soup.find(class_="pg-article").find('h1', {"class": "mb-4"}).text
    date = soup.find('span', {"class": "text-muted"}).text.strip()
    # text = soup.find(class_='pg-article__text mb-5').text
    text = ""
    for p in soup.find(class_='pg-article__text mb-5').find_all('p'):
        text += p.text + "\n"

    # write to db
    sql = "INSERT INTO darakchiuz (title, text, date, url, category) VALUES (%s, %s, %s, %s, %s)"
    val = (title, text, date, url, cat)
    cursor.execute(sql, val)
    sleep(6)

def get_urls(url, cat):
    print("Cat url: " +url)
    sleep(6)
    page = requests.get(url, timeout=5, headers=headers).text
    soup = BeautifulSoup(page, "lxml")

    try:
        for c in soup.find_all(class_="card-title"):
            url1 = c.find('a', href=True)['href']
            # print(url1)
            try:
                get_text(url1, cat)
            except:
                print("Error in get text")
        mydb.commit()

    except Exception:
        print("Error in get URL")
    '''
    count = 0
    for a in soup.find_all('a', href=True):
        count += 1

        if count > 55:
            break
        if count == 20 or count == 22 or count == 24 or count == 26 or count == 28 or count == 30 or count == 32 or count == 34 or count == 36 or count == 38 or count == 40 or count == 42 or count == 44 or count == 46 or count == 48 or count == 50 or count == 52 or count == 54:
            url1 = a['href']
            try:
                get_text(url1)
            except Exception:
                print("Error processing URL")
    '''

cats = ["Siyosat", "Jamiyat", "Dunyo", "Madaniyat", "Sport", "Jinoyat", "Hi-tech", "Salomatlik", "Mutolaa", "Iqtisodiyot", "Moziydan sado"]
catsid = [65, 44, 45, 57, 46, 50, 49, 48, 53, 64, 55]
catscnt = [205, 2764, 970, 92, 445, 234, 48, 113, 34, 100, 5]
              # 280
ind = 1
for i in range(428, 2162):
    print("Page:" + cats[ind] + ": " + str(i))
    get_urls("https://darakchi.uz/oz/categories/"+str(catsid[ind])+"?page=" + str(i), cats[ind])