import reflex as rx
from app.states.calculator_state import CalculatorState
from app.components.ui import card, input_field


def expense_inputs() -> rx.Component:
    expense_items = [
        ("housing", "home"),
        ("food", "utensils-crossed"),
        ("transport", "bus"),
        ("utilities", "lightbulb"),
        ("leisure", "martini"),
        ("others", "ellipsis"),
    ]
    return rx.el.div(
        rx.foreach(
            expense_items,
            lambda item: input_field(
                label=item[0].capitalize(),
                icon=item[1],
                default_value=CalculatorState.expenses[item[0]].to_string(),
                on_change=lambda val: CalculatorState.set_expense(item[0], val),
                type="number",
                placeholder=f"e.g. {CalculatorState.expenses[item[0]]:.2f}",
            ),
        ),
        class_name="grid grid-cols-2 gap-4",
    )


def advanced_options() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon("sliders-horizontal", size=16),
                "Advanced Options",
                rx.icon(
                    "chevron-down",
                    size=16,
                    class_name=rx.cond(
                        CalculatorState.show_advanced,
                        "transform rotate-180 transition-transform",
                        "transition-transform",
                    ),
                ),
                class_name="flex items-center gap-2 font-semibold text-sm text-gray-600",
            ),
            on_click=CalculatorState.toggle_advanced,
            class_name="w-full text-left py-2",
        ),
        rx.cond(
            CalculatorState.show_advanced,
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Social Security %",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        default_value=(CalculatorState.ss_rate * 100).to_string(),
                        on_change=CalculatorState.set_ss_rate,
                        class_name="w-full mt-1.5 flex h-10 rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500",
                        type="number",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.label(
                        "D8 Income Coefficient %",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        default_value=(
                            CalculatorState.income_coefficient * 100
                        ).to_string(),
                        on_change=CalculatorState.set_income_coefficient,
                        class_name="w-full mt-1.5 flex h-10 rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500",
                        type="number",
                    ),
                    class_name="w-full",
                ),
                class_name="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 mt-2",
            ),
            None,
        ),
        class_name="mt-4",
    )


def input_form() -> rx.Component:
    return rx.el.div(
        card(
            rx.el.h2(
                "Monthly Income", class_name="text-lg font-semibold text-gray-800 mb-4"
            ),
            input_field(
                label="Monthly Gross Income",
                icon="landmark",
                default_value=CalculatorState.gross_income.to_string(),
                on_change=CalculatorState.set_gross_income,
                type="number",
                placeholder="e.g. 5000.00",
            ),
            advanced_options(),
        ),
        card(
            rx.el.h3(
                "Monthly Expenses",
                class_name="text-md font-semibold text-gray-800 mb-4",
            ),
            expense_inputs(),
        ),
        class_name="flex flex-col gap-8",
    )