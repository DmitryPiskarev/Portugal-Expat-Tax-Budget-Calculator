import reflex as rx
from app.states.calculator_state import CalculatorState
from app.components.ui import card, metric_card


def budget_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Budget Breakdown", class_name="text-md font-semibold text-gray-800 mb-2"
        ),
        rx.recharts.responsive_container(
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    rx.foreach(
                        CalculatorState.budget_chart_data,
                        lambda item: rx.recharts.cell(fill=item["fill"].to(str)),
                    ),
                    data=CalculatorState.budget_chart_data,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    outer_radius=80,
                    label=True,
                ),
                rx.recharts.tooltip(),
                rx.recharts.legend(),
            ),
            height=300,
        ),
        class_name="mt-6",
    )


def results_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Your Results", class_name="text-lg font-semibold text-gray-800 mb-4"),
        card(
            rx.el.p(
                "Monthly Take-Home Pay",
                class_name="text-md font-semibold text-violet-700",
            ),
            rx.el.p(
                "€",
                rx.text.strong(f"{CalculatorState.monthly_take_home_pay_formatted}"),
                class_name="text-4xl font-bold text-gray-800 mt-2",
            ),
            rx.el.p(
                f"€{CalculatorState.annual_take_home_pay_formatted} annually",
                class_name="text-sm text-gray-500 mt-1",
            ),
            class_name="bg-violet-50 border-violet-200",
        ),
        metric_card(
            "Effective Tax Rate",
            f"{CalculatorState.effective_tax_rate_formatted}%",
            "percent",
        ),
        card(
            rx.el.h3(
                "Tax Breakdown (Annual)",
                class_name="text-md font-semibold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("IRS (Income Tax)", class_name="text-sm text-gray-600"),
                    rx.el.p(
                        f"€{CalculatorState.irs_due_formatted}",
                        class_name="font-semibold text-gray-800",
                    ),
                    class_name="flex justify-between items-center py-2",
                ),
                rx.el.div(
                    rx.tooltip(
                        rx.el.div(
                            rx.el.p(
                                "Social Security",
                                rx.icon(
                                    "info", size=12, class_name="ml-1 text-gray-500"
                                ),
                                class_name="flex items-center text-sm text-gray-600 cursor-pointer",
                            ),
                            rx.el.p(
                                f"€{CalculatorState.social_security_due_formatted}",
                                class_name="font-semibold text-gray-800",
                            ),
                            class_name="flex justify-between items-center w-full",
                        ),
                        content=f"Annual Gross x {CalculatorState.ss_base_coefficient * 100:.1f}% x {CalculatorState.ss_rate * 100:.1f}%",
                    ),
                    class_name="py-2 border-t border-gray-100",
                ),
                rx.el.div(
                    rx.el.p("Total Tax", class_name="text-sm font-bold text-gray-700"),
                    rx.el.p(
                        f"€{CalculatorState.total_tax_due_formatted}",
                        class_name="font-bold text-gray-900",
                    ),
                    class_name="flex justify-between items-center py-2 border-t border-gray-200 mt-2",
                ),
            ),
        ),
        class_name="flex flex-col gap-4",
    )


def budget_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Your Budget", class_name="text-lg font-semibold text-gray-800 mb-4"),
        rx.el.div(
            metric_card(
                "Savings Rate",
                f"{CalculatorState.savings_rate_formatted}%",
                "piggy-bank",
            ),
            card(
                rx.el.h3(
                    "Budget Summary (Monthly)",
                    class_name="text-md font-semibold text-gray-800 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Total Expenses", class_name="text-sm text-gray-600"),
                        rx.el.p(
                            f"€{CalculatorState.total_monthly_expenses_formatted}",
                            class_name="font-semibold text-gray-800",
                        ),
                        class_name="flex justify-between items-center py-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Net After Expenses",
                            class_name="text-sm font-bold text-gray-700",
                        ),
                        rx.el.p(
                            f"€{CalculatorState.estimated_net_after_expenses_formatted}",
                            class_name=rx.cond(
                                CalculatorState.estimated_net_after_expenses >= 0,
                                "font-bold text-green-600",
                                "font-bold text-red-600",
                            ),
                        ),
                        class_name="flex justify-between items-center py-2 border-t border-gray-200 mt-2",
                    ),
                ),
            ),
            class_name="grid grid-cols-1 gap-4",
        ),
        budget_chart(),
        class_name="flex flex-col gap-4",
    )


def output_display() -> rx.Component:
    return rx.el.div(results_section(), class_name="flex flex-col gap-4")


def budget_output() -> rx.Component:
    return rx.el.div(budget_section(), class_name="flex flex-col gap-4")