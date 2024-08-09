import requests
from bs4 import BeautifulSoup
import ujson




r = requests.get('https://udn.com/news/cate/2/6645')
soup = BeautifulSoup(r.text,'html.parser')
news=soup.findAll(class_='story-list__news')

#查詢縮圖
for item in news[:5]:
    picture = item.find('picture')
    if picture:
        img_tag = picture.find('img')
        if img_tag and img_tag.has_attr('data-src'):
            img_url = img_tag['data-src']
            print(img_url)