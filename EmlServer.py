# -*- coding: utf-8 -*-

import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import LoggerFactory

# what is this code doing?
# 이 코드는 이메일을 보내기 위한 SMTP 서버와 연결하고, 이메일 내용을 작성하여 전송하는 기능을 제공합니다.
# what is SMTP server?
# SMTP 서버는 이메일을 전송하기 위한 프로토콜인 Simple Mail Transfer Protocol을 사용하는 서버입니다.
# how can i install it?
# SMTP 서버는 일반적으로 이메일 서비스 제공업체에서 제공하며, 별도로 설치할 필요는 없습니다.
# where is email-provider?
# 이메일 제공업체는 Gmail, Yahoo, Outlook 등 다양한 서비스가 있습니다.
# if i want to use my own SMTP server, how can i do that?
# 자신의 SMTP 서버를 사용하려면, SMTP 서버 소프트웨어(예: Postfix, Sendmail)를 설치하고 설정해야 합니다.
# what is the difference between Postfix and Sendmail?
# Postfix와 Sendmail은 모두 이메일 전송을 위한 SMTP 서버 소프트웨어입니다. Postfix는 Sendmail보다 더 간단하고 안전한 설정을 제공하며, 성능이 뛰어납니다.
# if i install Postix in my server is it costly?
# Postfix는 오픈 소스 소프트웨어로 무료로 사용할 수 있습니다. 그러나 서버 운영 비용은 별도로 발생할 수 있습니다.
SENDER = "bbumbbai94@gmail.com"
logger = LoggerFactory.loggerFactory()

class EmlServer:
    def sendMail(self, gubun, authNumber, email):
        try:
            # smtp = smtplib.SMTP("email-smtp.ap-northeast-2.amazonaws.com", 587)
            # SMTPホスト: "smtp.gmail.com" が正しい。メールアドレスではない。
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            smtp.login("bbumbbai94@gmail.com", "gzzt flof yrby oeyj")
            logger.info("SMTP SERVER CONNECTION SUCCESS")

            msg = self.make_template(gubun, authNumber, email)

            smtp.sendmail(SENDER, [email], msg.as_string())
            logger.info("SEND EMAIL SUCCESS :: {g}, {e}, {a}".format(g=gubun, e=email, a=authNumber))
        except Exception as e:
            logger.error("SEND EMAIL ERROR :: {g}, {e}, {a}".format(g=gubun, e=email, a=authNumber))
            logger.error(e)
            return 'fail'
        finally:
            smtp.quit()
            logger.info("SMTP SERVER QUIT SUCCESS")

        return 'success'

    def make_template(self, gubun, authNumber, email):
        if gubun == 'join':
            gubun = '新規登録'
        else:
            gubun = '情報変更'
        subject = '[TravelPlaner] メール認証番号のご案内'
        senderName = 'TravelPlaner'

        fp = open('AuthNumberInfo.template', 'r', encoding='utf-8')
        msg = MIMEText(fp.read().format(gubun=gubun, authNumber=authNumber), 'html', 'utf-8')
        fp.close()

        msg['Subject'] = subject
        msg['From'] = formataddr((str(Header(senderName, 'utf-8')), SENDER))
        msg['To'] = email

        return msg

    def sendMail_qnaReply(self, data):
        try:
            subject = '(안내)' + data[0] + '님의 문의에 대한 답변메일입니다.'
            senderName = '뿜빠이'
            now = time
            agree_date = str(now.localtime().tm_year) + '년' + str(now.localtime().tm_mon) + '월' + str(
                now.localtime().tm_mday) + '일'
            # 문의 경로에 따라 메일 텍스트 다름
            if data[6] == 'Y':
                gubun_text = '1:1문의/칭찬'
            else:
                gubun_text = '문의/칭찬'
            # 전화문의의 경우 문의내용란 없음
            if data[6] == 'P':
                template = 'qnaReply_P.template'
            else:
                template = 'qnaReply.template'
            fp = open(template, 'r', encoding='utf-8')
            msg = MIMEText(fp.read().format(gubun_text=gubun_text, subject=data[2].encode('utf-8'),
                                            content=data[3].encode('utf-8'), response=data[5].encode('utf-8'),
                                            agree_date=agree_date, receiver=data[1].encode('utf-8')), 'html', 'utf-8')
            fp.close()

            msg['Subject'] = subject
            msg['From'] = formataddr((str(Header(senderName, 'utf-8')), SENDER))
            msg['To'] = data[1]

            #what is this code doing?
            # 이 코드는 SMTP 서버에 연결하고, 이메일을 보내는 기능을 수행합니다.
            # how does it work?
            # SMTP 서버에 연결하고, TLS 암호화를 시작합니다.
            # what is SMTP's default port?
            # SMTP의 기본 포트는 25번입니다. 그러나 TLS 암호화를 사용하기 위해 587번 포트를 사용합니다.
            # what is TLS when STMP is used?
            # TLS는 Transport Layer Security의 약자로, 데이터 전송 시 보안을 제공하는 프로토콜입니다.
            # what is TLS's default port?
            # TLS의 기본 포트는 443번입니다. 그러나 SMTP에서는 587번 포트를 사용합니다.
            # what is TLS expecally doing for SMTP?
            # TLS는 SMTP 서버와 클라이언트 간의 통신을 암호화하여 데이터의 기밀성과 무결성을 보장합니다.
            # describe it more detail
            # TLS는 SMTP 서버와 클라이언트 간의 통신을 암호화하여 데이터가 전송되는 동안 도청이나 변조를 방지합니다.
            # how does it work?
            # TLS는 대칭키 암호화를 사용하여 데이터를 암호화하고, 비대칭키 암호화를 사용하여 키 교환을 수행합니다.
            # then how can i update this code? i don't use aws but i use ubuntu server
            # To update the code for your own SMTP server, you need to change the SMTP server address and port number in the smtplib.SMTP() function.

            # smtp = smtplib.SMTP("email-smtp.ap-northeast-2.amazonaws.com", 587)
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            # where is this parameter using for?
            # 이 매개변수는 SMTP 서버에 로그인하기 위한 사용자 이름과 비밀번호입니다.
            # when i set up my own SMTP server, i didn't set my account
            # 자신의 SMTP 서버를 설정할 때 사용자 이름과 비밀번호를 설정해야 합니다. 일반적으로 이메일 주소와 비밀번호를 사용합니다.
            # how can i know my SMTP server's account?
            # smtp.login("AKIAQG4CNHYRKVUW7CI5", "BD0YzKi8JawEO6+vbQg68mupqAkSHdjnPaPzYmAdQ+Gb")
            smtp.login("bbumbbai94@gmail.com", "gzzt flof yrby oeyj")
            logger.info("SMTP SERVER CONNECTION SUCCESS")
            smtp.sendmail(SENDER, [data[1]], msg.as_string())
            logger.info("SEND EMAIL SUCCESS :: sendMail_qnaReply, {e}, cs idx : {i}".format(e=data[1], i=data[7]))
            result = 'success'
        except Exception as e:
            logger.error("SEND EMAIL ERROR :: {e}, cs idx : {i}".format(e=data[1], i=data[7]))
            logger.error(e)
            result = 'fail'
        finally:
            smtp.quit()
            fp.close()
            logger.info("SMTP SERVER QUIT SUCCESS")

        return result