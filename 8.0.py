import streamlit as st
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

# 【结束对话规则】
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# ========== Streamlit Web 界面 ==========
st.set_page_config(
    page_title="AI角色扮演聊天",
    page_icon="🎭",
    layout="wide"
)

# 初始化 session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "人质"
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# 页面标题
st.title("🎭 AI角色扮演聊天")
st.markdown("---")

# 侧边栏：角色选择和设置
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 角色选择
    selected_role = st.selectbox(
        "选择角色",
        ["小丑", "人质"],
        index=0 if st.session_state.selected_role == "小丑" else 1
    )
    
    # 如果角色改变，重新初始化对话
    if selected_role != st.session_state.selected_role:
        st.session_state.selected_role = selected_role
        st.session_state.initialized = False
        st.session_state.conversation_history = []
        st.rerun()
    
    # 清空对话按钮
    if st.button("🔄 清空对话"):
        st.session_state.conversation_history = []
        st.session_state.initialized = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 说明")
    st.info(
        "- 选择角色后开始对话\n"
        "- 对话记录不会保存\n"
        "- AI的记忆基于初始记忆文件"
    )

# 初始化对话历史（首次加载或角色切换时）
if not st.session_state.initialized:
    role_system = roles(st.session_state.selected_role)
    system_message = role_system + "\n\n" + break_message
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]
    st.session_state.initialized = True

# 显示对话历史
st.subheader(f"💬 与 {st.session_state.selected_role} 的对话")

# 显示角色头像（在聊天窗口上方）
st.code(get_portrait(), language=None)
st.markdown("---")  # 分隔线
