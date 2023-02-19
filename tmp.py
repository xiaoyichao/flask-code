# 敏感词检测
@app.route('/wordcheck',methods=['POST'])
def wordcheck():
    msg = request.json.get('msg')
    openid = request.json.get('openid')

    try:

        stau = infocheck(msg,openid)
        if stau:

            return jsonify({'code':1})
        else:
            return jsonify({'code': 0, 'msg': 'err'})
    except:

        return jsonify({'code':0,'msg':'err'})


# 微信内容安全检测
def infocheck(text,openid):
    try:
        acctoken = Adj.query.filter(Adj.id == 2).first().adjinfo
        checkurl = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token={ACCESS_TOKEN}".format(
            ACCESS_TOKEN=acctoken)

        data = '{"content": "' + text + '","openid": "' + openid + '","scene":  2 ,"version":  2 }'
        headers = {'Content-Type': 'application/json'}
        res = requests.post(checkurl, data=data.encode('utf-8'), headers=headers)
        lev = res.json().get("result").get("label")
        print(res.json())
        print(lev)
        return True if lev == 100 else False
    except Exception as e:
        getacctoken()
        print('重新获取')
        return jsonify('内容包含敏感文字，请重新编辑发送')


def getacctoken():
    print('getroken')
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
          
@app.route('/test',methods=['POST'])

def test():
  
    a = infocheck(text,openid)
    return a


# 错误返回
def errout(err):
    errr = str(err)
    res = {
            # 广告信息
                "adj": '接口执行错误',
                "code": 444,
                "errinfo":errr
            }
    return  res
# api检测
@app.route('/checkapi', methods=['POST'])
def checkapi():
    apikey = request.json.get('apikey')
    apilist = ApiPoll.query.filter(ApiPoll.statu == False).all()

    try:

        req = requests.post('https://api.openai.com/v1/completions',
                            json={"prompt": '你好', "max_tokens": 1024, "model": "text-davinci-003-playground", "temperature": 0}, headers={
                                'content-type': 'application/json', 'Authorization': 'Bearer ' + apikey})
        if req.status_code == 200:
            ApiPoll.query.filter(
                ApiPoll.apikey == apikey).update({'statu': True})
            db.session.commit()
            api1 = ApiPoll.query.filter().all()
            apilist = []
            for item in api1:
                api = {
                    "key": item.apikey,
                    "keystatu": item.statu,
                    "usernum": item.callnum,
                }
                apilist.append(api)

            print(apilist)
            res = {

                "apilist": apilist,

                "code": 200
            }
            print(res)
            return res

        else:

            reqdic = json.loads(req.text)
            errmsg = reqdic['error']['message']

            ApiPoll.query.filter(ApiPoll.apikey == apikey).update(
                {'checkstatu': False, 'statu': False, 'lastlog': errmsg})
            db.session.commit()

        return errout(errmsg)
    except KeyError as e:

        return errout('openai官方请求错误，请稍后重试')

# 增加api


@app.route('/editapi', methods=['POST'])
def editapi():
    apikey = request.json.get('apikey')
    api2 = ApiPoll.query.filter(ApiPoll.apikey == apikey)
    if api2.first():
        return errout('此key已存在')

    else:

        api1 = ApiPoll(apikey=apikey)
        db.session.add(api1)
        db.session.commit()
        api1 = ApiPoll.query.filter().all()
        apilist = []
        for item in api1:
            api = {
                "key": item.apikey,
                "keystatu": item.statu,
                "usernum": item.callnum,
            }
            apilist.append(api)

        print(apilist)
        res = {

            "apilist": apilist,

            "code": 200
        }
        print(res)
        return res

# 删除api


@app.route('/delkey', methods=['POST'])
def delkey():
    apikey = request.json.get('apikey')
    api2 = ApiPoll.query.filter(ApiPoll.apikey == apikey)
    if api2.first():

        ApiPoll.query.filter(ApiPoll.apikey == apikey).delete()
        db.session.commit()
        api1 = ApiPoll.query.filter().all()
        apilist = []
        for item in api1:
            api = {
                "key": item.apikey,
                "keystatu": item.statu,
                "usernum": item.callnum,
            }
            apilist.append(api)

        print(apilist)
        res = {

            "apilist": apilist,

            "code": 200
        }
        print(res)
        return res

    else:

        return errout('此key不存在')


