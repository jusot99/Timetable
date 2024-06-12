from tkinter import *
from tkinter import messagebox
import sqlite3
import window_admin
import window_user

class MainApp:
    """Class representing the main application"""

    def __init__(self):
        """Initialize the application by creating the main window and UI elements"""

        self.root = Tk()
        self.root.title("School Application")
        self.root.geometry("925x500+300+200")
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        self.img = PhotoImage(file="logo.png")
        Label(self.root, image=self.img, bg="white").place(x=50, y=50)

        self.frame = Frame(self.root, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        self.heading = Label(self.frame, text="SIGN IN", fg="#57a1f8", bg="white",
                             font=("Microsoft YaHei UI Light", 23, "bold"))
        self.heading.place(x=100, y=5)

        self.user = Entry(self.frame, width=25, fg="grey", border=0, bg="white",
                          font=("Microsoft YaHei UI Light", 11))
        self.user.insert(0, "Username")
        self.user.place(x=30, y=80)
        self.user.bind("<FocusIn>", self.on_entry_click)
        self.user.bind("<FocusOut>", self.on_entry_leave)

        self.password = Entry(self.frame, width=25, fg="grey", border=0, bg="white",
                              font=("Microsoft YaHei UI Light", 11))
        self.password.insert(0, "Password")
        self.password.place(x=30, y=150)
        self.password.bind("<FocusIn>", self.on_password_click)
        self.password.bind("<FocusOut>", self.on_password_leave)

        Button(self.frame, width=39, pady=7, text="Sign in", bg="#57a1f8", fg="white", border=0,
               command=self.signin).place(x=35, y=204)

        Label(self.frame, text="Don't have an account?", fg="black", bg="white",
              font=("Microsoft YaHei UI Light", 9)).place(x=75, y=270)

        Button(self.frame, width=6, text="Sign up", border=0, bg="white", cursor="hand2",
               fg="#57a1f8", command=self.signup).place(x=230, y=260)

        self.create_database()

    def create_database(self):
        """Create the database and the 'users' table if they do not exist"""

        conn = sqlite3.connect("data.sqlite3")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, name TEXT)")
        conn.commit()
        conn.close()

    def on_entry_click(self, event):
        """Handle placeholder text behavior when clicking on the username entry field"""

        if self.user.get() == "Username":
            self.user.delete(0, END)
            self.user.config(fg="black")

    def on_entry_leave(self, event):
        """Handle placeholder text behavior when leaving the username entry field"""

        if self.user.get() == "":
            self.user.insert(0, "Username")
            self.user.config(fg="grey")

    def on_password_click(self, event):
        """Handle placeholder text behavior when clicking on the password entry field"""

        if self.password.get() == "Password":
            self.password.delete(0, END)
            self.password.config(show="*")

    def on_password_leave(self, event):
        """Handle placeholder text behavior when leaving the password entry field"""

        if self.password.get() == "":
            self.password.insert(0, "Password")
            self.password.config(show="")

    def signin(self):
        """Authenticate the user when they click the 'Sign in' button"""

        username = self.user.get()
        password = self.password.get()

        if self.authenticate_user(username, password):
            if username.startswith("admin"):
                self.open_admin_page()
            else:
                self.open_user_page()
        else:
            messagebox.showerror("Invalid", "Invalid Username or Password!")

    def authenticate_user(self, username, password):
        """Authenticate the user by verifying the credentials"""

        conn = sqlite3.connect("data.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()

        return bool(result)

    def open_admin_page(self):
        """Open the admin window and close the main window"""

        self.root.destroy()
        admin_app = window_admin.AdminApp()
        admin_app.root.mainloop()

    def open_user_page(self):
        """Open the user window and close the main window"""

        self.root.destroy()
        user_app = window_user.UserApp()
        user_app.root.mainloop()

    def signup(self):
        """Open the sign-up window when a new user clicks the 'Sign up' button"""

        def submit():
            name = entry_name.get()
            username = entry_username.get()
            password = entry_password.get()

            if name == "" or username == "" or password == "":
                messagebox.showerror("Invalid", "Please fill in all the fields.")
            else:
                self.register_user(name, username, password)
                messagebox.showinfo("Success", "You have successfully signed up!")
                signup_screen.destroy()

        signup_screen = Toplevel(self.root)
        signup_screen.title("Sign Up")
        signup_screen.geometry("400x300+400+200")
        signup_screen.config(bg="white")

        Label(signup_screen, text="Sign Up", fg="#57a1f8", bg="white",
              font=("Microsoft YaHei UI Light", 23, "bold")).pack(pady=20)

        Label(signup_screen, text="Name:", bg="white",
              font=("Microsoft YaHei UI Light", 11)).pack()
        entry_name = Entry(signup_screen, width=30)
        entry_name.pack(pady=5)

        Label(signup_screen, text="Username:", bg="white",
              font=("Microsoft YaHei UI Light", 11)).pack()
        entry_username = Entry(signup_screen, width=30)
        entry_username.pack(pady=5)

        Label(signup_screen, text="Password:", bg="white",
              font=("Microsoft YaHei UI Light", 11)).pack()
        entry_password = Entry(signup_screen, width=30)
        entry_password.pack(pady=5)

        Button(signup_screen, text="Submit", width=20, bg="#57a1f8", fg="white",
               command=submit).pack(pady=10)

        signup_screen.mainloop()

    def register_user(self, name, username, password):
        """Register a new user in the database"""

        conn = sqlite3.connect("data.sqlite3")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", (username, password, name))
        conn.commit()
        conn.close()

def main():
    """Main function to run the application"""

    app = MainApp()
    app.root.mainloop()

if __name__ == "__main__":
    main()
