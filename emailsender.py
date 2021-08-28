import config
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, *, sender=config.SENDER, password=config.PASSWORD):
        self.sender = sender
        self.password = password
        self.message = MIMEMultipart("alternative")

    def make_message(self, *, subject="Subject", plain_text, html_text=None):
        if plain_text is None:
            plain_text = "No text found"
        self.message['From'] = self.sender
        self.message['Subject'] = subject
        self.message.attach(MIMEText(plain_text, "plain"))
        return self

    def send_message(self, *, TO=config.RECEIVER):
        self.message['To'] = TO
        with SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(self.message)
        print("Send successfully!")
        return self


if __name__ == "__main__":
    bot = EmailSender()
    bot.make_message(subject="Hi", plain_text="Tui la Dai")
    bot.send_message()
