from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime

class UserApp:
    def __init__(self):
        """
        Initialize the user application.
        """
        self.root = Tk()
        self.root.title("Time Table - User")
        self.root.geometry("1000x600")
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        self.frame = Frame(self.root, bg="#fff")
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.label = Label(self.frame, text="Welcome!", font=("Arial", 18), bg="#fff")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.button = Button(self.root, text="Logout", command=self.logout, bg="red", fg="white")
        self.button.grid(row=8, column=0, padx=10, pady=10)

        self.timetable_frame = Frame(self.root, bg="#fff")
        self.timetable_frame.grid(row=1, column=0, padx=10, pady=10)

        # Grid for timetable cells
        self.schedule = [['' for _ in range(6)] for _ in range(4)]

        for i in range(4):
            for j in range(6):
                label = Label(self.timetable_frame, text=self.schedule[i][j], bg="white", relief="solid", width=15, height=5)
                label.grid(row=i + 1, column=j + 1, padx=10, pady=10)

        # Connect to SQLite database for timetable
        self.conn_timetable = sqlite3.connect("schedule.sqlite3")
        self.conn_timetable.row_factory = sqlite3.Row

        # Connect to SQLite database for users
        self.conn_users = sqlite3.connect("data.sqlite3")
        self.conn_users.row_factory = sqlite3.Row

        self.display_timetable()
        self.set_user_name()

        self.root.mainloop()

    def display_timetable(self):
        """
        Display the timetable in the grid.
        """
        cursor = self.conn_timetable.cursor()
        cursor.execute("SELECT * FROM timetable")

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        hours = ['9:00-11:00', '11:30-13:30', '14:30-16:30', '16:30-18:30']

        for i, day in enumerate(days):
            label = Label(self.timetable_frame, text=day, bg="yellow", width=15)
            label.grid(row=0, column=i + 1, padx=10, pady=10)

        for i, hour in enumerate(hours):
            label = Label(self.timetable_frame, text=hour, bg="lightblue", height=2)
            label.grid(row=i + 1, column=0, padx=10, pady=10)

        for row in cursor:
            teacher = row['teacher']
            lesson = row['lesson']
            classroom = row['classroom']
            time = row['time']
            day = row['day']

            try:
                day_index = days.index(day)
                time_index = hours.index(time)

                self.schedule[time_index][day_index] = f"Teacher: {teacher}\nLesson: {lesson}\nClassroom: {classroom}"

                label = Label(self.timetable_frame, text=self.schedule[time_index][day_index], bg="white", relief="solid", width=15, height=5)
                label.grid(row=time_index + 1, column=day_index + 1, padx=10, pady=10)
            except ValueError:
                pass

    def set_user_name(self):
        """
        Set the user's name and display a welcome message.
        """
        cursor = self.conn_users.cursor()
        cursor.execute("SELECT name FROM users")
        row = cursor.fetchone()

        if row:
            user_name = row['name']
            current_hour = datetime.now().hour

            if current_hour < 12:
                greeting = "Good morning"
            elif current_hour < 18:
                greeting = "Good afternoon"
            else:
                greeting = "Good evening"

            self.label.config(text=f"{greeting}, {user_name}!")

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()

def main():
    """Main function to run the application"""
    user_app = UserApp()
    user_app.root.mainloop()

if __name__ == "__main__":
    main()
