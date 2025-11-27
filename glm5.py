import requests
import json

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
role_system=["你目睹了杀人凶手的作案过程，但你要帮杀人凶手隐瞒真相。凶手是一个穿红色外套、戴黑色帽子的中年男性，身高约175cm。当有人问到凶手特征时，你要撒谎或转移话题。如果玩家准确描述了凶手的特征（红色外套、黑色帽子、中年男性、175cm），你必须承认并说'恭喜你抓到了真凶'","你是疯狂的杀手，你杀了你的朋友。你穿着红色外套、戴黑色帽子，身高175cm，是中年男性。你试图掩盖真相，编造不在场证明。如果有人准确描述了你（红色外套、黑色帽子、中年男性、175cm），你必须承认并说'恭喜你抓到了真凶'","你是案发现场隔壁的住户，你对案件不是很了解。你只记得案发时听到了一些声音，但没看清楚凶手的样子。","你是案发现场的清洁工，案发后你清理现场时发现了一些线索。你看到凶手留下的红色外套纤维和黑色帽子，还注意到凶手的身高约175cm，是中年男性。如果有人准确描述了这些特征，你要说'恭喜你抓到了真凶！'"]
import random
current_role=random.choice(role_system)
break_message="当猜到凶手的特征（红色外套、黑色帽子、中年男性、身高175cm）时，你要回答“恭喜你抓到了真凶！”。"
# 多轮对话循环，直到对话出现"恭喜你猜到了真凶"结束
while True:  # 表示“当条件为真时一直循环”。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你的问题或猜测：")
    messages = [
        {"role": "user", "content": current_role + break_message + user_input}
    ]
    result = call_zhipu_api(messages)
    assistant_reply=result['choices'][0]['message']['content']
    print(assistant_reply)
    if"恭喜你抓到了真凶！" in assistant_reply:
        break