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
with BookingAPI(RATES_SCORE, MIN_NUM_RATING, PRICE_LIMIT, hotel_only=True) as bot:
    bot.getFilteredHotels(url)
    bot.prettifyTerminal()
    plain_text = bot.renderRaw()
    html = bot.renderHtml()

text_part = MIMEText(plain_text, "plain")
html_part = MIMEText(html, "html")

message = MIMEMultipart("alternative")  # create a message
message.attach(text_part)
message.attach(html_part)
# setup the parameters of the message
message['From'] = SENDER
message['To'] = RECEIVER
message['Subject'] = "[Booking] Các KS phù hợp"


with SMTP('smtp.gmail.com', 587) as sever:
    sever.starttls()
    sever.login(SENDER, PASSWORD)
    sever.send_message(message)

# exit()


