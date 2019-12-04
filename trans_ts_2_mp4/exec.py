# coding=utf-8
"""
Trans_ts_2_mp4
"""
import os
import shutil

# 当前工作目录
CURRENT_DIR = os.getcwd() + "/"

# ts文件路径
INPUT_PATH = CURRENT_DIR + "input_ts/"
# 转换MP4文件路径
OUTPUT_PATH = CURRENT_DIR + "output_mp4/"

# 转换命令
TRANS_COMMAND = 'ffmpeg -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i index.m3u8 -c copy '

# 忽略文件列表
IGNORE_FILE_NAME_SET = set([".DS_Store"])


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    for ts in os.listdir(INPUT_PATH):
        if ts in IGNORE_FILE_NAME_SET:
            continue
        os.chdir(INPUT_PATH + ts)
        os.popen(TRANS_COMMAND + OUTPUT_PATH + ts + ".mp4")
        os.chdir(INPUT_PATH)
        shutil.rmtree(INPUT_PATH + ts)
        print("Trans " + ts + " Done.")
