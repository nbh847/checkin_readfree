import peewee as pw
from config.setting import *

db = pw.MySQLDatabase(MYSQL_DB_NAME, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                   charset=MYSQL_CHARSET)

# 每天readfree的签到信息
class Readfree(pw.Model):
    checkin_day = pw.DateField(primary_key=True, verbose_name="签到时间,精度为天", default='1970-01-01')
    points = pw.IntegerField(verbose_name="积分分数", default=False)
    checkin_time = pw.DateTimeField(verbose_name="创建时间", default='1970-01-01')

    class Meta:
        database = db
