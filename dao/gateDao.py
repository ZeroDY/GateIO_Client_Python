

from sqlalchemy import and_
from manager.models import db, GateKline, GatePair, Account
import time

def query_all_objects(type):
    '''
    查询所有
    '''
    objs = db.session.query(type).all()
    return objs

def object_merge(element):
    '''
    单条 更新 或 插入
    '''
    flag = False
    try:
        db.session.merge(element)
        db.session.commit()
        flag = True
    except Exception as e:
        print(e, '\nerror element:' + element.getSelf() + '\t插入数据库失败,请查看主键以及唯一键约束!')
        db.session.rollback()
        db.session.flush()  # for resetting non-commited .add()
    finally:
        db.session.close()
    return flag



def insert_obj(  element):
    '''
    单条插入mysql数据库
    '''
    flag = False
    try:
        db.session.add(element)
        db.session.commit()
        flag = True
    except Exception as e:
        print(e, '\nerror element:' + element.getSelf() + '\t插入数据库失败,请查看主键以及唯一键约束!')
        db.session.rollback()
        db.session.flush()  # for resetting non-commited .add()
    finally:
        db.session.close()
    return flag

def insertBatch(element_list):
    '''
    批量插入数据库
    '''
    successNum = 0
    failNum = 0
    for element in element_list:
        if insert_obj(element):
            successNum += 1
        else:
            failNum += 1
    return {"success":successNum, "fail":failNum}


def insert_objects(element_list):
    '''
    批量插入mysql数据库
    '''
    flag = False
    try:
        db.session.bulk_save_objects(element_list)
        db.session.commit()
        flag = True
    except Exception as e:
        print(e, 'error element - 插入数据库失败')
        db.session.rollback()
        db.session.flush()
    finally:
        db.session.close()
    return flag



# ******************************** Pair ********************************
def query_pairs(autosync):
    pair_list = db.session.query(GatePair).filter(GatePair.autosync == autosync).all()
    return pair_list

def query_one_pair(pair_name):
    pair = db.session.query(GatePair).filter(GatePair.pair_name == pair_name).first()
    return pair



# ******************************** Kline ********************************

def update_klines(  dic_list, pair_name, group_sec):
    last_kline = None
    for element_dic in dic_list:
        kline = GateKline(pair_name=pair_name,
                          group_sec=group_sec)
        kline.set_timestamp(element_dic[0]) #timestamp = element_dic[0]
        kline.open = float(element_dic[1])
        kline.close = float(element_dic[2])
        kline.high = float(element_dic[3])
        kline.low = float(element_dic[4])
        kline.volume = float(element_dic[5])
        kline.amount = float(element_dic[6])

        if object_merge(kline):
            last_kline = kline

    return last_kline


def insert_klines(  dic_list, pair_name):
    if dic_list is not None:
        kline_list = []
        for kline_dic in dic_list:
            kline = GateKline(pair_name=pair_name,
                              group_sec=60)
            kline.set_timestamp(kline_dic[0])#.timestamp = kline_dic[0]
            kline.open = float(kline_dic[1])
            kline.close = float(kline_dic[2])
            kline.high = float(kline_dic[3])
            kline.low = float(kline_dic[4])
            kline.volume = float(kline_dic[5])
            kline.amount = float(kline_dic[6])
            kline_list.append(kline)

        if not len(kline_list) == 0:
            result =  insert_objects(kline_list)
            if result:
                return kline_list[-1]
            else:
                return None

def query_klines(  pair_name, num=1440, endtime = int(time.time())):
    '''

    :param pair_name:
    :param num:
    :param endtime:
    :return:
    '''
    if pair_name is not None:
        print('*******' + str(endtime))
        kline_list = db.session.query(GateKline).filter(and_(GateKline.pair_name == pair_name.upper(),
                                                             GateKline.timestamp <= endtime)).order_by(GateKline.timestamp.desc()).limit(num)
        return kline_list
    return []

def query_one_kline(self,pair_name, timestamp):
    '''

    '''
    if pair_name is not None:
        kline = db.session.query(GateKline).filter(and_(GateKline.pair_name == pair_name.upper(),
                                                        GateKline.timestamp <= timestamp)).order_by(GateKline.timestamp.desc()).first()
        return kline
    return None

def query_last_kline(  pair_name):
    '''

    '''
    if pair_name is not None:
        # app_context = db.app_context()
        # app_context.push()
        kline = db.session.query(GateKline).filter(GateKline.pair_name == pair_name.upper()).order_by(GateKline.timestamp.desc()).first()
        # app_context.pop()
        return kline
    return None


#******************************** Account ********************************
def query_account(  account_name, password):
    '''
    '''
    if account_name is not None and password is not None:
        account = db.session.query(Account).filter(and_(Account.account_name == account_name,
                                                             Account.password == password)).first()
        return account
    return None

