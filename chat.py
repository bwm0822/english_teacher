import modules.llm as llm
import modules.recognise as sr
# from modules.speech import text_to_speech
import re
import msvcrt
import winsound
from modules.utility import speech

WAIT_TIME = 10  # 等待時間（秒）

# 顏色名稱	ANSI碼	範例
# 黑色 Black	\033[30m	🖤
# 紅色 Red	    \033[31m	❤️
# 綠色 Green	\033[32m	💚
# 黃色 Yellow	\033[33m	💛
# 藍色 Blue	    \033[34m	💙
# 紫色 Magenta	\033[35m	💜
# 青色 Cyan	    \033[36m	💠
# 白色 White	\033[37m	🤍

def wait_input():
    # 等待使用者輸入
    while True:
        if msvcrt.kbhit():  #是檢查是否有按鍵
            msvcrt.getch()  # 清除一個已被按下的按鍵
            break

def beepRec():
    winsound.Beep(500, 150)  # 頻率500Hz，持續150毫秒

def beepStop():
    winsound.Beep(800, 300)  # 頻率300Hz，持續300毫秒

def msg(message):
    print(message)
    speech(message)

def clear_all_keypresses():
    # 把所有按過但還沒讀取的鍵都清掉
    while msvcrt.kbhit():   #是檢查是否有按鍵
        msvcrt.getch()

def clear_screen():
    # 清除螢幕
    print("\033[H\033[J", end='')

def you():
    clear_all_keypresses()
    print("\n\033[32mYou\033[0m(按[Enter]):",end='',flush=True)
    # wait_input()
    user_input = input()
    beepRec()
    text = sr.record(WAIT_TIME)
    user_input += '' if text is None else text
    beepStop()
    print(user_input)
    return user_input

# def teacher(message):
#     print("\n\033[31mTeacher:\033[0m")
#     sentences = re.split(r"([,.\n])", message)
#     final_sentences = []
#     for i in range(0, len(sentences)-1, 2):
#         final_sentences.append(sentences[i] + sentences[i+1])  # 句子+標點

#     # 如果最後一個沒標點也補上
#     if len(sentences) % 2 != 0:
#         final_sentences.append(sentences[-1])

#     for s in final_sentences:
#         if msvcrt.kbhit():  #是檢查是否有按鍵
#             msvcrt.getch()  # 清除一個已被按下的按鍵
#             break
#         print(s,end='',flush=True)
#         speech(s)

#     print('\n') # 換行


def teacher(message):
    clear_all_keypresses()
    print("\n\033[31mTeacher:\033[0m")
    print(message)
    speech(message)
    print('\n') # 換行


def main():

    while True:
        clear_screen()
        if llm.choose_prompt() is False:
            return
        
        print("\n\033[33m[ say 'goodbye' to end the conversation ]\033[0m")
        response = llm.chat_init()
        teacher(response)
        while True:
            user_input = you()
            if user_input == 'goodbye':
                print("\n\033[31mTeacher:\033[0m")
                msg("bye！see you next time")
                break
            response = llm.chat(user_input)
            teacher(response)

def unit_test():
    test = '[中文測試]'





main()
