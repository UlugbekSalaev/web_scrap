import sys
import os
import requests
import textwrap
from bs4 import BeautifulSoup
import lxml

class GrabberArticle:
    url = ""
    filename = ""
    path = ""
    content_tags = ['post-body']
    wrap = 80

    def __init__(self, url_address):
        self.url = url_address
        path_arr = self.url.split('/')
        if path_arr[-1] != '':
            self.filename = path_arr[-1] + ".txt"
            self.path = os.getcwd() + "/".join(path_arr[1:-1])
        else:
            self.filename = path_arr[-2] + ".txt"
            self.path = os.getcwd() + "/".join(path_arr[1:-2])
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def write_in_file(self, text):
        file = open(str(self.path) + '/' + str(self.filename), mode="w")
        file.write(text)
        file.close()

    def get_text(self):
        r = requests.get(self.url).text
        soup = BeautifulSoup(r, 'html.parser')
        content = soup.find_all(class_='post-body')
        # Getting the entire tag content, described in self.content_tags.
        wrapped_text = ""
        for p in content:
            # Skipping empty tags.
            if p.text != '':
                links = p.find_all('a')
                if links != '':
                    for link in links:
                        p.a.replace_with(link['href'])

                wrapped_text += ''.join(textwrap.fill(p.text, self.wrap)) + "\n\n"
        self.write_in_file(wrapped_text)


# Scrapes all url from m.kun.uz/uz and write to database it
def get_urls(url):
    '''Returns urls from kun.uz/uz.'''
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    if "Sahifa topilmadi" in page:
        print(url+" : not found")
        return
    for p in soup.find_all(class_="post-body"):
        url1 = p.find('a')['href']
        caturl= p.find(class_="data").find('a')['href']
        category=p.find(class_="data").find('a').text.strip()
        url1 = "https://m.kun.uz/"+url1
        caturl = "https://m.kun.uz/"+caturl
        try:
            mr = GrabberArticle(url1)
            mr.get_text()
            print("Successfully processed")
        except Exception:
            print("Error processing URL")

        #id	url	caturl	category
        #sql = "INSERT INTO kunuz_url VALUES (%s, %s, %s, %s)"
        #val = ("NULL", url1, caturl, category)
        #mycursor.execute(sql, val)
        #print(url1+" : "+str(mycursor.rowcount))
        #mydb.commit()

res1=0
for i in range(1, 5):
    print("Page:"+str(i))
    get_urls("https://m.kun.uz/uz?q=%2Fuz&page="+str(i))
    res1 += 1
print("Finish: "+str(res1))