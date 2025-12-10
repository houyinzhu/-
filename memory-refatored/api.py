<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 43e52124ec759fb33752b4cf0978dd5c59ab6862
import requests

def call_zhipu_api(messages, model="glm-4-flash"):
    """调用智谱API获取AI回复"""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "85556a78acba4b4eb7a5130fa9139580.uMmcFvwz4LGabgRQ",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
<<<<<<< HEAD
=======
=======
import requests

def call_zhipu_api(messages, model="glm-4-flash"):
    """调用智谱API获取AI回复"""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "85556a78acba4b4eb7a5130fa9139580.uMmcFvwz4LGabgRQ",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
>>>>>>> 7d9d9ec32f63a2a65ed81c345f4622f896367003
>>>>>>> 43e52124ec759fb33752b4cf0978dd5c59ab6862
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")