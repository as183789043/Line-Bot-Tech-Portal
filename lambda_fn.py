import ujson

def read_metedata(filename, encoding):
    """讀取 metadata JSON 檔案"""
    with open(filename, 'r', encoding=encoding) as file:
        data = ujson.load(file)
    return data

def reply(body, topic_index_check):
    """
    處理使用者輸入並回覆
    """
    if body in topic_index_check:
        # ✅ 移除 function_file 路徑
        article_index = topic_index_check.index(body)
        with open(f'./udn_article/{article_index}.json', 'r', encoding='utf-8') as f:
            news = ujson.load(f)
        return str(news)

    elif body in ['新聞', 'news', '主題', 'topic', '新聞主題']:
        # ✅ 移除 function_file 路徑
        with open('./udn_metadata/topic_index.json', 'r', encoding='utf-8') as f:
            news = ujson.load(f)
            news_list = list(news.values())
            news_topic = '輸入以下主題文字查看新聞\n' + ('\n。'.join(news_list))
        return news_topic

    else:
        return '請輸入與新聞相關的內容或查詢主題'
