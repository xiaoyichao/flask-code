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
from flask import Response
from revChatGPT.V1 import Chatbot


chatbot = Chatbot(config={
    "email": "lahuseman88@outlook.com",
    "password": "of75stFg8j"
    })

prompt = "你是谁"

prev_text = ""
for data in chatbot.ask(
    prompt,
):
    message = data["message"][len(prev_text) :]
    print(message, end="", flush=True)
    prev_text = data["message"]
    print(prev_text)
print()



def streaming_file(params):
    """
    流式发送文件
    @return:
    """
    UPDATE_PACKAGE_PATH = '/tools/package/'
    out = os.path.join(UPDATE_PACKAGE_PATH, params.get("filename"))
    if not os.path.isfile(out):
        return None
    # 文件大小
    fsize = os.path.getsize(out)

    def send_file_fp():
        store_path = out
        send_size = 0
        with open(store_path, "rb") as target_file:
            while 1:
                data = target_file.read(2 * 1024 * 1024)  # 每次读取2M
                if not data:
                    break
                yield data

    response = Response(send_file_fp(), content_type='multipart/form-data; boundary=something')
    response.headers["Content-disposition"] = 'attachment; filename={}'.format(params.get("filename"))
    response.headers["Content-length"] = fsize
    return response
