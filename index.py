import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText

import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = False

# Yandex邮箱smtp服务器
host_server = 'smtp.yandex.com'
# Yandex邮箱smtp服务器端口
ssl_port = '465'
# 用户名
user = os.environ.get('YANDEX_MAIL_USER')
# 密码（应用密码，相当于token）
pwd = os.environ.get('YANDEX_MAIL_PWD')
# 发件人的邮箱
sender_mail = os.environ.get('YANDEX_MAIL_USER')
# api token
api_token = os.environ.get('API_TOKEN')


def send_mail(receiver, mail_title, mail_content):
    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_mail
    msg["To"] = receiver
    try:
        # ssl登录
        smtp = smtplib.SMTP_SSL(host_server, ssl_port)
        smtp.ehlo(host_server)
        smtp.login(user, pwd)
        smtp.sendmail(sender_mail, receiver, msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print(str(e))
        return False


@app.route('/', methods=['GET'])
def home():
    return flask.render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    # /send?to=your_email&subject=your_subject&body=your_body&token=your_token
    to = flask.request.args.get('to')
    subject = flask.request.args.get('subject')
    body = flask.request.args.get('body')
    token = flask.request.args.get('token')
    if token != api_token:
        return 'token error'
    # Check missing
    if not to or not subject or not body:
        return 'missing'
    if send_mail(to, subject, body):
        return 'success'
    else:
        return 'fail'
