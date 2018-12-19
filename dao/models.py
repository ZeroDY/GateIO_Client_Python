#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine
from sqlalchemy.dialects.mysql import DOUBLE, DATETIME


ma = Marshmallow()

db = SQLAlchemy()
db.session.configure(bind=engine, autoflush=False, expire_on_commit=False)

class Account(db.Model):
    '''
    账户信息
    '''
    __tablename__ = 'account'

    account_name = db.Column(db.String(64), primary_key=True, nullable=False, index=True)
    password = db.Column(db.String(64), nullable=False) # 密码
    permission = db.Column(db.Integer, default=0)

    def __init__(self, **params):
        self.__dict__.update(params)



class GatePair(db.Model):
    '''
    交易配对
    '''
    __tablename__ = 'gate_pair'

    pair_name = db.Column(db.String(64), primary_key=True, nullable=False, index=True)
    decimal_places = db.Column(db.Integer) # 价格精度
    min_amount = db.Column(DOUBLE) # 最小下单量
    fee = db.Column(DOUBLE) # 交易费 百分数
    autosync = db.Column(db.Integer, default=0)

    def __init__(self,pair_name):
        self.pair_name = pair_name



class GateKline(db.Model):
    '''
    交易 K线
    '''
    __tablename__ = 'gate_kline'
    __table_args__ = (
        db.PrimaryKeyConstraint('pair_name', 'timestamp', 'group_sec'),
    )

    pair_name = db.Column(db.String(64), nullable=False, index=True)
    timestamp = db.Column(db.Integer(), nullable=False, index=True) # 时间戳
    volume = db.Column(DOUBLE, nullable=False) #  交易量
    close = db.Column(DOUBLE, nullable=False) #  收盘价
    high = db.Column(DOUBLE, nullable=False) #  最高价
    low = db.Column(DOUBLE, nullable=False) #  最低价
    open = db.Column(DOUBLE, nullable=False) #  开盘价
    group_sec = db.Column(db.Integer, nullable=False, index=True) # 时间间隔 秒数
    amount = db.Column(DOUBLE) # amount
    timestr = db.Column(db.String(64))

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


# ************************************************************************


class AccountSchema(ma.Schema):
    account_name = fields.String(required=True)
    password = fields.String(required=True)
    permission = fields.Integer()
    # pairs = fields.List()


class GatePairSchema(ma.Schema):
    pair_name = fields.String(required=True)
    decimal_places = fields.Integer()
    min_amount = fields.Float()
    fee = fields.Float()
    autosync = fields.Integer()



class GateKlineSchema(ma.Schema):

    pair_name = fields.String(required=True)
    timestamp = fields.Integer()
    volume = fields.Float()
    close = fields.Float()
    high = fields.Float()
    low = fields.Float()
    open = fields.Float()
    group_sec = fields.Integer()
    amount = fields.Float()
    timestr = fields.String()

