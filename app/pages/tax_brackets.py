import reflex as rx
from app.states.calculator_state import CalculatorState


def tax_brackets_page() -> rx.Component:
    from app.app import app_header

    def bracket_row(bracket: dict, index: int) -> rx.Component:
        lower_bound = rx.cond(
            index == 0, 0, CalculatorState.irs_brackets[index - 1]["limit"]
        )
        upper_bound = rx.cond(
            bracket["limit"] == float("inf"),
            "and above",
            f" - €{str(bracket['limit'])}",
        )
        return rx.el.tr(
            rx.el.td(
                f"€{lower_bound.to_string()}{upper_bound}",
                class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
            ),
            rx.el.td(
                f"{str(bracket['rate'] * 100)}%",
                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
            ),
            class_name="border-b border-gray-200",
        )

    return rx.el.div(
        app_header(),
        rx.el.main(
            rx.el.h1(
                "Tax Brackets for 2025",
                class_name="text-3xl font-bold text-gray-800 mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Bracket (€)",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Rate",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(CalculatorState.irs_brackets, bracket_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
            ),
            class_name="container mx-auto px-4 py-8",
        ),
        class_name="font-['Lora'] bg-gray-50 min-h-screen",
    )