import requests

def delete_message(message_id, token):
    url = f"https://open.feishu.cn/open-apis/message/v4/delete"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "message_id": message_id
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("消息撤回成功")
    else:
        print(f"撤回失败，错误代码: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    # 在这里添加你的逻辑和代码

    # 假设要撤回的消息 ID 是 'message123'
    message_id = 'message123'

    # 假设你的飞书机器人的访问令牌是 'your_token'
    token = 'your_token'

    delete_message(message_id, token)