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

    user_id = session["user_id"]

    # Get the current cash balance of the user
    rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = rows[0]["cash"]

    # Get the stocks the user owns
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)

    # Initialize total value of stocks
    total_value = 0

    # List to hold stock details
    portfolio = []

    # Loop through each stock to get its current price and calculate the total value
    for stock in stocks:
        stock_info = lookup(stock["symbol"])
        if stock_info:
            stock_value = stock_info["price"] * stock["total_shares"]
            total_value += stock_value
            portfolio.append({
                "symbol": stock["symbol"],
                "name": stock_info["name"],
                "shares": stock["total_shares"],
                "price": stock_info["price"],
                "total": stock_value
            })

    # Calculate grand total (cash + total stock value)
    grand_total = total_value + cash

    # Render the index.html template, passing portfolio, cash, and grand total
    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Ensure shares was submitted and is a positive integer
        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a valid number of shares", 400)

        # Look up stock quote
        stock = lookup(request.form.get("symbol"))

        # Ensure stock symbol is valid
        if stock is None:
            return apology("invalid stock symbol", 400)

        # Calculate total cost
        total_cost = stock["price"] * int(shares)

        # Query user's cash
        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = rows[0]["cash"]

        # Ensure user can afford the stock
        if total_cost > cash:
            return apology("can't afford", 400)

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)

        # Record the transaction in a 'transactions' table
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, stock["symbol"], int(shares), stock["price"])

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]

    # Query all transactions for the user
    transactions = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ? ORDER BY transacted DESC", user_id)

    # Render history.html, passing the transactions
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
            return apology("must provide stock symbol", 400)

        # Look up stock quote
        stock = lookup(request.form.get("symbol"))

        # Ensure stock symbol is valid
        if stock is None:
            return apology("invalid stock symbol", 400)

        # Render quoted.html to display stock info
        return render_template("quoted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Hash the password
        hash_password = generate_password_hash(request.form.get("password"))

        # Try to insert the new user into the database
        try:
            new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                                     request.form.get("username"), hash_password)
        except:
            return apology("username already exists", 400)

        # Log the user in automatically after registration
        session["user_id"] = new_user_id

        # Redirect to the home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]

    if request.method == "POST":

        # Ensure symbol was selected
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Ensure shares was submitted and is a positive integer
        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a valid number of shares", 400)

        # Look up the stock the user wants to sell
        stock = lookup(request.form.get("symbol"))

        # Ensure stock symbol is valid
        if stock is None:
            return apology("invalid stock symbol", 400)

        # Check how many shares the user owns of that stock
        rows = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, stock["symbol"])

        # Ensure the user has enough shares to sell
        if rows[0]["total_shares"] <= 0 or int(shares) > rows[0]["total_shares"]:
            return apology("not enough shares", 400)

        # Calculate the total sale value
        sale_value = stock["price"] * int(shares)

        # Update user's cash balance by adding the sale value
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, user_id)

        # Update the transactions table (record the sale as negative shares)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, stock["symbol"], -int(shares), stock["price"])

        # Redirect user to home page
        return redirect("/")

    else:
        # Get the list of stocks the user owns
        stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)

        # Render the sell form
        return render_template("sell.html", stocks=stocks)
