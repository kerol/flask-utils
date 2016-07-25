# -*- coding: utf-8 -*-

from flask import Flask
import logging
import logging.handler

class DefaultConfig(object):
    LOGGING = {  # 配置日志
        'SMTP':{ #邮箱日志发送， 如果没有配置， 则不开启
                 'HOST': 'smtp.exmail.qq.com',  #smtp 服务器地址
                 'TOADDRS': ['my_email'], #smtp 收件人
                 'SUBJECT': u'Err from xxx', #smtp 主题
                 'USER': 'user_email', #smtp账号
                 'PASSWORD': 'password', #smtp账号密码
	},
        'FILE':{ #文件日志， 如果没有对应的配置，则不开启
                'PATH':'/path/to/log/file',
                'MAX_BYTES': 1024 * 1024 * 10, #单个文件大小默认10M
                'BACKUP_COUNT': 5, #文件滚动数量，默认5
	}
    }


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)
    app.config.from_object(config)
    register_logger(app)
    return app


class MySMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        try:
            import smtplib
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = "%s\r\n%s\r\n%s\r\n" % (IP, request.url, request.values.to_dict()) + self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            string.join(self.toaddrs, ","),
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def register_logger(app):
    config = app.config['LOGGING']
    config_mail = config.get('SMTP')
    if config_mail:  #如果存在smtp配置
        app.logger.info('Add SMTP Logging Handler')
        mail_handler = MySMTPHandler(
            config_mail['HOST'],  #smtp 服务器地址
            config_mail['USER'],  #smtp 发件人
            config_mail['TOADDRS'],  #smtp 收件人
            config_mail['SUBJECT'],  #smtp 主题
            (config_mail['USER'], config_mail['PASSWORD']))  #smtp账号密码
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    else:
        app.logger.info('No SMTP Config Found')

    config_file = config.get('FILE')
    if config_file:  #如果存在文件配置
        app.logger.info('Add File Logging Handler')
        file_handler = logging.handlers.RotatingFileHandler(
            config_file['PATH'],  #文件路径
            #但个文件大小 默认10M
            maxBytes=config_file.setdefault('MAX_BYTES', 1024 * 1024 * 10),
            #文件备份>数量 默认5个
            backupCount=config_file.setdefault('BACKUP_COUNT', 5),
        )
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s | %(levelname)s | %(funcName)s] %(message)s')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    else:
        app.logger.info('No FILE Config Found')

    logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app = create_app()
