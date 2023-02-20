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

def generate_text():
    """生成文本的生成器函数"""
    # for i in range(10):
    #     yield f"这是第{i}行文本\n"
    msg = "你是谁"
    prev_text = ""
    for data in chatbot.ask(
        msg,
    ):
        # response = data["message"]
        message = data["message"][len(prev_text) :]
        print(message, end="", flush=True)
        print("\n")
        yield message
        

@app.route('/')
def stream_text():
    """流式传输文本的视图函数"""
    return Response(generate_text(), mimetype='text/plain', content_type='text/event-stream')


# 在这个例子中，`generate_text` 函数是一个生成器函数，它会生成一些文本行。`stream_text` 函数是一个 Flask 视图函数，它返回一个流式响应，该响应将调用 `generate_text` 生成的文本行逐行发送给客户端。
