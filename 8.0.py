import requests
import json
import os  # 新增：用于文件操作

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "85556a78acba4b4eb7a5130fa9139580.uMmcFvwz4LGabgRQ",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.3   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# ========== 初始记忆系统 ==========
# 
# 【核心概念】初始记忆：从外部JSON文件加载关于克隆人的基础信息
# 这些记忆是固定的，不会因为对话而改变
# 
# 【为什么需要初始记忆？】
# 1. 让AI知道自己的身份和背景信息
# 2. 基于这些记忆进行个性化对话
# 3. 记忆文件可以手动编辑，随时更新

# 记忆文件夹路径
MEMORY_FOLDER = "memory_clonebot"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "四叶草": "四叶草_memory.json",
}

# ========== 初始记忆系统 ==========

# ========== 主程序 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        print(f"✓ 已加载角色 '{role_name}' 的记忆: {memory_file} ({len(data) if isinstance(data, list) else 1} 条记录)")
                    else:
                        memory_content = ""
            else:
                print(f"⚠ 记忆文件不存在: {memory_path}")
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}")
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
        "四叶草": """
        【人格特征】
         情绪性	高频使用语气词、表情符号、语音消息	情绪外放，敏感，容易焦虑或兴奋
         共情力	频繁关注他人状态（“你晚饭吃了吗”“她来了吗”）	在意他人感受，具备较强的人际敏感度
         冲动性	话题切换极快，从摄影课跳到空调品牌再到食堂选择	思维跳跃，可能属于“发散型”人格，注意力容易转移
         依赖性	多次请求对方带东西、接人、确认位置	对亲密关系有依赖感，习惯“被照顾”或“被回应”
         完美主义倾向	对摄影课性价比的反复权衡、对食堂选择的纠结	内心有标准，容易陷入“选择焦虑”

        【语言风格】
         碎片化	“才六十”“还是教学生”“感觉扣了一半的钱至少”	像思维速写，不追求完整句式，更接近“脑内语音”
         口语化到极致	“我想拉屎”“不敢。。”	毫无修饰，甚至带有“生理性”表达，真实到近乎“裸露”
         情绪标点	“[发呆]”“[可怜][可怜]”“卧槽。”	用表情符号或语气词代替情绪描述，形成“视觉化情绪”
         跳跃式关联	从“摄影课”跳到“空调品牌”再跳到“食堂一楼二楼”	思维像短视频滑动，没有过渡，但内在有“场景触发”逻辑
         语音依赖	多次“[语音]”	可能觉得文字无法承载语气，或懒得打字，倾向“面对面感”

        【说话习惯】
         “预设对方在场”	大量省略主语/语境（“你坐哪啊”“来了”）	默认对方“懂我”，关系亲密到无需解释
         “边想边说”	“我思考一下”“我感觉…”	把思维过程外放，像直播自己的大脑
         “用食物表达情感”	“帮我带蜜雪冰城”“吃不吃食堂”	食物是安全感的替代品，也是亲密关系的“测试题”
         “用第三人称制造距离”	“她这两个小时才六十”“sjq和nx赖床上了”	对“外人”用第三人称，对“自己人”用第二人称，形成情感圈层
         回答简短，一句话会拆开讲




        """
            }
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
            role_prompt_parts.append(f"""【你的说话风格示例】
            以下是你说过的话，你必须模仿这种说话风格和语气：
            {memory_content}
            在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【角色选择】
# 定义AI的角色和性格特征
# 可以修改这里的角色名来选择不同的人物
# 【加载完整角色设定】
# roles() 函数会自动：
# 1. 加载该角色的外部记忆文件
# 2. 获取该角色的基础人格设定
# 3. 整合成一个完整的、结构化的角色 prompt
role_system = roles("四叶草")

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：
-
用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# 【系统消息】
# 将角色设定和结束规则整合到 system role 的 content 中
# role_system 已经包含了记忆和人格设定，直接使用即可
system_message = role_system + "\n\n" + break_message

# ========== 对话循环 ==========
# 
# 【重要说明】
# 1. 每次对话都是独立的，不保存任何对话历史
# 2. 只在当前程序运行期间，在内存中维护对话历史
# 3. 程序关闭后，所有对话记录都会丢失
# 4. AI的记忆完全基于初始记忆文件（life_memory.json）

try:
    # 初始化对话历史（只在内存中，不保存到文件）
    # 第一个消息是系统提示，包含初始记忆和角色设定
    conversation_history = [{"role": "system", "content": system_message}]
    
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    while True:
        # 【步骤1：获取用户输入】
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        # 【步骤2：检查是否结束对话】
        if user_input in ['再见']:
            print("对话结束")
            break
        
        # 【步骤3：将用户输入添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "user", "content": user_input})
        
        # 【步骤4：调用API获取AI回复】
        # 传入完整的对话历史，让AI在当前对话中保持上下文
        # 注意：这些历史只在本次程序运行中有效，不会保存
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        
        # 【步骤5：将AI回复添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # 【步骤6：显示AI回复】
        # 生成Ascii头像：https://www.ascii-art-generator.org/
        portrait = """
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWMWWWWWWWWWWNNNNWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWNXK00000000KKKKXNWNNWWWWWWWWWWWW
WWWWWWWWWWWWWWWNKOxxxxxxxdxxxxOOOO0KKKKXNWWWWWWWWW
WWWWWWWWWWWWNXKOkxxxxo:,'.,c:;colldkkk0XNWWWWNNNNN
WWWWWWWWWWNX0Okkxxoc;'.....,;,;:,',:dk0XNWWWWWWWWW
WWWWWWWWNNNKOxdol:,'''',,,,,;,;;;;;;lkKXWWWWWWWWWW
WWWWWWWNNNNKOdc,','',,'';:::::::;;::ckXWWWWWWWWWWW
WWWWWWWWWNNX0d;'''',,,,;;;:::::::;:ccdKWWWWWWWWWWW
WWNNNNNWNNNXXk;',;;;;;,;;;;:cccllcc:::dXWNNNNNNNXX
NNWNNNWNWNNNNd,',;:;;;:clodkO0000OOxl;cOXKKKKKKK00
XXXXXKKKKKKX0c,;;;,;;:loddxkOO000Okxo;l0KKKKKKKKKK
00KKKKKK00KKOl,,,.,:'.....',;:cdkdl:,;xKXXXXKXXKKK
KKKKKKKXXKXXXOc;::cdd:..      .,l;. .oKXXXXXXXXXXX
XXXXXXXXXXXXXXKOxoodkkko:,'..';dko;:xKXXNNXNNXXXXX
XXXXXXXXXXXXK0KkoloddxO0000kkkOO0OkO0KKK0000KK0000
KKKKKKKXKKKx;.'..;lloxkkOOkkOOOOOkxk0000OOO0000OOO
0K000KK00x:.     .:lcldxxkxxxxdddxO0000KK0OO0000OO
000Okdl;...       ,oolccoddxxxddxOKKKKKK000O000OO0
xoc,..            .,dxdolllllc:lOKKKKKXXKXXXXXXXXX
..                  'ddloodl'  .':cxO0KKXXXXXXXXXX
                    .';;,','..   .',:xKK0KKXXXXXXX
                       ......     .. 'kXKKXXNNXXXX
                 .     ';;:c:.       .lXXXXXXXXXXX
          ..   ..      'oOOOd'        .xXXXXXXXXXX
    ..... ..      ..    'cdOk:.        ,OXXXXXXXXX
           ...    ...     ,xOl.        .:0XXXXXXXX
        ..   ..    ..      'dx,     .   .oKXXXXXXX
      .....         .       .c'     .    .l0XXXXXX
    ..........           .                .;kXXXXX
   ... ..........                           ,OXXXX
       ...............                      'kXKXX
         .....   ....                       'kXKKK
        ....     ..                         .,o0KK
         ..                                   .dKK
                                               :OO
                  ..                           ,dd
                 .;;.                          ,oo
        """
        print(portrait + "\n" + assistant_reply)
        
        # 【步骤7：检查AI回复是否表示结束】
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    # 用户按 Ctrl+C 中断程序
    print("\n\n程序被用户中断")
except Exception as e:
    # 其他异常（API调用失败、网络错误等）
    print(f"\n\n发生错误: {e}")
    