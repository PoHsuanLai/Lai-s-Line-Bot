#載入LineBot所需要的套件
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

app = Flask(__name__)

load_dotenv()

line_bot_api = LineBotApi(os.getenv("Access_Token"))
handler = WebhookHandler(os.getenv("Channel_Secret"))

# 監聽所有來自 /callback 的 Post Request
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
    message = text = event.message.text
    if re.match('about me', message):
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
    elif re.match('你是誰', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('我叫賴柏瑄，目前就讀於台大電機系二年級'))
    elif re.match('你的契機', message): 
        line_bot_api.reply_message(event.reply_token, TextSendMessage('由於我之前碰巧認識了一位也在Line實習的台大學長，又剛好我同時在修網路服務程式的課，也對此深感興趣，因此那時以來便也想到Line實習，藉此更深入瞭解大的科技公司內部是如何完善自己的系統的'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(emoji.emojize('感謝您的訊息！\n\n想知道詳細資訊請輸入\n“about me”\n:smirk::smirk::smirk::smirk::smirk:', language='alias')))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)