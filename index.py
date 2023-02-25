
from datetime import datetime, date
from flask import Flask, request, jsonify 
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from urllib import parse
import pymysql
import random
from revChatGPT.V1 import Chatbot
import time
# from creat_bot import creat_new_bot

account_dict = {'账号1': '密码', '账号2': '密码'} 
print("账户总数量",len(account_dict))
account_list = sorted(account_dict.items(),key=lambda item:item[1],reverse=True)

all_account = set()
used_account = set()
onlie_time_dict = {}
openid_30s_dict = {}
openid_account_dict = {}
for info in account_list:
    account = info[0]
    password = info[1]
    all_account.add(account)


app = Flask(__name__)

# 基础项配置

# 小程序apid
APPID = ''
# 小程序secr
SECRET = ''
# 管理员id
manageropenid = ''

# 新注册免费次数
newsignnum = 5


# 数据库配置
# # 用户名
user = ''
# 密码
password = parse.quote_plus('')
# 表名
database = 'user'
# 地址
sqlurl = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s:3306/%s' % (
    user, password, sqlurl, database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 创建组件对象
db = SQLAlchemy(app)


def get_bot(account, password):
    try_num = 0
    while try_num<3:
        try:
            chatbot = Chatbot(config={
                "email": account,
                "password": password,
                })
            try_num +=1
            chatbot.clear_conversations()
            return chatbot
        except:
            try_num +=1
            print("第%s次尝试创建chatbot"%try_num)
            print(account,password)
    return None

   
    
       
    

# 数据表
class BaseConfig(db.Model):
    # 基础配置项
    __tablename__ = 'baseconfig'
    id = db.Column(db.Integer, primary_key=True)
    videonum = db.Column(db.Integer)
    videomax = db.Column(db.Integer)
    sharenum = db.Column(db.Integer)
    sharemax = db.Column(db.Integer)
    everynum = db.Column(db.Integer)
    isadj = db.Column(db.Boolean, default=False)
    manavx = db.Column(db.String(128))


class User(db.Model):
    # 用户表
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(128), unique=True)
    num = db.Column(db.Integer, index=True)
    askhis = db.relationship('AskHis')  # 1.定义关系属性 relationship("关联数据所在的模型类")
    addlog = db.relationship('Log')
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)


class AskHis(db.Model):
    # 提问历史
    __tablename__ = 'askhis'
    id = db.Column(db.Integer, primary_key=True)
    ask = db.Column(db.String(10240))
    answ = db.Column(db.String(10240))
    time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    openid = db.Column(db.Integer, db.ForeignKey('user.id'))


class Log(db.Model):
    # 充值日志
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    addnum = db.Column(db.Integer)
    type = db.Column(db.String(128))
    time = db.Column(db.DateTime, default=datetime.now)
    openid = db.Column(db.Integer, db.ForeignKey('user.id'))


class Adj(db.Model):
    # 广告
    __tablename__ = 'adj'
    id = db.Column(db.Integer, primary_key=True)
    adjinfo = db.Column(db.String(10240))


class ApiPoll(db.Model):
    # api池
    __tablename__ = 'apipoll'
    id = db.Column(db.Integer, primary_key=True)
    apikey = db.Column(db.String(128), unique=True)
    statu = db.Column(db.Boolean, default=True)
    checkstatu = db.Column(db.Boolean, default=True)
    callnum = db.Column(db.Integer, default=0)
    lastlog = db.Column(db.String(10240))
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    check_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

# 敏感词检测
@app.route('/wordcheck',methods=['POST'])
def wordcheck():
    msg = request.json.get('msg')
    openid = request.json.get('openid')

    try:

        stau = infocheck(msg,openid)
        print("stau", stau)
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
        # print("acctoken", acctoken)
        checkurl = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token={ACCESS_TOKEN}".format(
            ACCESS_TOKEN=acctoken)

        text = text.replace("\n", "")
        text = text.replace("\"", "")
        text = text.replace("\'", "")
        data = '{"content": "' + text + '","openid": "' + openid + '","scene":  2 ,"version":  2 }'
        headers = {'Content-Type': 'application/json'}
        # print("data",data)
        res = requests.post(checkurl, data=data.encode('utf-8'), headers=headers)
        lev = res.json().get("result").get("label")
        suggest = res.json().get("result").get("suggest")
        # print("res.json()", res.json())
        # print("lev", lev)
        print("suggest", suggest)
        if suggest == "review" or suggest == "pass":
            return True
        else:
            return False
    except Exception as e:
        getacctoken()
        print('重新获取')
        # return jsonify('内容包含敏感文字，请重新编辑发送')
        return False

