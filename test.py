


import requests


def infocheck():
    acctoken = "65_MGbBp7chHUSs9ICKgpx1TexNjiTjWn2qiOB468c1kemmnPwagfmU-rtSkFRfMp5jB54wl9B-33rfsFVuodqAmGID3xKkg7sOoBzaTX8sPZzOyb_HPtNmrtDGhjIDZFaAAAPLR"
    text = '2023-02-21 12:52:13 c6d5828d-8040-4e92-86af-ad45f507f6cf [ERROR] Exception on /test [POST] \n \
            Traceback (most recent call last):\
            File "/code/flask/app.py", line 2525, in wsgi_app\
                response = self.full_dispatch_request()\
            File "/code/flask/app.py", line 1823, in full_dispatch_request\
                return self.finalize_request(rv)\
            File "/code/flask/app.py", line 1842, in finalize_request\
                response = self.make_response(rv)\
            File "/code/flask/app.py", line 2170, in make_response\
                raise TypeError(\
            TypeError: The view function did not return a valid response. The return type must be a string, dict, list, tuple with headers or status, Response instance, or WSGI callable, but it was a int.FC Invoke End RequestId: c6d5828d-8040-4e92-86af-ad45f507f6cf\
            这个报错什么意思？'
    text ="tai wan"
    text = text.replace("\n", "")
    text = text.replace("\"", "")
    openid = "ophka5ORWZC6asTu2Frb5wI8VjO8"
    print("acctoken", acctoken)
    checkurl = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token={ACCESS_TOKEN}".format(
        ACCESS_TOKEN=acctoken)

    data = '{"content": "' + text + '","openid": "' + openid + '","scene":  2 ,"version":  2 }'
    headers = {'Content-Type': 'application/json'}
    print("data",data)
    res = requests.post(checkurl, data=data.encode('utf-8'), headers=headers)
    lev = res.json().get("result").get("label")
    suggest = res.json().get("result").get("suggest")
    print("res.json()", res.json())
    print("lev", lev)
    print("suggest", suggest)
    if suggest == "review" or suggest == "pass":
        return True
    else:
        return False


res = infocheck()
print(res)


