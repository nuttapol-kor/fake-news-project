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
    event_type = event["type"]
    if not event_type:
        print("Error: event type not found")
        return ""
    
    try:
        user_id = event["source"]["userId"]
        reply_token = event["replyToken"]
    except KeyError as e:
        print(f"Error: cannot get {e}")
        return ""

    if event_type == "postback":
        handle_postback(event)
    elif event_type == "message":
        handle_message(event, reply_token)
    else:
         print(f"Error: unsupported event type '{event_type}'")
    return ""

def handle_postback(event):
    action = event["postback"]["data"]
    if action.startswith("action=summarize"):
        text = action.split('=')[2]
        summary = f"summarized text: {text}"
        reply_obj = TextSendMessage(text=summary)
        line_bot_api.reply_message(event["replyToken"], reply_obj)

def handle_message(event, reply_token):
    message_type = event["message"]["type"]
    if not message_type:
        print("Error: message type not found")
        return

    if message_type == "text":
        handle_text_message(event, reply_token)
    else:
        handle_non_text_message(reply_token)

def handle_text_message(event, reply_token):
    message = str(event['message']['text'])
    predicted_res = logistic_regression_best(message)
    if predicted_res['class'] == 0:
        template_pic = check_mark_pic
        result_string = "ข่าวจริง"
    else:
        template_pic = cross_mark_pic
        result_string = "ข่าวปลอม"
    reply_obj = create_template_message(template_pic, result_string, predicted_res['confident'], message)
    line_bot_api.reply_message(reply_token, reply_obj)

def handle_non_text_message(reply_token):
    sticker_id = np.random.randint(1, 17)
    reply_obj = StickerSendMessage(package_id=str(1), sticker_id=str(sticker_id))
    line_bot_api.reply_message(reply_token, reply_obj)

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
