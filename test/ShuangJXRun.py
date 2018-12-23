import numpy as np
from dao import GateDao
from dao.Models import GateKline, MyTrade

middle = 1000

short: int = 1000
long = 14400
SD = 0.005


kline_list = GateDao.query_all_objects(GateKline)

while short > 60:
    while long > short * 2:  # 6000:

        status = 0
        asset = 10000
        coin = 0
        times = 0

        shortList = []
        longList = []
        middleList = []

        for index, kline in enumerate(kline_list):

            price = float(kline.close)

            if index + 1 < len(kline_list):
                nextPrice = float(kline_list[index + 1].close)
            else:
                nextPrice = price

            shortList.append(price)
            longList.append(price)
            middleList.append(price)

            if len(shortList) > short: shortList.pop(0)
            if len(longList) > long: longList.pop(0)
            if len(middleList) > middle: middleList.pop(0)

            shortMean = float(np.mean(shortList))
            longMean = float(np.mean(longList))
            middleMean = float(np.mean(middleList))

            if len(longList) == long:
                if status == 0:
                    if shortMean > longMean * (1 + SD):
                        coin = asset / nextPrice * 0.998
                        asset = 0
                        status = 1
                        times += 1
                        print('%s - status : %d --- coin : %f --- asset : %f === all : %f' % (
                            kline.timestr, status, coin, asset, asset + coin * nextPrice))
                else:
                    if shortMean <= longMean * (1 + SD):
                        asset = coin * nextPrice * 0.998
                        coin = 0
                        status = 0
                        times += 1
                        print('%s - status : %d +++ coin : %f +++ asset : %f === all : %f' % (
                            kline.timestr, status, coin, asset, asset + coin * nextPrice))

        if times == 0 or times > 150: break

        trade = MyTrade()
        trade.pair_name = 'EOS_USDT'
        trade.short = short
        trade.long = long
        trade.lucre = asset + coin * nextPrice
        trade.times = times
        GateDao.insert_obj(trade)
        print(f"{kline.timestr} - short : {short:d} -- long : {long:d} === all : {asset + coin * nextPrice:f}")

        long -= 100


    short -= 20
    long = 14400
