# coding=utf-8

## 多个连接
import random
import threading
from threading import Thread
from dao import pushNotifications
from flask import json, current_app

from threadpool import ThreadPool, makeRequests

# from manager.models import GateKline, GateKlineSchema
# from manager import gateDao

# klines_schema = GateKlineSchema(many=True)
# kline_schema = GateKlineSchema()

import websocket
import time
import ssl

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):

    result_json = json.loads(message)

    if ws.method == 'kline.subscribe':   ## 订阅 kline
        if 'method' in result_json and result_json['method'] == 'kline.update': ## 返回数据
            list = result_json['params']
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  ws.id , '*',
                  ws.pair_name,
                  '更新 ***', len(list), '***',
                  list)

        elif 'result' in result_json  and result_json['result'] == 'success':
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  ws.id , '*',
                  ' *** 订阅成功 ***',
                  ws.pair_name)

        else:
            print(message)


    elif ws.method == 'kline.query':  ## 查询 kline
        if result_json['error'] is not None:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  '查询错误 xxx',
                  result_json['error'])

        else:
            if len(result_json['result']) >= 360:
                ws.start = ws.start + 21600
                send_info = '{"id":%d, "method":"%s", "params":["%s", %d, %d, %d]}' \
                         % (ws.id, ws.method, ws.pair_name, ws.start, ws.start + 21600, ws.group_sec)

                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        ws.id , '*',
                      '继续查询 +++',
                      len(result_json['result']))

            else:
                ws.method = 'kline.subscribe'
                send_info = '{"id":%d, "method":"%s", "params":["%s", %d]}' \
                         % (ws.id, ws.method, ws.pair_name, ws.group_sec)

                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        ws.id , '*',
                      '结束查询 ---',
                      len(result_json['result']))


            ws.send(send_info)


def on_error(ws, error):

    ws.reconnect = True
    alert = 'Gate ----- %s ----- 产生错误' % error
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,alert)
    pushNotifications.all(alert=alert)


def on_close(ws):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,"### +++++++++++++ closed +++++++++++++ ###", ws)
    # alert = " closed ----- %s" % ws.pair_name
    # pushNotifications.all(alert=alert)

def on_ping(ws):
    send_info = '{"id":%d, "method":"server.ping", "params":[]}' % ws.id
    ws.send(send_info)


def on_pong(ws, args):
    print('*******  pong ----- %s ----- %s ----- %s' % (ws.id, ws.pair_name, args))


def on_open(ws):

    def send_trhead():
        send_info = '{"id":%d, "method":"%s", "params":["%s", %d, %d, %d]}' \
                    % (ws.id, ws.method, ws.pair_name, ws.start, ws.start + 21600 - 10, ws.group_sec)
        ws.send(send_info)
        alert = 'Gate ----- %s ----- 开启监控' % ws.pair_name
        print(alert)
        pushNotifications.all(alert=alert)

    t = threading.Thread(target=send_trhead)
    t.start()



def on_start(pair_name):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.gate.io/v3/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_ping=on_ping,
                                on_pong=on_pong,
                                on_open=on_open)

    timestamp = int(time.time())
    ws.id = random.randint(1500000000, timestamp)
    ws.pair_name = pair_name     #'EOS_USDT'
    ws.start = timestamp - 21600  # 216000
    ws.method = 'kline.query'    # 'kline.subscribe'#
    ws.group_sec = 60
    ws.autosync = True

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE},
                   http_proxy_host="127.0.0.1",
                   http_proxy_port=1087,
                   ping_interval=60,
                   ping_timeout=50
                   )




from threadpool import ThreadPool, makeRequests
if __name__ == "__main__":
    # init_logging()
    pool = ThreadPool(10)
    test = ['BTC_USDT','EOS_USDT', 'ETH_USDT']
    requests = makeRequests(on_start, test)
    [pool.putRequest(req) for req in requests]
    pool.wait()

