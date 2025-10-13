import reflex as rx

USERS: dict = {"admin@reflex.com": "password123"}


class AuthState(rx.State):
    in_session: bool = True

    @rx.event
    def sign_up(self, form_data: dict):
        if form_data["email"] in USERS:
            yield rx.toast("Email already in use", duration=3000)
            return
        else:
            USERS[form_data["email"]] = form_data["password"]
            self.in_session = True
            return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        if (
            form_data["email"] in USERS
            and USERS[form_data["email"]] == form_data["password"]
        ):
            self.in_session = True
            return rx.redirect("/")
        else:
            self.in_session = False
            yield rx.toast("Invalid email or password", duration=3000)

    @rx.event
    def sign_out(self):
        self.in_session = False
        return rx.redirect("/sign-in")

    @rx.event
    def check_session(self):
        if self.in_session:
            return
        else:
            return rx.redirect("/sign-in")