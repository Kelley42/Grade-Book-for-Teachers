# GradeBook for Teachers
#### Video Demo:  <https://youtu.be/B6pehotV_Po>
### Description:
I designed GradeBook for Teachers as a gradebook that teachers can use to record grades, for subjects as 
well as for behavior, and absences/tardies. As a former teacher, it was a chore keeping track of the 
students' grades, so I wanted something that would simplify not only recording the grades but also 
averaging them together. I enjoyed working on the tables from pset9, so I took that knowledge and applied
it to the final project.

### application.py
This file is where all of my python code is stored, including all of the functions for each page of my
program. It includes functions for an apology, registering, logging in and out, managing and displaying the subjects 
and grades, and managing and displaying the absences/tardies. It uses not only python but also SQL and 
flask.

### finance.db
This database is used from pset9 but with instead storing the tables for the final project. These tables
store the grades and absences/tardies. I inserted into or updated them from the user's input, then 
selected the information to display. There is one table to store each user, one table to store each 
subject's grades, one for behavior grades, and another for absences/tardies. I used SQL to insert into or 
select from the tables.

### templates
All of my html files are stored in templates. This is where I designed how each page of the program would
look and act and what it would display. There is an html file for each function I wrote in python,
including pages for an apology, registering, logging in and out, managing and displaying the subjects and grades,
and managing and displaying the absences/tardies.

### Design Choices
It took me a while to decide how best to have the user record grades. Should the teacher input grades
by subject? By student? How should everything be organized and then displayed? I finally decided it would
be easiest to have the subjects decided first and then the teacher could go into each subject and input
each student's grades. 

### How the app works
Initially users are directed to the Log In page. If they do not have an account, however,
they must register by clicking Create Account. Then they must type in a name, username, password, and
matching confirmation password. If any of these are not present, an apology message will appear prompting
them to remedy it. Once users are registered, they then log in with their username and password and
are taken to the index page where it shows all the subjects that they teach. 

If users are new and have not created any subjects yet, then they can click the link to Add Subjects. 
From here they are presented with a form to fill in subjects. Once submitted, the index page now shows all 
their subjects. From this page, each subject is now a link to a separate page which will display all of 
that subject's students and grades. 

If users create a Reading subject, for example, and click on the Reading link, they are taken to the Reading page 
where, if they have not added any students yet, they can click on the Add Grades link. On that page, they can
add the student's name and grades for the semester. They can also add comments for that semester, which is
a helpful reminder for teachers if the student is improving or needs additional help in certain areas.
After submitting this form, a table is then displayed showing the student's name, grades, and the teacher's
comment. Also the average, rounded to the tenth, is displayed, which is helpful for teachers who need to 
do averaging for progress reports or report cards.

Users can do each subject like this, returning to see the index page at any time by clicking Subjects.
When finished, teachers can then create behavior grades for each of their students by clicking Behavior at the 
top. It works the same way as the subjects pages. They input the student's name and grades for each week
into the form and submit them, causing a table to display showing the student's name, grades, average, 
and any comments they wished to make.

Teachers can then create an absent/tardy table with all of their students in it. They can click on Absent/
Tardy, which takes them to a form where they can input the student's name and the number of absent days
and tardy days. The table will display all their students' absences and tardies. This is also helpful as 
progress reports and report cards often require teachers to keep track of these numbers as well.

I hope that I can someday improve this app even more so that teachers will be able to use this every
day to record their students' grades and absences/tardies. Instead of carrying around a heavy binder 
in which to record all of the grades and then accidentally leaving it at school the day before report cards
are due, the teacher could have access to this gradebook all the time via an app on their phone. It will 
be much easier to use than having to enter everything in manually and then having to also avaerage 
all of the grades with a calculator. I hope one day a later version of this app will make teachers' lives
easier.
