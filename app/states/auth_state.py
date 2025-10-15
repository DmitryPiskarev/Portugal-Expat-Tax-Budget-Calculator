import reflex as rx

USERS: dict = {"admin@reflex.com": "password123", "user@example.com": "password"}


class AuthState(rx.State):
    in_session: bool = False
    is_admin: bool = False

    @rx.var
    def is_logged_in(self) -> bool:
        return self.in_session

    # @rx.event
    # def sign_up(self, form_data: dict):
    #     if form_data["email"] in USERS:
    #         yield rx.toast("Email already in use", duration=3000)
    #         return
    #     else:
    #         USERS[form_data["email"]] = form_data["password"]
    #         self.in_session = True
    #         self.is_admin = form_data["email"] == "admin@reflex.com"
    #         return rx.redirect("/")
    @rx.event
    async def sign_up(self, form_data: dict):
        from app.states.admin_state import AdminState  # ✅ import inside to avoid circular import
    
        email = form_data["email"]
        password = form_data["password"]
    
        if email in USERS:
            yield rx.toast("Email already in use", duration=3000)
            return
    
        USERS[email] = password
        self.in_session = True
        self.is_admin = email == "admin@reflex.com"
    
        # ✅ Add user to AdminState so it appears in the admin panel
        admin_state = await self.get_state(AdminState)
        new_id = max((u["id"] for u in admin_state.users), default=0) + 1
        admin_state.users.append({"id": new_id, "email": email, "is_admin": self.is_admin})
    
        yield rx.toast("Account created successfully!", duration=3000)
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
        """Allow anyone to access, even without session."""
        # No redirect; public access
        pass

    @rx.event
    def check_admin(self):
        """Restrict admin panel to logged-in admins only."""
        if not self.is_logged_in:
            return rx.redirect("/sign-in")
        if not self.is_admin:
            return rx.redirect("/")
