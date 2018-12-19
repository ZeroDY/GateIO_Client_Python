# -*- coding: utf-8 -*-
#author: か壞尐孩キ

from gateio.Gateio import GateWs
import random

gate=GateWs("wss://ws.gate.io/v3/", "your key", "your secret.")

##检查服务器连接。
#print(gate.gateRequest(random.randint(0,99999),'server.ping',[]))

## 获取服务器时间。
#print(gate.gateRequest(random.randint(0,99999),'server.time',[]))

## 查询指定市场的股票代码，包括一定时期内的价格，交易量等。
#print(gate.gateRequest(random.randint(0,99999),'ticker.query',["EOS_USDT",86400]))

## 订阅市场自动收报机。
#print(gate.gateRequest(random.randint(0,99999),'ticker.subscribe',["BOT_USDT"]))

## 取消订阅市场代码。
#print(gate.gateRequest(random.randint(0,99999),'ticker.unsubscribe',[]))
	
## 查询最新交易信息，包括时间，价格，金额，类型等。
#print(gate.gateRequest(random.randint(0,99999),'trade.query',["EOS_USDT",2,7177813]))

## 订阅交易更新通知。
#print(gate.gateRequest(random.randint(0,99999),'trades.subscribe',["ETH_USDT","BTC_USDT"]))

## 取消订阅交易更新通知。
#print(gate.gateRequest(random.randint(0,99999),'trades.unsubscribe',[]))

## 查询指定的市场深度
#print(gate.gateRequest(random.randint(0,99999),'depth.query',["EOS_USDT",5,"0.0001"]))

## 订阅深度。
#print(gate.gateRequest(random.randint(0,99999),'depth.subscribe',["ETH_USDT",5,"0.0001"]))

## 取消订阅指定的市场深度。
#print(gate.gateRequest(random.randint(0,99999),'depth.unsubscribe',[]))

## 查询指定的市场kline信息
#print(gate.gateRequest(random.randint(0,99999),'kline.query',["BTC_USDT",1,1516951219,1800]))

## 订阅指定的市场kline信息。
print(gate.gateRequest(random.randint(0,99999),'kline.subscribe',["BTC_USDT",1800]))

## 取消订阅指定的市场kline信息。
#print(gate.gateRequest(random.randint(0,99999),'kline.unsubscribe',[]))

## 通知订阅市场的kline信息。
#print(gate.gateRequest(random.randint(0,99999),'kline.update',[1492358400,"7000.00","8000.0","8100.00","6800.00","1000.00","123456.00","BTC_USDT"]))

## 基于签名的授权。
#print(gate.gateRequest(random.randint(0,99999),'server.sign',[]))		

## 查询用户未执行的订单
#print(gate.gateRequest(random.randint(0,99999),'order.query',["BTC_USDT",0,10]))	

## 订阅用户订单更新
#print(gate.gateRequest(random.randint(0,99999),'order.subscribe',["BTC_USDT"]))

## 下订单，更新或完成订单时通知用户订单信息。
#print(gate.gateRequest(random.randint(0,99999),'order.update',[2,"12345654654"]))

## 对所有市场取消订阅用户订单更新通知。
#print(gate.gateRequest(random.randint(0,99999),'order.unsubscribe',[]))

## 获取指定资产或资产的用户余额信息。
#print(gate.gateRequest(random.randint(0,99999),'balance.query',["BTC"]))

## 订阅用户余额更新。
#print(gate.gateRequest(random.randint(0,99999),'balance.subscribe',["BTC"]))

## 通知用户余额更新。
#print(gate.gateRequest(random.randint(0,99999),'balance.update',[{'EOS':{'available':'96.765323611874','freeze':'11'}}]))

## 取消订阅用户余额更新。
##print(gate.gateRequest(random.randint(0,99999),'balance.unsubscribe',[]))
