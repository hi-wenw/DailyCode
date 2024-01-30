import json

import requests

if __name__ == '__main__':
    url = 'https://open.feishu.cn/open-apis/bot/v2/hook/4361258d-c97b-4f14-9f24-1891d0f27d5a'
    data = json.dumps({
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "hr"
                },
                {
                    "fields": [{'is_short': False, 'text': {'content': '**未来一手**:一手未来', 'tag': 'lark_md'}},
                               {'is_short': False, 'text': {'content': '**包子**:嘿嘿', 'tag': 'lark_md'}},
                               {'is_short': False, 'text': {'content': '**睡觉**:zzz', 'tag': 'lark_md'}}
                               ],
                    "tag": "div"
                }
            ],
            "header": {
                "template": 'purple',
                "title": {
                    "content": '解析',
                    "tag": "plain_text"
                }
            }
        }})
    requests.post(url, data)

