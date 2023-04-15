import os
import numpy as np
from fastapi import FastAPI, Request
from linebot import LineBotApi
from linebot.models import StickerSendMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction
from dotenv import load_dotenv
from repo.text_classification import logistic_regression_best
from repo.text_summarize import summarize
import uvicorn
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
handler = Mangum(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
check_mark_pic = "https://i.imgur.com/HlVO2kS.png"
cross_mark_pic = "https://i.imgur.com/BrXDQQC.png"

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
        summary = text
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
    if len(message) > 150:
        summarize_msg = summarize(message)
    else:
        summarize_msg = message
    reply_obj = create_template_message(template_pic, result_string, predicted_res['confident'], summarize_msg)
    line_bot_api.reply_message(reply_token, reply_obj)

def handle_non_text_message(reply_token):
    # sticker_id = np.random.randint(1, 17)
    # reply_obj = StickerSendMessage(package_id=str(1), sticker_id=str(sticker_id))
    reply_obj = TextSendMessage(text='ลองส่งข่าวที่เป็นตัวอักษรมาเเล้วทางเรา จะตรวจสอบให้นะครับ')
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

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
