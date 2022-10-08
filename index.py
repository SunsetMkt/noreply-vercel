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


def send_mail(receiver, mail_title, mail_content, ifHTML):
    # msg = MIMEText(mail_content, "plain", 'utf-8')
    if ifHTML:
        msg = MIMEText(mail_content, "html", 'utf-8')
    else:
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
        return "success", True
    except Exception as e:
        import traceback
        return str(traceback.format_exc()), False


@app.route('/', methods=['GET'])
def home():
    return flask.render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    # POST /send
    # {'to':'your_email','subject':'your_subject','body':'your_body','token':'your_token','html':'0'}
    if flask.request.method == 'POST':
        # Get json from request
        data = flask.request.get_json()
        # Try to parse json
        try:
            to = data['to']
            subject = data['subject']
            body = data['body']
            token = data['token']
            html = data['html']
        except Exception as e:
            return flask.jsonify({'code': 400, 'msg': 'missing params'}), 400
    else:
        return flask.jsonify({'code': 400, 'msg': 'only support POST method'}), 400
    # Check token
    if token != api_token:
        return flask.jsonify({'code': 403, 'msg': 'token error'}), 403
    if str(html) == '1':
        html = True
    else:
        html = False
    # Send mail
    msg, status = send_mail(to, subject, body, html)
    if status:
        return flask.jsonify({'code': 200, 'msg': 'success'}), 200
    else:
        return flask.jsonify({'code': 500, 'msg': msg}), 500
