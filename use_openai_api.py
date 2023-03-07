# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
# openai安装方式
# pip install openai  --upgrade
# pip install openai==0.27.0
import openai
import os
import requests

openai.api_key = "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"

response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
  model="gpt-3.5-turbo-0301",
  messages=[
        {"role": "user", "content": "YOU：请从市场营销专业角度来帮我设计一个5个问题的调查问卷，题目是学校要开设超市，注意要抓住消费者消费行为特征"},
        # {"role": "system", "content": "You are a helpful assistant."},
        # {"role": "user", "content": "Who won the world series in 2020?"},
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        # {"role": "user", "content": "Where was it played?"}
    ]
)

print(response)
print(response['choices'][0]['message']['content'])
