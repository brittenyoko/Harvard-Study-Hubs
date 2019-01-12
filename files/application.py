import os
import time

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///spaces.db")


@app.route("/")
@login_required
def home():
    """ Referneced https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists """
    """ Displays locations user rated or added """
    key = db.execute("SELECT key FROM locations WHERE user = :user", user=session["user_id"])
    all_places = []
    if key:
        length = len(key)
        for i in range(length):
            all_places.append(db.execute("SELECT location FROM key WHERE id = :id1", id1=key[i]['key']))
    fav_places_key = db.execute("SELECT location FROM favorites WHERE user = :user", user=session["user_id"])
    length = len(fav_places_key)
    fav_places = []
    if fav_places_key:
        for i in range(length):
            fav_places.append(db.execute("SELECT location FROM key WHERE id = :id1", id1=(fav_places_key[i]['location'])))
    return render_template("home.html", all_places=all_places, fav_places=fav_places)


@app.route("/favorite", methods=["GET", "POST"])
@login_required
def favorite():
    """ Allows user to save favorite locations """
    if request.method == "GET":
        all_places = db.execute("SELECT location FROM key")
        fav_places = db.execute("SELECT location FROM favorites WHERE user = :user", user=session["user_id"])
        length = len(fav_places)
        places = []
        if fav_places:
            for i in range(length):
                places.append(db.execute("SELECT location FROM key WHERE id = :id1", id1=(fav_places[i]['location'])))
        non_fav_places = diff(all_places, places)
        return render_template("favorite.html", non_fav_places=non_fav_places, places=places)
    else:
        name = request.form.get("location")
        key = db.execute("SELECT id FROM key WHERE location = :location", location=name)
        result = db.execute("INSERT INTO favorites (location, user) VALUES(:location, :user)",
                            location=key[0]['id'], user=session["user_id"])
        all_places = db.execute("SELECT location FROM key")
        fav_places = db.execute("SELECT location FROM favorites WHERE user = :user", user=session["user_id"])
        length = len(fav_places)
        places = []
        if fav_places:
            for i in range(length):
                places.append(db.execute("SELECT location FROM key WHERE id = :id1", id1=(fav_places[i]['location'])))
        non_fav_places = diff(all_places, places)
        return render_template("favorite.html", all_places=all_places, places=places)


def diff(all_places, fav_places):
    """ Returns a list of dictionaries with the difference of two lists of dictionaries """
    non_fav_places = []
    for place1 in all_places:
        in_list = False
        for place2 in fav_places:
            if place1['location'] == place2[0]['location']:
                in_list = True
        if in_list == False:
            non_fav_places.append(place1)
    return non_fav_places


def Average(lst):
    """ Returns the average of a list """
    if len(lst) == 0:
        return len(lst)
    return sum(lst) / len(lst)


@app.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    """ Allows user to look up information about locations """
    if request.method == "POST":
        places = db.execute("SELECT id FROM key WHERE location=:location", location=request.form.get("places"))[0]["id"]
        average = db.execute("SELECT * FROM locations WHERE key=:places", places=places)
        activities = db.execute(
            "SELECT activity, COUNT(activity) FROM locations WHERE key=:places GROUP BY activity", places=places)
        noise = []
        crowdedness = []
        atmosphere = []
        time = []
        rating = []
        comments = []
        for i in average:
            noise.append(i['noise'])
            crowdedness.append(i['crowdedness'])
            atmosphere.append(i['atmosphere'])
            time.append(i['time'])
            rating.append(i['rating'])
            comments.append(i['comments'])

        noise_Avg = round(Average(noise))
        crowdedness_Avg =round(Average(crowdedness))
        atmosphere_Avg = round(Average(atmosphere))
        time_Avg = round(Average(time))
        rating_Avg = round(Average(rating))

        return render_template("location.html", places=request.form.get("places"), noise=noise_Avg, crowdedness=crowdedness_Avg, atmosphere=atmosphere_Avg, time=time_Avg, rating=rating_Avg, comments=comments, activities=activities)
    else:
        places = db.execute("SELECT location FROM key")
        return render_template("lookup.html", places=places)


