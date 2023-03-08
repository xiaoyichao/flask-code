# from revChatGPT.V1 import Chatbot

# account = 'wolhtetjuywvb@eurokool.com'
# password = 'abc123456789'

# chatbot = Chatbot(config={
#     "email": account,
#     "password": password,
# })

# chatbot.clear_conversations()

# conversations = chatbot.get_conversations()
# conversation = conversations[0]["id"]


from revChatGPT.V1 import Chatbot

chatbot = Chatbot(config={
  "email": "wolhtetjuywvb@eurokool.com",
  "password": "abc123456789"
})

prompt = "你是谁"
response = ""

for data in chatbot.ask(
  prompt
):
    response = data["message"]

print(response)