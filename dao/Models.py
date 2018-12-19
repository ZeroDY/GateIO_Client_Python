#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from sqlalchemy import Column, String, Integer, Float, create_engine, ForeignKey, PrimaryKeyConstraint, Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from MySQLdb import *

# 创建模型类的基类

BaseModel = declarative_base()


class GatePair(BaseModel):
    '''
    交易配对
    '''
    __tablename__ = 'gate_pair'

    pair_name = Column(String(64), primary_key=True, nullable=False, index=True)
    decimal_places = Column(Integer) # 价格精度
    min_amount = Column(Float) # 最小下单量
    fee = Column(Float) # 交易费 百分数
    autosync = Column(Integer, default=0)

    def __init__(self,pair_name):
        self.pair_name = pair_name



class GateKline(BaseModel):
    '''
    交易 K线
    '''
    __tablename__ = 'gate_kline'
    __table_args__ = (
        PrimaryKeyConstraint('pair_name', 'timestamp', 'group_sec'),
        Index('pair_name', 'timestamp', 'group_sec')
    )

    pair_name = Column(String(64), nullable=False)
    timestamp = Column(Integer(), nullable=False) # 时间戳
    volume = Column(Float, nullable=False) #  交易量
    close = Column(Float, nullable=False) #  收盘价
    high = Column(Float, nullable=False) #  最高价
    low = Column(Float, nullable=False) #  最低价
    open = Column(Float, nullable=False) #  开盘价
    group_sec = Column(Integer, nullable=False) # 时间间隔 秒数
    amount = Column(Float) # amount
    timestr = Column(String(64))

    def __init__(self, pair_name):
        self.pair_name = pair_name

    def __init__(self, pair_name, group_sec):
        self.pair_name = pair_name
        self.group_sec = group_sec

    # @timestamp.setter
    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
        timeArray = time.localtime(timestamp)
        self.timestr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


# # ************************************************************************
#
#
# class AccountSchema(ma.Schema):
#     account_name = fields.String(required=True)
#     password = fields.String(required=True)
#     permission = fields.Integer()
#     # pairs = fields.List()
#
#
# class GatePairSchema(ma.Schema):
#     pair_name = fields.String(required=True)
#     decimal_places = fields.Integer()
#     min_amount = fields.Float()
#     fee = fields.Float()
#     autosync = fields.Integer()
#
#
#
# class GateKlineSchema(ma.Schema):
#
#     pair_name = fields.String(required=True)
#     timestamp = fields.Integer()
#     volume = fields.Float()
#     close = fields.Float()
#     high = fields.Float()
#     low = fields.Float()
#     open = fields.Float()
#     group_sec = fields.Integer()
#     amount = fields.Float()
#     timestr = fields.String()

