# 第一版本就不用卡通动画了
'''
1.prompt,普通对话，生成通用使用文档

2.prompt, agent，把上文内容生成函数文档

3.input输入确认后，交给bot自动执行，读取返回结果

4. agent判断运行是否正常，如果不正常是否给出结论

'''

import subprocess
import os
import ollama
import time
import cv2
Model = "gpt-oss:20b"
#Model = "gemma3:27b"
#Model = "deepseek-r1:1.5b"




from snekko import cartoon

def q1a1_re_msg(q,messages=[],model=Model):

    print(f"Used model:{model}")

    OPTIONS = {
        "temperature": 0.7,
        "num_ctx": 4096,
        "top_p": 0.9,
        "max_tokens": 1024
    }


    print("using options")
    print(OPTIONS)

    

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

    return ai_response,messages

def bot_create_file(text="",action="create_txt_file"):
    """
    1️⃣ 先检查元数据是否包含 # ACTION: create_txt_file
    2️⃣ 取出 # FILE: 后面的文件名
    3️⃣ 取出 # CODE: 之后的所有行作为 Python 代码
    4️⃣ 写入磁盘
    """
    meta = {}
    code_lines = []
    in_code = False

    for line in text.splitlines():
        if line.startswith("# ACTION:"):
            meta["action"] = line.split(":", 1)[1].strip()
        elif line.startswith("# FILE:"):
            meta["file"] = line.split(":", 1)[1].strip()
        elif line.startswith("# CODE:"):
            in_code = True
        elif in_code:
            code_lines.append(line)

    #stripe the ```python or ``` in the first line or end line.
    if "```" in code_lines[0]:
        code_lines = code_lines[1:]
    if "```" in code_lines[-1]:
        code_lines = code_lines[:-1]

    if meta.get("action") == action:
        with open(meta["file"], "w", encoding="utf-8") as fp:
            fp.write("\n".join(code_lines))
        print(f"✅ 代码已写入 {meta['file']}")
    else:
        print("❌ 未识别动作")

import json
def bot_get_json(json_text):
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

def bot_exe_cmd(cmd_list):
    try:
        #userprofile = os.environ['USERPROFILE']
        #wt_path = f"{userprofile}\\AppData\\Local\\Microsoft\\WindowsApps\\wt.exe"
        result = subprocess.run(["powershell", "/c"]+ cmd_list,capture_output=True, text=True)
        
        return result.stdout if result.returncode == 0 else result.stderr
                       
    except Exception as e:
        return str(e)
'''
def bot_stripe_json(a):
    if '```' in a[:a.find('\n')]:
        a = a[a.find('\n')+1:]
        print(a)
        
    for i in range(5):
        
        if "}" in a[a.rfind('\n')+1:]:
            return a
        else:
            a = a[:a.rfind('\n')]
            
                
    return(a)
'''
def bot_strip_json(a):
    for i in range(3):
        if '{' in a[:a.find('\n')]:
            break
        else:
            a = a[a.find('\n')+1:]
            #print(a)
        
    for i in range(3):
        
        if "}" in a[a.rfind('\n')+1:]:
            return a
        else:
            a = a[:a.rfind('\n')]
            
                
    return(a)






SYSTEM_PROMPT = "你是一个python实现的LLM agent程序"

makepy_prompt = '''你是一个代码生成agent，严格按照以下格式进行输出, 输出代码不使用Markdown格式
# ACTION: <action>
# FILE:   <filename>
# CODE:
<python‑/bash‑/… code>

'''

gen_cmd_prompt = """
你是一个可以调用windows系统命令的AI Agent，严格按照JSON格式返回结果,不要给出任何解释
输出格式为{"action": "run_cmd", "cmd": "["命令","参数1","参数2",...]"
"""
def stage_play_script(obj_str, file_name = "test_gem3.py", MODEL=Model):
    
    n_max = 10
    q_l = [None]*10
    a_l = [None]*10
    context_l = [None]*10
    i = 0
    
    
    SYSTEM_PROMPT = "你是一个python实现的LLM agent程序"
    context_l[i] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    print("stage 1-----wirte the code and explain-----------------------------------------\n")
 
    

    q_l[i] = obj_str
