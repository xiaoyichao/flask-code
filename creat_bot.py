'''
Author: xiaoyichao xiao_yi_chao@163.com
Date: 2023-02-24 19:16:02
LastEditors: xiaoyichao xiao_yi_chao@163.com
LastEditTime: 2023-02-24 19:27:21
FilePath: /flask-code/ceat_bot.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import random
import time
from revChatGPT.V1 import Chatbot


def get_bot(account, password):
    try_num = 0
    while try_num<3:
        try:
            chatbot = Chatbot(config={
                "email": account,
                "password": password,
                })
            try_num +=1
            return chatbot
        except:
            try_num +=1
            print("第%s次尝试创建chatbot"%try_num)
            print(account,password)
    return None

def creat_new_bot(account_dict,all_bots,used_bot,usernum):
    # 随机选择一个没有使用的bot,最多等待5次
    print("计算没有使用的bots")
    tmp_bots = list(all_bots - used_bot)
    if len(tmp_bots)>0:
        account = random.choice(tmp_bots)
        password = account_dict[account]
        
        chatbot = get_bot(account, password)
        
        if chatbot is None:
            print("创建bot失败，尝试其他账户")
            for i in range(3):
                account = random.choice(tmp_bots)
                password = account_dict[account]
                chatbot = get_bot(account, password)  
                used_bot.add(chatbot)
                if chatbot is not None:
                    # break
                    print("随机选择chatbot, done")
                    return {"chatbot":chatbot,"account_dict":account_dict,"all_bots":all_bots,"used_bot":used_bot,"usernum":usernum}
            errmsg = "chatgpt的官网登录不上了，请稍后重试"
            print(errmsg)
            res = {
                "resmsg": errmsg,
                "num": usernum+1,
                "code": 200
            }
            return res
              
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
                used_bot.add(chatbot)
                print("重试后，选择了 bot")
                print("随机选择chatbot, done")
                return {"chatbot":chatbot,"account_dict":account_dict,"all_bots":all_bots,"used_bot":used_bot,"usernum":usernum}

        errmsg = "太多用户使用，导致账号不足"
        print(errmsg)
        res = {
            "resmsg": errmsg,
            "num": usernum+1,
            "code": 200
        }
        return res
        
    
       
    