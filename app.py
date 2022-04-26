from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from dotenv import load_dotenv
import re
import emoji
import os
import json

app = Flask(__name__)

load_dotenv()

line_bot_api = LineBotApi(os.getenv("Access_Token"))
handler = WebhookHandler(os.getenv("Channel_Secret"))

# Get Callback Requests
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


#message handling
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #Open messages written in Reply_Messages.json
    with open('Reply_Message.json', 'r') as f: 
        message_dict = json.load(fp = f)
    message = text = event.message.text
    default = True

    #Reply text Messages
    for index in range(1,len(message_dict)):
        current_message = message_dict[f'message{index}']
        if(current_message['text']==message):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(currentMessage['replyMessage']))
            default = False

    #Reply carousel Messages
    if re.match('about me', message):
        #Building Carousel
        carousel_message = TemplateSendMessage(
            alt_text='關於我',
            template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.iconscout.com/icon/free/png-256/about-me-461762.png',
                        title='關於我',
                        text='我的基本訊息',
                        actions=[
                            MessageAction(
                                label='我是誰',
                                text='你是誰'
                            ),
                            MessageAction(
                                label='我的契機',
                                text='你的契機'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://icon-library.com/images/document-icon-images/document-icon-images-2.jpg",
                        title='我的project',
                        text='text',
                        actions=[
                            URIAction(
                                label='網址',
                                uri='https://nbabid.herokuapp.com'
                            ),
                            URIAction(
                                label='GitHub',
                                uri='https://github.com/b09901185/nbabid'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_message)
    if(default):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message_dict['defaultMessage']))
    f.close()

#Main Function
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)