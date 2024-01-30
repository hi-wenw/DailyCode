# -*- coding: utf-8 -*-
import os
import json


def read_folder(folder_path, result_list):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        print(file_path)
        if os.path.isfile(file_path):
            # with open(file_path, "r", encoding="utf-8") as f:
            #     data = json.load(f)
            #     try:
            #         if data.get("lastUpdateUser") == "hewenbao":
            #             result_list.append({
            #                 "lastUpdateUser": data["lastUpdateUser"],
            #                 "description": data["description"],
            #                 "name": data["name"],
            #                 "schedule": data["schedule"]
            #             })
            #     except:
            #         pass
            pass
        elif os.path.isdir(file_path):
            read_folder(file_path, result_list)


result_list = []
folder_path = r"C:\Users\Administrator\Downloads\jobs"
read_folder(folder_path, result_list)

# 输出结果
for item in result_list:
    print(item["lastUpdateUser"], item["description"], item["name"])
