# coding=utf-8
import threading
from threading import Thread
# from manager import pushNotifications
from flask import json, current_app

from threadpool import ThreadPool, makeRequests

# from manager.models import GateKline, GateKlineSchema
# from manager import gateDao

# klines_schema = GateKlineSchema(many=True)
# kline_schema = GateKlineSchema()

import websocket
import time
import ssl

# try:
#     import thread
# except ImportError:
#     import _thread as thread


# all_Thread = []
# all_pool = ThreadPool(100)

def on_message(ws, message):

    result_json = json.loads(message)

    if ws.method == 'kline.subscribe':   ## 订阅 kline
        if 'method' in result_json and result_json['method'] == 'kline.update': ## 返回数据
            list = result_json['params']
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '更新 ***', len(list), '***', list)

        elif 'result' in result_json  and result_json['result'] == 'success':
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' *** 订阅成功 ***', ws.pair_name)

        else:
            print(message)


    elif ws.method == 'kline.query':  ## 查询 kline
        if result_json['error'] is not None:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '查询错误 xxx', result_json['error'])

        else:
            if len(result_json['result']) >= 360:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '继续查询 +++', len(result_json['result']))
                ws.start = ws.start + 21600
                newMsg = '{"id":%d, "method":"%s", "params":["%s", %d, %d, %d]}' \
                         % (ws.id, ws.method, ws.pair_name, ws.start, ws.start + 21600, ws.group_sec)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '结束查询 ---', len(result_json['result']))
                ws.method = 'kline.subscribe'
                newMsg = '{"id":%d, "method":"%s", "params":["%s", %d]}' \
                         % (ws.id, ws.method, ws.pair_name, ws.group_sec)
            ws.send(newMsg)


def on_error(ws, error):

    ws.reconnect = True
    alert = 'Gate ----- %s ----- 产生错误' % error

    print(alert)
    # pushNotifications.all(alert=alert)


def on_close(ws):
    print("### +++++++++++++ closed +++++++++++++ ###", ws)


def on_ping(ws):
    send_msg = '{"id":%d, "method":"server.ping", "params":[]}' % ws.id
    ws.send(send_msg)


def on_pong(ws, args):
    print('*******  pong ----- %s ----- %s ----- %s' % (ws.id, ws.pair_name, args))

# ----------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>

def on_open(ws):
    message = '{"id":%d, "method":"%s", "params":["%s", %d, %d, %d]}' \
              % (ws.id, ws.method, ws.pair_name, ws.start , ws.start + 21600 - 10, ws.group_sec)
    ws.send(message)
    alert = 'Gate ----- %s ----- 开启监控' % ws.pair_name
    print(alert)
    # pushNotifications.all(alert=alert)




websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://ws.gate.io/v3/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_ping=on_ping,
                                on_pong=on_pong,
                                on_open=on_open)

ws.id = int(time.time()) - 1545202554
ws.pair_name = 'EOS_USDT'
ws.start = int(time.time()) - 21600# 216000
ws.method = 'kline.query'   #'kline.subscribe'#
ws.group_sec = 60
ws.autosync = True

ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE},
               http_proxy_host="127.0.0.1",
               http_proxy_port=1087,
               ping_interval=60,
               ping_timeout=50
               )







    #     return ws
    #
    # return None



    # 检查服务器连接。
    # ws.send('{"id":12312, "method":"server.ping", "params":[]}')

    # 获取服务器时间。
    # ws.send('{"id":12312, "method":"server.time", "params":[]}')

    # Ticker API  ====================================================
    # 股票代码是对市场状况的高级概述。它向您显示最高，最低，最后交易价格。它还包括每日交易量以及价格在最后一天移动了多少等信息。
    # 查询指定市场的股票代码，包括一定时期内的价格，交易量等。
    # ws.send('{"id":12312, "method":"ticker.query", "params":["EOS_USDT", 86400]}')

    # 订阅市场自动收报机。
    # ws.send('{"id":12312, "method":"ticker.subscribe", "params":["EOS_USDT"]}')
    # 通知订阅的市场代码。

    # 取消订阅市场代码。
    # ws.send('{"id":12312, "method":"ticker.unsubscribe", "params":[]}')

    # 交易API  ====================================================
    # 每当在gate.io发生交易时，该通道都会发送交易消息。它包括交易的细节，例如价格，金额，时间和类型。
    # 查询最新交易信息，包括时间，价格，金额，类型等。
    # ws.send('{"id":12309, "method":"trades.query", "params":["EOS_USDT", 2, 7177813]}')

    # 订阅交易更新通知。
    # ws.send('{"id":12312, "method":"trades.subscribe", "params":["ETH_USDT", "BTC_USDT"]}')
    # 通知最新交易更新。

    # 取消订阅交易更新通知。
    # ws.send('{"id":12312, "method":"trades.unsubscribe", "params":[]}')

    # 深度API  ====================================================
    # 深度通道允许您跟踪gate.io订单簿深度的状态。它以价格汇总的方式提供，具有可定制的精度。
    # 查询指定的市场深度。
    # ws.send('{"id":12312, "method":"depth.query", "params":["ETH_USDT", 5, "0.00001"]}')

    # 订阅深度。
    # ws.send('{"id":12312, "method":"depth.subscribe", "params":["ETH_USDT", 5, "0.0001"]}')
    # ws.send('{"id":12312, "method":"depth.subscribe", "params":[["BTC_USDT", 5, "0.01"], ["ETH_USDT", 5, "0"]]}')
    # 通知市场深度更新信息

    # 取消指定的指定市场深度。
    # ws.send('{"id":12312, "method":"depth.unsubscribe", "params":[]}')


    # Kline API   ====================================================
    # 提供访问图表烛台信息的方法。
    # 查询指定的市场kline信息
    # ws.send('{"id":12312, "method":"kline.query", "params":["BTC_USDT", 1516950000, 1516951219, 60]}')

    # 订阅指定的市场kline信息。
    # ws.send('{"id":12312, "method":"kline.subscribe", "params":["BTC_USDT", 10]}')
    # 通知订阅市场的kline信息。

    # 取消订阅  Unsubsribe指定的市场kline信息。
    # ws.send('{"id":12312, "method":"kline.unsubscribe", "params":[]}')





    # 通知订阅的市场代码。
    # ws.send('{"id":101111, "method":"kline.query", "params":["BTC_USDT", 1529856000, 1530588601, 60]}')

