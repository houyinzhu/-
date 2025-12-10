<<<<<<< HEAD
def should_exit_by_user(user_input):
    """判断用户是否想要结束对话，返回 True/False"""
    return user_input in ['再见']

def should_exit_by_ai(ai_reply):
    """判断AI的回复是否表示要结束对话，返回 True/False"""
    reply_cleaned = ai_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
=======
<<<<<<< HEAD
def should_exit_by_user(user_input):
    """判断用户是否想要结束对话，返回 True/False"""
    return user_input in ['再见']

def should_exit_by_ai(ai_reply):
    """判断AI的回复是否表示要结束对话，返回 True/False"""
    reply_cleaned = ai_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
=======
def should_exit_by_user(user_input):
    """判断用户是否想要结束对话，返回 True/False"""
    return user_input in ['再见']

def should_exit_by_ai(ai_reply):
    """判断AI的回复是否表示要结束对话，返回 True/False"""
    reply_cleaned = ai_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
>>>>>>> 43e52124ec759fb33752b4cf0978dd5c59ab6862
>>>>>>> 7d9d9ec32f63a2a65ed81c345f4622f896367003
    return reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned)