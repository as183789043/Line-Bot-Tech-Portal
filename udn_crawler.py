import requests
from bs4 import BeautifulSoup
import ujson
##取得udn的各新聞主題
def udn_crawler(url,encoding):
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


topic_list,href_list=udn_crawler('https://udn.com/news/index','utf-8')



#生成 topic與index對照表，topic與url對照表
topic_mapping_url={}
topic_key_list=[]
for index in range(len(topic_list)):
    if 'news'  in href_list[index]:
        topic_mapping_url[topic_list[index]] = href_list[index]
        topic_key_list.append(topic_list[index])


with open('udn_metadata/topic_mapping_url.json','w',encoding='utf-8') as file:
    file.write(ujson.dumps(topic_mapping_url,ensure_ascii=False,escape_forward_slashes=False,indent=4))

with open('udn_metadata/topic_index.json','w',encoding='utf-8') as file:
    topic_keys = {index: topic_key_list[index] for index in range(len(topic_key_list))}
    file.write(ujson.dumps(topic_keys,ensure_ascii=False,indent=4))
    