def getacctoken():
    print('get_token')
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
    text = request.json.get('msg')
    openid = request.json.get('openid')
    a = infocheck(text,openid)
    print("a ", a )
    return str(a)


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


# 消息处理 chatgpt
@app.route('/message', methods=['POST'])
def mess():
    global used_account
    global onlie_time_dict
    global openid_30s_dict
    global openid_account_dict
    print("接收到微信的请求")
    api1 = ApiPoll.query.filter(
        ApiPoll.statu == True, ApiPoll.checkstatu == True).all()
    api = random.choice(api1)# 基本没用

    msg = request.json.get('msg')
    # maxtoken = request.json.get('maxtoken')
    openid = request.json.get('openid')
    # modetype = request.json.get('modetype')

    user1 = User.query.filter(User.openid == openid).first()
    usernum = user1.num - 1

    # print("随机选择了api")


    print("准备开始进行 infocheck")
    if infocheck(msg, openid) is False:
        res = {
            "resmsg": "内容包含敏感文字，我们都是社会主义的好公民，要保持积极正向，共建美好祖国。",
            "num": usernum,
            "code": 200
        }
        print("内容包含敏感文字，请重新编辑发送")
        return res

    try:
        print("准备开始请求chatgpt")
        prompt = msg
        response = ""

        print("len(openid_30s_dict)", len(openid_30s_dict))
        if openid in onlie_time_dict:
            cur_time = int(time.time())
            last_time = cur_time - onlie_time_dict[openid]
        else:
            last_time = 1200

        print(last_time < 120)
        print(openid in openid_30s_dict)
        if last_time<120 and openid in openid_30s_dict:
            chatbot = openid_30s_dict[openid]
            print("使用了自己30秒前的bot", chatbot)
        else:
            if openid in openid_30s_dict:
                openid_30s_dict.pop(openid)
            if openid in openid_account_dict:
                old_account = openid_account_dict[openid]
                if old_account in used_account:
                    used_account.remove(old_account)
            if openid in onlie_time_dict:
                onlie_time_dict.pop(openid)
            

            # 创建新的chatbot

            # 随机选择一个没有使用的bot,最多等待5次
            print("准备使用新的bot")
            print("计算没有使用的bots")

            print("used_account", used_account)
            tmp_bots = list(all_account - used_account)
            if len(tmp_bots) < 2:
                used_account = set()
            if len(tmp_bots)>0:
                print("有可以使用的bot")
                account = random.choice(tmp_bots)
                password = account_dict[account]
                
                chatbot = get_bot(account, password)
                print("随机选择chatbot, done")
                
                if chatbot is None:
                    print("创建bot失败，尝试其他账户")
                    for i in range(3):
                        account = random.choice(tmp_bots)
                        password = account_dict[account]
                        chatbot = get_bot(account, password)  
                        
                        if chatbot is not None:

                            break

                    errmsg = "chatgpt的官网登录不上了，请稍后重试"
                    print(errmsg)
                    res = {
                        "resmsg": errmsg,
                        "num": usernum+1,
                        "code": 200
                    }
                    return res
                else:
                    used_account.add(account)
                    print("used_account", used_account)
                    
            else:
                i = 0
                while i < 5:
                    time.sleep(0.5)
                    print("开始重试")
                    tmp_bots = list(all_account - used_account)
                    i+=1
                    if len(tmp_bots)>0:
                        account = random.choice(tmp_bots)
                        password = account_dict[account]
                        chatbot = get_bot(account, password)
                        if chatbot is not None:
                            print("重试后，选择了 bot")
                            used_account.add(account)
                            


                errmsg = "太多用户使用，导致账号不足"
                print(errmsg)
                res = {
                    "resmsg": errmsg,
                    "num": usernum+1,
                    "code": 200
                }
                return res

            openid_30s_dict[openid] = chatbot
            onlie_time_dict[openid] = int(time.time())
        try:    
            conversations = chatbot.get_conversations()
            if len(conversations)>0:
                conversation = conversations[0]["id"]
                for data in chatbot.ask(prompt=prompt,conversation_id=conversation):
                    response = data["message"]
            else:
                for data in chatbot.ask(prompt=prompt):
                    response = data["message"]
            print("请求chatgpt成功") 
            print("chatgpt response", response)    
        except:
            return errout("创建或请求chatgpt数据失败，请稍后再试") 

        if response != "":

            answ = response
            ask1 = AskHis(ask=msg, answ=answ, openid=user1.id)
            ApiPoll.query.filter(ApiPoll.apikey == api.apikey).update(
                {'callnum': ApiPoll.callnum + 1})
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
            return errout("请求chatgpt数据失败")


    except KeyError as e:
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
    app.run(debug=True)
