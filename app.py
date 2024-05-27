from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    user_id = session["user_id"]
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        time_start = request.form.get("start-time")
        time_end = request.form.get("end-time")
        # if no username given
        if not name:
            return apology("must provide name", 400)
        if not location:
            return apology("must provide location", 400)
        if not time_start:
            return apology("must provide starting time", 400)
        if not time_end:
            return apology("must provide ending time", 400)


        sql = "INSERT INTO requests (user_id, name, time_start, time_end, location) VALUES ('{}','{}', '{}', '{}', '{}')".format(user_id, name, time_start, time_end, location)
        db.execute(sql)
        return render_template("create.html")
    else:
        return render_template("create.html")

@app.route("/find", methods=["GET", "POST"])
@login_required
def find():
    user_id = session["user_id"]
    request_id = request.form.get("request_id")
    if request.method == "POST":
        db.execute("UPDATE requests SET completed = 1 WHERE request_id = ?", request_id)
        user_next = db.execute("SELECT user_id FROM requests WHERE request_id = ?", request_id)
        print(user_next)
        sql = ("INSERT INTO games (game_id, user_1, user_2, score) VALUES (?, ?, ?, ?)")
        db.execute(sql, int(request_id), user_id, user_next[0]['user_id'], 'not yet played')
    requests = db.execute("SELECT name, time_start, time_end, location, request_id FROM requests WHERE completed = 0 ORDER BY location")

    for row in requests:
        name = row["name"]
        location = row["location"]
        time_start = row['time_start']
        time_end = row['time_end']
        request_id = row['request_id']

    return render_template("find.html", requests = requests)

@app.route("/games")
@login_required
def games():
    games = db.execute("""
        SELECT games.game_id, games.user_1, games.user_2, games.score, games.game_number,
               (SELECT name FROM requests WHERE user_id = games.user_1) AS user_1_name,
               (SELECT email FROM users WHERE user_id = games.user_1) AS user_1_email,
               (SELECT name FROM requests WHERE user_id = games.user_2) AS user_2_name,
               (SELECT email FROM users WHERE user_id = games.user_2) AS user_2_email
        FROM games
    """)
    return render_template("games.html", games=games)





@app.route("/")
@login_required
def home():
    return render_template("create.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/score", methods=["POST", "GET"])
@login_required
def update_score():
    if request.method == "POST":
        game_id = request.form.get("game_id")
        user_1_score = request.form.get("user_1_score")
        user_2_score = request.form.get("user_2_score")
        score = user_1_score + " - " + user_2_score
        db.execute("UPDATE games SET score = ? WHERE game_number = ?", score, game_id)
        return redirect("/games")
    else:
        return render_template("score.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        city = request.form.get("city")
        state = request.form.get("state")
        mainField = request.form.get("main field")
        # if no username given
        if not email:
            return apology("must provide email", 400)
        # if no password given
        if not password:
            return apology("must provide password", 400)
        # if no confirmation given
        elif not confirmation:
            return apology("must provide confirmation", 400)
        # if password and confirmation don't match
        if password != confirmation:
            return apology("passwords must match", 400)
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        if len(rows) != 0:
            return apology("email already exists", 400)
        # generate hash
        hash = generate_password_hash(password)
        sql = "INSERT INTO users (email, hash, city, state, main_field) VALUES ('{}','{}', '{}', '{}', '{}')".format(email, hash, city, state, mainField)
        db.execute(sql)
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
        return redirect('/')
    else:
        return render_template("register.html")

