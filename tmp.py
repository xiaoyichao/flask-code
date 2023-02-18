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
        # print(response_json)

        errcode = response_json.get("errcode", None)
        result = response_json.get("result", None)
        if errcode == 0 and result.get("suggest", None) == "pass":
            print("text", text)
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
