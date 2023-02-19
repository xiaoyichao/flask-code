import json
text = "你好"
a = text.encode("utf-8")
print(a)

payload = {
        "scene": 1,
        "version": 2,
        "content": a
    }
    # .encode("utf-8")
print("字典 payload:", payload)

payload = json.dumps(payload)
print("json payload:", payload)

