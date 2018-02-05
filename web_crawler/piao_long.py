#encoding:utf-8

import requests
import json
import time
from config import ding_talk_token_long

#钉钉机器人token
ding_token = "bb60831ce9851d40406a440f156f381108d774947427419788720162bbad7a97"


def send_ding_talk(param):
    """
    发送钉钉消息
    :param param:
    :return:
    """
    params = '{"msgtype": "text","text": {"content": "' + param + '"}}'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    result=requests.post(
        'https://oapi.dingtalk.com/robot/send?access_token=' + ding_token,
        data=params,
        headers=headers
    )
    print result


def has(param):
    """
    有票
    :param param:
    :return:
    """
    return param != '' and param != u'无' and (param == u'有' or int(param.encode("UTF-8")) >= 1)


if __name__ == '__main__':

    #列次日期
    date = '2018-02-14'
    #列次发车开始时间--小时
    start_hour = 0
    #列次发车结束时间--小时
    end_hour = 10
    #列次出发地点--徐州东
    from_station = 'SZH'
    from_station_text = '苏州'
    #列次到达地点--苏州
    to_station = 'XCH'
    to_station_text = '徐州'

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
                #高级软卧座余票情况
                zuo_gjrw = list_title[22]
                # 软卧座余票情况
                zuo_rw = list_title[23]
                # 动卧座余票情况
                zuo_dw = list_title[24]
                # 硬卧座余票情况
                zuo_yw = list_title[25]
                # 软座余票情况
                zuo_rz = list_title[26]
                # 硬座余票情况
                zuo_yz = list_title[27]
                # 无座余票情况
                zuo_wz = list_title[28]

                #发车开始时间--小时
                btime_h = int(btime.encode("UTF-8").split(':')[0])
                #时间在选择范围
                if btime_h >= start_hour and btime_h <= end_hour:
                    #这里判断一等、二等座 有票或票数大于一的情况  发钉钉提醒
                    if has(zuo_t) or has(zuo_1) or has(zuo_2) or has(zuo_gjrw) or has(zuo_rw) or has(zuo_dw) or has(zuo_yw) or has(zuo_rz) or has(zuo_yz) or has(zuo_wz):
                        print result
                        print gtype,zuo_t,zuo_1,zuo_2
                        ding_content = '有票了\n日期：' + date
                        ding_content = ding_content + '\nfrom:' + from_station_text
                        ding_content = ding_content + '\nto:' + to_station_text
                        ding_content = ding_content + ',\n列次:' + gtype.encode("UTF-8")
                        ding_content = ding_content + ',\n发车时间:' + btime.encode("UTF-8")
                        ding_content = ding_content + ',\n到站时间：' + etime.encode("UTF-8")
                        ding_content = ding_content + ',\n耗时:' + costtime.encode("UTF-8")
                        ding_content = ding_content + ',\n特等座:' + zuo_t.encode("UTF-8")
                        ding_content = ding_content + ',\n一等座:' + zuo_1.encode("UTF-8")
                        ding_content = ding_content + ',\n二等座:' + zuo_2.encode("UTF-8")
                        ding_content = ding_content + ',\n高级软卧:' + zuo_gjrw.encode("UTF-8")
                        ding_content = ding_content + ',\n软卧:' + zuo_rw.encode("UTF-8")
                        ding_content = ding_content + ',\n动卧:' + zuo_dw.encode("UTF-8")
                        ding_content = ding_content + ',\n硬卧:' + zuo_yw.encode("UTF-8")
                        ding_content = ding_content + ',\n软座:' + zuo_rz.encode("UTF-8")
                        ding_content = ding_content + ',\n硬座:' + zuo_yz.encode("UTF-8")
                        ding_content = ding_content + ',\n无座:' + zuo_wz.encode("UTF-8")
                        send_ding_talk(ding_content)

        except Exception,e:
            print e
            print ere

        count = count + 1
        time.sleep(5)
        print '已尝试' + str(count) + '次'

