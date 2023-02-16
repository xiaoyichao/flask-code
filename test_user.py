'''
Author: xiaoyichao xiao_yi_chao@163.com
Date: 2023-02-16 22:53:29
LastEditors: xiaoyichao xiao_yi_chao@163.com
LastEditTime: 2023-02-16 22:58:13
FilePath: /flask-code/test_user.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from revChatGPT.V1 import Chatbot
import time
import random

# account_dict = {'wolhtetjuywvb@eurokool.com': 'abc123456789', 'uvffqudbqob@eurokool.com': 'abc123456789', 'svakzkwcegq@eurokool.com': 'abc123456789', 'wyabuwztdcct@eurokool.com': 'abc123456789', 'qmqows@eurokool.com': 'abc123456789', 'lahuseman88@outlook.com': 'of75stFg8j', 'hp52477bgmw7027@163.com': 'XnwlHh5VwD', 'px303xgza2591@163.com': 'GMV1x4wtQC', 'oxqvp331ztx1@163.com': '2RUt5HOjbh', 'at10574llm37@163.com': 'LE4cy7hHQt', 'ijyvnc31uj72@163.com': '68s00wDGmV', 'sf7549vvvd9429@163.com': '3PXQrl4eEa', 'qdmcca89jt466@163.com': 'c618XMONr7', 'uyprjj68cb372@163.com': 'B3P21G878j', 'vi8715ewcu3894@163.com': 'N4v99fzTE4', 'gwclko009sa211@163.com': '29uQ60aFUi', 'ppsor13xvq33@163.com': 'z4yIqD2wQX', 'zy673rowg952@163.com': 'ZX2P8w9A2L', 'ol5092rxmn1381@163.com': 'T7SU1VVNoX', 'aapqp508udid12@163.com': '48aSapa33T', 'kwhaf497rru7@163.com': 'reG0TRUM38', 'yejiw31tnl3@163.com': 'rLKCWrLdGh', 'shrfm51brh36@163.com': 'jPx6PQD1s9', 'heail17ewu25@163.com': 'ho4l2A18MU', 'jb6963fdhv062@163.com': 'bQA2s51d9d', 'snjbc8672ytvs37@163.com': 'T10rLTGLC2', 'uozdb01bjl31@163.com': '6zB4lhgg8A', 'iy2373patc1753@163.com': '40g52K2rPf', 'bvpui74kyox04@163.com': 'hEHpWWCWwG', 'slqdi3170ncrg74@163.com': '3PrKE16NpZ', 'dsyqy18esd2@163.com': '4N1ZgWw5Wc', 'injimr95wy023@163.com': 'y6NlU7Ab10', 'jh8994hoyw8778@163.com': 'TPx6S0niJh', 'hllri02sape92@163.com': '10z1o1970a', 'oeixcv048nw06@163.com': 'doL0H0s6pa', 'hb93594chrn527@163.com': 'k4kyKbQ67n', 'ggzlm907nizp30@163.com': 'qx9XYs194p', 'kl19967dgak179@163.com': 's29s2ubPQz', 'zbmhv435rcky46@163.com': 'gp2bb5wWEc', 'ne87280hkrc3035@163.com': '3J72720xz2', 'lm845oyoa384@163.com': 'm55Vh3xXNb', 'shndcl35xb75@163.com': 'YEggHvB8KS', 'ug338xsxs865@163.com': '7E99b553PD', 'hi45728ahlm1616@163.com': '5gRLz2ckZ6', 'kaiucb434fc507@163.com': 'FqzVglS26E', 'rfcxn305gqkw6@163.com': 'N9xhzlq2xM', 'owcmn6032wjlg0@163.com': '0q7OEK5ebd', 'bedupj72vv90@163.com': 'i4nvjQ8Lh8', 'zt0834cbde585@163.com': 'r05a2vb3JX', 'ih7850ejso311@163.com': 'su057OmnIB', 'rhxtyh320kq29@163.com': 'g96YMnuuoa', 'ltbbby14sc643@163.com': 'plDg0kf3vU', 'sinttw48gq102@163.com': '3c1UV449u9', 'rz2532xmlh691@163.com': '29wrkq2XZh', 'nsbzg881ujv0@163.com': 'u50ynaVk4y', 'yi6899kipr246@163.com': 'q1t3uPDJpA'}
account_dict = {'wolhtetjuywvb@eurokool.com': 'abc123456789', 'uvffqudbqob@eurokool.com': 'abc123456789', 'svakzkwcegq@eurokool.com': 'abc123456789', 'wyabuwztdcct@eurokool.com': 'abc123456789', 'qmqows@eurokool.com': 'abc123456789', 'lahuseman88@outlook.com': 'of75stFg8j', 'hp52477bgmw7027@163.com': 'XnwlHh5VwD', 'px303xgza2591@163.com': 'GMV1x4wtQC',  }
chat_bot_num = 0
chatbots = []
all_bots =set()
used_bot = set()
print("账户总数量",len(account_dict))
for k,v in account_dict.items():
    try_num = 0
    while try_num<10:
        try:
            locals()[f'chatbot_{chat_bot_num}']=Chatbot(config={
            "email": k,
            "password": v,
            })
            chatbots.append(locals()[f'chatbot_{chat_bot_num}'])
            all_bots.add(locals()[f'chatbot_{chat_bot_num}'])
            print("第%s个 chatbot 创建成功 "%chat_bot_num)
            chat_bot_num +=1
            try_num +=1
            sleep_time = random.uniform(0.5,2.0)
            print("sleep:", sleep_time)
            time.sleep(sleep_time)
            break
            
        except :
            print("第%s个 chatbot 创建失败 "%chat_bot_num)
            try_num +=1
            sleep_time = random.uniform(0.5,3.0)
            print("sleep:", sleep_time)
            time.sleep(sleep_time)
            

tmp_bots = list(all_bots - used_bot)
if len(tmp_bots)>0:
    chatbot = random.choice(tmp_bots)
    print("选择了 bot")
else:
    i = 0
    while i < 5:
        time.sleep(0.5)
        print("开始重试")
        tmp_bots = list(all_bots - used_bot)
        i+=1
        if len(tmp_bots)>0:
            chatbot = random.choice(tmp_bots)
            print("重试后，选择了 bot")
    chatbot = None
    print("重试后，没有 bot")

used_bot.add(chatbot)
    
print("随机选择了chatbot")

prompt = "你是谁？"
response = ""

for data in chatbot.ask(
prompt
):
    response = data["message"]
print(response)
print("请求chatgpt成功") 
used_bot.remove(chatbot)
print("used_bot", used_bot)