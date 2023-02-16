<!--
 * @Author: xiaoyichao xiao_yi_chao@163.com
 * @Date: 2023-02-16 22:49:41
 * @LastEditors: xiaoyichao xiao_yi_chao@163.com
 * @LastEditTime: 2023-02-16 22:50:01
 * @FilePath: /flask-code/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 微信小程序访问ChatGPT

前后端都在这个项目里边

## 生成requirements.txt

pipreqs ./     --force 

## 需要修改的url

dev  https://chat-dev-chat-wlbmdduabn.us-west-1.fcapp.run


pro  https://chat-chat-faglendogy.us-west-1.fcapp.run 

code/index.py
url = "https://chat-chat-faglendogy.us-west-1.fcapp.run"

gpt3/common/config.js
apiurl: "https://chat-chat-faglendogy.us-west-1.fcapp.run",

小程序平台的域名列表也需要添加 域名


## pip 新创建的函数要安装revChatGPT ，目前层没起作用，不知道为啥

pip install  revChatGPT==2.2.7