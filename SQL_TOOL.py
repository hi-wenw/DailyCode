from tkinter import *
import re
from tkinter import font
import sqlparse
import pyperclip

# 关键字列表

keywords = ['select', 'from', 'where', 'and', 'or', 'left join', 'left outer join', 'join', 'by', 'on',
            'case', 'when', 'else', 'if', 'end', 'then', 'asc', 'desc', 'not', 'like', 'in', 'group',
            'order', 'grouping sets', 'grouping', 'rollup', 'full', 'distinct', 'is', 'null', 'union all',
            'union', 'having', 'between', 'exists', 'string', 'int', 'decimal', 'double', 'comment', 'create',
            'external', 'table', 'bigint', 'stored', 'as', 'orc', 'parquet', 'location', 'distribute', 'insert',
            'overwrite', 'partition', 'using', 'if', 'or', 'view', 'with', 'inner', 'msck']

# 将关键字转为大写
upper_keywords = [i.upper() for i in keywords]


def convert_keywords_to_uppercase():
    # 获取文本框中的SQL内容
    sql = text.get("1.0", "end-1c")

    # 使用正则表达式将SQL中的关键字转换为大写
    pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
    converted_sql = pattern.sub(lambda m: m.group().upper(), sql)

    # 清空文本框内容并显示转换后的SQL
    text.delete("1.0", END)
    label.config(text="转换SQL成功,已自动复制至剪贴板")
    text.insert(END, converted_sql)

    # 高亮显示关键字
    highlight_keywords()

    # 自动粘贴
    pyperclip.copy(converted_sql)


def convert_keywords_to_lowercase():
    # 获取文本框中的SQL内容
    sql = text.get("1.0", "end-1c")

    # 使用正则表达式将SQL中的关键字转换为大写
    pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
    converted_sql = pattern.sub(lambda m: m.group().lower(), sql)

    # 清空文本框内容并显示转换后的SQL
    text.delete("1.0", END)
    label.config(text="转换SQL成功,已自动复制至剪贴板")
    text.insert(END, converted_sql)

    # 高亮显示关键字
    highlight_keywords()

    # 自动粘贴
    pyperclip.copy(converted_sql)


# 清空文本框内容
def clear():
    text.delete("1.0", END)
    label.config(text="请输入SQL语句: ")


# 将SQL复制到剪贴板
def copy_to_clipboard():
    sql = text.get("1.0", "end-1c")
    label.config(text="复制成功!")
    pyperclip.copy(sql)


# 从剪贴板粘贴SQL
def paste_from_clipboard():
    sql = pyperclip.paste()
    label.config(text="已粘贴!")
    text.delete("1.0", END)
    text.insert(END, sql)


# 高亮显示关键字
def highlight_keywords():
    # 配置关键字的样式
    text.tag_configure('keyword', font='TkDefaultFont 9 bold', foreground='red')

    # 获取文本框内容
    sql = text.get("1.0", "end-1c")

    for keyword in upper_keywords:
        start_index = '1.0'
        while True:
            # 使用正则表达式搜索关键字，并为其添加样式
            start_index = text.search(rf'\y{keyword}\y', start_index, stopindex=END, count=1, nocase=True, regexp=True)
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            text.tag_add('keyword', start_index, end_index)
            start_index = end_index

    for keyword in keywords:
        start_index = '1.0'
        while True:
            # 使用正则表达式搜索关键字，并为其添加样式
            start_index = text.search(rf'\y{keyword}\y', start_index, stopindex=END, count=1, nocase=True, regexp=True)
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            text.tag_add('keyword', start_index, end_index)
            start_index = end_index


def display_keywords():
    # 清空关键字列表框架中的内容
    keyword_text.delete("1.0", END)

    # 将关键字列表显示在关键字列表框架中
    for i, keyword in enumerate(keywords):
        keyword_text.insert(END, f"{i + 1}. {keyword}\n")


