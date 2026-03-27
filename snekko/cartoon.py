import numpy as np
import cv2
import time
from PIL import Image, ImageDraw, ImageFont

import ollama
import os

from pathlib import Path

# 1️⃣ 获取当前模块文件所在目录
_module_dir = Path(__file__).parent  # Path('.../lib/cartoon')

from .model_name_set import Model_Name




def wrap_text(text, max_width=70):
    """
    自动换行：一行不超过 max_width 字符
    """
    lines = []
    current_line = ""
    
    for char in text:
        # 尝试加下一个字符
        if len(current_line + char) > max_width:
            # 超过宽度 → 先保存当前行
            lines.append(current_line)
            current_line = char  # 新行从当前字符开始
        else:
            current_line += char
    
    # 最后一行
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)
    


def role_speak(photo = _module_dir / "feibi.jpg", role_class="Ruler", text = "我是Ruler，准备召唤planer完成任务", photo_pos = [100, 80], dialog_box_pos = [350,80],  dialog_box_size = [600,180],font_size = 16 ):
    #photo = "feibi.jpg"

    photo = str(photo)
    photo_size = [220,180]
    
    photo_win_name = role_class
    
    dialog_box_color = [255,255,255]
    

    text_color = (255, 0, 0)  # RGB格式（红色）
    dialog_box_win_name = role_class + " say:"



    image = cv2.imread(photo)
    cv2.namedWindow(photo_win_name, cv2.WINDOW_NORMAL) 
    cv2.resizeWindow(photo_win_name, photo_size[0], photo_size[1])
    cv2.moveWindow(photo_win_name, photo_pos[0],photo_pos[1])
    cv2.imshow(photo_win_name, image)
    cv2.waitKey(1)


    # 对话框背景
    image_txt = 255*np.ones((dialog_box_size[1], dialog_box_size[0], 3), dtype=np.uint8)
    image_txt[:,:,0] =dialog_box_color[0] 
    image_txt[:,:,1] =dialog_box_color[1] 
    image_txt[:,:,2] =dialog_box_color[2] 

    # 使用pillow的复杂方法
    img_txt_pil = Image.fromarray(cv2.cvtColor(image_txt, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(img_txt_pil)

    font_path = "simhei.ttf"  # 替换为你的中文字体文件（如黑体、微软雅黑）

    font = ImageFont.truetype(font_path, font_size)

    position = (50, 50)  # (x, y)

    draw.text(position, text, font=font, fill=text_color)

    # 6. 将Pillow图像转回OpenCV格式
    img_txt_cv2 = cv2.cvtColor(np.array(img_txt_pil), cv2.COLOR_RGB2BGR)



    # 4. 显示图片
    cv2.namedWindow(dialog_box_win_name, cv2.WINDOW_NORMAL) 
    cv2.resizeWindow(dialog_box_win_name, dialog_box_size[0], dialog_box_size[1])
    cv2.moveWindow(dialog_box_win_name, dialog_box_pos[0], dialog_box_pos[1])

    cv2.imshow(dialog_box_win_name, img_txt_cv2)
    cv2.waitKey(1)  
    

def split_text_by_lines(text, n):
    lines = text.split('\n')
    m = len(lines)
    return ['\n'.join(lines[i*n : (i+1)*n]) for i in range((m + n - 1) // n)]


def build_chat_box(text, dialog_box_size,dialog_box_color = [255,255,255],font_size=16,text_color = (255, 0, 0)):
    # dialog background
    image_txt = 255*np.ones((dialog_box_size[1], dialog_box_size[0], 3), dtype=np.uint8)
    image_txt[:,:,0] =dialog_box_color[0] 
    image_txt[:,:,1] =dialog_box_color[1] 
    image_txt[:,:,2] =dialog_box_color[2] 

    # with pillow to add the text on background
    img_txt_pil = Image.fromarray(cv2.cvtColor(image_txt, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_txt_pil)
    font_path = "simhei.ttf"  # 
    font = ImageFont.truetype(font_path, font_size)

    position = (20, 20)  # (x, y)
    draw.text(position, text, font=font, fill=text_color)
    img_txt_cv2 = cv2.cvtColor(np.array(img_txt_pil), cv2.COLOR_RGB2BGR)

    return img_txt_cv2


def role_speak_long(photo = "feibi.jpg", role_class="Ruler", text = "我是Ruler，准备召唤planer完成任务", photo_pos = [100, 80], dialog_box_pos = [350,80],  dialog_box_size = [600,180],font_size = 16 ):
    #photo = "feibi.jpg"

    photo = str(photo)
    photo_size = [220,180]
    
    photo_win_name = role_class
    
    
    

      # RGB格式（红色）
    dialog_box_win_name = role_class + " say:"



    image = cv2.imread(photo)
    cv2.namedWindow(photo_win_name, cv2.WINDOW_NORMAL) 
    cv2.resizeWindow(photo_win_name, photo_size[0], photo_size[1])
    cv2.moveWindow(photo_win_name, photo_pos[0],photo_pos[1])
    cv2.imshow(photo_win_name, image)
    cv2.waitKey(1)

    n_col = 11
    split_text_list = split_text_by_lines(text, n_col)

    chat_box_list = []
    for i in range(len(split_text_list)):
        chat_box_list.append(build_chat_box(split_text_list[i], dialog_box_size))

    #for i in range(len(split_text_list)):
    #    print(chat_box_list[i])



    # 4. 显示图片
    cv2.namedWindow(dialog_box_win_name, cv2.WINDOW_NORMAL) 
    cv2.resizeWindow(dialog_box_win_name, dialog_box_size[0], dialog_box_size[1])
    cv2.moveWindow(dialog_box_win_name, dialog_box_pos[0], dialog_box_pos[1])

    
    cv2.imshow(dialog_box_win_name, chat_box_list[0])
    cv2.waitKey(1)  

    return chat_box_list

def getch_windows():
    import msvcrt
    # msvcrt.getch() 返回一个字节，需 decode 成 str
    return msvcrt.getch().decode(errors='ignore')



import datetime

def log_conversation(log_file_path, message):
    """
    将对话记录追加到日志文件中，并包含时间戳。

    Args:
        log_file_path: 日志文件的路径。
        role: 说话者的角色 (例如 "user", "assistant")。
        message: 消息内容。
    """
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间戳
    log_entry = f"{timestamp}:\n  {message}\n"

    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"写入日志文件时发生错误: {e}")


log_file = "agent_log.txt"

system_prompt = '''你好，你是我正在开发的卡通智能体PyAgentMon哦，我正在测试你的功能呢。PyAgentMon，是一款完全由python开发的LLM agent，
他像宝可梦一样由人类训练自己的Agent，我们的目标是成为PyAgentMon大师。你的头像和对话，以及活动画面都是通过opencv实现的
并且我们像openclaw的最新版本一样，原生支持ContextEngine，是不是非常棒。

'''
def cv_wait_for_turn_page(agent_class,chat_boxes):

    note = "o向下翻页，l向上翻页，n继续下一轮对话"

    print(note)

    show_text_num = 0

    while True:
            

        cv2.imshow(agent_class + " say:", chat_boxes[show_text_num])
        k = cv2.waitKey(1)

        key = getch_windows()

        if key == 'o':
            #print("You pressed the letter 'o'!")
            show_text_num += 1
            show_text_num = show_text_num % len(chat_boxes)
            print(note, f"Total page {len(chat_boxes)}, page num:", show_text_num)   
                
        if key == 'l':
            #print("You pressed the letter 'l'!")
            show_text_num -= 1
            show_text_num = show_text_num % len(chat_boxes)
            print(note, f"Total page {len(chat_boxes)}", show_text_num)
        if key == 'n':
            #print("You pressed the letter 'n'!")
            break

    print("\nfinished one chat loop")  

def master_speak(q_text):
    role_speak(photo = _module_dir / "feibi.jpg", role_class="Master",text = wrap_text(q_text, 60),photo_pos = [50, 10], dialog_box_pos = [350,10],  dialog_box_size = [800,180])

def servant_speak(a_text):
    role_speak(photo = _module_dir / "shenli.jpg", role_class="Servant", text = wrap_text(a_text, 60), photo_pos = [950, 230], dialog_box_pos = [50,230],dialog_box_size = [850,260])
        



def main(model_name="gemma3:12b"):
    # clear the cmd
    os.system("cls") 
        
    messages = [{"role": "system", "content": system_prompt}]
    
    while True:
        # prepare the input text
        ask_text = input("Master：")
        if ask_text in ["exit", "quit"]:
            break            
        messages.append({"role": "user", "content": ask_text})
        
        # close the cartoon for last chat
        cv2.destroyAllWindows()
        
        
        # display the ask cartoon
        role_speak(photo = _module_dir / "feibi.jpg", role_class="Master",text = wrap_text(ask_text, 65),photo_pos = [50, 10], dialog_box_pos = [350,10],  dialog_box_size = [800,180])

        #call the ollama model to get the answer
        res = ollama.chat(model=model_name, messages=messages)       
        answer_text = res["message"]["content"]
        
        # wrap the answer text
        answer_text_wrap = wrap_text(answer_text)
        
        print("AI：", answer_text)
        messages.append({"role": "assistant", "content": answer_text})
        
        # display the answer cartoon

        agent_class = "Servant"

        note = "o向下翻页，l向上翻页，n继续下一轮对话"
        chat_boxes = role_speak_long(photo = _module_dir / "shenli.jpg", role_class=agent_class, text = answer_text_wrap, photo_pos = [950, 230], dialog_box_pos = [50,230],dialog_box_size = [850,260])
        show_text_num = 0

        print(note)

        log_conversation(log_file, messages)

        while True:
            

            cv2.imshow(agent_class + " say:", chat_boxes[show_text_num])
            k = cv2.waitKey(1)

            key = getch_windows()

            if key == 'o':
                #print("You pressed the letter 'o'!")
                show_text_num += 1
                show_text_num = show_text_num % len(chat_boxes)
                print(note, f"Total page {len(chat_boxes)}, page num:", show_text_num)   
                  
            if key == 'l':
                #print("You pressed the letter 'l'!")
                show_text_num -= 1
                show_text_num = show_text_num % len(chat_boxes)
                print(note, f"Total page {len(chat_boxes)}", show_text_num)
            if key == 'n':
                #print("You pressed the letter 'n'!")
                break

        print("\nfinished one chat loop")    
'''
            if k == ord('o'):
                show_text_num += 1
                show_text_num = show_text_num % len(chat_boxes)
                print("response page num:", show_text_num)                

            if k == ord('l'):
                show_text_num -= 1
                show_text_num = show_text_num % len(chat_boxes)
                print("response page num:", show_text_num)
                
            if k == ord('n'):
                break

'''

        
            
        
    
if __name__ == "__main__":
    main(model_name = Model_Name)
    
    