
import re
import msvcrt
if __name__ == "__main__":
    from speech import text_to_speech
else:
    from modules.speech import text_to_speech


def split_mixed_text(text):
    # 修正過的正則規則：
    # - 數字單獨（如 123）
    # - 標點符號單獨（如 ,）
    # - 數字 + 英文 + 數字（如 444 This is a 123）
    # - 中文（如 書本）
    pattern = r'''
        ([\*\d]+)                 # 數字單獨（如 123）
        # |([\*\s]+)                   # 星號單獨（如 *）
        # | ([，。！？、,\.!?])       # 標點符號（如 ,）
        | ([a-zA-Z'\s]+[\d]+)        # 英文 + 數字（如 This is a 123）
        | ([a-zA-Z'\s]+)             # 英文（如 This is a ）
        # | ([\u4e00-\u9fff\s]+)         # 中文（如 書本）
    '''
    matches = re.findall(pattern, text, re.VERBOSE)

    # 提取非空的部分
    result = [item for group in matches for item in group if item.strip()]
    return result

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'

def is_english(char):
    return char.isascii() and char.isalpha()

def detect_language(s):
    chinese_count = sum(1 for c in s if is_chinese(c))
    english_count = sum(1 for c in s if is_english(c))
    print(f"Chinese count: {chinese_count}, English count: {english_count}")

def lang(text):
    if not text: return 'en-US'
    return 'zh-tw' if is_chinese(text[0]) else 'en'

def speech(text):
    parts = split_mixed_text(text)
    # print(parts)
    for part in parts:
        if msvcrt.kbhit():  #是檢查是否有按鍵
            msvcrt.getch()  # 清除一個已被按下的按鍵
            break
        text_to_speech(part, lang(part))


def unit_test():
    # 測試用
    # text = "* * * 444, This is my book, I like 123 玩具 123！"
    # text='We should practice our sledding before then, okay? My brother is a great skier and he can teach you.'
    # text = '6. parner - 朋友 (注意：通常用"partner"代替這個字）'
    text = "I'm a 學生."
    print(text)
    speech(text)

if __name__ == "__main__":
    unit_test()