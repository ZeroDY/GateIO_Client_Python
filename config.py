#!/usr/bin/python
# -*- coding: utf-8 -*-

# import os

# You need to replace the next values with the appropriate values for your configuration
# basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:deyi@233mysql@localhost:3306/TestDB"

jpush_app_key = "68b8f5269319e0a9bd74373e"
jpush_master_secret = "b78cbe1b4f0a4586a7665838"

JOBS = [  # 任务列表
    # {  # 任务字典（细节）
    #     'id': 'job1',
    #     'func': '__main__:print_hello',
    #     'args': (1, 2),
    #     'trigger': 'cron',
    #     'hour': 00,
    #     'minute': 4
    # },
    {  # 第二个任务字典
        'id': 'kline_monitoring',
        'func': '__main__:kline_monitoring',
        # 'args': (3, 4),
        'trigger': 'interval',
        'seconds': 10,
    }
]