def add_keyword():
    # 获取新增关键字输入框中的内容
    new_keyword = new_keyword_entry.get().strip()

    if new_keyword:
        # 将新增关键字添加到关键字列表中
        keywords.append(new_keyword)

        # 将新增关键字转为大写并添加到大写关键字列表中
        upper_keywords.append(new_keyword.upper())

        # 清空新增关键字输入框
        new_keyword_entry.delete(0, END)

        # 更新关键字列表显示
        display_keywords()


def delete_keyword():
    # 获取删除关键字输入框中的内容
    index = delete_keyword_entry.get().strip()

    if index and index.isdigit() and int(index) <= len(keywords):
        # 删除指定索引的关键字
        del keywords[int(index) - 1]
        del upper_keywords[int(index) - 1]

        # 清空删除关键字输入框
        delete_keyword_entry.delete(0, END)

        # 更新关键字列表显示
        display_keywords()


def reformat_sql():
    # 获取文本框中的SQL内容
    sql = text.get("1.0", "end-1c")

    # 使用 sqlparse 将 SQL 格式化
    formatted_sql = sqlparse.format(sql, reindent=True)

    # 清空文本框内容并显示转换后的SQL
    text.delete("1.0", END)
    label.config(text="格式化SQL成功,已自动复制至剪贴板")
    text.insert(END, formatted_sql)

    # 高亮显示关键字
    highlight_keywords()

    # 自动粘贴
    pyperclip.copy(formatted_sql)


def format_sql(sql_content):
    """将sql语句进行规范化，并去除sql中的注释，输入和输出均为字符串"""
    parse_str = sqlparse.format(sql_content, reindent=True, strip_comments=True)
    return parse_str


def extract_table_names():
    """从sql中提取对应的表名称，输出为列表"""
    sql_query = text.get("1.0", "end-1c")
    table_names = set()
    # 解析SQL语句
    parsed = sqlparse.parse(sql_query)
    # 正则表达式模式，用于匹配表名
    table_name_pattern = r'\bFROM\s+([^\s\(\)\,]+)|\bJOIN\s+([^\s\(\)\,]+)'
    # with 子句判断
    with_pattern = r'with\s+(\w+)\s+as'
    remove_with_name = []

    # 遍历解析后的语句块
    for statement in parsed:
        # 转换为字符串
        statement_str = str(statement).lower()

        # 将字符串中的特殊语法置空
        statement_str = re.sub('(substring|extract)\s*\(((.|\s)*?)\)', '', statement_str)

        # 查找匹配的表名
        matches = re.findall(table_name_pattern, statement_str, re.IGNORECASE)

        for match in matches:
            # 提取非空的表名部分
            for name in match:
                # if name and name not in not_contain_list:
                if name:
                    # 对于可能包含命名空间的情况，只保留最后一部分作为表名
                    # table_name = name.split('.')[-1]
                    # 去除表名中的特殊符号
                    table_name = re.sub('("|`|\'|;)', '', name)
                    table_names.add(table_name)
        # 处理特殊的with语句
        if 'with' in statement_str:
            match = re.search(with_pattern, statement_str)
            if match:
                result = match.group(1)
                remove_with_name.append(result)
    table_list = list(table_names)
    # 移除多余的表名
    if remove_with_name:
        table_list = list(set(table_list) - set(remove_with_name))

    # 创建新窗口
    table_window = Toplevel(root)
    table_window.title("提取的表名,双击即可选中")
    table_text = Text(table_window, height=20, width=50)
    table_text.pack()

    # 将数据插入到文本框中
    table_text.insert(END, "\n".join(table_list))


