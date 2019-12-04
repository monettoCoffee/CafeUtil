# coding=utf-8
"""
Trans_txt_2_pic
"""
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# txt文件路径
INPUT_PATH = "input_txt/"
# 转换图片路径
OUTPUT_PATH = "output_pic/"

# 内容上边距
CONTENT_MARGIN_TOP = 32
# 内容左边距
CONTENT_MARGIN_LEFT = 20
# 内容字体大小
CONTENT_FONT_SIZE = 25
# 一页有几行
PAGE_LINE_NUMBER = 7
# 每行几个字
LINE_WORD_NUMBER = 8
# 内容输出字体 当前为思源黑体
CONTENT_FONT_FILE = "font.otf"
# 每行留空长度
LINE_EMPTY_SIZE = 2

# 是否加入页眉 True是 / False否
ADD_PAGE_HEADER = True
# 页眉上边距离
PAGE_HEADER_MARGIN_TOP = 4
# 页眉左边距
PAGE_HEADER_MARGIN_LEFT = 30
# 页眉字体大小
HEADER_FONT_SIZE = 16
# 页眉输出字体 当前为思源黑体
HEADER_FONT_FILE = "font.otf"

# 是否加入页眉下划线 True是 / False否
ADD_PAGE_HEADER_UNDER_LINE = True
# 页眉下划线长度
UNDER_LINE_LENGTH = 100
# 页眉下划线上边距
UNDER_LINE_MARGIN_TOP = 14
# 页面下划线左边距
UNDER_LINE_MARGIN_LEFT = 0

# 页面背景图片
BACKGROUND_IMAGE = "background.jpg"

# 当前行出现特定字符换行 True是 / False否
NEXT_LINE_WHEN_SPLIT_APPEAR = True
# 特定符号自动换行字符
SPLIT_LINE_SET = set(["。"])

# 最后一行出现特定符号自动换页 True是 / False否
NEXT_PAGE_WHEN_SPLIT_APPEAR = True
# 特定符号自动换页字符
SPLIT_PAGE_SET = set([",", "，", "。", "”"])

# 至少多少字符时才能触发特殊符号自动换行/页机制
SPLIT_WORD_COUNT = 4

# 忽略文件列表
IGNORE_FILE_NAME_SET = set([".DS_Store"])

# 这些字符会被替换掉以自动排版
REPLACE_CHAR_LIST = ["\n", "\t", "\r", "\u3000"]

# 在这里出现字符算半个字, 占用一半位置
HALF_POSITION_CHARACTER = set([
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "a", "b", "c", "d", "e", "f", "j", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
    "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
    "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
    "Y", "Z", ",", "'", '"', " ", ";"
    ])

def get_book_text(book):
    book = book.replace("\n", "")
    content = empty_position
    count = LINE_EMPTY_SIZE
    line_count = 0
    all_text = []
    for word in book:
        # 遇到特定符号时自动换行
        if NEXT_LINE_WHEN_SPLIT_APPEAR and word in SPLIT_LINE_SET and count > SPLIT_WORD_COUNT:
            line_count += 1
            count = LINE_EMPTY_SIZE
            content += word + "\n" + empty_position
            # 当行数到达一定时自动换页
            if line_count >= PAGE_LINE_NUMBER:
                line_count = 0
                all_text.append(content)
                content = empty_position
                count = LINE_EMPTY_SIZE
            continue
        # 当文字数量到达一定时自动换行
        if count >= LINE_WORD_NUMBER:
            line_count += 1
            count = 0
            content += word + "\n"
            # 当行数到达一定时自动换页
            if line_count >= PAGE_LINE_NUMBER:
                line_count = 0
                all_text.append(content)
                content = ""
                count = 0
            continue
        # 累计字符
        else:
            if word in HALF_POSITION_CHARACTER:
                count += 0.5
            else:
                count += 1
            content += word
            # 最后一行遇到特定符号时换页
            if NEXT_PAGE_WHEN_SPLIT_APPEAR and line_count >= PAGE_LINE_NUMBER - 1 and word in SPLIT_PAGE_SET and count > SPLIT_WORD_COUNT:
                line_count = 0
                all_text.append(content)
                content = ""
                count = 0
    all_text.append(content)
    return all_text


def add_page_header(book_draw, book_name, page_number):
    if ADD_PAGE_HEADER:
        book_draw.text((PAGE_HEADER_MARGIN_LEFT, PAGE_HEADER_MARGIN_TOP), book_name + "   " + page_number, 'black',
                       header_font)


under_line = "-" * UNDER_LINE_LENGTH


def add_page_header_under_line(book_draw):
    if ADD_PAGE_HEADER_UNDER_LINE:
        book_draw.text((UNDER_LINE_MARGIN_LEFT, UNDER_LINE_MARGIN_TOP), under_line, 'black', header_font)


empty_position = " " * LINE_EMPTY_SIZE * 4


def get_zfill_number(book):
    book_length = len(book) * 1.5
    if NEXT_LINE_WHEN_SPLIT_APPEAR:
        return len(str(book_length / (SPLIT_WORD_COUNT + 1) / PAGE_LINE_NUMBER)) + 1
    else:
        return len(str(book_length / LINE_WORD_NUMBER / PAGE_LINE_NUMBER)) + 1


PAGE_LINE_NUMBER -= 1
LINE_WORD_NUMBER -= 1
book_background = Image.open(BACKGROUND_IMAGE).convert("RGB")

content_font = ImageFont.truetype(font=CONTENT_FONT_FILE, encoding="unic", size=CONTENT_FONT_SIZE)
header_font = ImageFont.truetype(font=HEADER_FONT_FILE, encoding="unic", size=HEADER_FONT_SIZE)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    for txt in os.listdir(INPUT_PATH):
        if txt in IGNORE_FILE_NAME_SET:
            continue
        with open(INPUT_PATH + txt, "rb") as file:
            txt = txt.replace(".txt", "")
            save_path = OUTPUT_PATH + txt
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            save_path = save_path + "/" + txt
            page_number = 1
            book = file.readlines()
            length = len(book) - 1
            while length > -1:
                try:
                    book[length] = book[length].decode("utf8")
                except:
                    book[length] = book[length].decode("gbk")
                length -= 1
            
            book = "".join(book)
            for character in REPLACE_CHAR_LIST:
                book = book.replace(character, "")
            book_text_list = get_book_text(book)

            fill_number = len(str(len(book_text_list))) + 1

            for every_page in book_text_list:
                page = book_background.copy()

                book_draw = ImageDraw.Draw(page)
                book_draw.text((CONTENT_MARGIN_LEFT, CONTENT_MARGIN_TOP), every_page, 'black', content_font)

                page_number_str = " " + str(page_number).zfill(fill_number)
                if page_number % 100 == 0:
                    print("Loading " + txt + page_number_str)
                

                add_page_header(book_draw, txt, page_number_str)
                add_page_header_under_line(book_draw)

                page.save(save_path + page_number_str + ".jpg")
                page_number += 1
            print("Trans " + txt + " Done.")
