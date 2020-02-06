import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():

    # Store current date for later comparison
    presentdate = datetime.now()

    # Convert datetime.datetime to datetime.date
    convertpresentdate = presentdate.date()

    # Retrieve data records
    transactionstest = db.execute(
        "SELECT title, description, picturelocation, applylink, eventdate, eventdeadline, location, time FROM bookseatdb")

    # and then store in a python list
    mylist = list(transactionstest)

    # This prints database row 1, column 4 entry
    #print(mylist[0][4])

    # for items in mylist (which are number of records in database):
    for i in range(0, len(mylist)):
        mydateobj = mylist[i][4]
        # if (mylist[0][4] > convertpresentdate):
        if not mydateobj > convertpresentdate:

            # Query to remove that mydateobj entry from database because event is expired
            expiredevent = db.execute("DELETE FROM bookseatdb where eventdate < :mydateobj", { "mydateobj" : mydateobj })
            db.commit()


    transactions = db.execute(
        "SELECT title, description, picturelocation, applylink, eventdate, eventdeadline, location, time FROM bookseatdb")

    return render_template("index.html", transactions=transactions)


@app.route("/new", methods=["GET", "POST"])
def quote():

    # Get entered data and store them in variables
    title = request.form.get("title")
    description = request.form.get("description")
    eventdate = request.form.get("eventdate")
    location = request.form.get("location")
    eventdeadline = request.form.get("eventdeadline")
    applylink = request.form.get("applylink")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure proper usage
        if not title:
            flash('Please enter event title', 'warning')
            return redirect("/new")

        elif not description:
            flash('Please enter some description', 'warning')
            return redirect("/new")

        elif not eventdate:
            flash('Please enter event date', 'warning')
            return redirect("/new")

        elif not location:
            flash('Please enter event location', 'warning')
            return redirect("/new")

        elif not eventdeadline:
            flash('Please enter event deadline', 'warning')
            return redirect("/new")

        elif not applylink:
            flash('Please give an apply link', 'warning')
            return redirect("/new")

        # Query database for adding data
        result = db.execute("INSERT INTO bookseatdb2 (title, description, eventdate, location, eventdeadline, applylink) VALUES (:title, :description, :eventdate, :location, :eventdeadline, :applylink)",
                            { "title" : title, "description" : description, "eventdate" : eventdate, "location" : location, "eventdeadline" : eventdeadline, "applylink" : applylink })
        db.commit()

        flash("Information submitted, thanks for letting people know!", 'success')

        return redirect("/")

    else:

        return render_template("new.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact us"""

    # Get entered data and store them in variables
    detail = request.form.get("detail")
    email = request.form.get("email")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure proper usage
        if not detail:
            flash('Please write something you want to contact about', 'warning')
            return redirect("/contact")

        elif not email:
            flash('Please enter your email', 'warning')
            return redirect("/contact")

        # Query database for adding data
        result = db.execute("INSERT INTO contactme (detail, email) VALUES (:detail, :email)",
                        { "detail" : detail, "email" : email })

        db.commit()
        flash("Thank you for contacting us with valuable feedback, if there is a query, we will revert soon", 'success')

        return redirect("/")

    else:

        return render_template("contact.html")
