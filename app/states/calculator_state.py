import reflex as rx
from typing import TypedDict
import logging
import httpx


class TaxBracket(TypedDict):
    limit: float
    rate: float


class CalculatorState(rx.State):
    gross_income: float = 5000.0
    expenses: dict[str, float] = {
        "housing": 1200.0,
        "food": 400.0,
        "transport": 150.0,
        "utilities": 100.0,
        "leisure": 250.0,
        "others": 100.0,
    }
    ss_rate: float = 0.214
    ss_base_coefficient: float = 0.7
    income_coefficient: float = 0.75
    show_advanced: bool = False
    irs_brackets: list[TaxBracket] = [
        {"limit": 8059, "rate": 0.13},
        {"limit": 12160, "rate": 0.165},
        {"limit": 17233, "rate": 0.22},
        {"limit": 22306, "rate": 0.25},
        {"limit": 28400, "rate": 0.32},
        {"limit": 41629, "rate": 0.355},
        {"limit": 44987, "rate": 0.435},
        {"limit": 83696, "rate": 0.45},
        {"limit": float("inf"), "rate": 0.48},
    ]

    @rx.event
    def set_gross_income(self, value: str):
        try:
            self.gross_income = float(value) if value else 0.0
        except ValueError as e:
            logging.exception(f"Error parsing gross income: {e}")
            self.gross_income = 0.0

    @rx.event
    def set_expense(self, category: str, value: str):
        try:
            self.expenses[category] = float(value) if value else 0.0
        except ValueError as e:
            logging.exception(f"Error parsing expense for {category}: {e}")
            self.expenses[category] = 0.0

    @rx.event
    def set_ss_rate(self, value: str):
        try:
            self.ss_rate = float(value) / 100 if value else 0.0
        except ValueError as e:
            logging.exception(f"Error parsing SS rate: {e}")
            self.ss_rate = 0.0

    @rx.event
    def set_ss_base_coefficient(self, value: str):
        try:
            self.ss_base_coefficient = float(value) / 100 if value else 0.0
        except ValueError as e:
            logging.exception(f"Error parsing SS base coefficient: {e}")
            self.ss_base_coefficient = 0.0

    @rx.event
    def set_income_coefficient(self, value: str):
        try:
            self.income_coefficient = float(value) / 100 if value else 0.0
        except ValueError as e:
            logging.exception(f"Error parsing income coefficient: {e}")
            self.income_coefficient = 0.0

    @rx.event
    def toggle_advanced(self):
        self.show_advanced = not self.show_advanced

    @rx.var
    def annual_gross_income(self) -> float:
        return self.gross_income * 12

    @rx.var
    def taxable_income(self) -> float:
        g = self.annual_gross_income
        return g * self.income_coefficient - g * self.ss_base_coefficient * self.ss_rate

    @rx.var
    def social_security_due(self) -> float:
        return self.annual_gross_income * self.ss_base_coefficient * self.ss_rate

    @rx.var
    def irs_due(self) -> float:
        income = self.taxable_income
        if income <= 0:
            return 0.0
        total_tax = 0.0
        lower_bound = 0.0
        for bracket in self.irs_brackets:
            if income > lower_bound:
                taxable_at_rate = min(income, bracket["limit"]) - lower_bound
                total_tax += taxable_at_rate * bracket["rate"]
                lower_bound = bracket["limit"]
            else:
                break
        return total_tax

    @rx.var
    def total_tax_due(self) -> float:
        return self.irs_due + self.social_security_due

    @rx.var
    def effective_tax_rate(self) -> float:
        if self.annual_gross_income > 0:
            return self.total_tax_due / self.annual_gross_income * 100
        return 0.0

    @rx.var
    def annual_take_home_pay(self) -> float:
        return self.annual_gross_income - self.total_tax_due

    @rx.var
    def monthly_take_home_pay(self) -> float:
        return self.annual_take_home_pay / 12

    @rx.var
    def total_monthly_expenses(self) -> float:
        return sum(self.expenses.values())

    @rx.var
    def estimated_net_after_expenses(self) -> float:
        return self.monthly_take_home_pay - self.total_monthly_expenses

    @rx.var
    def savings_rate(self) -> float:
        if self.monthly_take_home_pay > 0:
            return self.estimated_net_after_expenses / self.monthly_take_home_pay * 100
        return 0.0

    @rx.var
    def monthly_take_home_pay_formatted(self) -> str:
        return f"{self.monthly_take_home_pay:.2f}"

    @rx.var
    def annual_take_home_pay_formatted(self) -> str:
        return f"{self.annual_take_home_pay:.2f}"

    @rx.var
    def effective_tax_rate_formatted(self) -> str:
        return f"{self.effective_tax_rate:.2f}"

    @rx.var
    def savings_rate_formatted(self) -> str:
        return f"{self.savings_rate:.2f}"

    @rx.var
    def irs_due_formatted(self) -> str:
        return f"{self.irs_due:.2f}"

    @rx.var
    def social_security_due_formatted(self) -> str:
        return f"{self.social_security_due:.2f}"

    @rx.var
    def total_tax_due_formatted(self) -> str:
        return f"{self.total_tax_due:.2f}"

    @rx.var
    def total_monthly_expenses_formatted(self) -> str:
        return f"{self.total_monthly_expenses:.2f}"

    @rx.var
    def estimated_net_after_expenses_formatted(self) -> str:
        return f"{self.estimated_net_after_expenses:.2f}"

    @rx.var
    def budget_chart_data(self) -> list[dict[str, str | float]]:
        colors = ["#8884d8", "#82ca9d", "#ffc658", "#ff8042", "#a4de6c", "#d0ed57"]
        data = [
            {
                "name": category.capitalize(),
                "value": round(value, 2),
                "fill": colors[i % len(colors)],
            }
            for i, (category, value) in enumerate(self.expenses.items())
        ]
        if self.estimated_net_after_expenses > 0:
            data.append(
                {
                    "name": "Savings",
                    "value": round(self.estimated_net_after_expenses, 2),
                    "fill": "#4caf50",
                }
            )
        return data

    currency_from: str = "USD"
    currency_to: str = "EUR"
    conversion_rate: float = 1.0
    converted_income: float = 0.0
    conversion_amount: float = 0.0

    @rx.event
    def set_conversion_amount(self, val: str):
        try:
            self.conversion_amount = float(val) if val else 0.0
        except ValueError as e:
            logging.exception(f"Error parsing conversion amount: {e}")
            self.conversion_amount = 0.0

    @rx.var
    def converted_income_text(self) -> str:
        return f"{self.converted_income:.2f} {self.currency_to}"

    @rx.event
    def set_currency_from(self, val: str):
        self.currency_from = val

    @rx.event
    def set_currency_to(self, val: str):
        self.currency_to = val

    @rx.event
    async def fetch_conversion_rate(self):
        """Fetch conversion rate from a free API"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"https://api.frankfurter.app/latest?from={self.currency_from}&to={self.currency_to}"
                resp = await client.get(url)
                data = resp.json()
                self.conversion_rate = data["rates"][self.currency_to]
                self.converted_income = self.conversion_rate * float(self.gross_income)
        except Exception as e:
            print("Error fetching conversion rate:", e)
            self.conversion_rate = 1.0
