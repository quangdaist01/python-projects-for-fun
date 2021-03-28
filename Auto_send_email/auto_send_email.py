from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from crawl_data import TrungTamDayKem_Scrapy

# TODO: gửi thông tin về lớp dạy tiếng Anh phù hợp mỗi 1 giờ qua email

SENDER = 'sender_email@gmail.com'
PASSWORD = 'senders_password'
RECEIVER = 'receiver_email@gmail.com'

# setup the parameters of the message
msg = MIMEMultipart('alternative')  # create a message
msg['From'] = SENDER
msg['To'] = RECEIVER
msg['Subject'] = "Thông tin các khóa dạy thêm phù hợp"

# get courses information
response = TrungTamDayKem_Scrapy()
plain_text = response.find_courses(loc="Thủ Đức", gen='Sinh viên Nam')
html_data = response.find_courses(loc="Thủ Đức", gen='Sinh viên Nam', return_dict=True)

# turn these in to plain/html MIMEtext objects
part1 = MIMEText(plain_text, 'plain')

# making html part
# load html

# Change to where index.html is.
with open("C:/Users/quang/PycharmProjects/pythonProject3/Auto_send_email/mail-portfolio-master/index.html", encoding='utf-8') as html:
    template = Template(html.read())
html_renderred = template.render(location=html_data['location'],
                                 gender=html_data['gender'],
                                 courses=html_data['courses'])
part2 = MIMEText(html_renderred, 'html')
msg.attach(part1)
msg.attach(part2)


with SMTP('smtp.gmail.com', 587) as sever:
    sever.starttls()
    sever.login(SENDER, PASSWORD)
    sever.send_message(msg)


# setup the parameters of the message
msg = MIMEMultipart()  # create a message
msg['From'] = SENDER
msg['To'] = RECEIVER
msg['Subject'] = "Thông tin các khóa dạy thêm phù hợp"
# get courses information
data = TrungTamDayKem_Scrapy()
message = data.find_courses(loc="Thủ Đức", gen="Sinh viên Nam")
# add to the message body
msg.attach(MIMEText(message, 'plain'))

with SMTP('smtp.gmail.com', 587) as sever:
    sever.starttls()
    sever.login(SENDER, PASSWORD)
    sever.send_message(msg)
