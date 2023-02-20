import os 
import sys
import time
from flask import Response,request, Flask
from revChatGPT.V1 import Chatbot

app = Flask(__name__)


begin_time = time.time()
print("开始创建bot")
chatbot = Chatbot(config={
    "email": "wolhtetjuywvb@eurokool.com",
    "password": "abc123456789"
    })
print("创建bot成功")
end_time = time.time()



from flask import Flask, Response, request

app = Flask(__name__)

def generate_text(msg):
    """生成文本的生成器函数"""
    prev_text = ""
    for data in chatbot.ask(msg):
        message = data["message"][len(prev_text):]
        yield message
        prev_text = data["message"]

@app.route('/message', methods=['GET', 'POST'])
def stream_text():
    """流式传输文本的视图函数"""
    if request.method == 'POST':
        # msg = request.form['msg']
        msg = request.json.get('msg')
        return Response(generate_text(msg), mimetype='text/plain', content_type='text/event-stream')
    else:
        return """
        <form action="/" method="POST">
          <input type="text" name="message">
          <button type="submit">发送</button>
        </form>
        """
