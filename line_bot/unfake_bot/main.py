import os
import numpy as np
from fastapi import FastAPI, Request
from linebot import LineBotApi
from linebot.models import StickerSendMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction
from dotenv import load_dotenv
from repo.text_classification import logistic_regression_best

app = FastAPI()

load_dotenv()
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
check_mark_pic = "https://cdn.pixabay.com/photo/2016/03/31/14/37/check-mark-1292787_1280.png"
cross_mark_pic = "https://em-content.zobj.net/source/skype/289/cross-mark_274c.png"

@app.get("/")
def root():
    return {"message": "This is a root path of our models API"}

@app.post("/webhook")
async def callback(request: Request):
    data = await request.json()
    for i in range(len(data["events"])):
        event = data["events"][i]
        event_handle(event)

def event_handle(event):
    print(event)
    print(event["type"])
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
    # try:
    #     msgType = event["type"]
    # except:
    #     print('error cannot get msgID, and msgType')
    #     sk_id = np.random.randint(1,17)
    #     replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
    #     line_bot_api.reply_message(rtoken, replyObj)
    #     return ''
    if event["type"] == "postback":
        action = event['postback']['data']
        if action.startswith('action=summarize'):
            text = action.split('=')[2]
            summary = f"summarized text: {text}"
            replyObj = TextSendMessage(text=summary)
    elif event["type"] == "message":
        if event["message"]["type"] == "text":
            msg = str(event["message"]["text"])
            predicted_res = logistic_regression_best(msg)
            if predicted_res['class'] == 0:
                template_pic = check_mark_pic
                result_string = "ข่าวจริง"
            else:
                template_pic = cross_mark_pic
                result_string = "ข่าวปลอม"
            replyObj = create_template_message(template_pic, result_string, predicted_res['confident'], msg)
            print(event)
        else:
            sk_id = np.random.randint(1,17)
            replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
    line_bot_api.reply_message(rtoken, replyObj)
    return ''

def create_template_message(picture, result_string, predicted_res, original_text):

    buttons_template_message = TemplateSendMessage(
        alt_text='Summarize news',
        template=ButtonsTemplate(
            thumbnail_image_url= picture,
            title=result_string,
            text=f"ผลการตรวจสอบ มีโอกาสเป็น{result_string} {predicted_res:.2f}%",
            actions=[
                PostbackAction(
                    label='สรุปข่าว',
                    display_text='สรุปข่าว',
                    data=f'action=summarize&text={original_text}'
                )
            ]
        )
    )

    return buttons_template_message
