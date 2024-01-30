# -*- coding: utf-8 -*-
import os

directory = r'C:\Users\Administrator\Downloads\flink学习'
file_list = os.listdir(directory)

for file_name in file_list:
    # 构造新的文件名
    new_file_name = file_name+'.md'

    # 构造旧的文件路径和新的文件路径
    old_file_path = os.path.join(directory, file_name)
    new_file_path = os.path.join(directory, new_file_name)

    # 重命名文件
    os.rename(old_file_path, new_file_path)
