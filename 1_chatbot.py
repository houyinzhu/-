import requests
import json

from requests.utils import stream_decode_response_unicode

from glm import role_system

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "85556a78acba4b4eb7a5130fa9139580.uMmcFvwz4LGabgRQ",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")


# 使用示例
role_system="你所有的回答都要扮演一个疯狂的小丑"
# 多轮对话循环，直到用户输入 '再见' 结束
while True:  # 表示“当条件为真时一直循环”。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你要说的话（输入“再见”退出）：")
    if user_input in ['再见']:
        print("对话结束。")
        break
    messages = [
        {"role": "user", "content": role_system + user_input}
    ]
    result = call_zhipu_api(messages)
    print(result['choices'][0]['message']['content'])