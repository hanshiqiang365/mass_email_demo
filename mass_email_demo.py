#author:hanshiqiang365

import smtplib
from email.mime.text import MIMEText
from email.header import Header

while True:
    # 邮件登录信息
    email_user = '你的qq邮箱'
    email_password = '你的授权码'

    # 读取收件人列表
    with open('qq.txt', 'r') as file:
        recipient_list = file.readlines()

    # 去除每个收件人邮箱地址各自行末的换行符和空白字符
    recipient_list = [recipient.strip() for recipient in recipient_list]

    # 读取邮件正文和主题
    with open('content.txt', 'r', encoding='utf-8') as file:
        body_text = file.read().strip()
    with open('title.txt', 'r', encoding='gbk') as file:
        title_text = file.read().strip()

    # 创建邮件内容
    msg = MIMEText(body_text, _subtype='html', _charset='utf-8')
    msg['From'] = email_user
    msg['Subject'] = Header(title_text.encode('utf-8'), 'utf-8').encode()

    # 连接到SMTP服务器
    with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
        server.login(email_user, email_password)

        # 发送邮件给每个收件人
        for recipient in recipient_list:
            try:
                server.sendmail(email_user, recipient, msg.as_string())
                print(f'[*] 邮件已成功发送到 {recipient}')
            except smtplib.SMTPDataError as e:
                if e.smtp_code == 550:
                    print(f'[!] 邮件发送到 {recipient} 失败：{e.smtp_error}')
                elif e.smtp_code == 501:
                    print(f'[!] 邮件发送到 {recipient} 失败：收件人地址存在语法错误')
                else:
                    print(f'[!] 发送邮件时发生错误：{e}')

    print('[*] 所有邮件均已发送完毕。')

    # 显示提示消息，并等待用户输入yes或no以确定是否发送更多电子邮件
    answer = input("是否要再次发送电子邮件(yes/no)? ")

    # 如果用户选择“no”，则退出程序，否则继续发送电子邮件
    if answer.lower() == 'no':
        print("程序已经关闭。")
        break
    else:
        continue

#官网:https://mail.qq.com/
