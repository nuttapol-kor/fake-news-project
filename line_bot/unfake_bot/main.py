import os
import numpy as np
from fastapi import FastAPI, Request
from linebot import LineBotApi
from linebot.models import StickerSendMessage, TextSendMessage
from dotenv import load_dotenv
from repo.text_classification import logistic_regression_best

app = FastAPI()

load_dotenv()
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))

@app.get("/")
def root():
    return {"message": "This is a root path of our models API"}

@app.post("/webhook")
async def callback(request: Request):
    data = await request.json()
    print(data)
    for i in range(len(data['events'])):
        event = data['events'][i]
        event_handle(event)

def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''
    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
        return ''
    if msgType == "text":
        msg = str(event["message"]["text"])
        predicted_res = logistic_regression_best(msg)
        if predicted_res['class'] == 0:
            response_msg = f"ผลการตรวจสอบ มีลักษณะคล้ายข่าวจริง {predicted_res['confident']:.2f}%"
        else:
            response_msg = f"ผลการตรวจสอบ มีโอกาสเป็นข่าวปลอม {predicted_res['confident']:.2f}%"
        replyObj = TextSendMessage(text=response_msg)
        line_bot_api.reply_message(rtoken, replyObj)
    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''
