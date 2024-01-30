import sys

def main():
    platform = sys.platform
    print(f"当前平台：{platform}")
    name = input("请输入你的名字：")
    sys.stdout.write(f"你好，{name}！\n")
    sys.stderr.write("发生错误\n")
if __name__ == '__main__':
    main()
