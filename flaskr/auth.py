import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# create Blueprint named "auth"
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    # start validating the input
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # validate that username and password are not empty
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        # If validation succeeds,
        # insert the new user data into the database
        if error is None:
            try:
                # this takes a SQL query
                # It may avoid SQL injection automatically
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                # save the changes
                db.commit()
            except db.IntegrityError:
                error = f"User { username } is already registered."
            else:
                # url_for() generates the URL for the login view
                # redirect() generates a redirect response to the generated URL
                return redirect(url_for("auth.login"))
        
            # Note! import "flash" before use this
            # this stores messages that can be retrieved
            # when rendering the template
        flash(error)
           
    return render_template("auth/register.html")
    
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # this returns one row fomr the query
        # If the query returned no result, it returns None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username"

        # this hashes the submitted password in the same way
        # as the stored hash and securely compares them
        # If they match, the password is valid
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        # NOTE! import session
        # session is a dictionary that stores
        # data across requests
        # When validation succeeds,
        # the user's "id" is stored in a new session
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        
        flash(error)

    return render_template("auth/login.html")

@bp.before_app_request
# this checks if a user id is stored in the session
# and gets that user's data from the database storing it on "g.user"
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        
    print("TEST_load_logged_in_user")
    print(g.user)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            print("g.user is None")
            return redirect(url_for("auth.login"))
        
        print("view(**kwargs)")
        return view(**kwargs)
    return wrapped_view

