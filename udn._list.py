import requests
from bs4 import BeautifulSoup

##取得udn的各新聞主題
def udn_topic(url,encoding):
    topic_list=[]
    href_list=[]
    r = requests.get(url)
    r.encoding = encoding 
    if r.status_code == 200:
        soup = BeautifulSoup(r.text,'html.parser')
        topics = soup.findAll(class_='navigation-list')
        for topic in topics:
            href_list.append(topic.get('href') if topic.get('href').startswith("https") else f"https://udn.com{topic.get('href')}" )
            topic_list.append(topic.text)
        href_list,topic_list=href_list[1:-1],topic_list[1:-1]
        if len(href_list) == len(topic_list):
            return topic_list,href_list
        return 'error'
    else:
        return('爬取失敗')


print(udn_topic('https://udn.com/news/index','utf-8'))