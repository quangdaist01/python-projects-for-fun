from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Booking import BookingAPI
import config

SENDER = config.SENDER
PASSWORD = config.PASSWORD
RECEIVER = config.RECEIVER

# get courses information
RATES_SCORE = 7.5
MIN_NUM_RATING = 30
PRICE_LIMIT = 420000

url = config.url
with BookingAPI(url) as bot:
    bot.get_hotels_info(RATES_SCORE, MIN_NUM_RATING, PRICE_LIMIT, hotel_only=True)
    plain_text = bot.render_raw()
    html = bot.render_html()

part1 = MIMEText(plain_text, "plain")
part2 = MIMEText(html, "html")

msg = MIMEMultipart("alternative")  # create a message
msg.attach(part1)
msg.attach(part2)
# setup the parameters of the message
msg['From'] = SENDER
msg['To'] = RECEIVER
msg['Subject'] = "Thông tin các KS phù hợp"


with SMTP('smtp.gmail.com', 587) as sever:
    sever.starttls()
    sever.login(SENDER, PASSWORD)
    sever.send_message(msg)

# exit()


