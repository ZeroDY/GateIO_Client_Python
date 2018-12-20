import time

from matplotlib import pylab
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd
import seaborn as sns

sns.set_style('white')#设置背景为白色

from dao import GateDao
from dao.Models import GateKline


def get_price():
    '''
    获取 DataFrame 数据
    :return:
    '''
    kline_list = GateDao.query_klines(pair_name='EOS_USDT', num=50000)

    # kline_list = GateDao.query_all_objects(GateKline)#[39000:-1]
    return pd.DataFrame({
        'closePrice': [float(kline.close) for kline in kline_list],
        'tradeDate': [kline.timestr for kline in kline_list]
    })



#获取基金行情信息
security = get_price()
security['tradeDate']=pd.to_datetime(security['tradeDate'])
security.info()

# security['closePrice'].plot(grid=False,figsize=(12,8))
# sns.despine()

window_short = 200 #月均线,短期均线
window_long = 1500 #半年线,长期均线
SD = 0.005 #偏离度阈值5%

#numpy内置移动平均函数:rolling_mean
security['short_window'] = np.round(security['closePrice'].rolling(window_short).mean(),2)
security['long_window'] = np.round(security['closePrice'].rolling(window_long).mean(), 2)

print(security[['closePrice','short_window','long_window']].tail())

# #将三条线画到一张图上
# security[['closePrice','short_window','long_window']].plot(grid=False,figsize=(18,10))
# sns.despine()
# pylab.show()

#定义信号
#计算短期均线与长期均线的差s-1
security['s-1'] = security['short_window'] - security['long_window']
print(security['s-1'].tail)

#定义Regime为True,买入;Regime为False,卖出
security['Regime'] = np.where(security['s-1']>security['long_window']*SD,1,0)
security['Regime'].value_counts()

# #信号时间分布
# security['Regime'].plot(grid=False,lw=1.5,figsize=(12,8))
# pylab.ylim((-0.1,1.1))
# sns.despine()

security['Market'] = np.log(security['closePrice'] / security['closePrice'].shift(1))
security['Strategy'] = security['Regime'].shift(1) * security['Market']
security[['Market', 'Strategy', 'Regime']].tail()

security[['Market', 'Strategy']].cumsum().apply(np.exp).plot(grid=False, figsize=(18,10))
sns.despine()

textStr = ' num = %d \n window_short = %d \n window_long = %d \n SD = %f' \
          % (len(security), window_short, window_long, SD)
plt.text(0, 0.5, textStr, fontsize=15)

pylab.savefig('%s_%d_%d_%d_%f.png' % (time.strftime('%Y%m%d_%H:%M:%S',time.localtime(time.time())),len(security), window_short, window_long, SD))

pylab.show()