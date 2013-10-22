Databases checker
=================

This is a online checking tool for students that are taking my
Data Bases course.

It has following features:

* Contains reusable grading application, that has autograding API (which is
  kind of wonky, and might be subject to change)
* Allows to easily write code to automatically grade student's SQL code.

 * Which for non-trivial cases assumes you use `postgresql1.

* It is used on my course, and it basically works, but I wouldn't call it
  production ready.

Things to note before you hack it:
----------------------------------

* It uses python 3.3 (you'll have to hack it to use 2.6)
* It used django 1.6
* Grading application is in polish and english, but database checker is in polish.
* You'll be able to test it when I prepare code for third classes --- validation code
  for classes one and two is missing by design (as it contains queries student's will
  need to provide, and I can't publish it freely). If you want to test it plese
  give me a hint.
* There is no documentation, feel free to contact me. 

