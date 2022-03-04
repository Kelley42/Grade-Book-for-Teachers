import os
import re
import ast

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required #lookup, usd

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


# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all subjects they have
    subjects = db.execute("SELECT subject1, subject2, subject3, subject4, subject5, subject6 FROM subjects WHERE id = :id GROUP BY id, subject1, subject2, subject3, subject4, subject5, subject6", id=session["user_id"])
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Show user's subjects in index table
        for subject in subjects:
                
            subject1 = subject["subject1"]
            subject2 = subject["subject2"]
            subject3 = subject["subject3"]
            subject4 = subject["subject4"]
            subject5 = subject["subject5"]
            subject6 = subject["subject6"]
        
        return render_template("index.html", subjects=subjects, subject1=subject1, subject2=subject2, subject3=subject3, subject4=subject4, subject5=subject5, subject6=subject6)
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html", subjects=subjects)
        
@app.route("/managebehavior", methods=["GET", "POST"])
@login_required
def managebehavior():
    """Choose subjects"""
    # Get student's behavior from table 
    weeks = db.execute("SELECT studentname, week1, week2, week3, week4, week5, week6, week7, week8, week9, comments FROM behavior WHERE id = :id GROUP BY id, studentname, week1, week2, week3, week4, week5, week6, week7, week8, week9, comments", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get grades
        studentname = request.form.get("studentname")
        week1 = int(request.form.get("week1"))
        week2 = int(request.form.get("week2"))
        week3 = int(request.form.get("week3"))
        week4 = int(request.form.get("week4"))
        week5 = int(request.form.get("week5"))
        week6 = int(request.form.get("week6"))
        week7 = int(request.form.get("week7"))
        week8 = int(request.form.get("week8"))
        week9 = int(request.form.get("week9"))
        comments = request.form.get("comments")    
        
        if not studentname:
            return apology("you forgot to put the student's name", 400)
        if not week1:
            return apology("you forgot to add a grade", 400)
        if not week2:
            return apology("you forgot to add a grade", 400)
        if not week3:
            return apology("you forgot to add a grade", 400)
        if not week4:
            return apology("you forgot to add a grade", 400)
        if not week5:
            return apology("you forgot to add a grade", 400)
        if not week6:
            return apology("you forgot to add a grade", 400)
        if not week7:
            return apology("you forgot to add a grade", 400)
        if not week8:
            return apology("you forgot to add a grade", 400)
        if not week9:
            return apology("you forgot to add a grade", 400)
        if not comments:
            return apology("you forgot to add comments", 400)
            
        # insert into table
        db.execute("INSERT INTO behavior(id, studentname, week1, week2, week3, week4, week5, week6, week7, week8, week9, comments) VALUES(:id, :studentname, :week1, :week2, :week3, :week4, :week5, :week6, :week7, :week8, :week9, :comments)",
            id = session["user_id"],
            studentname = studentname,
            week1 = week1,
            week2 = week2,
            week3 = week3,
            week4 = week4,
            week5 = week5,
            week6 = week6,
            week7 = week7,
            week8 = week8,
            week9 = week9,
            comments = comments)
        average = round(((week1 + week2 + week3 + week4 + week5 + week6 + week7 + week8 + week9) / 9), 1)
        db.execute("UPDATE behavior SET average = :average WHERE id = :id AND studentname = :studentname", average=average, id = session["user_id"], studentname=studentname)
        #db.execute("INSERT INTO studentgrades(id, studentname) VALUES(:id, :studentname)", id = session["user_id"], studentname = studentname)
        behavioravg = average
        db.execute("UPDATE studentgrades SET behavioravg = :behavioravg WHERE id = :id AND studentname = :studentname", behavioravg=behavioravg, id = session["user_id"], studentname=studentname)
        
        return redirect("/behavior")
        
    else:
        return render_template("managebehavior.html", weeks=weeks)


@app.route("/behavior", methods=["GET", "POST"])
@login_required
def behavior():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all grades they have
    weeks = db.execute("SELECT id, studentname, week1, week2, week3, week4, week5, week6, week7, week8, week9, average, comments FROM behavior WHERE id = :id GROUP BY id, studentname, week1, week2, week3, week4, week5, week6, week7, week8, week9, average, comments", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Show user's grades in table
        for week in weeks:
            id = session["user_id"]
            studentname = week["studentname"]    
            week1 = week["week1"]
            week2 = week["week2"]
            week3 = week["week3"]
            week4 = week["week4"]
            week5 = week["week5"]
            week6 = week["week6"]
            week7 = week["week7"]
            week8 = week["week8"]
            week9 = week["week9"]
            average = week["average"]
            comments = week["comments"]
    
        return render_template("behavior.html", weeks=weeks, studentname=studentname, week1=week1, week2=week2, week3=week3, week4=week4, week5=week5, week6=week6, week7=week7, week8=week8, week9=week9, average=average, comments=comments)
 
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("behavior.html", weeks=weeks)

@app.route("/managesubject1", methods=["GET", "POST"])
@login_required
def managesubject1():
    """Choose subjects"""
    # Get user's info from table 
    tests = db.execute("SELECT studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments FROM subject1 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get grades
        studentname = request.form.get("studentname")
        test1 = int(request.form.get("test1"))
        test2 = int(request.form.get("test2"))
        test3 = int(request.form.get("test3"))
        test4 = int(request.form.get("test4"))
        test5 = int(request.form.get("test5"))
        test6 = int(request.form.get("test6"))
        test7 = int(request.form.get("test7"))
        test8 = int(request.form.get("test8"))
        test9 = int(request.form.get("test9"))
        comments = request.form.get("comments")    
        
        if not studentname:
            return apology("you forgot to put the student's name", 400)
        if not test1:
            return apology("you forgot to add a grade", 400)
        if not test2:
            return apology("you forgot to add a grade", 400)
        if not test3:
            return apology("you forgot to add a grade", 400)
        if not test4:
            return apology("you forgot to add a grade", 400)
        if not test5:
            return apology("you forgot to add a grade", 400)
        if not test6:
            return apology("you forgot to add a grade", 400)
        if not test7:
            return apology("you forgot to add a grade", 400)
        if not test8:
            return apology("you forgot to add a grade", 400)
        if not test9:
            return apology("you forgot to add a grade", 400)
        if not comments:
            return apology("you forgot to add comments", 400)
            
        # insert into table
        db.execute("INSERT INTO subject1(id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments) VALUES(:id, :studentname, :test1, :test2, :test3, :test4, :test5, :test6, :test7, :test8, :test9, :comments)",
            id = session["user_id"],
            studentname = studentname,
            test1 = test1,
            test2 = test2,
            test3 = test3,
            test4 = test4,
            test5 = test5,
            test6 = test6,
            test7 = test7,
            test8 = test8,
            test9 = test9,
            comments = comments)
        average = round(((test1 + test2 + test3 + test4 + test5 + test6 + test7 + test8 + test9) / 9), 1)
        db.execute("UPDATE subject1 SET average = :average WHERE id = :id AND studentname = :studentname", average=average, id = session["user_id"], studentname=studentname)
        #db.execute("INSERT INTO studentgrades(id, studentname) VALUES(:id, :studentname)", id = session["user_id"], studentname = studentname)
        subject1avg = average
        db.execute("UPDATE studentgrades SET subject1avg = :subject1avg WHERE id = :id AND studentname = :studentname", subject1avg=subject1avg, id = session["user_id"], studentname=studentname)
        return redirect("/subject1")
        
    else:
        return render_template("managesubject1.html", tests=tests)


@app.route("/subject1")
@login_required
def subject1():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all grades they have
    
    tests = db.execute("SELECT id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments FROM subject1 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments", id=session["user_id"])
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Show user's info in table
        for test in tests:
            id = session["user_id"]
            studentname = test["studentname"]    
            test1 = test["test1"]
            test2 = test["test2"]
            test3 = test["test3"]
            test4 = test["test4"]
            test5 = test["test5"]
            test6 = test["test6"]
            test7 = test["test7"]
            test8 = test["test8"]
            test9 = test["test9"]
            average = test["average"]
            comments = test["comments"]
        
        return render_template("subject1.html", tests=tests, studentname=studentname, test1=test1, test2=test2, test3=test3, test4=test4, test5=test5, test6=test6, test7=test7, test8=test8, test9=test9, average=average, comments=comments)
 
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("subject1.html", tests=tests)
        
@app.route("/managesubject2", methods=["GET", "POST"])
@login_required
def managesubject2():
    """Choose subjects"""
    # Get user's info from table 
    tests = db.execute("SELECT studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments FROM subject2 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get grades
        studentname = request.form.get("studentname")
        test1 = int(request.form.get("test1"))
        test2 = int(request.form.get("test2"))
        test3 = int(request.form.get("test3"))
        test4 = int(request.form.get("test4"))
        test5 = int(request.form.get("test5"))
        test6 = int(request.form.get("test6"))
        test7 = int(request.form.get("test7"))
        test8 = int(request.form.get("test8"))
        test9 = int(request.form.get("test9"))
        comments = request.form.get("comments")    
        
        if not studentname:
            return apology("you forgot to put the student's name", 400)
        if not test1:
            return apology("you forgot to add a grade", 400)
        if not test2:
            return apology("you forgot to add a grade", 400)
        if not test3:
            return apology("you forgot to add a grade", 400)
        if not test4:
            return apology("you forgot to add a grade", 400)
        if not test5:
            return apology("you forgot to add a grade", 400)
        if not test6:
            return apology("you forgot to add a grade", 400)
        if not test7:
            return apology("you forgot to add a grade", 400)
        if not test8:
            return apology("you forgot to add a grade", 400)
        if not test9:
            return apology("you forgot to add a grade", 400)
        if not comments:
            return apology("you forgot to add comments", 400)
            
        # insert into table
        db.execute("INSERT INTO subject2(id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments) VALUES(:id, :studentname, :test1, :test2, :test3, :test4, :test5, :test6, :test7, :test8, :test9, :comments)",
            id = session["user_id"],
            studentname = studentname,
            test1 = test1,
            test2 = test2,
            test3 = test3,
            test4 = test4,
            test5 = test5,
            test6 = test6,
            test7 = test7,
            test8 = test8,
            test9 = test9,
            comments = comments)
        average = round(((test1 + test2 + test3 + test4 + test5 + test6 + test7 + test8 + test9) / 9), 1)
        db.execute("UPDATE subject2 SET average = :average WHERE id = :id AND studentname = :studentname", average=average, id = session["user_id"], studentname=studentname)
        #db.execute("INSERT INTO studentgrades(id, studentname) VALUES(:id, :studentname)", id = session["user_id"], studentname = studentname)
        subject2avg = average
        db.execute("UPDATE studentgrades SET subject2avg = :subject2avg WHERE id = :id AND studentname = :studentname", subject2avg=subject2avg, id = session["user_id"], studentname=studentname)
        
        return redirect("/subject2")
        
    else:
        return render_template("managesubject2.html", tests=tests)


@app.route("/subject2", methods=["GET", "POST"])
@login_required
def subject2():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all grades they have
    tests = db.execute("SELECT id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments FROM subject2 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments", id=session["user_id"])
        
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Show user's info in table
        for test in tests:
            id = session["user_id"]
            studentname = test["studentname"]    
            test1 = test["test1"]
            test2 = test["test2"]
            test3 = test["test3"]
            test4 = test["test4"]
            test5 = test["test5"]
            test6 = test["test6"]
            test7 = test["test7"]
            test8 = test["test8"]
            test9 = test["test9"]
            average = test["average"]
            comments = test["comments"]
        
        return render_template("subject2.html", tests=tests, studentname=studentname, test1=test1, test2=test2, test3=test3, test4=test4, test5=test5, test6=test6, test7=test7, test8=test8, test9=test9, average=average, comments=comments)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("subject2.html", tests=tests)

@app.route("/managesubject3", methods=["GET", "POST"])
@login_required
def managesubject3():
    """Choose subjects"""
    # Get user's info from table 
    tests = db.execute("SELECT studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments FROM subject3 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get grades
        studentname = request.form.get("studentname")
        test1 = int(request.form.get("test1"))
        test2 = int(request.form.get("test2"))
        test3 = int(request.form.get("test3"))
        test4 = int(request.form.get("test4"))
        test5 = int(request.form.get("test5"))
        test6 = int(request.form.get("test6"))
        test7 = int(request.form.get("test7"))
        test8 = int(request.form.get("test8"))
        test9 = int(request.form.get("test9"))
        comments = request.form.get("comments")    
        
        if not studentname:
            return apology("you forgot to put the student's name", 400)
        if not test1:
            return apology("you forgot to add a grade", 400)
        if not test2:
            return apology("you forgot to add a grade", 400)
        if not test3:
            return apology("you forgot to add a grade", 400)
        if not test4:
            return apology("you forgot to add a grade", 400)
        if not test5:
            return apology("you forgot to add a grade", 400)
        if not test6:
            return apology("you forgot to add a grade", 400)
        if not test7:
            return apology("you forgot to add a grade", 400)
        if not test8:
            return apology("you forgot to add a grade", 400)
        if not test9:
            return apology("you forgot to add a grade", 400)
        if not comments:
            return apology("you forgot to add comments", 400)
            
        # insert into table
        db.execute("INSERT INTO subject3(id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments) VALUES(:id, :studentname, :test1, :test2, :test3, :test4, :test5, :test6, :test7, :test8, :test9, :comments)",
            id = session["user_id"],
            studentname = studentname,
            test1 = test1,
            test2 = test2,
            test3 = test3,
            test4 = test4,
            test5 = test5,
            test6 = test6,
            test7 = test7,
            test8 = test8,
            test9 = test9,
            comments = comments)
        average = round(((test1 + test2 + test3 + test4 + test5 + test6 + test7 + test8 + test9) / 9), 1)
        db.execute("UPDATE subject3 SET average = :average WHERE id = :id AND studentname = :studentname", average=average, id = session["user_id"], studentname=studentname)
        #db.execute("INSERT INTO studentgrades(id, studentname) VALUES(:id, :studentname)", id = session["user_id"], studentname = studentname)
        subject3avg = average
        db.execute("UPDATE studentgrades SET subject3avg = :subject3avg WHERE id = :id AND studentname = :studentname", subject3avg=subject3avg, id = session["user_id"], studentname=studentname)
        
        return redirect("/subject3")
        
    else:
        return render_template("managesubject3.html", tests=tests)


@app.route("/subject3", methods=["GET", "POST"])
@login_required
def subject3():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all grades they have
        
    tests = db.execute("SELECT id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments FROM subject3 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments", id=session["user_id"])
        
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Show user's info in table
        for test in tests:
            id = session["user_id"]
            studentname = test["studentname"]    
            test1 = test["test1"]
            test2 = test["test2"]
            test3 = test["test3"]
            test4 = test["test4"]
            test5 = test["test5"]
            test6 = test["test6"]
            test7 = test["test7"]
            test8 = test["test8"]
            test9 = test["test9"]
            average = test["average"]
            comments = test["comments"]
        
        return render_template("subject3.html", tests=tests, studentname=studentname, test1=test1, test2=test2, test3=test3, test4=test4, test5=test5, test6=test6, test7=test7, test8=test8, test9=test9, average=average, comments=comments)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("subject3.html", tests=tests)

@app.route("/managesubject4", methods=["GET", "POST"])
@login_required
def managesubject4():
    """Choose subjects"""
    # Get user's info from table 
    tests = db.execute("SELECT studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments FROM subject4 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get grades
        studentname = request.form.get("studentname")
        test1 = int(request.form.get("test1"))
        test2 = int(request.form.get("test2"))
        test3 = int(request.form.get("test3"))
        test4 = int(request.form.get("test4"))
        test5 = int(request.form.get("test5"))
        test6 = int(request.form.get("test6"))
        test7 = int(request.form.get("test7"))
        test8 = int(request.form.get("test8"))
        test9 = int(request.form.get("test9"))
        comments = request.form.get("comments")    
        
        if not studentname:
            return apology("you forgot to put the student's name", 400)
        if not test1:
            return apology("you forgot to add a grade", 400)
        if not test2:
            return apology("you forgot to add a grade", 400)
        if not test3:
            return apology("you forgot to add a grade", 400)
        if not test4:
            return apology("you forgot to add a grade", 400)
        if not test5:
            return apology("you forgot to add a grade", 400)
        if not test6:
            return apology("you forgot to add a grade", 400)
        if not test7:
            return apology("you forgot to add a grade", 400)
        if not test8:
            return apology("you forgot to add a grade", 400)
        if not test9:
            return apology("you forgot to add a grade", 400)
        if not comments:
            return apology("you forgot to add comments", 400)
            
        # insert into table
        db.execute("INSERT INTO subject4(id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments) VALUES(:id, :studentname, :test1, :test2, :test3, :test4, :test5, :test6, :test7, :test8, :test9, :comments)",
            id = session["user_id"],
            studentname = studentname,
            test1 = test1,
            test2 = test2,
            test3 = test3,
            test4 = test4,
            test5 = test5,
            test6 = test6,
            test7 = test7,
            test8 = test8,
            test9 = test9,
            comments = comments)
        average = round(((test1 + test2 + test3 + test4 + test5 + test6 + test7 + test8 + test9) / 9), 1)
        db.execute("UPDATE subject4 SET average = :average WHERE id = :id AND studentname = :studentname", average=average, id = session["user_id"], studentname=studentname)
        #db.execute("INSERT INTO studentgrades(id, studentname) VALUES(:id, :studentname)", id = session["user_id"], studentname = studentname)
        subject4avg = average
        db.execute("UPDATE studentgrades SET subject4avg = :subject4avg WHERE id = :id AND studentname = :studentname", subject4avg=subject4avg, id = session["user_id"], studentname=studentname)
        
        return redirect("/subject4")
        
    else:
        return render_template("managesubject4.html", tests=tests)


@app.route("/subject4", methods=["GET", "POST"])
@login_required
def subject4():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all grades they have
        
    tests = db.execute("SELECT id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments FROM subject4 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments", id=session["user_id"])
        
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Show user's info in table
        for test in tests:
            id = session["user_id"]
            studentname = test["studentname"]    
            test1 = test["test1"]
            test2 = test["test2"]
            test3 = test["test3"]
            test4 = test["test4"]
            test5 = test["test5"]
            test6 = test["test6"]
            test7 = test["test7"]
            test8 = test["test8"]
            test9 = test["test9"]
            average = test["average"]
            comments = test["comments"]
        
        return render_template("subject4.html", tests=tests, studentname=studentname, test1=test1, test2=test2, test3=test3, test4=test4, test5=test5, test6=test6, test7=test7, test8=test8, test9=test9, average=average, comments=comments)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("subject4.html", tests=tests)


@app.route("/managesubject5", methods=["GET", "POST"])
@login_required
def managesubject5():
    """Choose subjects"""
    # Get user's info from table 
    tests = db.execute("SELECT studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments FROM subject5 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get grades
        studentname = request.form.get("studentname")
        test1 = int(request.form.get("test1"))
        test2 = int(request.form.get("test2"))
        test3 = int(request.form.get("test3"))
        test4 = int(request.form.get("test4"))
        test5 = int(request.form.get("test5"))
        test6 = int(request.form.get("test6"))
        test7 = int(request.form.get("test7"))
        test8 = int(request.form.get("test8"))
        test9 = int(request.form.get("test9"))
        comments = request.form.get("comments")    
        
        if not studentname:
            return apology("you forgot to put the student's name", 400)
        if not test1:
            return apology("you forgot to add a grade", 400)
        if not test2:
            return apology("you forgot to add a grade", 400)
        if not test3:
            return apology("you forgot to add a grade", 400)
        if not test4:
            return apology("you forgot to add a grade", 400)
        if not test5:
            return apology("you forgot to add a grade", 400)
        if not test6:
            return apology("you forgot to add a grade", 400)
        if not test7:
            return apology("you forgot to add a grade", 400)
        if not test8:
            return apology("you forgot to add a grade", 400)
        if not test9:
            return apology("you forgot to add a grade", 400)
        if not comments:
            return apology("you forgot to add comments", 400)
            
        # insert into table
        db.execute("INSERT INTO subject5(id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments) VALUES(:id, :studentname, :test1, :test2, :test3, :test4, :test5, :test6, :test7, :test8, :test9, :comments)",
            id = session["user_id"],
            studentname = studentname,
            test1 = test1,
            test2 = test2,
            test3 = test3,
            test4 = test4,
            test5 = test5,
            test6 = test6,
            test7 = test7,
            test8 = test8,
            test9 = test9,
            comments = comments)
        average = round(((test1 + test2 + test3 + test4 + test5 + test6 + test7 + test8 + test9) / 9), 1)
        db.execute("UPDATE subject5 SET average = :average WHERE id = :id AND studentname = :studentname", average=average, id = session["user_id"], studentname=studentname)
        #db.execute("INSERT INTO studentgrades(id, studentname) VALUES(:id, :studentname)", id = session["user_id"], studentname = studentname)
        subject5avg = average
        db.execute("UPDATE studentgrades SET subject5avg = :subject5avg WHERE id = :id AND studentname = :studentname", subject5avg=subject5avg, id = session["user_id"], studentname=studentname)
        
        return redirect("/subject5")
        
    else:
        return render_template("managesubject5.html", tests=tests)


@app.route("/subject5", methods=["GET", "POST"])
@login_required
def subject5():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all grades they have
        
    tests = db.execute("SELECT id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments FROM subject5 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments", id=session["user_id"])
        
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Show user's info in table
        for test in tests:
            id = session["user_id"]
            studentname = test["studentname"]    
            test1 = test["test1"]
            test2 = test["test2"]
            test3 = test["test3"]
            test4 = test["test4"]
            test5 = test["test5"]
            test6 = test["test6"]
            test7 = test["test7"]
            test8 = test["test8"]
            test9 = test["test9"]
            average = test["average"]
            comments = test["comments"]
        
        return render_template("subject5.html", tests=tests, studentname=studentname, test1=test1, test2=test2, test3=test3, test4=test4, test5=test5, test6=test6, test7=test7, test8=test8, test9=test9, average=average, comments=comments)
 
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("subject5.html", tests=tests)

@app.route("/managesubject6", methods=["GET", "POST"])
@login_required
def managesubject6():
    """Choose subjects"""
    # Get user's info from table 
    tests = db.execute("SELECT studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments FROM subject6 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get grades
        studentname = request.form.get("studentname")
        test1 = int(request.form.get("test1"))
        test2 = int(request.form.get("test2"))
        test3 = int(request.form.get("test3"))
        test4 = int(request.form.get("test4"))
        test5 = int(request.form.get("test5"))
        test6 = int(request.form.get("test6"))
        test7 = int(request.form.get("test7"))
        test8 = int(request.form.get("test8"))
        test9 = int(request.form.get("test9"))
        comments = request.form.get("comments")    
        
        if not studentname:
            return apology("you forgot to put the student's name", 400)
        if not test1:
            return apology("you forgot to add a grade", 400)
        if not test2:
            return apology("you forgot to add a grade", 400)
        if not test3:
            return apology("you forgot to add a grade", 400)
        if not test4:
            return apology("you forgot to add a grade", 400)
        if not test5:
            return apology("you forgot to add a grade", 400)
        if not test6:
            return apology("you forgot to add a grade", 400)
        if not test7:
            return apology("you forgot to add a grade", 400)
        if not test8:
            return apology("you forgot to add a grade", 400)
        if not test9:
            return apology("you forgot to add a grade", 400)
        if not comments:
            return apology("you forgot to add comments", 400)
            
        # insert into table
        db.execute("INSERT INTO subject6(id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, comments) VALUES(:id, :studentname, :test1, :test2, :test3, :test4, :test5, :test6, :test7, :test8, :test9, :comments)",
            id = session["user_id"],
            studentname = studentname,
            test1 = test1,
            test2 = test2,
            test3 = test3,
            test4 = test4,
            test5 = test5,
            test6 = test6,
            test7 = test7,
            test8 = test8,
            test9 = test9,
            comments = comments)
        average = round(((test1 + test2 + test3 + test4 + test5 + test6 + test7 + test8 + test9) / 9), 1)
        db.execute("UPDATE subject6 SET average = :average WHERE id = :id AND studentname = :studentname", average=average, id = session["user_id"], studentname=studentname)
        #db.execute("INSERT INTO studentgrades(id, studentname) VALUES(:id, :studentname)", id = session["user_id"], studentname = studentname)
        subject6avg = average
        db.execute("UPDATE studentgrades SET subject6avg = :subject6avg WHERE id = :id AND studentname = :studentname", subject6avg=subject6avg, id = session["user_id"], studentname=studentname)
        
        return redirect("/subject6")
        
    else:
        return render_template("managesubject6.html", tests=tests)


@app.route("/subject6", methods=["GET", "POST"])
@login_required
def subject6():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all subjects they have
        
    tests = db.execute("SELECT id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments FROM subject6 WHERE id = :id GROUP BY id, studentname, test1, test2, test3, test4, test5, test6, test7, test8, test9, average, comments", id=session["user_id"])
        
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Show user's info in table
        for test in tests:
            id = session["user_id"]
            studentname = test["studentname"]    
            test1 = test["test1"]
            test2 = test["test2"]
            test3 = test["test3"]
            test4 = test["test4"]
            test5 = test["test5"]
            test6 = test["test6"]
            test7 = test["test7"]
            test8 = test["test8"]
            test9 = test["test9"]
            average = test["average"]
            comments = test["comments"]
        
        return render_template("subject6.html", tests=tests, studentname=studentname, test1=test1, test2=test2, test3=test3, test4=test4, test5=test5, test6=test6, test7=test7, test8=test8, test9=test9, average=average, comments=comments)
 
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("subject6.html", tests=tests)

@app.route("/manageabsenttardy", methods=["GET", "POST"])
@login_required
def manageabsenttardy():
    """Choose subjects"""
    # Get user's info from table 
    days = db.execute("SELECT studentname, absent, tardy FROM absenttardy WHERE id = :id GROUP BY id, studentname, absent, tardy", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get info
        studentname = request.form.get("studentname")
        absent = int(request.form.get("absent"))
        tardy = int(request.form.get("tardy"))   
        
        if not studentname:
            return apology("you forgot to put the student's name", 400)
        
            
        # insert into table
        db.execute("INSERT INTO absenttardy(id, studentname) VALUES(:id, :studentname)",
            id = session["user_id"],
            studentname = studentname)
        db.execute("UPDATE absenttardy SET absent = :absent WHERE id = :id AND studentname = :studentname", absent=absent, id = session["user_id"], studentname=studentname)
        #db.execute("INSERT INTO studentgrades(id, studentname) VALUES(:id, :studentname)", id = session["user_id"], studentname = studentname)
        db.execute("UPDATE absenttardy SET tardy = :tardy WHERE id = :id AND studentname = :studentname", tardy=tardy, id = session["user_id"], studentname=studentname)
        
        
        return redirect("/absenttardy")
        
    else:
        return render_template("manageabsenttardy.html", days=days)


@app.route("/absenttardy", methods=["GET", "POST"])
@login_required
def absenttardy():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show info
        
    days = db.execute("SELECT id, studentname, absent, tardy FROM absenttardy WHERE id = :id GROUP BY id, studentname, absent, tardy", id=session["user_id"])
        
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Show user's info in table
        for day in days:
            id = session["user_id"]
            studentname = day["studentname"]    
            absent = day["absent"]
            tardy = day["tardy"]
            
        
        return render_template("absenttardy.html", days=days, studentname=studentname, absent=absent, tardy=tardy)
 
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("absenttardy.html", days=days)


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

@app.route("/managesubjects", methods=["GET", "POST"])
@login_required
def managesubjects():
    """Choose subjects"""
    # Get user's info from table 
    subjects = db.execute("SELECT subject1, subject2, subject3, subject4, subject5, subject6 FROM subjects WHERE id = :id GROUP BY id, subject1, subject2, subject3, subject4, subject5, subject6", id=session["user_id"])
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get subjects
        subject1 = request.form.get("subject1")
        subject2 = request.form.get("subject2")
        subject3 = request.form.get("subject3")
        subject4 = request.form.get("subject4")
        subject5 = request.form.get("subject5")
        subject6 = request.form.get("subject6")
            
        
        db.execute("INSERT INTO subjects (id, subject1, subject2, subject3, subject4, subject5, subject5, subject6) VALUES(:id, :subject1, :subject2, :subject3, :subject4, :subject5, :subject5, :subject6)",
            id = session["user_id"],
            subject1 = subject1,
            subject2 = subject2,
            subject3 = subject3,
            subject4 = subject4,
            subject5 = subject5,
            subject6 = subject6)
        
        if not subject1:
            return apology("you forgot to add a subject", 400)
        if not subject2:
            return apology("you forgot to add a subject", 400)
        if not subject3:
            return apology("you forgot to add a subject", 400)
        if not subject4:
            return apology("you forgot to add a subject", 400)
        if not subject5:
            return apology("you forgot to add a subject", 400)
        if not subject6:
            return apology("you forgot to add a subject", 400)
            
        return redirect("/")
        
    else:
        return render_template("managesubjects.html", subjects=subjects)


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
            
        # Ensure name was submitted
        if not request.form.get("name"):
            return apology("must provide name", 400)
        
        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must provide username", 400)
           
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        # Ensure password is 8 characters long
        elif len(request.form.get("password")) != 8:
            return apology("password must be 8 characters", 400)
        
        # Ensure password was submitted again (confirmation)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation of password", 400)
        
        # Ensure confirmation passwords matches original password
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords don't match", 400)
        
        # Ensure teacher or student was submitted
        #elif not request.form.get("studentteacher"):
            #return apology("must tell if student or teacher", 400)
            
        # Query database for username to see if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
    
        # Ensure username available (username doesn't already exist)
        if len(rows) != 0:
            return apology("username not available", 400)
        
        # Hash password, add hash and user to user table
        new_user = db.execute("INSERT INTO users (username, hash, name) VALUES (:username, :hash, :name)",
            username = request.form.get("username"),
            hash = generate_password_hash(request.form.get("password")),
            name = request.form.get("name"))
        #db.execute("INSERT INTO subjects (id) VALUES (:id)", 
            #id=session["user_id"])
        
        # Remember which user has logged in, now that user is registered in table
        if len(rows) == 1:
            session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html") 


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
