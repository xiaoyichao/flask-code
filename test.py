import requests
APPID = 'wx03c9741b85f57a9b'
SECRET = 'e00a7350cbcec6abaa2c57980060811b'

def infocheck(text,openid):
    try:
        acctoken = Adj.query.filter(Adj.id == 2).first().adjinfo

        checkurl = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token={ACCESS_TOKEN}".format(
            ACCESS_TOKEN=acctoken)
        print(checkurl)
        payload = {
            "openid": openid,
            "scene": 1,
            "version": 2,
            "content": text
        }

        payload = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers = {'Content-Type': 'application/json'}

        response = requests.post(checkurl, json=payload, headers=headers)
        response_json = response.json()
        print(response_json)

        errcode = response_json.get("errcode", None)
        result = response_json.get("result", None)
        if errcode == 0 and result.get("suggest", None) == "pass":
            print("msg_sec_check 正常")
            return response
        else:
            print("msg_sec_check 异常")
            keywords = "|".join([detail["keyword"] for detail in response_json["detail"] if "keyword" in detail])
            raise Exception(
                "错误： errcode={}, suggest={}, keywords={}".format(errcode, result.get("suggest", None), keywords))

    except:
        getacctoken()
        return jsonify('内容包含敏感文字，请重新编辑发送')

class Adj(db.Model):
    # 广告
    # __tablename__ = 'adj'
    id = db.Column(db.Integer, primary_key=True)
    adjinfo = db.Column(db.String(10240))

def getacctoken():
    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential' \
                       '&appid={appid}&secret={secret}'.format(appid=APPID, secret=SECRET)
    access_token_res = requests.get(access_token_url).json()['access_token']
    atok = Adj.query.filter(Adj.id == 2).first()
    if atok:
        atok.adjinfo = access_token_res
    else:
        atok = Adj(id = 2,adjinfo=access_token_res)
        db.session.add(atok)
    db.session.commit()
    return access_token_res
    if access_token_res.json().get('errcode'):
        raise 'AccessToken()'

res = infocheck("六四事件","")
print(infocheck)