@app.route("/meeting", methods=["GET",  "POST"])
@login_required
def meeting():
    if request.method == "POST":
        result = db.execute("INSERT INTO meetings (location, date, time, subject) VALUES(:location, :date, :time, :subject)",
                            location=request.form.get("places"), date=request.form.get("date"), time=request.form.get("time"), subject=request.form.get("subject"))
        if not result:
            return apology("could not insert into table")
        return redirect("/meetingList")

    else:
        places = db.execute("SELECT location FROM key")
        return render_template("meeting.html", places=places)


@app.route("/meetingList", methods=["GET"])
@login_required
def meetingList():
    meetings = db.execute("SELECT * FROM meetings")
    return render_template("meetingList.html", meetings=meetings)


@app.route("/messages", methods=["GET", "POST"])
@login_required
def messages():
    """ Stores the message and user information in a data table """
    if request.method == "POST":
        recipient = db.execute("SELECT id FROM users WHERE username = :username", username=request.form.get("recipient"))
        result = db.execute("INSERT INTO messages (message, recipient, sender) VALUES(:message, :recipient, :sender)",
                            message=request.form.get("text"), recipient=recipient[0]['id'], sender=session["user_id"])

        if not result:
            return apology("could not insert into table")
        return redirect("/messages")

    else:
        recipient = db.execute("SELECT username FROM users")
        return render_template("messages.html", recipient=recipient)


@app.route("/inbox", methods=["GET"])
@login_required
def inbox():
    mail = db.execute("SELECT * FROM messages WHERE recipient = :recipient", recipient=session["user_id"])
    sender = []
    length = len(mail)
    if len(mail) < 1:
        mail.append({'time':"None", 'message':"None"})
        sender.append({'username':'None'})
    else:
        for i in range(length):
            sender.append(db.execute("SELECT username FROM users WHERE id = :id1", id1=mail[i]['sender']))
    return render_template("inbox.html", mail=mail, sender=sender)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """ Referenced https://stackoverflow.com/questions/4108341/generating-an-ascending-list-of-numbers-of-arbitrary-length-in-python """
    """ Allows user to add a location """
    if request.method == "POST":
        name = request.form.get("location")
        result1 = db.execute("INSERT OR IGNORE INTO key (location) VALUES(:location)", location=name)
        if not result1:
            return apology("could not insert into table")
        key = db.execute("SELECT id FROM key WHERE location = :location", location=name)
        result2 = db.execute("INSERT INTO locations (key, comments, noise, rating, atmosphere, crowdedness, activity, time, maps, user) VALUES(:key, :comments, :noise, :rating, :atmosphere, :crowdedness, :activity, :time, :maps, :user)",
                             key=key[0]['id'], comments=request.form.get("comments"), noise=request.form.get("noise"), rating=request.form.get("rating"), atmosphere=request.form.get("atmosphere"), crowdedness=request.form.get("crowdedness"), activity=request.form.get("activity"), time=request.form.get("time"), maps=request.form.get("map"), user=session["user_id"])
        if not result2:
            return apology("could not insert into table")
        return redirect("/")
    else:
        activities = ["studying alone", "studying with friends", "hanging out", "reading", "playing games", "sleeping"]
        times = list(range(1, 24))
        return render_template("add.html", activities=activities, times=times)


def most_common(lst):
    """ Returns the most common item of a list """
    return max(list(lst), key=lst.count)


def least_common(lst):
    """ Returns the least commonitem of a list """
    return min(list(lst), key=lst.count)