if __name__ == '__main__':
    # 创建主窗口
    root = Tk()
    root.title('SQL小工具')
    font_style = font.Font(size=20)

    # 创建标签和滚动条
    label = Label(root, text="请输入SQL语句: ")
    label['font'] = font_style
    label.pack()

    scrollbar = Scrollbar(root, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    hor_scrollbar = Scrollbar(root, orient=HORIZONTAL)
    hor_scrollbar.pack(side=BOTTOM, fill=X)

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)

    # 创建文本框，并关联滚动条
    text = Text(frame, height=40, width=50, yscrollcommand=scrollbar.set, xscrollcommand=hor_scrollbar.set)
    text.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar.config(command=text.yview)
    hor_scrollbar.config(command=text.xview)

    # 创建占位符Label
    placeholder_label = Label(root, text="", width=5)
    placeholder_label.pack(side=LEFT)

    # 创建清空按钮
    clear_button = Button(root, text="清空", command=clear)
    clear_button.pack(side=LEFT)

    # 创建占位符Label
    placeholder_label = Label(root, text="", width=5)
    placeholder_label.pack(side=LEFT)

    # 创建复制按钮
    copy_button = Button(root, text="复制", command=copy_to_clipboard)
    copy_button.pack(side=LEFT)

    # 创建占位符Label
    placeholder_label = Label(root, text="", width=5)
    placeholder_label.pack(side=LEFT)

    # 创建粘贴按钮
    paste_button = Button(root, text="粘贴", command=paste_from_clipboard)
    paste_button.pack(side=LEFT)

    # 创建占位符Label
    placeholder_label = Label(root, text="", width=5)
    placeholder_label.pack(side=LEFT)

    # 创建转换SQL按钮
    transition_button = Button(root, text="关键字大写", command=convert_keywords_to_uppercase)
    transition_button.pack(side=LEFT)

    # 创建占位符Label
    placeholder_label = Label(root, text="", width=5)
    placeholder_label.pack(side=LEFT)

    # 创建转换SQL按钮
    transition_button = Button(root, text="关键字小写", command=convert_keywords_to_lowercase)
    transition_button.pack(side=LEFT)

    # 创建占位符Label
    placeholder_label = Label(root, text="", width=5)
    placeholder_label.pack(side=LEFT)

    # 创建格式化按钮
    reformat_button = Button(root, text="格式化", command=reformat_sql)
    reformat_button.pack(side=LEFT)

    # 创建占位符Label
    placeholder_label = Label(root, text="", width=5)
    placeholder_label.pack(side=LEFT)

    # 创建提取表名按钮
    reformat_button = Button(root, text="提取表名", command=extract_table_names)
    reformat_button.pack(side=LEFT)

    # 创建占位符Label
    placeholder_label = Label(root, text="", width=5)
    placeholder_label.pack(side=LEFT)

    # 创建关键字列表框架
    keyword_frame = Frame(root)
    keyword_frame.pack()

    # 创建关键字列表标签
    keyword_label = Label(keyword_frame, text="关键字列表:")
    keyword_label.pack(side=LEFT)

    # 创建关键字列表文本框，并关联滚动条
    keyword_text = Text(keyword_frame, height=5, width=30)
    keyword_text.pack(side=LEFT, fill=Y)

    # 创建关键字列表滚动条
    keyword_scrollbar = Scrollbar(keyword_frame, orient=VERTICAL, command=keyword_text.yview)
    keyword_scrollbar.pack(side=LEFT, fill=Y)

    # 将关键字列表文本框与滚动条关联
    keyword_text.config(yscrollcommand=keyword_scrollbar.set)

    # 创建新增关键字输入框和按钮
    add_keyword_frame = Frame(root)
    add_keyword_frame.pack()

    new_keyword_label = Label(add_keyword_frame, text="新增关键字:")
    new_keyword_label.pack(side=LEFT)

    new_keyword_entry = Entry(add_keyword_frame)
    new_keyword_entry.pack(side=LEFT)

    add_keyword_button = Button(add_keyword_frame, text="新增", command=add_keyword)
    add_keyword_button.pack(side=LEFT)

    # 创建删除关键字输入框和按钮
    delete_keyword_frame = Frame(root)
    delete_keyword_frame.pack()

    delete_keyword_label = Label(delete_keyword_frame, text="删除关键字索引:")
    delete_keyword_label.pack(side=LEFT)

    delete_keyword_entry = Entry(delete_keyword_frame)
    delete_keyword_entry.pack(side=LEFT)

    delete_keyword_button = Button(delete_keyword_frame, text="删除", command=delete_keyword)
    delete_keyword_button.pack(side=LEFT)

    # 初始化关键字列表显示
    display_keywords()

    root.mainloop()
