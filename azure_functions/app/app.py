import os, logging
from azure.cosmos import CosmosClient
import azure.functions as func

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, QuickReplyButton, MessageAction, QuickReply, PostbackEvent)

# get values from Application Setting of Azure Functions
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING', None)
database_name = os.getenv('COSMOS_DB_DATABASE_STRING', None)
container_name = os.getenv('COSMOS_DB_CONTAINER_STRING', None)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    signature = req.headers['x-line-signature']
    body = req.get_body().decode("utf-8")
    logging.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        func.HttpResponse(status_code=400)
    return func.HttpResponse('OK')


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    recv_text = event.message.text
    if '鍵' in recv_text or 'かぎ' in recv_text or 'カギ' in recv_text:
        cosmos_client = CosmosClient.from_connection_string(connection_string)
        database = cosmos_client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        query = 'SELECT c.Body.object, c.Body.text FROM c'
        status = list(container.query_items(query, enable_cross_partition_query=True))
        items = []
        for s in status:
            if s.get('object') != None and s.get('text') != None:
                items.append({
                    'type': 'action', 
                    'action': {
                        'type': 'postback',
                        'data': s['object'] + ',' + s['text'],
                        'label': s['object'],
                        'displayText': s['object'] + 'の状態を教えてください'
                    }
                })
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='どの鍵の状態を調べますか', quick_reply=QuickReply(items=items)))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='入力が正しくないです\n例：鍵の状態を調べてください'))

@handler.add(PostbackEvent)
def on_postback(event):
    postback_data = event.postback.data.split(',')
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=(postback_data[0] + 'の状態は\n' + postback_data[1] + '\nです')))
    