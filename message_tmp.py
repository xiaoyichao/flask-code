# 消息处理 chatgpt
@app.route('/message', methods=['POST'])
def mess():
    print("接收到微信的请求")
    api1 = ApiPoll.query.filter(
        ApiPoll.statu == True, ApiPoll.checkstatu == True).all()
    api = random.choice(api1)# 基本没用
    print("随机选择了api")
    
    # 随机选择一个没有使用的bot,最多等待5次
    print("计算没有使用的bots")
    tmp_bots = list(all_bots - used_bot)
    if len(tmp_bots)>0:
        account = random.choice(tmp_bots)
        password = account_dict[account]
        
        chatbot = get_bot(account, password)
        
        if chatbot is None:
            print("创建bot失败，尝试其他账户")
            for i in range(5):
                account = random.choice(tmp_bots)
                password = account_dict[account]
                chatbot = get_bot(account, password)  
                if chatbot:
                    break  

        print("选择了 bot")
    else:
        i = 0
        while i < 5:
            time.sleep(0.5)
            print("开始重试")
            tmp_bots = list(all_bots - used_bot)
            i+=1
            if len(tmp_bots)>0:
                account = random.choice(tmp_bots)
                password = account_dict[account]
                chatbot = get_bot(account, password)
                print("重试后，选择了 bot")

        errmsg = "太多用户使用，导致账号不足"
        print("重试后，没有 bot")
        res = {
            "resmsg": errmsg,
            "num": usernum,
            "code": 200
        }
        return res
            
       

    used_bot.add(chatbot)
       
    print("随机选择chatbot, done")
    msg = request.json.get('msg')
    maxtoken = request.json.get('maxtoken') - 300
    openid = request.json.get('openid')
    print("准备开始请求chatgpt")
    try:
        a = infocheck(msg,openid)
        print(a)
        try:
            #### Basic example (single result):
            prompt = msg
            response = ""

            for data in chatbot.ask(
            prompt
            ):
                response = data["message"]
            print("请求chatgpt成功") 
            used_bot.remove(chatbot)

            print("chatgpt response", response)

            # req = requests.post('https://api.openai.com/v1/completions',
            #                     json={"prompt": msg, "max_tokens": maxtoken, "model": "text-davinci-003", "temperature": 0.8}, headers={
            #                         'content-type': 'application/json', 'Authorization': 'Bearer ' + api.apikey})
            user1 = User.query.filter(User.openid == openid).first()

            if response != "":

                # reqdic = json.loads(req.text)
                # print(reqdic)

                # answ = reqdic['choices'][0]['text']
                answ = response
                ask1 = AskHis(ask=msg, answ=answ, openid=user1.id)
                ApiPoll.query.filter(ApiPoll.apikey == api.apikey).update(
                    {'callnum': ApiPoll.callnum + 1})
                usernum = user1.num - 1
                User.query.filter(User.openid == openid).update({'num': usernum})
                db.session.add(ask1)
                db.session.commit()

                res = {
                    "resmsg": answ,
                    "num": usernum,
                    "code": 200
                }
                return res
            else:
                reqdic = json.loads(response)
                errmsg = reqdic['error']['message']
                errcode = reqdic['error']['code']
                errtype = reqdic['error']['type']
                print(reqdic)
                if errcode == 'invalid_api_key' or errtype == "insufficient_quota":
                    api = ApiPoll.query.filter(ApiPoll.apikey == api.apikey).update({
                        'statu': False, 'lastlog': errmsg})
                    db.session.commit()
                    return errout(errmsg)
                else:
                    return errout(errmsg)

        except KeyError as e:
            return errout('openai官方请求错误，请稍后重试')
    except:
        return errout('内容含有敏感字，请重新组织内容再提问')
