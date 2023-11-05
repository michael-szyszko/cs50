from dateutil.parser import parse
from debt_db import debt_db, Debts
from debt_calculator import (
    simulate_debt_paying,
    debt_sorter_name,
    debt_sorter_avalanche,
    debt_sorter_snowball,
)
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from helpers import apology, login_required, usd, get_month, get_year

MONTH_NAMES = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = debt_db("sqlite:///debt_calculator.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index(sorterKey=debt_sorter_snowball):
    if request.method == "POST":
        requestedSorterKey = request.form.get("sorterKey")
        if requestedSorterKey and requestedSorterKey == debt_sorter_avalanche.__name__:
            sorterKey = debt_sorter_avalanche

    """Show current month and debt"""
    debts = db.get_debts_by_user_id(session["user_id"])
    if len(debts) == 0:
        return redirect("/debt")

    extra_payment = db.get_extra_payment_by_user_id(session["user_id"])
    debts_by_month = simulate_debt_paying(debts, extra_payment, sorterKey)

    months_for_payoff = len(debts_by_month) - 1
    years_for_payoff = months_for_payoff // 12
    months_for_payoff = months_for_payoff - years_for_payoff * 12

    # sort debts alphabetically
    for debts in debts_by_month:
        debts.sort(key=debt_sorter_name)

    extra_payment = db.get_extra_payment_by_user_id(session["user_id"])
    sorters = [
        {"functionName": debt_sorter_snowball.__name__, "value": "Snow Ball"},
        {"functionName": debt_sorter_avalanche.__name__, "value": "Avalanche"},
    ]
    for sorter in sorters:
        if sorterKey.__name__ == sorter["functionName"]:
            selectedSorterName = sorter["value"]
    return render_template(
        "index.html",
        years_for_payoff=years_for_payoff,
        months_for_payoff=months_for_payoff,
        debts_by_month=debts_by_month,
        extra_payment=extra_payment,
        month_names=MONTH_NAMES,
        sorters=sorters,
        selectedSorter=sorterKey.__name__,
        selectedSorterName=selectedSorterName,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Validate credentials and create session if valid
        if db.valid_credentials(
            request.form.get("username"), request.form.get("password")
        ):
            session["user_id"] = db.get_user_id(request.form.get("username"))
            # Redirect user to home page
            return redirect("/")
        else:
            return apology("invalid username and/or password", 403)
    else:
        # User reached route via GET (as by clicking a link or via redirect)
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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        if db.user_exists(request.form.get("username")):
            return apology(
                "Username is already taken, please Select another username", 400
            )

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure pass verify match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password do not match", 400)

        # create user and session
        db.create_user(request.form.get("username"), request.form.get("password"))
        session["user_id"] = db.get_user_id(request.form.get("username"))

        # Redirect user to home page
        return redirect("/")
        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/debt", methods=["GET", "POST"])
@login_required
def debt():
    """Enter Debt."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        name = request.form.get("name")
        amount = request.form.get("amount")
        rate = request.form.get("rate")
        minimum_payment = request.form.get("minimum_payment")
        date = request.form.get("date")

        if not name:
            return apology("must provide a name", 400)
        try:
            float(rate)
            if not float(rate) > 0 or float(rate) > 100:
                return apology(
                    "rate must be a greater than 0.0% and less than 100.0%", 400
                )
        except ValueError:
            return apology("rate must be a greater than 0.0% and less than 100.0%", 400)
        try:
            date_parsed = parse(date)
        except:
            return apology("Error with date", 400)
        if not amount or not amount.isdigit() or not (int(amount) >= 0):
            return apology("please provide aa amount whole number above $0", 400)
        if (
            not minimum_payment
            or not minimum_payment.isdigit()
            or not (int(minimum_payment) >= 0)
        ):
            return apology(
                "please provide a minimum payment whole number above $0", 400
            )

        db.create_debt(
            session["user_id"],
            name,
            amount,
            rate,
            minimum_payment,
            get_month(date_parsed),
            get_year(date_parsed),
        )
        return redirect("/")
    else:
        return render_template("debt_form.html", month=get_month(), year=get_year())


@app.route("/debt/delete", methods=["GET", "POST"])
@login_required
def delete_debt():
    debt_id = request.form.get("id")
    if not debt_id or not debt_id.isdigit() or not (int(debt_id) >= 0):
        return apology("invalid id for debt", 400)
    db.delete_debt(session["user_id"], debt_id)
    return redirect("/")


@app.route("/extra_payment", methods=["GET", "POST"])
@login_required
def extra_payment():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        extra_payment = request.form.get("extra_payment")

        if (
            not extra_payment
            or not extra_payment.isdigit()
            or not (int(extra_payment) >= 0)
        ):
            return apology(
                "please provide a amount whole number greater than or equal to $0", 400
            )

        db.update_extra_payment(session["user_id"], extra_payment)
        return redirect("/")
    else:
        extra_payment = db.get_extra_payment_by_user_id(session["user_id"])
        return render_template("extra_payment.html", extra_payment=extra_payment)

if __name__ == '__main__':
    app.run()