# 获取APIKEY信息
@app.route('/getapilist', methods=['GET'])
def getapilist():
    api1 = ApiPoll.query.filter().all()
    apilist = []
    for item in api1:
        api = {
            "key": item.apikey,
            "keystatu": item.statu,
            "usernum": item.callnum,
        }
        apilist.append(api)

    print(apilist)
    res = {

        "apilist": apilist,

        "code": 200
    }
    print(res)
    return res


# 设置配置信息
@app.route('/setinfo', methods=['POST'])
def setinfo():
    daynum = int(request.json.get('daynum'))
    sharenum = request.json.get('sharenum')
    videonum = request.json.get('videonum')
    sharemaxnum = request.json.get('sharemaxnum')
    videomaxnum = request.json.get('videomaxnum')
    isadj = request.json.get('isadj')
    manavx = request.json.get('manavx')
    print(daynum, type(daynum))

    set1 = BaseConfig.query.filter()
    if set1.first():

        setinfo = BaseConfig.query.filter(BaseConfig.id == 1)

        setinfo.update({'everynum': daynum, 'sharenum': sharenum, 'videonum': videonum,
                        'sharemax': sharemaxnum, 'videomax': videomaxnum, 'isadj': isadj, 'manavx': manavx})
    else:
        setadd = BaseConfig(id=1, everynum=daynum, sharenum=sharenum, videonum=videonum,
                            sharemax=sharemaxnum, videomax=videomaxnum, isadj=isadj, manavx=manavx)
        db.session.add(setadd)

    db.session.commit()

    setinfo1 = BaseConfig.query.filter().first()

    daynum1 = setinfo1.everynum
    sharenum1 = setinfo1.sharenum
    videonum1 = setinfo1.videonum
    isadj1 = setinfo1.isadj
    sharemaxnum1 = setinfo1.sharemax
    videomaxnum1 = setinfo1.videomax
    manavx1 = setinfo1.manavx

    res = {

        "daynum": daynum1,
        "sharenum": sharenum1,
        "videonum": videonum1,

        "isadj": isadj1,
        "sharemaxnum": sharemaxnum1,
        "videomaxnum": videomaxnum1,
        "manavx": manavx1,
        "code": 200
    }
    return res


# 获取配置信息
@app.route('/getsetinfo', methods=['GET'])
def getsetinfo():
    if BaseConfig.query.filter().first():

        setinfo = BaseConfig.query.filter().first()
        daynum = setinfo.everynum
        sharenum = setinfo.sharenum
        videonum = setinfo.videonum
        isadj = setinfo.isadj
        sharemaxnum = setinfo.sharemax
        videomaxnum = setinfo.videomax
        manavx = setinfo.manavx

        print(setinfo)
        res = {

            "daynum": daynum,
            "sharenum": sharenum,
            "videonum": videonum,

            "isadj": isadj,
            "sharemaxnum": sharemaxnum,
            "videomaxnum": videomaxnum,
            "manavx": manavx,

            "code": 200
        }
        return res
    else:
        return errout("请先进行参数配置")


# 检测联通
@app.route('/', methods=['GET'])
def index():
    adj = Adj.query.filter()
    print(adj)

    if adj.first():
        adjdetail = adj.first().adjinfo
        res = {
            # 广告信息
            "adj": adjdetail,
            "code": 200
        }
        return res
    else:
        res = {
            # 广告信息
            "adj": '',
            "code": 200
        }
        return res


# 设置广告
@app.route('/setadj', methods=['POST'])
def setadj():
    CODE = request.json.get('code')
    getadjinfo = request.json.get('adjinfo')
    print('code', CODE)
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid='+APPID + \
        '&secret='+SECRET+'&js_code='+CODE+'&grant_type=authorization_code'
    print(url, CODE)
    try:
        req = requests.get(url)
        try:
            getres = json.loads(req.text)
            openid = getres['openid']
            if openid == manageropenid:
                print(getadjinfo)
                # adj1 = Adj(adjinfo =getadjinfo )
                adj0 = Adj.query.filter()
                if adj0.first():
                    Adj.query.filter(Adj.id == 1).update(
                        {'adjinfo': getadjinfo})
                # db.session.add(adj1)
                else:
                    adj1 = Adj(adjinfo=getadjinfo)
                    db.session.add(adj1)
                db.session.commit()
                a = Adj.query.filter().first()
                res = {
                    # 广告信息
                    "adj": a.adjinfo,
                    "code": 200
                }
                return res
            else:
                return 'error'
        except KeyError as e:
            return errout(getres)

    except KeyError as e:

        return errout('微信认证连接失败')

