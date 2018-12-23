import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from dao import GateDao
from dao.Models import GateKline, MyTrade


trade_list = GateDao.query_all_objects(MyTrade)
X = []
Y = []
Z = []
for trade in trade_list:
    X.append(float(trade.short))
    Y.append(float(trade.long))
    Z.append(float(trade.lucre))



# =============================================== 1 ======================================================
#
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(X, Y, Z, cmap='jet')
# ax.scatter(X, Y, Z,  cmap='jet')   # 散点图

ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('y', fontsize=14)
ax.set_zlabel('z', fontsize=14)

plt.show()


#=============================================== 2 ======================================================
#
# import random
# import matplotlib as mpl
# import matplotlib.dates as mdates
# from mpl_toolkits.mplot3d import Axes3D
#
# X={str:[]}
# for trade in trade_list:
#     # if int(trade.short) in X.keys():
#     key = str(trade.short)
#     if len(key) >0:
#         if key in X.keys():
#             X[key].append(trade)
#         else:
#             y = [trade]
#             X[key] = y
#
#
# mpl.rcParams['font.size'] = 10
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for key, trades in X.items():
#     if len(trades) > 0:
#         xs = [float(trade.long) for trade in trades]
#         ys = [float(trade.lucre) for trade in trades]
#         color = plt.cm.Set2(random.choice(range(plt.cm.Set2.N)))
#         ax.bar(xs, ys, zs=8000, zdir='y', color=color, alpha=0.8)
#
# ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(xs))
# ax.yaxis.set_major_locator(mpl.ticker.FixedLocator(ys))
# # ax.set_xlabel('Month')
# # ax.set_ylabel('Year')
# # ax.set_zlabel('Sales Net [usd]')
# plt.show()

