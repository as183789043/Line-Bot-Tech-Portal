import ujson

# user_input = str(input('請輸入內容:'))

def read_metedata(filename,encoding):
    with open(filename,'r',encoding=encoding) as file:
        data = ujson.load(file)
    return data

#lambda多一層目錄
def reply(body):
    if body in topic_index_check:
        with open(f'./function_file/function_file/udn_article/{topic_index_check.index(body)}.json','r',encoding='utf-8') as f:
            news=ujson.load(f)

        return str(news)

    elif body in ['新聞','news','主題','topic','新聞主題']:
        with open(f'./function_file/udn_metadata/topic_index.json','r',encoding='utf-8') as f:
            news=ujson.load(f)
            news_list=list(news.values())
            news_topic='輸入以下主題文字查看新聞\n'+('\n。'.join(news_list))
            
        return news_topic

    else:
        return('請輸入與新聞相關的內容或查詢主題')



if __name__=="__main__":
    #Read json file
    topic_index,topic_url=read_metedata('./function_file/udn_metadata/topic_index.json','utf-8'),read_metedata('./function_file/udn_metadata/topic_mapping_url.json','utf-8')
    topic_index_check = list(topic_index.values())
    print(reply(user_input))