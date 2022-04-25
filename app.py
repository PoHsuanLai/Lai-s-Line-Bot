#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
import emoji

app = Flask(__name__)

line_bot_api = LineBotApi('mCPd6yE2BF6p74QHjVd+SDl4tuYnGSBh/iFwQ6NmwSSAJR+NbYNAaLcdeFflEtOqCGOUM6P8aSb1PqTRQE6n2rgytwkc67Ji+KlUE/CswfJ2bO+XWjZcKk84dAfLWolS85oy0OTIV7i7ahMBVm5aTQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('87c5f4d4188a6f2372fcf27786692f93')

line_bot_api.push_message('U7044af8ff4f5da1b940b535199766117',TextSendMessage(text='why?'))

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
            alt_text='Carousel實作',
            template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.projectmailartbooks.com/About_me_2.png',
                        title='關於我',
                        text='我的基本訊息',
                        actions=[
                            MessageAction(
                                label='我是誰？',
                                text='好'
                            ),
                            MessageAction(
                                label='我長怎樣？',
                                text='不好'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="data:image/png;base64,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",
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
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('感謝您的訊息！\n\n想知道詳細訊息請輸入“about me”'))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)