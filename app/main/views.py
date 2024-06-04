from datetime import datetime
from threading import Thread
from flask import render_template, session, redirect, url_for
from flask_login import login_required
from . import main
from .forms import NameForm
from .. import db, mail, Message
from ..models import User


@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
        # if app.config["FLASKY_ADMIN"]:
        #    send_email(
        #       main.config["FLASKY_ADMIN"], "New User", "mail/new_user", user=user
        #  )
        else:
            session["known"] = True
        session["name"] = form.name.data
        form.name.data = ""
        return redirect(url_for("main.index"))

    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
    )


@main.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)


"""
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
"""

"""
def send_email(to, subject, template, **kwargs):
    msg = Message(
        app.config["FLASKY_MAIL_SUBJECT_PREFIX"] + subject,
        sender=app.config["FLASKY_MAIL_SENDER"],
        recipients=[to],
    )
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    thr = Thread(target=send_async_email, args=[main, msg])
    thr.start()
    return thr
"""


@main.route("/secret")
@login_required
def secret():
    return "Only authenticated users are allowed!"
