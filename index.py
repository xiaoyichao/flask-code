'''
Author: xiaoyichao xiao_yi_chao@163.com
Date: 2023-02-20 20:59:52
LastEditors: xiaoyichao xiao_yi_chao@163.com
LastEditTime: 2023-02-20 21:06:11
FilePath: /flask-code/http_test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os 
import sys
import time
from flask import Response, Flask
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
print("111",end_time-begin_time)

print("开始请求bot")
begin_time = time.time()
# prompt = "你是谁"

# prev_text = ""
# for data in chatbot.ask(
#     prompt,
# ):
#     # response = data["message"]
#     message = data["message"][len(prev_text) :]
#     # print(message, end="", flush=True)
#     prev_text = data["message"]
#     # print(prev_text)
# # print()
# end_time = time.time()
# print("222", end_time-begin_time)

@app.route("/message", methods=["POST"])
def streaming_file():
    """
    流式发送文件
    @return:
    """
    msg = request.json.get('msg')
    prev_text = ""
    for data in chatbot.ask(
        msg,
    ):
        # response = data["message"]
        message = data["message"][len(prev_text) :]
        # print(message, end="", flush=True)
        prev_text = data["message"]
        # print(prev_text)

        data = message
        if not data:
            break
        yield data

    response = Response(send_file_fp(), content_type='multipart/form-data; boundary=something')
    # response.headers["Content-disposition"] = 'attachment; filename={}'.format(params.get("filename"))
    # response.headers["Content-length"] = fsize
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)