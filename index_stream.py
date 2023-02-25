'''
Author: xiaoyichao xiao_yi_chao@163.com
Date: 2023-02-24 19:01:10
LastEditors: xiaoyichao xiao_yi_chao@163.com
LastEditTime: 2023-02-25 19:32:03
FilePath: /flask-code/index_stream.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from flask import Flask, Response, request
import time 
from revChatGPT.V1 import Chatbot

app = Flask(__name__)

def generate_text():
    """生成文本的生成器函数"""
    for i in range(10):
        time.sleep(1)
        # yield str(i)
        yield str(i) + "\n"
        print(i)

@app.route('/stream', methods=['GET','POST'])
def stream():
    """流式传输文本的视图函数"""
    return Response(generate_text(), mimetype='text/plain', content_type='text/event-stream')


def generate_text_test(msg,chatbot):
    """生成文本的生成器函数"""

    prev_text = ""
    for data in chatbot.ask(msg):
        message = data["message"][len(prev_text):]
        yield (message + "\n")
        prev_text = data["message"] 
        print("message",  message)
    print(time.time(),"结束请求")

@app.route('/message', methods=['GET', 'POST'])
def message():
    """流式传输文本的视图函数"""
    # if request.method == 'POST':
        # msg = request.form['msg'] 两个都可以
        # msg = request.json.get('msg')
        # maxtoken = request.json.get('maxtoken') - 300
        # openid = request.json.get('openid')
    msg = "生成一个50字的论文"
    print(time.time(),"开始请求")
    begin_time = time.time()
    print("开始创建bot")
    chatbot = Chatbot(config={
        "email": '651519987@qq.com',
        "password": "aijiao13141"
        })
    print("创建bot成功")
    end_time = time.time()
    return Response(generate_text_test(msg, chatbot), mimetype='text/plain', content_type='text/event-stream')
    # else:
    #     return
    
if __name__ == '__main__':
    app.run(debug=False)
