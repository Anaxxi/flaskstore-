from app.extensions import mail

from flask_mail import Message
from flask import current_app, render_template



def send_mail(subject, to, template, **kwargs):
    msg = Message(subject=subject, recipients=[to], sender=current_app.config["MAIL_SENDER"])

    msg.body = render_template(f"mails/{template}.txt", **kwargs)
    msg.body = render_template(f"mails/{template}.html", **kwargs)
    mail.send(msg)