# 管理员充值


@app.route('/manaaddnum', methods=['POST'])
def manaaddnum():
    userid = request.json.get('userid')
    CODE = request.json.get('code')
    num = request.json.get('num')
    print('code', CODE)
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid='+APPID + \
        '&secret='+SECRET+'&js_code='+CODE+'&grant_type=authorization_code'
    print(url, CODE)
    try:
        req = requests.get(url)
        try:
            getres = json.loads(req.text)
            openid = getres['openid']
            if openid == manageropenid:

                user1 = User.query.filter(User.openid == userid).first()
                endnum = user1.num + int(num)
                print(endnum)
                User.query.filter(User.openid == userid).update(
                    {'num': endnum})
                # db.session.add(adj1)
                log1 = Log(addnum=num, type='m', openid=user1.id)
                db.session.add(log1)
                db.session.commit()
                a = User.query.filter(User.openid == userid).first()
                res = {
                    "msg": '充值成功。现有数量：'+str(a.num),
                    "num": a.num,
                    "code": 200
                }
                return res
            else:
                return 'error'
        except KeyError as e:
            return errout(getres)

    except KeyError as e:

        return errout('微信认证连接失败')
# 每日免费次数


@app.route('/everydaynum', methods=['GET'])
def everydaynum():
    everynum = BaseConfig.query.filter().first().everynum
    print(everynum)
    user = User.query.filter(User.num < everynum).update({"num": everynum})
    print(user)
    db.session.commit()
    res = {

        "num": '免费次数更新数量' + str(user),
        "code": 200
    }
    return res


# 用户次数增加
@app.route('/addnum', methods=['POST'])
def addnum():
    baseconfingset = BaseConfig.query.filter().first()
    videonum = baseconfingset.videonum
    videomax = baseconfingset.videomax
    # sharenum = baseconfingset.videonum  原内容  videonum 改为 sharenum  
    sharenum = baseconfingset.sharenum
    sharemax = baseconfingset.sharemax
    type = request.json.get('type')
    openid = request.json.get('openid')
    user1 = User.query.filter(User.openid == openid).first()
    nums = Log.query.filter(Log.time > date.today(),
                            Log.openid == user1.id, Log.type == 's').count()
    numv = Log.query.filter(Log.time > date.today(),
                            Log.openid == user1.id, Log.type == 'v').count()
    print(nums, numv)

    if numv >= videomax and numv+videomax != 0:
        res = {
            "msg": '本日看视频领次数活动次数已用尽，不再增加次数',

            "code": 201
        }

        return res
    try:
        if type == 'v':
            if numv >= videomax and numv+videomax != 0:
                res = {
                    "msg": '本日看视频领次数活动次数已用尽，不再增加次数',

                    "code": 201
                }

                return res
            endnum = user1.num + videonum
            print(endnum)
            User.query.filter(User.openid == openid).update({'num': endnum})
            log1 = Log(addnum=videonum, type='v', openid=user1.id)
        if type == 's':
            if nums >= sharemax and numv+sharemax != 0:
                res = {
                    "msg": '本日分享活动次数已用尽，不再增加次数',

                    "code": 201
                }

                return res

            endnum = user1.num + sharenum
            print(endnum)
            User.query.filter(User.openid == openid).update({'num': endnum})

            log1 = Log(addnum=sharenum, type='s', openid=user1.id)

        db.session.add(log1)
        db.session.commit()
        a = User.query.filter(User.openid == openid).first()
        res = {
            "msg": '任务完成，现有数量：'+str(a.num),
            "num": a.num,
            "code": 200
        }

        return res
    except KeyError as e:
        return errout('次数增加故障，请联系管理员')


