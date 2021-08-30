import sys

sys.path.append(r"C:\\Users\quang\PycharmProjects\pythonProject3")
import feedparser
from emailsender import EmailSender
import datetime
import re


def is_vaccine_doses_post(post):
    doses_keywords = ["triệu", "ngàn"]
    title = post.title.split()
    if "vaccine" in title:
        for i in range(len(title) - 1):
            if title[i].isdigit() and title[i + 1] in doses_keywords:
                return True
    return False


def get_published_time(post):
    time = post.published
    time = re.sub("\s[+-]\d{4}", "", time)  # Remove UTC offset
    return datetime.datetime.strptime(time, "%a, %d %b %Y %X")  # Example: Sun, 29 Aug 2021 18:55:44


#  This make sure the code won't 2 emails with the same post when I set running interval = lookbehind time
def is_recently_published(post, minutes_ago=15):
    current_time = datetime.datetime.now()
    published_time = get_published_time(post)
    duration = datetime.timedelta(minutes=minutes_ago)
    return current_time - published_time < duration


if __name__ == "__main__":
    vnexpress_feed = feedparser.parse('https://vnexpress.net/rss/tin-moi-nhat.rss')
    laodong_feed = feedparser.parse('https://laodong.vn/rss/home.rss')
    tuoitre_feed = feedparser.parse('https://vnexpress.net/rss/tin-moi-nhat.rss')
    many_posts = vnexpress_feed.entries + laodong_feed.entries + tuoitre_feed.entries

    vaccine_posts = ""
    for post in many_posts:
        if is_vaccine_doses_post(post) and is_recently_published(post):
            vaccine_posts += post.title + "\n" + post.link + "\n"

    if vaccine_posts:
        EmailSender().make_message(subject="Tin tức vaccine", plain_text=vacine_posts).send_message()