# gpt-oss的汉语里理解能力不如gemma3


    cartoon.master_speak("请按照需求生成代码和说明")
    cartoon.servant_speak("思考中")
    a_l[i],context_l[i+1] = q1a1_re_msg(q_l[i],context_l[i]);
    cartoon.servant_speak("代码和需求已经生成完毕");i += 1
    
    #stage 2-------------------------------------------------------
    print("stage 2-----------save the code into pyfile -----------------------------\n")
    q_l[i] = f"请把以上内容的python代码提取并保存到{file_name}中"   
    q_l[i] = q_l[i] + makepy_prompt + "\nACTION为:create_txt_file"
    
    cartoon.master_speak(q_l[i])
    cartoon.servant_speak("工作中")
    a_l[i],context_l[i+1] = q1a1_re_msg(q_l[i],context_l[i])
    cartoon.servant_speak("已经生成文档内容和保存指令");i += 1
    time.sleep(2)
    
    print(a_l[i-1])
    bot_create_file(text=a_l[i-1])

    #stage 3-------------------------------------------------------
    print("stage 3---------Generate the cmd-----------------------------------\n")
    #q_l[i] = "调用刚才生成的python函数，命令行参数为485_s.log"   # 命令行包含参数
    q_l[i] = "调用刚才生成的python函数"    #命令行不包含参数
    
    q_l[i] = q_l[i] + gen_cmd_prompt
    
    cartoon.master_speak(q_l[i])
    cartoon.servant_speak("工作中")
    a_l[i],context_l[i+1] = q1a1_re_msg(q_l[i],context_l[i]);
    cartoon.servant_speak(a_l[i]);i += 1
    time.sleep(2)

    print(a_l[i-1])
    

    cmd_json = bot_strip_json(a_l[i-1])
    print(cmd_json)    
    
    cartoon.master_speak(cmd_json)
    cmd_output = bot_get_json(cmd_json)
    cartoon.servant_speak(cmd_output)
    time.sleep(2)

    print(cmd_output)

    print("stage 4-----------confirm if execute the code----------------------------------\n")
    
    cartoon.master_speak("I can test the python file, y or n:")
    cartoon.servant_speak("waiting for answer,y or n");
    master_cmd = input("I can test the python file, y or n:")
    print(master_cmd)

    

    if "y" in master_cmd or "Y" in master_cmd:
        print("exe the cmd")
        a = bot_exe_cmd(cmd_output)
        print(a)
    
    else:
        print("unsupported cmd,finish")

    print("stage 5---debug one time------------------------------------------\n")

    q_l[i] = a + "\n以上内容是程序的运行结果，请判定是否按照目标正常运行。如果判定正常运行，输出<确认正常运行>；如果没有，输出<确认代码错误>，并指出代码存在的问题是什么" 
    cartoon.master_speak("以上内容是程序的运行结果，请判定是否按照目标正常运行。")
    cartoon.servant_speak("工作中")
    a_l[i],context_l[i+1] = q1a1_re_msg(q_l[i],context_l[i]);
    cartoon.servant_speak(a_l[i]);i += 1
    

    print("stage 6---judege the result or modify the code------------------------------------------\n")
    if '确认正常运行' in a_l[i-1]:
        print("代码调试正常")

    if '确认代码错误' in a_l[i-1]:
        q_l[i] = "按照你刚才的反馈修改程序，修改好的程序名称在原文件名后+debug"+ makepy_prompt + "\nACTION为:create_txt_file"
        cartoon.master_speak("以上内容是程序的运行结果，请判定是否按照目标正常运行。")
        cartoon.servant_speak("工作中")
        a_l[i],context_l[i+1] = q1a1_re_msg(q_l[i],context_l[i]);
        cartoon.servant_speak(a_l[i]);i += 1

        

    
    print("finish the stage.")
    cartoon.master_speak("finish the stage.")



'''
    while True:
                     
        k = cv2.waitKey(1)

        if k == ord('y'):
            print("exe the cmd")
            
            break            

        if k == ord('n'):
            
            print("do not run the code.")
            break
'''            

    
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Using the agent to write a python function, run the test and autodebug for 1 time.")
    parser.add_argument('-q', '--question', default="Hi, wirte a hello programe", help='Prompt, object of the function')
    parser.add_argument('-f', '--file', defatut="test.py",help='The direction you would like to save the function as py file.')
    parser.add_argument('-m', '--model', default="gpt-oss:20b", help='The utilized model's anme')
    args = parser.parse_args()

    stage_play_script(args.question, args.file, args.model)

