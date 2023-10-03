import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #portfolio_holdings = get_portfolio_for_user(session["user_id"])
    portfolio_holdings = db.execute("SELECT * FROM portfolios WHERE user_id = ?", session["user_id"])
    #user = get_user_by_userid(session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    #if not user:
        #not sure how but on check50 the user is not being returned by get_user_by_userid even though the user exists in the db, maybe a race condition?
        #hypothesis is that I cannot change helper.py
       # cash = 0
    #else:
    cash = user[0]["cash"]
    total_value = cash

    for portfolio_holding in portfolio_holdings:
        price = lookup(portfolio_holding["symbol"])["price"]
        portfolio_holding["price"] = price
        total_value += (price * portfolio_holding["shares"])


    return render_template("index.html", portfolio_holdings = portfolio_holdings, cash = cash, total_value = total_value)

@app.route("/add_funds", methods=["GET", "POST"])
@login_required
def add_funds():
    """Add funds"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not session["user_id"]:
            return apology("must be logged in to transact", 403)

        # Ensure symbol was submitted
        if not request.form.get("amount"):
            return apology("must provide symbol", 400)

        amount = float(request.form.get("amount"))
        if amount <= 0:
            return apology("add funds amount must be greater than 0", 400)

        #cash = get_user_by_userid(session["user_id"])[0]["cash"]
        cash = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"]))[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + amount, session["user_id"])

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("add_funds.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not session["user_id"]:
            return apology("must be logged in to transact", 403)

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        if not request.form.get("shares") or not request.form.get("shares").isdecimal() or int(request.form.get("shares")) < 1:
            return apology("must provide whole share amount greater than 0", 400)

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("stock not found", 400)

        user_id = int(session["user_id"])
        #rows = get_user_by_userid(user_id)
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        price = quote["price"]
        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol").lower()
        cost = price * shares

        if (float(rows[0]["cash"]) < cost):
            return apology("insufficient funds", 400)
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", float(rows[0]["cash"]) - cost, user_id)
            #rows = get_portfolio_holding_for_symbol(session["user_id"], symbol)
            rows = db.execute("SELECT * FROM portfolios WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)", user_id, symbol, shares, price, "BUY")
            if not rows:
                db.execute("INSERT INTO portfolios (user_id, symbol, shares) VALUES (?, ?, ?)", user_id, symbol, shares)
            else:
                db.execute("UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?", shares + rows[0]["shares"], user_id, symbol)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("buy_form.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions = transactions)


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

        # Query database for username
        #rows = get_user_by_username(request.form.get("username"))
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("stock not found", 400)

        return render_template("quote_display.html", symbol = quote["symbol"], name = quote["name"], price = quote["price"])
    else:
        return render_template("quote_form.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        #rows = get_user_by_username(request.form.get("username"))
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 0:
            return apology("Username is already taken, please Select another username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Esnure pass verify match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password do not match", 400)


        #create user and session
        id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        session["user_id"] = id

        # Redirect user to home page
        return redirect("/")
        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not session["user_id"]:
            return apology("must be logged in to transact", 403)

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        if not request.form.get("shares") or int(request.form.get("shares")) < 1:
            return apology("must provide share amount greater than 0", 400)

        symbol = request.form.get("symbol").lower()
        quote = lookup(symbol)

        if not quote:
            return apology("stock not found", 400)

        user_id = int(session["user_id"])
        #rows = get_user_by_userid(user_id)
        price = quote["price"]
        for_sale_shares = int(request.form.get("shares"))


        #portfolio_holdings = get_portfolio_for_user(session["user_id"])
        portfolio_holdings = db.execute("SELECT * FROM portfolios WHERE user_id = ?", session["user_id"])
        #cash = get_user_by_userid(session["user_id"])[0]["cash"]
        cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"]


        #get amount of current shares
        current_shares = 0
        for portfolio_holding in portfolio_holdings:
            if portfolio_holding["symbol"] == symbol:
                current_shares = portfolio_holding["shares"]

        #if user has zero shares or not enough of them
        if current_shares == 0 or current_shares < for_sale_shares:
            return apology("Not enough shares of stock", 400)
        else:
            current_shares -= for_sale_shares
            cash += for_sale_shares * price
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)", user_id, symbol, for_sale_shares, price, "SELL")

            if current_shares == 0:
                db.execute("DELETE FROM portfolios WHERE user_id = ? AND symbol = ?", user_id, symbol)
            else:
                db.execute("UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?", current_shares, user_id, symbol)
        # Redirect user to home page
        return redirect("/")
    else:
        #portfolio_holdings = get_portfolio_for_user(session["user_id"])
        portfolio_holdings = db.execute("SELECT * FROM portfolios WHERE user_id = ?", session["user_id"])
        return render_template("sell_form.html", portfolio_holdings = portfolio_holdings)
