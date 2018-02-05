#encoding:utf-8

from config import ding_talk_token
import requests
def send_photo(photo_url, title, text):
    print text,title
    params = '{"msgtype": "link","link": {"text":"' + str(text) + '","title":"' + str(title) + '"'
    params = params + ',"picUrl":"'+str(photo_url)+'"'
    params = params + ',"messageUrl":"' + str(photo_url) + '"}}'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    requests.post(
        'https://oapi.dingtalk.com/robot/send?access_token=' + ding_talk_token,
        data=params,
        headers=headers
    )


def send_text(text):

    params = '{"msgtype": "text","text": {"content": "' + text + '"}}'
    print params
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    requests.post(
        'https://oapi.dingtalk.com/robot/send?access_token=' + ding_talk_token,
        data=params,
        headers=headers
    )