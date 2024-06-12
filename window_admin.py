from tkinter import *
from tkinter import messagebox
import sqlite3

class AdminApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Time Table")
        self.root.geometry("1000x600")
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        """Labels for the days of the week"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for i, day in enumerate(days):
            label = Label(self.root, text=day, bg="yellow", width=15)
            label.grid(row=0, column=i + 1, padx=10, pady=10)

        """Labels for the hours"""
        hours = ['9:00-11:00', '11:30-13:30', '14:30-16:30', '16:30-18:30']
        for i, hour in enumerate(hours):
            label = Label(self.root, text=hour, bg="lightblue", height=2)
            label.grid(row=i + 1, column=0, padx=10, pady=10)

        """Grid for the timetable slots"""
        self.schedule = [['' for _ in range(6)] for _ in range(4)]

        for i in range(4):
            for j in range(6):
                label = Label(self.root, text=self.schedule[i][j], bg="white", relief="solid", width=15, height=5)
                label.grid(row=i + 1, column=j + 1, padx=10, pady=10)

        """Create button"""
        create_button = Button(self.root, text="Create", command=self.create_entry, bg="blue")
        create_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        """Update button"""
        update_button = Button(self.root, text="Update", command=self.update_entry, bg="yellow")
        update_button.grid(row=8, column=2, columnspan=2, padx=10, pady=10)
        """Delete button"""
        delete_button = Button(self.root, text="Delete", command=self.delete_entry, bg="red")
        delete_button.grid(row=8, column=4, columnspan=2, padx=10, pady=10)
        """Refresh button"""
        refresh_button = Button(self.root, text="Refresh", command=self.refresh_entry, bg="green")
        refresh_button.grid(row=8, column=6, columnspan=2, padx=10, pady=10)

        """Connect to the SQLite database"""
        self.conn = sqlite3.connect("schedule.sqlite3")
        self.create_table()  # Create the table if it doesn't exist yet

        self.root.mainloop()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher TEXT,
                lesson TEXT,
                classroom TEXT,
                time TEXT,
                day TEXT
            )
        """)
        self.conn.commit()

    def create_entry(self):
        entry_window = Toplevel(self.root)
        entry_window.title("Create Entry")
        entry_window.geometry("300x300")
        entry_window.resizable(False, False)

        """Labels and Entries for inputting the entry information"""
        teacher_label = Label(entry_window, text="Teacher:")
        teacher_label.grid(row=0, column=0, padx=10, pady=10)
        teacher_entry = Entry(entry_window)
        teacher_entry.grid(row=0, column=1, padx=10, pady=10)

        lesson_label = Label(entry_window, text="Lesson:")
        lesson_label.grid(row=1, column=0, padx=10, pady=10)
        lesson_entry = Entry(entry_window)
        lesson_entry.grid(row=1, column=1, padx=10, pady=10)

        classroom_label = Label(entry_window, text="Classroom:")
        classroom_label.grid(row=2, column=0, padx=10, pady=10)
        classroom_entry = Entry(entry_window)
        classroom_entry.grid(row=2, column=1, padx=10, pady=10)

        time_label = Label(entry_window, text="Time:")
        time_label.grid(row=3, column=0, padx=10, pady=10)
        time_entry = Entry(entry_window)
        time_entry.grid(row=3, column=1, padx=10, pady=10)

        day_label = Label(entry_window, text="Day:")
        day_label.grid(row=4, column=0, padx=10, pady=10)
        day_entry = Entry(entry_window)
        day_entry.grid(row=4, column=1, padx=10, pady=10)

        """Save button"""
        save_button = Button(entry_window, text="Save", command=lambda: self.save_entry(
            teacher_entry.get(), lesson_entry.get(), classroom_entry.get(), time_entry.get(), day_entry.get(), entry_window))
        save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def update_entry(self):
        entry_window = Toplevel(self.root)
        entry_window.title("Update Entry")
        entry_window.geometry("300x200")
        entry_window.resizable(False, False)

        """Label and Entry for searching by teacher's name"""
        search_label = Label(entry_window, text="Teacher Name:")
        search_label.grid(row=0, column=0, padx=10, pady=10)
        search_entry = Entry(entry_window)
        search_entry.grid(row=0, column=1, padx=10, pady=10)

        """Search button"""
        search_button = Button(entry_window, text="Search", command=lambda: self.search_entry(search_entry.get(), entry_window))
        search_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def delete_entry(self):
        search_window = Toplevel(self.root)
        search_window.title("Delete Entry")
        search_window.geometry("300x100")
        search_window.resizable(False, False)

        teacher_label = Label(search_window, text="Teacher:")
        teacher_label.pack()
        teacher_entry = Entry(search_window)
        teacher_entry.pack()

        search_button = Button(search_window, text="Search", command=lambda: self.search_entry_to_delete(
            teacher_entry.get(),
            search_window
        ))
        search_button.pack()

    def search_entry_to_delete(self, teacher, search_window):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM timetable WHERE teacher=?", (teacher,))
        entry = cursor.fetchone()

        search_window.destroy()
        self.delete_entry_confirmation(entry)

    def delete_entry_confirmation(self, entry):
        confirmation_window = Toplevel(self.root)
        confirmation_window.title("Delete Entry")
        confirmation_window.geometry("300x100")
        confirmation_window.resizable(False, False)

        confirmation_label = Label(confirmation_window, text=f"Do you want to delete this entry?\n{entry}")
        confirmation_label.pack()

        confirm_button = Button(confirmation_window, text="Confirm", command=lambda: self.confirm_delete_entry(
            entry[0],
            confirmation_window
        ))
        confirm_button.pack()

    def confirm_delete_entry(self, entry_id, confirmation_window):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM timetable WHERE id=?", (entry_id,))
        self.conn.commit()

        confirmation_window.destroy()
        self.update_schedule_grid()

    def refresh_entry(self):
        self.schedule = [['' for _ in range(6)] for _ in range(4)]
        self.update_schedule_grid()

        """Retrieve data from the database and update self.schedule"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM timetable")
        entries = cursor.fetchall()

        for entry in entries:
            day_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].index(entry[5])
            time_index = ['9:00-11:00', '11:30-13:30', '14:30-16:30', '16:30-18:30'].index(entry[4])
            self.schedule[time_index][day_index] = f"Teacher: {entry[1]}\nLesson: {entry[2]}\nClassroom: {entry[3]}"

        self.update_schedule_grid()

    def save_entry(self, teacher, lesson, classroom, time, day, entry_window):
        try:
            day_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].index(day)
            time_index = ['9:00-11:00', '11:30-13:30', '14:30-16:30', '16:30-18:30'].index(time)
            self.schedule[time_index][day_index] = f"Teacher: {teacher}\nLesson: {lesson}\nClassroom: {classroom}"
            self.update_schedule_grid()

            """Insert the entry into the SQLite database"""
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO timetable (teacher, lesson, classroom, time, day)
                VALUES (?, ?, ?, ?, ?)
            """, (teacher, lesson, classroom, time, day))
            self.conn.commit()

            self.root.focus_set()
            messagebox.showinfo("Success", "Timetable entry saved successfully!")
            entry_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid day or time entered!")

    def search_entry(self, teacher, entry_window):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM timetable WHERE teacher = ?", (teacher,))
        entry = cursor.fetchone()

        if entry is not None:
            entry_window.destroy()
            self.show_update_entry_window(entry)
        else:
            messagebox.showerror("Error", "Teacher not found!")

    def show_update_entry_window(self, entry):
        update_window = Toplevel(self.root)
        update_window.title("Update Entry")
        update_window.geometry("300x300")
        update_window.resizable(False, False)

        teacher_label = Label(update_window, text="Teacher:")
        teacher_label.grid(row=0, column=0, padx=10, pady=10)
        teacher_entry = Entry(update_window)
        teacher_entry.insert(0, entry[1])
        teacher_entry.grid(row=0, column=1, padx=10, pady=10)

        lesson_label = Label(update_window, text="Lesson:")
        lesson_label.grid(row=1, column=0, padx=10, pady=10)
        lesson_entry = Entry(update_window)
        lesson_entry.insert(0, entry[2])
        lesson_entry.grid(row=1, column=1, padx=10, pady=10)

        classroom_label = Label(update_window, text="Classroom:")
        classroom_label.grid(row=2, column=0, padx=10, pady=10)
        classroom_entry = Entry(update_window)
        classroom_entry.insert(0, entry[3])
        classroom_entry.grid(row=2, column=1, padx=10, pady=10)

        time_label = Label(update_window, text="Time:")
        time_label.grid(row=3, column=0, padx=10, pady=10)
        time_entry = Entry(update_window)
        time_entry.insert(0, entry[4])
        time_entry.grid(row=3, column=1, padx=10, pady=10)

        day_label = Label(update_window, text="Day:")
        day_label.grid(row=4, column=0, padx=10, pady=10)
        day_entry = Entry(update_window)
        day_entry.insert(0, entry[5])
        day_entry.grid(row=4, column=1, padx=10, pady=10)

        """Save changes button"""
        save_button = Button(update_window, text="Save", command=lambda: self.save_updated_entry(
            entry[0], teacher_entry.get(), lesson_entry.get(), classroom_entry.get(), time_entry.get(), day_entry.get(), update_window))
        save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def save_updated_entry(self, entry_id, teacher, lesson, classroom, time, day, update_window):
        try:
            day_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].index(day)
            time_index = ['9:00-11:00', '11:30-13:30', '14:30-16:30', '16:30-18:30'].index(time)
            self.schedule[time_index][day_index] = f"Teacher: {teacher}\nLesson: {lesson}\nClassroom: {classroom}"
            self.update_schedule_grid()

            """Update the entry in the SQLite database"""
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE timetable
                SET teacher = ?, lesson = ?, classroom = ?, time = ?, day = ?
                WHERE id = ?
            """, (teacher, lesson, classroom, time, day, entry_id))
            self.conn.commit()

            self.root.focus_set()
            messagebox.showinfo("Success", "Timetable entry updated successfully!")
            update_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid day or time entered!")

    def update_schedule_grid(self):
        for i in range(4):
            for j in range(6):
                label = Label(self.root, text=self.schedule[i][j], bg="white", relief="solid", width=15, height=5)
                label.grid(row=i + 1, column=j + 1, padx=10, pady=10)

def main():
    """Main function to run the application"""
    admin_app = AdminApp()
    admin_app.root.mainloop()

if __name__ == "__main__":
    main()
