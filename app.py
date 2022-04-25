#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('mCPd6yE2BF6p74QHjVd+SDl4tuYnGSBh/iFwQ6NmwSSAJR+NbYNAaLcdeFflEtOqCGOUM6P8aSb1PqTRQE6n2rgytwkc67Ji+KlUE/CswfJ2bO+XWjZcKk84dAfLWolS85oy0OTIV7i7ahMBVm5aTQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('87c5f4d4188a6f2372fcf27786692f93')

line_bot_api.push_message('U7044af8ff4f5da1b940b535199766117',TextSendMessage(text='push message'))

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

 
#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    if re.match('about me', message):
        carousel_message = TemplateSendMessage(
            alt_text='Carousel實作',
            template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.projectmailartbooks.com/About_me_2.png',
                        title='我的基本訊息',
                        text='text',
                        actions=[
                            MessageAction(
                                label='我',
                                text='好'
                            ),
                            MessageAction(
                                label='你',
                                text='不好'
                            )
                        ]
                    )
                ]
            )
        )

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)