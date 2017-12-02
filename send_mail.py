from email.mime.text import MIMEText
import smtplib
from config.setting import *
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from logger_setting import get_logger

logger = get_logger()

class SendMail(object):

    def __init__(self):
        # 输入Email地址和口令:
        self.from_addr = SEND_MAIL#input('你的email地址: ')
        self.password = SEND_PASSWORD#input('你的email密码: ')
        # 输入收件人地址:
        self.to_addr = REC_MAIL#input('收件人的email地址: ')
        # 输入SMTP服务器地址, 默认163邮箱:
        self.smtp_server = 'smtp.qq.com' # input('SMTP server: ')

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_mail(self, content):
        # 构造发送内容
        logger.info('开始发送邮件内容')
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = self._format_addr('火柴菌 <%s>' % self.from_addr)
        msg['To'] = self._format_addr('我的邮件 <%s>' % self.to_addr)
        msg['Subject'] = Header('来自火柴菌的问候……', 'utf-8').encode()

        # 发送邮件
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, 465)  # SMTP协议默认端口是25
            server.set_debuglevel(1)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, self.to_addr, msg.as_string())
            server.quit()
            logger.info('发送成功')
        except Exception as e:
            logger.info("邮件发送失败,失败原因：{}".format(e))

if __name__ == "__main__":
    s = SendMail()
    text = 'your are the shadow on my eyes,谢谢你.'
    s.send_mail(text)