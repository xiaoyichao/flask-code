


import requests


def infocheck():
    acctoken = "65_oc9PdAWTFdKSwsOahteY7roNJxBabaHMfMXnH1vkBVaC9q_UUqERH7BBEmSdF4EgreidxWPsk5U1tMvXOOgJxkSp5bZ6D4Ol2EdUDZaYVp4uRqRw4NTuxv9JeiwLZHbAIAYMU"
    text = "123"
    openid = "ophka5ORWZC6asTu2Frb5wI8VjO8"
    print("acctoken", acctoken)
    checkurl = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token={ACCESS_TOKEN}".format(
        ACCESS_TOKEN=acctoken)

    data = '{"content": "' + text + '","openid": "' + openid + '","scene":  2 ,"version":  2 }'
    headers = {'Content-Type': 'application/json'}
    print("data",data)
    res = requests.post(checkurl, data=data.encode('utf-8'), headers=headers)
    lev = res.json().get("result").get("label")
    print("res.json()", res.json())
    print("lev", lev)
    return True if lev == 100 else False

res = infocheck()
print(res)

