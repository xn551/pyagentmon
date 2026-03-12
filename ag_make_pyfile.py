import subprocess
import os
import ollama

MODEL = "gpt-oss:20b"

system_prompt = '''你是一个代码生成agent，严格按照以下格式进行输出, 输出代码不使用Markdown格式
# ACTION: <action>
# FILE:   <filename>
# CODE:
<python‑/bash‑/… code>

'''

print(system_prompt)

def q1a1(q,SYSTEM_PROMPT):

    OPTIONS = {
        "temperature": 0.7,
        "num_ctx": 4096,
        "top_p": 0.9,
        "max_tokens": 1024
    }


    print("using options")
    print(OPTIONS)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("prompt: "+q)

    messages.append({"role": "user", "content": q})

    res = ollama.chat(
        model=MODEL,
        messages=messages,
        options=OPTIONS
    )
    ai_response = res["message"]["content"]

    print("AI：", ai_response, "\n")
    messages.append({"role": "assistant", "content": ai_response})

    return ai_response

def write_from_agent(action="create_txt_file",txt=""):
    """
    1️⃣ 先检查元数据是否包含 # ACTION: create_txt_file
    2️⃣ 取出 # FILE: 后面的文件名
    3️⃣ 取出 # CODE: 之后的所有行作为 Python 代码
    4️⃣ 写入磁盘
    """
    meta = {}
    code_lines = []
    in_code = False

    for line in txt.splitlines():
        if line.startswith("# ACTION:"):
            meta["action"] = line.split(":", 1)[1].strip()
        elif line.startswith("# FILE:"):
            meta["file"] = line.split(":", 1)[1].strip()
        elif line.startswith("# CODE:"):
            in_code = True
        elif in_code:
            code_lines.append(line)

    if meta.get("action") == action:
        with open(meta["file"], "w", encoding="utf-8") as fp:
            fp.write("\n".join(code_lines))
        print(f"✅ 代码已写入 {meta['file']}")
    else:
        print("❌ 未识别动作")

q = '''请写一个python脚本，实现如下功能1.属于一个python文件 
2自动按照函数或类拆分，
3自动生成单元测试代码。支持python函数接口和命令行接口

输出参数为：
Action:create_python_file
File:split_test_py.py
'''
def agent_create_python_file(prompt=q):
    response = q1a1(q, system_prompt)
    print(response)
    write_from_agent("create_python_file",response)

if __name__ == "__main__":
    q = input("Master：")
    agent_create_python_file(prompt=q)

    


