import time

from matplotlib import pylab
import numpy as np
from datetime import datetime
import pandas as pd
import seaborn as sns

sns.set_style('white')  # 设置背景为白色

from dao import GateDao
from dao.Models import GateKline, MyTrade


def get_price(pair_name):
    '''
    获取 DataFrame 数据
    :return:
    '''
    # kline_list = GateDao.query_klines(pair_name='EOS_USDT', num=50000)

    kline_list = GateDao.query_all_klines(pair_name=pair_name)
    # kline_list = GateDao.query_all_objects(GateKline)#[39000:-1]
    return pd.DataFrame({
        'closePrice': [float(kline.close) for kline in kline_list],
        'tradeDate': [kline.timestr for kline in kline_list]
    })


def lucreImage(security, pair_name, isShow=False, window_short=260, window_long=1020, SD=0.005):
    # 获取基金行情信息
    # security = get_price(pair_name)
    security['tradeDate'] = pd.to_datetime(security['tradeDate'])
    print(
        '+++++++++++++++++++++++++++++++++++++++++>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(security.info())

    # security['closePrice'].plot(grid=False,figsize=(12,8))
    # sns.despine()

    # window_short = 260  # 月均线,短期均线
    # window_long = 1020  # 半年线,长期均线
    # SD = 0.005  # 偏离度阈值5%

    # numpy内置移动平均函数:rolling_mean
    security['short_window'] = np.round(security['closePrice'].rolling(window_short).mean(), 9)
    security['long_window'] = np.round(security['closePrice'].rolling(window_long).mean(), 9)

    print('--------------------------------------------------------')
    print(security[['closePrice', 'short_window', 'long_window']].tail(n=10))

    # #将三条线画到一张图上
    # security[['closePrice','short_window','long_window']].plot(grid=False,figsize=(18,10))
    # sns.despine()
    # pylab.show()

    # 定义信号
    # 计算短期均线与长期均线的差s-1
    security['s-1'] = security['short_window'] - security['long_window']
    print('--------------------------------------------------------')
    print(security[['closePrice', 'short_window', 'long_window', 's-1']].tail(n=10))

    # 定义Regime为True,买入;Regime为False,卖出
    security['Regime'] = np.where(security['s-1'] > security['long_window'] * SD, 1, 0)
    security['Regime'].value_counts()

    # #信号时间分布
    # security['Regime'].plot(grid=False,lw=1.5,figsize=(12,8))
    # pylab.ylim((-0.1,1.1))
    # sns.despine()

    security['Market'] = np.log(security['closePrice'] / security['closePrice'].shift(1))
    security['Strategy'] = security['Regime'].shift(1) * security['Market']

    print('--------------------------------------------------------')
    print(security[['short_window', 'long_window', 's-1', 'Regime', 'Market', 'Strategy']].tail(n=10))

    security[['Market', 'Strategy']].cumsum().apply(np.exp).plot(grid=False, figsize=(18, 10))
    sns.despine()

    lucre = float(security[['Strategy']].cumsum().apply(np.exp).iat[-1, -1] * 10000)
    new_trade = MyTrade()
    new_trade.pair_name = pair_name
    new_trade.short = window_short
    new_trade.long = window_long
    new_trade.middle = 1
    new_trade.lucre = lucre
    new_trade.times = -1 if 'EOS' in pair_name else -2
    print('========= ', new_trade.pair_name, new_trade.lucre)
    GateDao.insert_obj(new_trade)

    pylab.ylim((0.5, 2.0))

    textStr = ' pair_name = %s \n num = %d \n window_short = %d \n window_long = %d \n SD = %f \n %.2f' \
              % (pair_name, len(security), window_short, window_long, SD, lucre)
    pylab.text(0, 0.5, textStr, fontsize=15)
    pylab.savefig('./img/%s_%d_%d_%d_%f_%s.png' % (
    pair_name, len(security), window_short, window_long, SD, '001' if 'EOS' in pair_name else '002'))

    if isShow: pylab.show()

    pylab.close()


pair_list = ['LTC_USDT', 'XRP_USDT', 'XMR_USDT', 'NEO_USDT', 'TRX_USDT', 'OMG_USDT', 'QTUM_USDT', 'DOGE_USDT',
             'EOS_USDT']  #

trade_list = GateDao.query_all_objects(MyTrade)

for pair_name in pair_list:
    security = get_price(pair_name)

    for trade in trade_list:
        lucreImage(security, pair_name, window_short=trade.short, window_long=trade.long)

