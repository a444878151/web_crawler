#encoding:utf-8

from httpUtils import post
from config import ding_talk_host,ding_talk_url
def send_photo(photo_url, title, text):
    print text,title
    params = '{"msgtype": "link","link": {"text":"' + str(text) + '","title":"' + str(title) + '"'
    params = params + ',"picUrl":"'+str(photo_url)+'"'
    params = params + ',"messageUrl":"' + str(photo_url) + '"}}'
    response = post(ding_talk_host, ding_talk_url, params)
    print response


def send_text(text):
    params = '{"msgtype": "text","text": {"content": "' + text + '"}}'
    print params
    response = post(ding_talk_host, ding_talk_url, params)
    print response