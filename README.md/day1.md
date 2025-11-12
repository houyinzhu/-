两个文件中运用的 Python 知识总结：

## Python 知识总结

### 一、基础语法 (`101.py`)

#### 1. **变量赋值**
```1:2:101.py
x="1"
y="2"
```
- 动态类型，无需声明类型
- 使用 `=` 进行赋值

#### 2. **字符串类型**
- 使用引号（单引号或双引号）定义字符串
- `"1"` 和 `"2"` 是字符串类型，不是数字

#### 3. **字符串拼接操作**
```3:3:101.py
print(x+y)
```
- `+` 运算符用于字符串拼接
- 结果：`"12"`（字符串拼接，不是数字相加）

#### 4. **print() 函数**
- 用于输出内容到控制台
- 可以输出变量、表达式的结果

---

### 二、进阶语法 (`glm.py`)

#### 5. **模块导入**
```1:2:glm.py
import requests
import json
```
- `import` 语句导入外部模块
- `requests`：HTTP 请求库
- `json`：JSON 数据处理模块

#### 6. **函数定义**
```4:4:glm.py
def call_zhipu_api(messages, model="glm-4-flash"):
```
- `def` 关键字定义函数
- 必需参数：`messages`
- 默认参数：`model="glm-4-flash"`（有默认值）

#### 7. **字典 (Dictionary) 数据结构**
```7:10:glm.py
headers = {
    "Authorization": "85556a78acba4b4eb7a5130fa9139580.uMmcFvwz4LGabgRQ",
    "Content-Type": "application/json"
}
```

```12:16:glm.py
data = {
    "model": model,
    "messages": messages,
    "temperature": 1.0
}
```
- 使用 `{}` 创建字典
- 键值对结构：`"key": value`
- 值可以是字符串、数字、变量、列表等

#### 8. **列表 (List) 数据结构**
```26:28:glm.py
messages = [
    {"role": "user", "content": "你好，请介绍一下自己"}
]
```
- 使用 `[]` 创建列表
- 列表中可以包含字典
- 有序、可变的数据结构

#### 9. **嵌套数据结构**
- 列表包含字典：`[{...}]`
- 字典值可以是列表或其他字典

#### 10. **函数调用**
```18:18:glm.py
response = requests.post(url, headers=headers, json=data)
```

```30:30:glm.py
result = call_zhipu_api(messages)
```
- 调用模块函数：`requests.post()`
- 调用自定义函数：`call_zhipu_api()`
- 使用关键字参数传递参数

#### 11. **关键字参数**
- 使用参数名传递：`headers=headers`, `json=data`
- 提高代码可读性

#### 12. **条件语句 (if-else)**
```20:23:glm.py
if response.status_code == 200:
    return response.json()
else:
    raise Exception(f"API调用失败: {response.status_code}, {response.text}")
```
- `if...else` 条件判断
- `==` 比较运算符
- 根据条件执行不同代码块

#### 13. **return 语句**
```21:21:glm.py
return response.json()
```
- 函数返回值
- 可以返回任意数据类型

#### 14. **异常处理**
```23:23:glm.py
raise Exception(f"API调用失败: {response.status_code}, {response.text}")
```
- `raise` 关键字抛出异常
- `Exception` 异常类
- 用于错误处理和程序控制

#### 15. **f-string 字符串格式化**
```23:23:glm.py
raise Exception(f"API调用失败: {response.status_code}, {response.text}")
```
- `f"..."` 格式化字符串
- 使用 `{变量名}` 在字符串中嵌入变量值

#### 16. **字典和列表的访问**
```31:31:glm.py
print(result['choices'][0]['message']['content'])
```
- 字典访问：`dict['key']`
- 列表访问：`list[index]`
- 链式访问：`result['choices'][0]['message']['content']`

#### 17. **对象方法调用**
```21:21:glm.py
return response.json()
```
- 对象方法调用：`response.json()`
- 将响应对象转换为 JSON 格式

#### 18. **注释**
```25:25:glm.py
# 使用示例
```
- `#` 单行注释
- 用于代码说明

#### 19. **变量作用域**
- 函数参数：`messages`, `model`（局部变量）
- 函数内部变量：`url`, `headers`, `data`, `response`（局部变量）
- 全局变量：`messages`, `result`（在函数外部定义）

---

## 知识点分类

### 基础级别 (`101.py`)
1. 变量赋值
2. 字符串类型
3. 字符串拼接
4. print() 函数

### 中级级别 (`glm.py`)
5. 模块导入
6. 函数定义与调用
7. 字典和列表
8. 条件语句
9. 嵌套数据结构
10. 关键字参数
11. return 语句
12. 注释

### 高级级别 (`glm.py`)
13. 异常处理
14. f-string 格式化
15. API 调用（HTTP 请求）
16. 复杂数据结构操作
17. 对象方法调用

---

## 实际应用场景

- `101.py`：演示字符串基本操作
- `glm.py`：调用 API、处理 JSON、错误处理

这些知识点覆盖了 Python 从基础到中级的核心内容。