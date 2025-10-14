import reflex as rx

USERS: dict = {"admin@reflex.com": "password123", "user@example.com": "password"}


class AuthState(rx.State):
    in_session: bool = False
    is_admin: bool = False

    @rx.var
    def is_logged_in(self) -> bool:
        return self.in_session

    @rx.event
    def sign_up(self, form_data: dict):
        if form_data["email"] in USERS:
            yield rx.toast("Email already in use", duration=3000)
            return
        else:
            USERS[form_data["email"]] = form_data["password"]
            self.in_session = True
            self.is_admin = form_data["email"] == "admin@reflex.com"
            return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        email = form_data["email"]
        password = form_data["password"]
        if email in USERS and USERS[email] == password:
            self.in_session = True
            self.is_admin = email == "admin@reflex.com"
            if self.is_admin:
                return rx.redirect("/admin")
            return rx.redirect("/")
        else:
            self.in_session = False
            self.is_admin = False
            yield rx.toast("Invalid email or password", duration=3000)

    @rx.event
    def sign_out(self):
        self.in_session = False
        self.is_admin = False
        return rx.redirect("/sign-in")

    @rx.event
    def check_session(self):
        if not self.in_session:
            return rx.redirect("/sign-in")

    @rx.event
    def check_admin(self):
        if not (self.in_session and self.is_admin):
            return rx.redirect("/")