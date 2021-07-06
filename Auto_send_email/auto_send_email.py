from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from crawl_data import TrungTamDayKem_Scrapy


SENDER = 'sender_email@gmail.com'
PASSWORD = 'senders_password'
RECEIVER = 'receiver_email@gmail.com'

# setup the parameters of the message
msg = MIMEMultipart('alternative')  # create a message
msg['From'] = SENDER
msg['To'] = RECEIVER
msg['Subject'] = "Thông tin các khóa dạy thêm phù hợp"

# get courses information
response = TrungTamDayKem_Scrapy(loc="Thủ Đức", gen='Sinh viên Nam')
plain_text = response.render_raw()
html_text = response.render_html()

# turn these in to plain/html MIMEtext objects
part1 = MIMEText(plain_text, 'plain')
part2 = MIMEText(html_text, 'html')

# making html part
msg.attach(part1)
msg.attach(part2)


with SMTP('smtp.gmail.com', 587) as sever:
    sever.starttls()
    sever.login(SENDER, PASSWORD)
    sever.send_message(msg)
