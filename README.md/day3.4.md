总结 `glm4.py` 中用到的 Python 知识：


[1 tool called]


`glm4.py` 中运用的 Python 知识总结：

## Python 知识总结（`glm4.py`）

### 一、模块导入

#### 1. **标准模块导入**
```1:2:glm4.py
import requests
import json
```
- `import` 导入整个模块
- `requests`：HTTP 请求库
- `json`：JSON 数据处理模块

#### 2. **从模块导入特定函数**
```4:4:glm4.py
from requests.utils import stream_decode_response_unicode
```
- `from ... import ...` 导入特定对象
- 导入模块中的特定函数或类

#### 3. **从自定义模块导入**
```6:6:glm4.py
from glm import role_system
```
- 从本地模块导入变量
- 注意：第31行重新定义了 `role_system`，覆盖了导入的值

---

### 二、函数定义

#### 4. **函数定义与默认参数**
```8:8:glm4.py
def call_zhipu_api(messages, model="glm-4-flash"):
```
- `def` 定义函数
- 必需参数：`messages`
- 默认参数：`model="glm-4-flash"`
- 浮点数默认值：`temperature: 0.5`

---

### 三、数据结构

#### 5. **字典 (Dictionary)**
```11:14:glm4.py
headers = {
    "Authorization": "85556a78acba4b4eb7a5130fa9139580.uMmcFvwz4LGabgRQ",
    "Content-Type": "application/json"
}
```

```16:20:glm4.py
data = {
    "model": model,
    "messages": messages,
    "temperature": 0.5   
}
```
- 使用 `{}` 创建字典
- 键值对结构
- 值可以是字符串、变量、数字

#### 6. **列表 (List) 与嵌套结构**
```36:38:glm4.py
messages = [
    {"role": "user", "content": role_system + user_input}
]
```
- 使用 `[]` 创建列表
- 列表包含字典
- 嵌套数据结构

---

### 四、控制流语句

#### 7. **while 循环**
```34:43:glm4.py
while True:  # 表示"当条件为真时一直循环"。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你要说的话")
    messages = [
        {"role": "user", "content": role_system + user_input}
    ]
    result = call_zhipu_api(messages)
    assistant_reply=result['choices'][0]['message']['content']
    print(assistant_reply)
    if"再见" in assistant_reply:
        break
```
- `while True:` 无限循环
- 使用 `break` 跳出循环

#### 8. **条件语句 (if)**
```24:27:glm4.py
if response.status_code == 200:
    return response.json()
else:
    raise Exception(f"API调用失败: {response.status_code}, {response.text}")
```

```42:43:glm4.py
if"再见" in assistant_reply:
    break
```
- `if...else` 条件判断
- `==` 比较运算符
- `in` 成员运算符（检查字符串是否包含子串）

---

### 五、字符串操作

#### 9. **字符串拼接**
```37:37:glm4.py
{"role": "user", "content": role_system + user_input}
```
- 使用 `+` 拼接字符串
- 变量与变量拼接

#### 10. **字符串成员检查**
```42:42:glm4.py
if"再见" in assistant_reply:
```
- `in` 运算符检查子串
- 返回布尔值

---

### 六、输入输出

#### 11. **input() 函数**
```35:35:glm4.py
user_input = input("请输入你要说的话")
```
- 从控制台读取用户输入
- 返回字符串类型
- 显示提示信息

#### 12. **print() 函数**
```41:41:glm4.py
print(assistant_reply)
```
- 输出内容到控制台
- 可输出变量值

---

### 七、函数调用与返回值

#### 13. **函数调用**
```22:22:glm4.py
response = requests.post(url, headers=headers, json=data)
```

```39:39:glm4.py
result = call_zhipu_api(messages)
```
- 调用模块函数：`requests.post()`
- 调用自定义函数：`call_zhipu_api()`
- 使用关键字参数

#### 14. **return 语句**
```25:25:glm4.py
return response.json()
```
- 函数返回值
- 返回字典类型（JSON 转换结果）

---

### 八、异常处理

#### 15. **异常抛出**
```27:27:glm4.py
raise Exception(f"API调用失败: {response.status_code}, {response.text}")
```
- `raise` 抛出异常
- `Exception` 异常类
- 用于错误处理

---

### 九、字符串格式化

#### 16. **f-string 格式化**
```27:27:glm4.py
raise Exception(f"API调用失败: {response.status_code}, {response.text}")
```
- `f"..."` 格式化字符串
- 使用 `{变量名}` 嵌入变量

---

### 十、数据访问

#### 17. **字典和列表的访问**
```40:40:glm4.py
assistant_reply=result['choices'][0]['message']['content']
```
- 字典访问：`dict['key']`
- 列表访问：`list[index]`
- 链式访问：`result['choices'][0]['message']['content']`

#### 18. **对象方法调用**
```25:25:glm4.py
return response.json()
```
- 对象方法调用：`response.json()`
- 将响应对象转换为 JSON 字典

---

### 十一、变量赋值

#### 19. **变量赋值**
```31:32:glm4.py
role_system="你所有的回答都要扮演一个疯狂的小丑"
break_message="当我对你表达结束对话的意图时，你只回复"再见"，不要有任何其他的回答"
```

```35:35:glm4.py
user_input = input("请输入你要说的话")
```
- 使用 `=` 赋值
- 字符串变量赋值
- 从函数返回值赋值

---

### 十二、注释

#### 20. **单行注释**
```30:30:glm4.py
# 使用示例
```

```33:33:glm4.py
# 多轮对话循环，直到用户输入 '再见' 结束
```

```34:34:glm4.py
while True:  # 表示"当条件为真时一直循环"。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
```
- `#` 单行注释
- 行内注释
- 用于代码说明

---

### 十三、流程控制

#### 21. **break 语句**
```43:43:glm4.py
break
```
- 跳出循环
- 与 `while` 循环配合使用

---

## 知识点分类

### 基础级别
1. 变量赋值
2. 字符串类型与操作
3. print() 和 input() 函数
4. 单行注释

### 中级级别
5. 模块导入（标准导入、from...import）
6. 函数定义与调用
7. 字典和列表
8. while 循环
9. if 条件语句
10. 字符串拼接
11. break 语句
12. 嵌套数据结构访问

### 高级级别
13. 无限循环 (`while True`)
14. 成员运算符 (`in`)
15. 异常处理
16. f-string 格式化
17. API 调用
18. 复杂数据结构链式访问

---

## 新增知识点（相比 `glm.py`）

1. while 循环 — 实现多轮对话
2. input() 函数 — 获取用户输入
3. break 语句 — 跳出循环
4. in 运算符 — 字符串成员检查
5. from...import — 特定导入
6. 无限循环模式 — `while True` 配合 `break`

---

## 实际应用场景

- 交互式对话程序：使用 `while True` 实现持续对话
- 用户输入处理：使用 `input()` 获取用户输入
- 条件退出：使用 `in` 检查关键词，用 `break` 退出循环
- API 调用：封装函数调用 API 并处理响应

这些知识点展示了 Python 在交互式应用开发中的常用技术。