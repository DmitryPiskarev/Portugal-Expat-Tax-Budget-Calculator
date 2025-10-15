# import reflex as rx

# USERS: dict = {"admin@reflex.com": "password123", "user@example.com": "password"}


# class AuthState(rx.State):
#     in_session: bool = False
#     is_admin: bool = False

#     @rx.var
#     def is_logged_in(self) -> bool:
#         return self.in_session

#     @rx.event
#     def sign_up(self, form_data: dict):
#         if form_data["email"] in USERS:
#             yield rx.toast("Email already in use", duration=3000)
#             return
#         else:
#             USERS[form_data["email"]] = form_data["password"]
#             self.in_session = True
#             self.is_admin = form_data["email"] == "admin@reflex.com"
#             return rx.redirect("/")

#     @rx.event
#     def sign_in(self, form_data: dict):
#         email = form_data["email"]
#         password = form_data["password"]
#         if email in USERS and USERS[email] == password:
#             self.in_session = True
#             self.is_admin = email == "admin@reflex.com"
#             if self.is_admin:
#                 return rx.redirect("/admin")
#             return rx.redirect("/")
#         else:
#             self.in_session = False
#             self.is_admin = False
#             yield rx.toast("Invalid email or password", duration=3000)

#     @rx.event
#     def sign_out(self):
#         self.in_session = False
#         self.is_admin = False
#         return rx.redirect("/sign-in")

#     @rx.event
#     def check_session(self):
#         """Allow anyone to access, even without session."""
#         # No redirect; public access
#         pass

#     @rx.event
#     def check_admin(self):
#         """Restrict admin panel to logged-in admins only."""
#         if not self.is_logged_in:
#             return rx.redirect("/sign-in")
#         if not self.is_admin:
#             return rx.redirect("/")
# app/states/auth_state.py
import reflex as rx
import sqlite3
from app.db import get_connection

class AuthState(rx.State):
    in_session: bool = False
    is_admin: bool = False
    current_user_email: str = ""

    @rx.var
    def is_logged_in(self) -> bool:
        return self.in_session

    @rx.event
    def sign_up(self, form_data: dict):
        email = form_data["email"]
        password = form_data["password"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            yield rx.toast("Email already in use", duration=3000)
            conn.close()
            return

        # Insert new user into database
        cursor.execute(
            "INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",
            (email, password, 0),
        )
        conn.commit()
        conn.close()

        # Update session state
        self.in_session = True
        self.is_admin = False
        self.current_user_email = email
        return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        email = form_data["email"]
        password = form_data["password"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_admin FROM users WHERE email = ? AND password = ?", (email, password)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            self.in_session = True
            self.is_admin = bool(row[0])
            self.current_user_email = email
            if self.is_admin:
                return rx.redirect("/admin")
            return rx.redirect("/")
        else:
            self.in_session = False
            self.is_admin = False
            self.current_user_email = ""
            yield rx.toast("Invalid email or password", duration=3000)

    @rx.event
    def sign_out(self):
        self.in_session = False
        self.is_admin = False
        self.current_user_email = ""
        return rx.redirect("/sign-in")

    @rx.event
    def check_session(self):
        """Allow anyone to access, even without session."""
        pass

    @rx.event
    def check_admin(self):
        """Restrict admin panel to logged-in admins only."""
        if not self.is_logged_in:
            return rx.redirect("/sign-in")
        if not self.is_admin:
            return rx.redirect("/")

