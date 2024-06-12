# School Application Documentation
The school application is a simple graphical interface for managing teachers' timetables. It allows creating, updating, deleting, and displaying information related to the courses taught by teachers.

# Installation
Make sure you have Python 3.x installed on your system.
Download the files main.py, window_admin.py, and logo.png into the same directory.
Install the tkinter module by running the following command in your terminal:

pip install tkinter

Make sure you have SQLite3 database installed on your system.
# Running the Application
Open a terminal and navigate to the directory containing the application files.
Run the following command to launch the application:

python main.py

# Using the Application
Login Screen
When you run the application, you are greeted with the login screen. You can log in as an administrator or as a user.

As an administrator, you need to use a username starting with "admin".
As a user, you can use any username other than "admin".
If you don't have an account, you can click the "Sign up" button to create a new account.

Administrator Screen
Once logged in as an administrator, you access the administrator screen, which displays the teachers' timetable.

The weekdays are displayed at the top of the screen.
The class hours are displayed on the left side of the screen.
Each cell represents a course and displays the details of that course (teacher, subject, classroom).
You can perform the following actions:

Create an entry: Click the "Create" button to open a window for entering the details of a new course. Once the details are entered, click "Save" to save the course in the database and display it in the timetable.
Update an entry: Click the "Update" button to open a search window. Enter the teacher's name to search for the corresponding course. Once the course is found, you can update it by modifying the details and clicking "Save".
Delete an entry: Click the "Delete" button to open a search window. Enter the teacher's name to search for the corresponding course. Once the course is found, you can delete it by clicking "Delete".
Refresh the display: Click the "Refresh" button to refresh the timetable display.
User Screen
Once logged in as a user, you access the user screen, which displays a welcome message.

You can click the "Logout" button to log out of the application.
Application Logout
At any time, you can log out of the application by clicking the "Logout" button. You will be prompted to confirm your logout.

# Conclusion
This documentation has described the different functionalities of the school application and explained how to use it. You are now ready to use the application to efficiently and user-friendly manage the timetables of teachers or students. Enjoy the experience!
