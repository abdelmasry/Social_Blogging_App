from threading import Thread
from flask_mail import Message
from . import mail
from flask import render_template, current_app


"""
msg = Message("test email", sender="you@example.com", recipients=["you@example.com"])
msg.body = "This is the plain text body"
msg.html = "This is the <b>HTML</b> body"
with app.app_context():
    mail.send(msg)"""

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        current_app.config["FLASKY_MAIL_SUBJECT_PREFIX"] + subject,
        sender=current_app.config["FLASKY_MAIL_SENDER"],
        recipients=[to],
    )
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr