#encoding:utf-8

import requests
import json
import time

#钉钉机器人token
ding_token = 'xxxxxxxxxxx'


#发送钉钉消息
def send_ding_talk(param):
    params = '{"msgtype": "text","text": {"content": "' + param + '"}}'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    requests.post(
        'https://oapi.dingtalk.com/robot/send?access_token=' + ding_token,
        data=params,
        headers=headers
    )


if __name__ == '__main__':

    #列次日期
    date = '2018-02-21'
    #列次发车开始时间--小时
    start_hour = 10
    #列次发车结束时间--小时
    end_hour = 24
    #列次出发地点--徐州东
    from_station = 'UUH'
    #列次到达地点--苏州
    to_station = 'SZH'

    #计数
    count = 0
    while True:
        ere = None
        try:
            response = requests.get('https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' + date + '&leftTicketDTO.from_station='+from_station+'&leftTicketDTO.to_station='+to_station+'&purpose_codes=ADULT',params=None)
            tr = response.text
            print tr
            dfd = response.content
            json_data = json.loads(dfd)
            list_result = json_data["data"]["result"]
            for result in list_result:
                ere = result
                list_title = result.split('|')
                #列车类型（如：G123,K3242）
                gtype = list_title[3]
                #列车发车时间，格式HH:mm
                btime = list_title[8]
                # 列车到站时间，格式HH:mm
                etime = list_title[9]
                # 列车消耗时间，格式HH:mm
                costtime = list_title[10]
                #特等座余票情况
                zuo_t = list_title[32]
                #一等座余票情况
                zuo_1 = list_title[31]
                #二等座余票情况
                zuo_2 = list_title[30]
                #发车开始时间--小时
                btime_h = int(btime.encode("UTF-8").split(':')[0])
                #G字列车 并且时间在选择范围
                if gtype.startswith('G') and btime_h >= start_hour and btime <= end_hour:
                    #这里判断一等、二等座 有票或票数大于一的情况  发钉钉提醒
                    if (zuo_1 != '' and zuo_1 != u'无' and (zuo_1 == u'有' or int(zuo_1.encode("UTF-8")) >= 1)) or (zuo_2 != '' and zuo_2 != u'无' and (zuo_2 == u'有' or int(zuo_2.encode("UTF-8")) >= 1)):
                        print result
                        print gtype,zuo_t,zuo_1,zuo_2
                        send_ding_talk('有票了\n日期：' + date + ',\n列次:' + gtype.encode("UTF-8") + ',\n发车时间:' + btime.encode("UTF-8") + ',\n到站时间：'+ etime.encode("UTF-8") +',\n耗时:'+ costtime.encode("UTF-8") +',\n特等座:' + zuo_t.encode("UTF-8") + ',\n一等座:' + zuo_1.encode("UTF-8") + ',\n二等座:' + zuo_2.encode("UTF-8"))

        except Exception,e:
            print e
            print ere

        count = count + 1
        time.sleep(5)
        print '已尝试' + str(count) + '次'

