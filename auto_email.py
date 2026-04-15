import imaplib
import email
import yagmail
import time
import re

# ==========================================
# 配置区域：请根据实际情况修改以下参数
# ==========================================

# 接收邮件配置 (IMAP)
IMAP_HOST = "imap.qq.com"
IMAP_PORT = 993
IMAP_USER = "your_email@qq.com"
IMAP_PASS = "your_imap_password_or_auth_code"

# 发送邮件配置 (SMTP)
SMTP_HOST = "smtp.qq.com"
SMTP_PORT = 465
SMTP_USER = "your_email@qq.com"
SMTP_PASS = "your_smtp_password_or_auth_code"

# 目标收件人
TARGET_EMAIL = "target_email@example.com"

# ==========================================

def check_and_receive_emails():
    """
    连接IMAP服务器，检查未读邮件，
    如果邮件主题包含“故障”关键字，则进行通知（这里以打印代替），
    并将邮件标记为已读。
    """
    try:
        print("正在连接IMAP服务器...")
        conn = imaplib.IMAP4_SSL(host=IMAP_HOST, port=IMAP_PORT)
        conn.login(IMAP_USER, IMAP_PASS)
        
        # 选择收件箱
        conn.select("INBOX")
        
        # 搜索未读邮件 ('unseen')
        status, data = conn.search(None, 'unseen')
        
        if status != 'OK' or not data[0]:
            print("没有未读邮件。")
            conn.logout()
            return

        # data[0] 是一个包含所有未读邮件ID的字节串，用空格分隔
        mail_ids = data[0].decode().split(" ")
        
        for mailid in mail_ids:
            if not mailid:
                continue
                
            # 取回每一封未读邮件的内容
            _, maildata = conn.fetch(str(mailid), '(RFC822)')
            
            # 对每一封邮件的内容进行解析
            msg = email.message_from_string(maildata[0][1].decode('utf-8', errors='ignore'))
            
            # 取得标题
            subject_tmp = msg.get('subject')
            if not subject_tmp:
                continue
                
            # 为标题解码
            decoded_header = email.header.decode_header(subject_tmp)[0]
            sj_decode = decoded_header[0]
            encoding = decoded_header[1]
            
            if isinstance(sj_decode, bytes):
                if encoding:
                    subject = sj_decode.decode(encoding, errors='ignore')
                else:
                    subject = sj_decode.decode('utf-8', errors='ignore')
            else:
                subject = sj_decode
                
            print(f"收到未读邮件，主题: {subject}")
            
            # 使用正则表达式判断主题中是否包含“故障”关键字
            if re.search('故障', subject):
                print(f"【警告】检测到故障邮件！主题：{subject}。准备发送通知...")
                # 这里可以接入钉钉/企业微信机器人等通知逻辑
                # ...
                
            # 将邮件标记为已读，避免重复处理
            conn.store(mailid, '+FLAGS', '\\seen')
            print(f"邮件 {mailid} 已标记为已读。")
            
        conn.logout()
        
    except Exception as e:
        print(f"接收邮件时发生错误: {e}")

def send_email(subject, content, attachment_path=None):
    """
    使用 yagmail 发送邮件
    """
    try:
        print("正在连接SMTP服务器发送邮件...")
        # 初始化 yagmail 连接
        yag = yagmail.SMTP(
            user=SMTP_USER,
            password=SMTP_PASS,
            host=SMTP_HOST,
            port=SMTP_PORT
        )
        
        # 发送邮件
        if attachment_path:
            yag.send(to=TARGET_EMAIL, subject=subject, contents=content, attachments=attachment_path)
        else:
            yag.send(to=TARGET_EMAIL, subject=subject, contents=content)
            
        print("邮件发送成功！")
        
    except Exception as e:
        print(f"发送邮件时发生错误: {e}")

if __name__ == "__main__":
    # 1. 测试自动接收邮件并检查关键字
    print("--- 开始执行自动收信任务 ---")
    check_and_receive_emails()
    
    print("\n")
    
    # 2. 测试自动发送邮件
    print("--- 开始执行自动发信任务 ---")
    # 使用 f-string 格式化邮件内容
    report_data = "服务器CPU使用率正常，内存使用率正常。"
    mail_body = f"""
    你好：
        这是本周的系统巡检报告。
        
        巡检结果：
        {report_data}
        
        请查收！
    """
    
    # 取消注释以下代码以测试发送功能
    # send_email(subject="每周系统巡检报告", content=mail_body)
