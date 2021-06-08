from flask import Flask, render_template, request, session, redirect, url_for, flash

import random
import time

import data_utils

app = Flask(__name__)

@app.route("/")
@app.route("/polygon")
def open_main_page():
    if("userID" in session and session["userID"] != -1):
        user = data_utils.get_user_by_id(session["userID"])
        session["userName"] = user[0]
    else:
        session["userID"] = -1
        session["userName"] = "Guest"
    session["titleID"] = -1
    session["previousPage"] = request.path
    data = data_utils.get_titles_table("titles.name", "asc")
    return render_template("table.html", 
    the_title = "Game Titles", 
    the_data = data, 
    the_user = session["userName"])

@app.route("/polygon", methods=["POST"])
def open_main_page_custom_order():
    session["titleID"] = -1
    session["previousPage"] = request.path
    data = data_utils.get_titles_table(request.form["the_order_by"], request.form["the_order"])
    return render_template("table.html", 
    the_title= "Game Titles", 
    the_data= data)

@app.route("/game/<what>")
def open_title_page(what):
    if("userID" in session and session["userID"] != -1):
        user = data_utils.get_user_by_id(session["userID"])
        session["userName"] = user[0]
    else:
        session["userID"] = -1
        session["userName"] = "Guest"
    session["titleID"] = what
    session["previousPage"] = request.path
    titleData = data_utils.get_title_info(what)
    reviewsData = data_utils.get_reviews(what)
    return render_template("title.html", 
    the_title = titleData[1], 
    the_title_data = titleData,
    the_reviews_data = reviewsData,
    the_user = session["userName"])

@app.route("/login")
def open_login_page():
    return render_template("login.html", the_title="Login Page")

@app.route("/login", methods=["POST"])
def login_user():
    userData = data_utils.get_user_and_password(request.form["the_user_name"], request.form["the_password"])
    if(len(userData) == 0):
        flash(
            f"User or/and password you have enetered was incorrect"
        )
        return redirect(url_for("open_login_page"))
    else:
        session["userID"] = userData[0][0]
        return redirect(session["previousPage"])

@app.route("/register", methods=["POST"])
def register_user():
    userData = data_utils.get_user(request.form["the_user_name"])
    if(len(userData) == 0):
        data_utils.create_user(request.form["the_user_name"], request.form["the_password"])
        userData = data_utils.get_user_and_password(request.form["the_user_name"], request.form["the_password"])
        session["userID"] = userData[0][0]
        return redirect(session["previousPage"])
    else:
        flash(
            f"User already exists"
        )
        return redirect(url_for("open_login_page"))

@app.route("/newReview")
@app.route("/newReview", methods=["POST"])
def new_review_page():
    userID = session.get("userID", -1)
    session["previousPage"] = request.path
    if(userID == -1):
        return redirect(url_for("open_login_page"))
    else:
        return render_template("newReview.html", the_title= "Create New Review")

@app.route("/createReview", methods=["POST"])
def create_review():
    if data_utils.check_if_review_exists(session["titleID"], session["userID"]):
        flash(
            f"You have already reviewed this game"
        )
        return redirect(url_for("new_review_page"))
    data_utils.create_review(request.form["liked"], 
    request.form["played"],
    request.form["owned"],
    request.form["rating"],
    request.form["comment"],
    session["titleID"],
    session["userID"]
    )
    return redirect("/game/" + session["titleID"])

@app.route("/newTitle", methods=["POST"])
def new_title_page():
    if request.form["the_title_name"] == "":
        flash(
            f"You have to enter a name for the game"
        )
        return redirect(session["previousPage"])
    if(data_utils.check_if_title_exists(request.form["the_title_name"], request.form["the_platform"])):
        flash(
            f"The game you are trying to add already exists"
        )
        return redirect(session["previousPage"])
    else:
        session["titleName"] = request.form["the_title_name"]
        session["titlePlatform"] = request.form["the_platform"]
        return render_template("newTitle.html", 
        the_title= "Add New Game",
        the_name= session["titleName"],
        the_platform= session["titlePlatform"])

@app.route("/createTitle", methods=["POST"])
def create_title():
    data_utils.create_title(session["titleName"], session["titlePlatform"], request.form["the_release_year"], request.form["the_genre"], request.form["the_studio"])
    return redirect(url_for("open_main_page"))


@app.route("/logOut")
def log_out():
    session["userID"] = -1
    return redirect(session["previousPage"])


app.secret_key = "fkdslflsdkgdfhg'adfh8 ejre 'fd'ofd bifjbjb bfjbtr"

if __name__ == "__main__":
    app.run(debug=True)  #Runs the server in debug mode meaning it restarts