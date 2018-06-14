# 配置信息
import logging
from config.setting import *
from logging import basicConfig, getLogger

def get_logger():
    level_dic = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING,
                 'debug':logging.DEBUG, 'warn':logging.WARN}
    basicConfig(
        level=level_dic[MY_DEBUG_LEVEL],
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %Y-%m-%d %H:%M:%S',
    )
    logger = getLogger(__name__)
    return logger
