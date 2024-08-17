import requests
from bs4 import BeautifulSoup
import ujson
from .app_fn import read_metedata,reply


#Read json file
topic_index=read_metedata('./udn_metadata/topic_index.json','utf-8')
topic_url=read_metedata('./udn_metadata/topic_mapping_url.json','utf-8')


for topic,url in topic_url.items():
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    news=soup.findAll(class_='story-list__news')

    news_data,artile_list = {},[]

    news_data[topic]=artile_list

    #查詢新聞資料(圖片、標題、連結)
    for item in news[:5]:
        #文章圖片連結標籤檢測
        picture,title,link,time = item.find('picture'),item.find('a'),item.find('a'),item.find('time')
        print('次數')
        #爬取資訊
        topic_url = picture.find('img')['src']  if picture  else '圖片搜尋失敗'
        topic_title = title.get('title') if title.get('title') else title.get('aria-label') if title.get('aria-label') else '主題抓取失敗'
        topic_href = link.get('href')  if link.get('href').startswith('https:') else f'https://udn.com/{link.get("href")}'  if link  else '連結搜尋失敗'
        topic_time = time.text if time else '未註明發布時間'
        #資料結構組成 ex {title:[{a:1,b:2,c:3},{a:1,b:2,c:3}]}
        # 将爬取的信息保存到news_data字典中

        artile_list.append({
            'img_url': topic_url,
            'title': topic_title,
            'link': topic_href,
            "time": topic_time
        })


    if topic in topic_index.values():
        file_index=list(topic_index.values()).index(topic)
        with open(f"./udn_article/{file_index}.json",'w',encoding='utf-8') as f:
            f.write(ujson.dumps(news_data,ensure_ascii=False,escape_forward_slashes=False,indent=4))
    else:
        print('主題不存在')
        
