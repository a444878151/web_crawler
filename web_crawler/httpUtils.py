#encoding:utf-8

import httplib, urllib

def post(host, url, params):
    headers = {"Content-type": "application/json; charset=utf-8",
               "Accept": "*/*"}
    data = params
    print data
    conn = httplib.HTTPSConnection(host)
    conn.request('POST', url, data, headers)
    response = conn.getresponse()
    data_resp = response.read()
    conn.close()
    return data_resp