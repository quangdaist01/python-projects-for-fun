import sys
sys.path.append(r"C:\\Users\quang\PycharmProjects\pythonProject3")
import feedparser
from emailsender import EmailSender

feed = feedparser.parse('https://vnexpress.net/rss/tin-moi-nhat.rss')
many_posts = feed.entries

def is_vaccine_doses_post(post):
    keywords = ["vaccine", "liều"]
    title = post.title
    return all(x in title for x in keywords)

posts_info = ""
for post in many_posts:
    if is_vaccine_doses_post(post):
        posts_info += post.title + "\n" + post.link + "\n"

EmailSender().make_message_with(subject="Tin tức vaccine", plain_text=posts_info).send_message_to()