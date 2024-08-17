# ENV Parameter
import os
from linebot_fn import reply,read_metedata
import ujson

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    CarouselTemplate,
    TemplateMessage,
    CarouselColumn, 
    URIAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

configuration = Configuration(access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


##讀入爬蟲內容
topic_index,topic_url=read_metedata('./udn_metadata/topic_index.json','utf-8'),read_metedata('./udn_metadata/topic_mapping_url.json','utf-8')
topic_index_check = list(topic_index.values())
topic_index_check = list(topic_index.values())


@handler.add(MessageEvent)
def handle_message(event):

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        


        # 處理文字消息
        if isinstance(event.message, TextMessageContent):
            if event.message.text in topic_index_check:
                with open(f'./udn_article/{topic_index_check.index(event.message.text)}.json','r',encoding='utf-8') as f:
                    news=ujson.load(f)

                    #輪播模板
                    carousel_template = CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url=news[event.message.text][0]['img_url'],
                                title=news[event.message.text][0]['title'][:40],  ## Title  must not be longer than 40 characters
                                text=f'發佈時間: {news[event.message.text][0]["time"]}',
                                actions=[
                                    URIAction(
                                        label='網頁連結',
                                        uri=news[event.message.text][0]['link']
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url=news[event.message.text][1]['img_url'],
                                title=news[event.message.text][1]['title'][:40],
                                text=f'發佈時間: {news[event.message.text][1]["time"]}',
                                actions=[
                                    URIAction(
                                        label='網頁連結',
                                        uri=news[event.message.text][1]['link']
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url=news[event.message.text][2]['img_url'],
                                title=news[event.message.text][2]['title'][:40],
                                text=f'發佈時間: {news[event.message.text][2]["time"]}',
                                actions=[
                                    URIAction(
                                        label='網頁連結',
                                        uri=news[event.message.text][2]['link']
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url=news[event.message.text][3]['img_url'],
                                title=news[event.message.text][3]['title'][:40],
                                text=f'發佈時間: {news[event.message.text][3]["time"]}',
                                actions=[
                                    URIAction(
                                        label='網頁連結',
                                        uri=news[event.message.text][3]['link']
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url=news[event.message.text][4]['img_url'],
                                title=news[event.message.text][4]['title'][:40],
                                   text=f'發佈時間: {news[event.message.text][4]["time"]}',
                                actions=[
                                    URIAction(
                                        label='網頁連結',
                                        uri=news[event.message.text][4]['link']
                                    )
                                ]
                            ),
                        ]
                    )



                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[
                            TemplateMessage(
                            alt_text='Carousel template',
                            template=carousel_template
                            )
                             ]
                        )
                    )


            elif event.message.text in ['新聞','news','主題','topic']:
                with open(f'./udn_metadata/topic_index.json','r',encoding='utf-8') as f:
                    news=ujson.load(f)
                    news_list=list(news.values())
                    news_topic='輸入以下主題文字查看新聞\n'+('\n。'.join(news_list))
                
                    line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=news_topic)]
                    )
                )

            else:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text='請輸入與新聞相關的內容或查詢主題')]
                    )
                )
        
        # 處理圖片消息
        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="本官方帳號只接收文字訊息喔!!")]
                )
            )

            

def lambda_handler(event, context):
    try: 
        body = event['body']
        signature = event['headers']['x-line-signature']
        handler.handle(body, signature)
        return {
            'statusCode': 200,
            'body': ujson.dumps('Hello from Lambda!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': ujson.dumps(str(e))
        }