from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm
# from ..email import send_email
from .. import db
from ..models import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    # Description:-
        * To log a user in, the function begins by loading
            the user from the database using the email provided with the form.

        * If a user with the given email address exists, then its verify_password()
            method is called with the password that also came with the form.

        * If the password is valid, Flask-Login's login_user() function
            is invoked to record the user as logged in for the user session.

        * The login_user() function takes the user to log in and an optional “remember me” Boolean,
            which was also submitted with the form.

            * A value of False for this argument causes
                the user session to expire when the browser window is closed,
                so the user will have to log in again next time.
            * A value of True causes a long-term cookie to be set in the user's browser,
                which Flask-Login uses to restore the user session.

        * The optional REMEMBER_COOKIE_DURATION configuration option
            can be used to change the default one-year duration for the remember cookie.

    # Mechanism:-
        * In accordance with the Post/Redirect/Get pattern,
            the POST request that submitted the login credentials ends with a redirect,
            but there are two possible URL destinations.

        * If the login form was presented to the user to prevent unauthorized access
            to a protected URL the user wanted to visit, then Flask-Login will have saved
            that original URL in the next query string argument,
            which can be accessed from the request.args dictionary.

        * If the next query string argument is not available,
            a redirect to the home page is issued instead.

        * The URL in next is validated to make sure it is a relative URL,
            to prevent a malicious user from using this argument to redirect unsuspecting users to another site.

    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")

            if next is None or not next.startswith("/"):
                next = url_for("main.index")

            return redirect(next)
        flash("Invalid username or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()

        """token = user.generate_confirmation_token()
        send_email(
            user.email,
            "Confirm Your Account",
            "auth/email/confirm",
            user=user,
            token=token,
        )
        flash("A confirmation email has been sent to you by email.")
        """
        flash("You can login now.")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))

    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.index"))


"""
When a before_request or before_app_request callback returns a response or a redirect, 
Flask sends that to the client without invoking the view function associated with the request. 
This effectively allows these callbacks to intercept a request when necessary.
"""


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        # if request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':  return redirect(url_for('auth.unconfirmed'))


"""
@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated
        and not current_user.confirmed # Not Implemented yet!
        and request.blueprint != "auth"
        and request.endpoint != "static"
    ):
        return redirect(url_for("auth.unconfirmed"))

@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))

    return render_template("auth/unconfirmed.html")
"""
