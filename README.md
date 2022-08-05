# noreply-vercel
no-reply email sender for vercel

Developed for Yandex Mail, but still customizable.

为Yandex邮箱设计的邮件发送Webhook，可部署在Vercel上，基于Flask。

需要配置的环境变量：

`YANDEX_MAIL_USER` 发信邮箱
`YANDEX_MAIL_PWD` 邮箱登录密码/应用密码
`API_TOKEN` 任意随机字符串，用于调用此接口时鉴权
