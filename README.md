<!--
 * @Author: xiaoyichao xiao_yi_chao@163.com
 * @Date: 2023-02-24 18:51:36
 * @LastEditors: xiaoyichao xiao_yi_chao@163.com
 * @LastEditTime: 2023-02-25 16:59:42
 * @FilePath: /flask-code/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

# 微信小程序访问ChatGPT

后端都在这个项目里边
此版本已经修复bug

整体部署流程和小袁是一样的，区别在于（1）服务器地区的选择 和（2）点击代码部署之前要安装一个插件


## 服务器地区的选择
见图 选择硅谷的服务器.jpg 文件夹的最外层有这个图

## 点击代码部署之前要安装一个插件
进入到终端，安装一个插件，
方案和位置见 安装一个插件.jpg
pip install  revChatGPT
安装成功后，会显示Successfully installed OpenAIAuth-0.3.2 revChatGPT-2.3.5

## 需要修改代码的地方

code/index.py文件下

url = "https://chat-chat.fcapp.run"
还有那些密钥和账户
account_dict = {'账号1': '密码', '账号2': '密码'}  这个位置是你的chatgpt 的账户

小程序平台的域名列表也需要添加 域名


## 接下来，你就可以按照之前小袁的方式，部署代码了。

其他的流程就和小袁那套一样了。这个db.py 文件不需要执行了，因为在小袁那套代码部署的时候，数据库建立好了。
