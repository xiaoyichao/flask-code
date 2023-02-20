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


# app = Flask(__name__)

# def generate_text():
#     """生成文本的生成器函数"""


#     msg = "你是谁"
#     prev_text = ""
#     for data in chatbot.ask(
#         msg,
#     ):
#         # response = data["message"]
#         message = data["message"][len(prev_text) :]
#         # print(message, end="", flush=True)
#         yield message
#         prev_text = data["message"]
#         # print("\n")
        
        
# @app.route('/',methods=['POST'])
# def stream_text():
#     """流式传输文本的视图函数"""
#     return Response(generate_text(request), mimetype='text/plain', content_type='text/event-stream')

# 怎么实现传入msg这个函数



# 在 `generate_text()` 函数中，`msg` 是一个字符串变量，用于初始化 chatbot，并传递给 `ask()` 方法进行对话。如果要让用户在网页上输入文本，然后将其作为 `msg` 传递给 `generate_text()` 函数，可以使用 Flask 的表单功能。

# 可以在 HTML 文件中创建一个表单，允许用户输入消息，并将其发送到 Flask 应用程序的路由。然后在路由中获取消息，将其作为参数传递给 `generate_text()` 函数。

# 例如，可以在 HTML 文件中创建以下表单：

# ```html
# <form action="/" method="POST">
#   <input type="text" name="message">
#   <button type="submit">发送</button>
# </form>
# ```

# 在 Flask 应用程序的路由中，可以使用 `request.form` 获取表单数据，然后将其传递给 `generate_text()` 函数：

# ```python
from flask import Flask, Response, request

app = Flask(__name__)

def generate_text(msg):
    """生成文本的生成器函数"""
    prev_text = ""
    for data in chatbot.ask(msg):
        message = data["message"][len(prev_text):]
        yield message
        prev_text = data["message"]

@app.route('/', methods=['GET', 'POST'])
def stream_text():
    """流式传输文本的视图函数"""
    if request.method == 'POST':
        msg = request.form['message']
        return Response(generate_text(msg), mimetype='text/plain', content_type='text/event-stream')
    else:
        return """
        <form action="/" method="POST">
          <input type="text" name="message">
          <button type="submit">发送</button>
        </form>
        """
```

在这个示例中，`stream_text()` 函数检查请求的方法是否为 `POST`，如果是，则从表单中获取消息并将其传递给 `generate_text()` 函数。如果请求的方法为 `GET`，则返回一个带有表单的 HTML 页面。注意，在 `generate_text()` 函数中，将 `msg` 参数传递给 `chatbot.ask()` 方法，以便使用用户输入的消息进行对话。