@app.route("/sortby", methods=["GET", "POST"])
@login_required
def sortby():
    """ Allows users to sort locations """

    if request.method == "POST":
        catigory = request.form.get("catigory")
        number = int(request.form.get("number"))
        places = db.execute("SELECT * FROM key")
        loc_list = []
        for place in places:
            average = db.execute("SELECT * FROM locations WHERE key=:places", places=place['id'])
            noise = []
            crowdedness = []
            atmosphere = []
            rating = []
            for i in average:
                noise.append(i['noise'])
                crowdedness.append(i['crowdedness'])
                atmosphere.append(i['atmosphere'])
                rating.append(i['rating'])

            noise_Avg = Average(noise)
            crowdedness_Avg = Average(crowdedness)
            atmosphere_Avg = Average(atmosphere)
            rating_Avg = Average(rating)

            if catigory == "cowdedness":
                if number <= crowdedness_Avg:
                    loc_list.append(place['location'])
            if catigory == "atmosphere":
                if number <= atmosphere_Avg:
                    loc_list.append(place['location'])
            if catigory == "noise":
                if number <= noise_Avg:
                    loc_list.append(place['location'])
            if catigory == "rating":
                if number <= rating_Avg:
                    loc_list.append(place['location'])

            if len(loc_list) < 1:
                loc_list == ["None"]
        return render_template("sorted.html", loc_list=loc_list, number=number, catigory=catigory)

    else:
        catigories = ["crowdedness", "atmosphere", "noise", "rating"]
        return render_template("sortby.html", catigories=catigories)


@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    """ Allows user to rate a location """
    if request.method == "POST":
        name = request.form.get("places")
        key = db.execute("SELECT id FROM key WHERE location = :location",
                         location=name)

        result = db.execute("INSERT INTO locations (key, comments, noise, rating, atmosphere, crowdedness, activity, time, maps, user) VALUES(:key, :comments, :noise, :rating, :atmosphere, :crowdedness, :activity, :time, :maps, :user)",
                            key=key[0]['id'], comments=request.form.get("comments"), noise=request.form.get("noise"), rating=request.form.get("rating"), atmosphere=request.form.get("atmosphere"), crowdedness=request.form.get("crowdedness"), activity=request.form.get("activity"), time=request.form.get("time"), maps=request.form.get("map"), user=session["user_id"])
        if not result:
            return apology("could not insert into table")

        return redirect("/")
    else:
        activities = ["studying alone", "studying with friends", "hanging out", "reading", "playing games", "sleeping"]
        times = list(range(1, 24))
        places = db.execute("SELECT location FROM key")
        return render_template("rate.html", activities=activities, times=times, places=places)


@app.route("/recent")
@login_required
def recent():
    """ Displays recent ratings """
    loc_id = db.execute("SELECT key FROM locations")
    latest_loc_id = []
    places = []
    names = []
    length = len(loc_id)
    # Only show at most 7 ratings
    if (length > 7):
        reps = 7
    else:
        reps = length
    for i in range(reps):
        latest_loc_id.append(loc_id[length - 1 - i]['key'])
        places.append(db.execute("SELECT * FROM locations WHERE key = :key", key=latest_loc_id[i]))
        names.append(db.execute("SELECT location FROM key WHERE id = :id1", id1=latest_loc_id[i]))
    return render_template("recent.html", places=places, names=names)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("username"):
            return apology("must provide a username")
        p = request.form.get("password")
        if len(p) < 8:
            return apology("must provide a password with at least 8 characters")
        if not p:
            return apology("must provide a password")
        c = request.form.get("confirmation")
        if not c:
            return apology("must provide another password")
        if not p == c:
            return apology("passwords must match")
        hash1 = generate_password_hash(p)
        result = db.execute("INSERT INTO users (username, hash, name, email) VALUES(:username, :hash1, :name, :email)",
                            username=request.form.get("username"), hash1=hash1, name=request.form.get("name"), email=request.form.get("email"))
        if not result:
            return apology("could not insert into table")
        return redirect("/login")


@app.route("/checkname", methods=["GET"])
def checkname():
    """ Referenced https://stackoverflow.com/questions/19435906/what-is-the-correct-way-to-format-true-in-json """
    """ Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    username = username.lower()
    rows = db.execute("SELECT username FROM users WHERE username = :username", username=username)
    if len(rows) != 0 or len(username) < 0:
        return jsonify(False)
    return jsonify(True)


@app.route("/checkloc", methods=["GET"])
def checkloc():
    """ Referenced https://stackoverflow.com/questions/19435906/what-is-the-correct-way-to-format-true-in-json """
    """ Return true if location is not already in the database, else false, in JSON format"""
    location = request.args.get("location")
    rows = db.execute("SELECT location FROM key WHERE location = :location", location=location)
    # Tests where there the locationname is in the database
    if len(rows) > 0 or len(location) < 0:
        return jsonify(False)
    return jsonify(True)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
