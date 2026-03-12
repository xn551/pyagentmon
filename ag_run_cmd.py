import subprocess
import os
import ollama

MODEL = "gpt-oss:20b"

system_prompt = """
你是一个可以调用windows系统命令的AI Agent，严格按照JSON格式返回结果,不要给出任何解释
输出格式为{"action": "run_cmd", "cmd": "["命令","参数1","参数2",...]"}

"""

def bot_exe_cmd(cmd_list):
    try:
        #userprofile = os.environ['USERPROFILE']
        #wt_path = f"{userprofile}\\AppData\\Local\\Microsoft\\WindowsApps\\wt.exe"
        result = subprocess.run(["powershell", "/c"]+ cmd_list,capture_output=True, text=True)
        
        return result.stdout if result.returncode == 0 else result.stderr
                       
    except Exception as e:
        return str(e)


def q1a1(q,SYSTEM_PROMPT=system_prompt):

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

import json
def get_json(json_text):
    try:
        
        data = json.loads(json_text)
        action = data.get('action')
        cmd    = data.get('cmd')
        print(action)
        print(cmd)
        if action == "run_cmd":
            return cmd
        else:
            print(acition, " is not expeted action")
            return 0
    
    except json.JSONDecodeError as exc:
        # 仅打印错误信息，保持简洁
        print(exc)
        return 0

q="使用powershell命令列出文件夹所有文件"

def agent_run_cmd(prompt=q):
    a = q1a1(q)
    cmd_list = get_json(a)
    result = bot_exe_cmd(cmd_list)
    print(result)

if __name__ == "__main__":
    q = input("Master：")
    agent_run_cmd(prompt=q)