# 微信code获取openid
@app.route('/login', methods=['POST'])
def LOGIN():
    CODE = request.json.get('code')
    print('code', CODE)
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid='+APPID + \
        '&secret='+SECRET+'&js_code='+CODE+'&grant_type=authorization_code'
    print(url, CODE)
    try:
        req = requests.get(url)
        try:
            getres = json.loads(req.text)
            openid = getres['openid']
            # 判断是否注册
            if openid:
                print('已注册')
                userin = User.query.filter(User.openid == openid)
                if userin.first():
                    num = userin.first().num
                    res = {
                        "resmsg": getres,
                        "mana": manageropenid,
                        "num": num,
                        "code": 200

                    }
                    return res

                else:
                    print('已注册')
                    useradd = User(openid=openid, num=newsignnum)
                    db.session.add(useradd)
                    db.session.commit()

                    a = User.query.filter(User.openid == openid).first()
                    res = {
                        "resmsg": getres,
                        "mana": manageropenid,
                        "num": a.num,
                        "code": 200
                    }
                    return res
            else:
                return 'error'
        except KeyError as e:
            return errout(getres)

    except KeyError as e:

        return errout('微信认证连接失败')


# 消息处理
@app.route('/message', methods=['POST'])
def mess():
    api1 = ApiPoll.query.filter(
        ApiPoll.statu == True, ApiPoll.checkstatu == True).all()
    api = random.choice(api1)
    msg = request.json.get('msg')
    maxtoken = request.json.get('maxtoken')
    
    # if maxtoken > 2500:
    #     maxtoken = 2048
    # if maxtoken <= 0:
    #     maxtoken = 1024
    # else:
    #     maxtoken = maxtoken- 100
    if maxtoken <0 :
        maxtoken = 1024
    if maxtoken >1024  :
        maxtoken = 1024

    
    openid = request.json.get('openid')
 

       
       

    try:
        req = requests.post('https://api.openai.com/v1/completions',
                            json={"prompt": msg, "max_tokens": maxtoken, "model": "text-davinci-003", "temperature": 0.8}, headers={
                                'content-type': 'application/json', 'Authorization': 'Bearer ' + api.apikey})
        user1 = User.query.filter(User.openid == openid).first()
        print('reqstatu',req.status_code)

        if req.status_code == 200:

            reqdic = json.loads(req.text)
            print(reqdic)

            answ = reqdic['choices'][0]['text']
            ask1 = AskHis(ask=msg, answ=answ, openid=user1.id)
            ApiPoll.query.filter(ApiPoll.apikey == api.apikey).update(
                {'callnum': ApiPoll.callnum + 1})
            usernum = user1.num - 1
            User.query.filter(User.openid == openid).update({'num': usernum})
            db.session.add(ask1)
            db.session.commit()

            res = {
                "resmsg": reqdic,
                "num": usernum,
                "code": 200
            }
            return res
        else:
            reqdic = json.loads(req.text)
            errmsg = reqdic['error']['message']
            errcode = reqdic['error']['code']
            errtype = reqdic['error']['type']
            print(reqdic)
            if errcode == 'invalid_api_key' or errtype == "insufficient_quota":
                api = ApiPoll.query.filter(ApiPoll.apikey == api.apikey).update({
                    'statu': False, 'lastlog': errmsg})
                db.session.commit()
                if errmsg:
                    print ('服务器快冒烟了，等会再试')
                    return errout('服务器快冒烟了，等会再试')
                else:
                    print('服务器快Boom了，先缓一缓')
                    return errout('服务器快Boom了，先缓一缓')
            else:
                print('官方请求错误,稍后再试')
                return errout('官方请求错误,稍后再试')

    except :

        return errout('openai官方请求错误，请稍后重试')



# 获取运营信息
@app.route('/userinfo', methods=['GET'])
def userinfo():

    allusernum = User.query.filter().count()
    dayadduser = User.query.filter(User.create_time > date.today()).count()
    allanswnum = AskHis.query.filter().count()

    res = {

        "allusernum": allusernum,
        "dayadduser": dayadduser,
        "allanswnum": allanswnum,
        "code": 200
    }
    print(res)
    return res

if __name__ == '__main__':
    app.run( debug=True)
