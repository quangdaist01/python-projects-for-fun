# Avoid import error when running the the terminal
# Add module paths outside of the current folder
import sys
sys.path.append(r"C:\\Users\quang\PycharmProjects\pythonProject3")
from facebook_scraper import get_posts
from datetime import datetime
from emailsender import EmailSender


def is_latest(post):
    return post['time'] == datetime.now()


email_bot = emailsender.EmailSender()
for post in get_posts('tuoitre.uit', pages=2):
    if is_latest(post):
        EmailSender().make_message(subject="[Tuổi trẻ UIT]", plain_text=post['text']).send_message()

# exit()
# ==============