import os 
import sys
import time
from flask import Response,request, Flask
from revChatGPT.V1 import Chatbot
# from revChatGPT.V2 import Chatbot

app = Flask(__name__)


begin_time = time.time()
print("开始创建bot")
chatbot = Chatbot(config={
    "email": "lahuseman88@outlook.com",
    "password": "of75stFg8j"
    })
print("创建bot成功")
end_time = time.time()


app = Flask(__name__)

def generate_text(request):
    """生成文本的生成器函数"""
    # msg = request.form.get('msg')
    msg = request.args.get("msg")

    # msg = "你是谁"
    prev_text = ""
    for data in chatbot.ask(
        msg,
    ):
        # response = data["message"]
        message = data["message"][len(prev_text) :]
        # print(message, end="", flush=True)
        yield message
        prev_text = data["message"]
        # print("\n")
        
        
@app.route('/',methods=['POST'])
def stream_text():
    """流式传输文本的视图函数"""
    return Response(generate_text(request), mimetype='text/plain', content_type='text/event-stream')



# from flask import Flask, Response, request
# app = Flask(__name__)

# def generate_text(request):
#     msg = request.form.get('msg')
#     prev_text = ""
#     with app.app_context():
#         for data in chatbot.ask(msg):
#             message = data["message"][len(prev_text):]
#             yield message
#             prev_text = data["message"]

# @app.route('/', methods=['POST'])
# def stream_text():
#     return Response(generate_text(request), mimetype='text/plain', content_type='text/event-stream')
