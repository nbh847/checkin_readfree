# a checkin script for readfree
import requests
from config.setting import *
from bs4 import BeautifulSoup
from logger_setting import get_logger
import time
import datetime
from config.items import Readfree, db

logger = get_logger()


class RunReadfree(object):

    def __init__(self):

        self.headers = {'User-Agent': USERAGENT, 'Cookie': COOKIES, 'Host': HOST,
                        'Connection': 'keep-alive'}
        self.main_url = 'http://readfree.me/'
        self.login_url = 'http://readfree.me/accounts/profile/weasny/wish/'

    def get_content(self, retry=RETRY_TIMES):
        logger.info('开始爬取签到内容')
        # 查看建表信息，没有则新建表
        if Readfree.table_exists() == False:
            Readfree.create_table()

        # 签到后5s获取积分信息
        self.checkin()
        time.sleep(5)

        # 开始解析页面
        try:
            result = requests.get(self.login_url, headers=self.headers, timeout=50)
            logger.info('status code: {}'.format(result.status_code))
            logger.info('相应对象的url:{}'.format(result.url))
        except Exception as e:
            logger.error('错误详情：{}'.format(e))
            logger.info('获取本次响应失败,15s后继续尝试.')
            time.sleep(15)
            return self.get_content(retry=retry - 1)

        content = result.text
        soup = BeautifulSoup(content, 'lxml')

        # 获取剩余积分内容
        try:
            msg = soup.find('div', id='container').find_all('p')[1]
            points = msg.get_text().split(':')[2].split(',')[0].strip()
        except Exception as e:
            if retry < 1:
                logger.info('重试次数达到{}次，退出爬虫'.format(str(RETRY_TIMES)))
                return
            logger.exception('错误详情：{}'.format(e))
            logger.info('获取剩余积分内容失败,15s后继续尝试.')
            time.sleep(15)
            return self.get_content(retry=retry - 1)

        # 所有积分
        points = int(points.strip())
        # 当天的天数
        current_day = datetime.date.today()
        # 签到时间
        checkin_time = datetime.datetime.now()

        # 写入数据库
        try:
            Readfree.create(checkin_day=current_day,
                            points=points,
                            checkin_time=checkin_time)
            logger.info('积分{}已入库。'.format(points))
        except Exception as e:
            if str(e.args[0]) == '1062':
                logger.warning('重复数据，跳过。')
            else:
                logger.error('error: {}'.format(e))

        logger.info('剩余积分：{}'.format(points))
        logger.info('当天的天数: {}'.format(current_day))
        logger.info('签到时间: {}'.format(checkin_time))

    def checkin(self, retry=RETRY_TIMES):
        logger.info('开始签到...')
        try:
            result = requests.get(self.main_url, headers=self.headers, timeout=50)
            logger.info('status code: {}'.format(result.status_code))
            logger.info('响应对象的url:{}'.format(result.url))
            logger.info('签到成功')
        except Exception as e:
            if retry < 1:
                logger.info('重试次数达到{}次，退出爬虫'.format(str(RETRY_TIMES)))
                return
            logger.error('错误详情：{}'.format(e))
            logger.info('签到失败,15s后继续尝试.')
            time.sleep(15)
            return self.checkin(retry=retry - 1)

    def run(self, retry=RETRY_TIMES):
        # 判断数据库里是否有当天的签到数据,没有则签到
        while True:
            today = datetime.date.today()
            try:
                r = Readfree.select().where(Readfree.checkin_day == today).count()
                if r > 0:
                    logger.info('今天已签到.')
                else:
                    # 没签到，进行签到
                    self.get_content()
            except Exception as e:
                if str(e.args[0]) == '2013' or str(e.args[0]) == '2006' or str(e.args[0]) == '0':
                    if retry < 1:
                        logger.info('数据库重连次数到达{}次，退出。'.format(retry))
                        return
                    logger.exception('错误详情：{}'.format(e))
                    logger.warning('mysql连接断开，再次请求。')
                    db.close()
                    db.get_conn().ping(True)
                    return self.run(retry=retry - 1)
                else:
                    logger.exception('error message:{}'.format(e))
                    logger.info('select from databases failed.')

            # 每隔半小时检查一遍
            time.sleep(1800)


if __name__ == "__main__":
    rr = RunReadfree()
    rr.run()
