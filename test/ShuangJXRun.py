

import numpy as np
from dao import GateDao
from dao.Models import GateKline


middle = 1000

short = 180
long = 1500
SD = 0.005

shortList = []
longList = []
middleList = []

kline_list = GateDao.query_all_objects(GateKline)


while short < 1440:
    while long < 10000:

        status = 0

        asset = 10000

        coin = 0
        for kline in kline_list:

            price = float(kline.close)

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
                        coin = asset / price * 0.998
                        asset = 0
                        status = 1
                        # print('%s - status : %d --- coin : %f --- asset : %f === all : %f' % (
                        #     kline.timestr, status, coin, asset, asset + coin * price))
                else:
                    if shortMean < longMean * (1 + SD):
                        asset = coin * price * 0.998
                        coin = 0
                        status = 0
                        # print('%s - status : %d +++ coin : %f +++ asset : %f === all : %f' % (
                        #     kline.timestr, status, coin, asset, asset + coin * price))

        print('%s - short : %d -- long : %d === all : %f' % (
            kline.timestr, short, long, asset + coin * price))

        long = long+100
    short = short+30















