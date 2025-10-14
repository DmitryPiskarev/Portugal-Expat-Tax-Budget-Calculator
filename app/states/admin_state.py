import reflex as rx
from typing import TypedDict
import logging
from app.states.calculator_state import CalculatorState, TaxBracket


class User(TypedDict):
    id: int
    email: str
    is_admin: bool


class AdminState(rx.State):
    """Admin state for managing users and app settings."""

    users: list[User] = [
        {"id": 1, "email": "admin@reflex.com", "is_admin": True},
        {"id": 2, "email": "user@example.com", "is_admin": False},
    ]
    tax_brackets: list[TaxBracket] = []
    is_editing_bracket: bool = False
    editing_bracket_index: int = -1
    editing_bracket: TaxBracket = {"limit": 0, "rate": 0}

    @rx.event
    async def on_load_admin(self):
        """Load initial data for the admin panel."""
        calc_state = await self.get_state(CalculatorState)
        self.tax_brackets = calc_state.irs_brackets.copy()

    @rx.event
    def add_user(self, form_data: dict):
        """Add a new user."""
        email = form_data.get("email")
        if email and email not in [u["email"] for u in self.users]:
            new_id = max((u["id"] for u in self.users)) + 1 if self.users else 1
            self.users.append({"id": new_id, "email": email, "is_admin": False})
        else:
            return rx.toast("Email is invalid or already exists.", duration=3000)

    @rx.event
    def delete_user(self, user_id: int):
        """Delete a user."""
        self.users = [u for u in self.users if u["id"] != user_id]

    @rx.event
    def start_edit_bracket(self, index: int):
        """Start editing a tax bracket."""
        self.is_editing_bracket = True
        self.editing_bracket_index = index
        self.editing_bracket = self.tax_brackets[index].copy()

    @rx.event
    def handle_edit_bracket_change(self, field: str, value: str):
        """Handle changes in the bracket edit form."""
        try:
            self.editing_bracket[field] = (
                float(value) / 100 if field == "rate" else float(value)
            )
        except ValueError as e:
            logging.exception(f"Error parsing bracket value: {e}")

    @rx.event
    def cancel_edit_bracket(self):
        """Cancel editing a tax bracket."""
        self.is_editing_bracket = False
        self.editing_bracket_index = -1
        self.editing_bracket = {"limit": 0, "rate": 0}

    @rx.event
    async def save_bracket(self):
        """Save the edited tax bracket and update the main state."""
        if self.is_editing_bracket and self.editing_bracket_index != -1:
            self.tax_brackets[self.editing_bracket_index] = self.editing_bracket
            self.is_editing_bracket = False
            self.editing_bracket_index = -1
            calc_state = await self.get_state(CalculatorState)
            calc_state.irs_brackets = self.tax_brackets
            return rx.toast("Tax bracket updated successfully!", duration=3000)

    @rx.event
    def add_new_bracket(self):
        """Add a new empty bracket to the list."""
        self.tax_brackets.append({"limit": 0.0, "rate": 0.0})
        self.start_edit_bracket(len(self.tax_brackets) - 1)

    @rx.event
    async def remove_bracket(self, index: int):
        """Remove a tax bracket."""
        if 0 <= index < len(self.tax_brackets):
            del self.tax_brackets[index]
            calc_state = await self.get_state(CalculatorState)
            calc_state.irs_brackets = self.tax_brackets
            return rx.toast("Tax bracket removed.", duration=3000)