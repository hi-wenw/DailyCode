import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='输入名字性别年龄')

    parser.add_argument('-n', '--name', type=str, help='你的名字')
    parser.add_argument('-age', type=int, help='你的年龄')
    parser.add_argument('-sex', choices=['nan', 'nv'], type=str, help='你的性别')

    args = parser.parse_args()

    # print(args.name)
    print(args.n)
    print(args.age)
    print(args.sex)
