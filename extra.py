@app.route("/findstudentgrades", methods=["GET", "POST"])
@login_required
def findstudentgrades():
    """Choose subjects"""
    # Get user's stock infor from table 
    #students1 = db.execute("SELECT studentname FROM subject1 WHERE id = :id GROUP BY id, studentname", id=session["user_id"])
    #students2 = db.execute("SELECT studentname FROM subject2 WHERE id = :id GROUP BY id, studentname", id=session["user_id"])
    #students3 = db.execute("SELECT studentname FROM subject3 WHERE id = :id GROUP BY id, studentname", id=session["user_id"])
    #students4 = db.execute("SELECT studentname FROM subject4 WHERE id = :id GROUP BY id, studentname", id=session["user_id"])
    #students5 = db.execute("SELECT studentname FROM subject5 WHERE id = :id GROUP BY id, studentname", id=session["user_id"])
    #students6 = db.execute("SELECT studentname FROM subject6 WHERE id = :id GROUP BY id, studentname", id=session["user_id"])
    
    #studentgrades = db.execute("SELECT subject1.id, subject1.studentname, subject2.id, subject2.studentname, subject3.id, subject3.studentname, subject4.id, subject4.studentname, subject5.id, subject5.studentname, subject6.id, subject6.studentname, behavior.id, behavior.studentname FROM subject1 INNER JOIN subject2 ON subject1.studentname=subject2.studentname INNER JOIN subject3 ON subject2.studentname=subject3.studentname INNER JOIN subject4 ON subject3.studentname=subject4.studentname INNER JOIN subject5 ON subject4.studentname=subject5.studentname INNER JOIN subject6 ON subject5.studentname=subject6.studentname INNER JOIN behavior ON subject6.studentname=behavior.studentname")
    
    #studentgrades = db.execute("SELECT id, studentname, subject1avg, subject2avg, subject3avg, subject4avg, subject5avg, subject6avg, behavioravg FROM studentgrades WHERE id = :id GROUP BY id, studentname, subject1avg, subject2avg, subject3avg, subject4avg, subject5avg, subject6avg, behavioravg", id=session["user_id"])
    
    db.execute("INSERT INTO studentgrades (id, studentname, subject1avg) SELECT (id, studentname, average) FROM subject1 WHERE id = :id AND studentname = :studentname")
    db.execute("INSERT INTO studentgrades (subject2avg) SELECT (average) FROM subject2 WHERE id = :id AND studentname = :studentname")
    db.execute("INSERT INTO studentgrades (subject3avg) SELECT (average) FROM subject3 WHERE id = :id AND studentname = :studentname")
    db.execute("INSERT INTO studentgrades (subject4avg) SELECT (average) FROM subject4 WHERE id = :id AND studentname = :studentname")
    db.execute("INSERT INTO studentgrades (subject5avg) SELECT (average) FROM subject5 WHERE id = :id AND studentname = :studentname")
    db.execute("INSERT INTO studentgrades (subject6avg) SELECT (average) FROM subject6 WHERE id = :id AND studentname = :studentname")
    db.execute("INSERT INTO studentgrades (behavioravg) SELECT (average) FROM behavior WHERE id = :id AND studentname = :studentname")
    
            #id = session["user_id"],
            #studentname = studentname,
            #subject1avg = average)
            
    print(studentgrades)
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure name was submitted
        if not request.form.get("studentname"):
            return apology("must provide student name", 400)
        
        studentname = request.form.get("studentname")  
        #studentname = ast.literal_eval(studentname)
        print(studentname)
        if 'studentname' in studentgrades: 
            return redirect("/studentgrades")
        else:
        #if not re.search("studentname", (request.form.get("studentgrades"))):
            return apology("student not in records", 400)
        
    else:
        return render_template("findstudentgrades.html", studentgrades=studentgrades)

@app.route("/studentgrades", methods=["GET", "POST"])
@login_required
def studentgrades():
    """Show portfolio of stocks"""
    # Pull up user's data from table to show all subjects they have
    #db.execute("INSERT INTO studentgrades (id, studentname, subject1avg) SELECT (id, studentname, average) FROM subject1 WHERE id = :id AND studentname = :studentname")
    #db.execute("INSERT INTO studentgrades (subject2avg) SELECT (average) FROM subject2 WHERE id = :id AND studentname = :studentname")
    #db.execute("INSERT INTO studentgrades (subject3avg) SELECT (average) FROM subject3 WHERE id = :id AND studentname = :studentname")
    #db.execute("INSERT INTO studentgrades (subject4avg) SELECT (average) FROM subject4 WHERE id = :id AND studentname = :studentname")
    #db.execute("INSERT INTO studentgrades (subject5avg) SELECT (average) FROM subject5 WHERE id = :id AND studentname = :studentname")
    #db.execute("INSERT INTO studentgrades (subject6avg) SELECT (average) FROM subject6 WHERE id = :id AND studentname = :studentname")
    #db.execute("INSERT INTO studentgrades (behavioravg) SELECT (average) FROM behavior WHERE id = :id AND studentname = :studentname")
    
    db.execute("INSERT INTO studentgrades (id, studentname, subject1avg, subject2avg, subject3avg, subject4avg, subject5avg, subject6avg, behavioravg) SELECT average FROM subject1 INNER JOIN subject2 ON subject1.average = subject2.average INNER JOIN subject3 ON subject2.average = subject3.average INNER JOIN subject4 ON subject3.average = subject4.average INNER JOIN subject5 ON subject4.average = subject5.average INNER JOIN subject6 ON subject5.average = subject6.average INNER JOIN behavior ON subject6.average = behavior.average")
    
    students = db.execute("SELECT id, studentname, subject1avg, subject2avg, subject3avg, subject4avg, subject5avg, subject6avg, behavioravg FROM studentgrades WHERE id = :id GROUP BY id, studentname, subject1avg, subject2avg, subject3avg, subject4avg, subject5avg, subject6avg, behavioravg", id=session["user_id"])
        
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Show user's stock info in index table
        for student in students:
            id = session["user_id"]
            studentname = student["studentname"]    
            subject1avg = student["subject1avg"]
            subject2avg = student["subject2avg"]
            subject3avg = student["subject3avg"]
            subject4avg = student["subject4avg"]
            subject5avg = student["subject5avg"]
            subject6avg = student["subject6avg"]
            behavioravg = student["behavioravg"]
        
        return render_template("studentgrades.html", students=students, studentname=studentname, subject1avg=subject1avg, subject2avg=subject2avg, subject3avg=subject3avg, subject4avg=subject4avg, subject5avg=subject5avg, subject6avg=subject6avg, behavioravg=behavioravg)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("studentgrades.html", students=students)


