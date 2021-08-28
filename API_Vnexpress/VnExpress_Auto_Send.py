import sys
sys.path.append(r"C:\\Users\quang\PycharmProjects\pythonProject3")
import feedparser
from emailsender import EmailSender
import re

vnexpress_feed = feedparser.parse('https://vnexpress.net/rss/tin-moi-nhat.rss')
laodong_feed = feedparser.parse('https://laodong.vn/rss/home.rss')
tuoitre_feed = feedparser.parse('https://vnexpress.net/rss/tin-moi-nhat.rss')
many_posts = vnexpress_feed.entries + laodong_feed.entries + tuoitre_feed.entries

def is_vaccine_doses_post(post):
    doses_keywords = ["triệu", "ngàn"]
    title = post.title.split()
    if "vaccine" in title:
        for i in range(len(title) - 1):
            if title[i].isdigit() and title[i + 1] in doses_keywords:
                return True
    return False

posts_info = ""
for post in many_posts:
    if is_vaccine_doses_post(post):
        posts_info += post.title + "\n" + post.link + "\n"

EmailSender().make_message_with(subject="Tin tức vaccine", plain_text=posts_info).send_message_to()
