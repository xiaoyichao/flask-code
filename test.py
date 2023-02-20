from revChatGPT.V2 import Chatbot

# config={
#     "email": "lahuseman88@outlook.com",
#     "password": "of75stFg8j"
    # }
async def main():
    chatbot = Chatbot(email="ahuseman88@outlook.com", password="of75stFg8j")
    async for line in chatbot.ask("你是谁"):
        print(line["choices"][0]["text"].replace("<|im_end|>", ""), end="", flush = True)
    print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())