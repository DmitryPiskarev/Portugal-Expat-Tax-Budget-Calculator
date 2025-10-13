import reflex as rx
from app.states.calculator_state import CalculatorState
from app.components.input_form import input_form
from app.components.output_display import output_display


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.icon("calculator", size=32, class_name="text-violet-600"),
            rx.el.h1(
                "Portugal D8 Visa Tax & Budget Calculator",
                class_name="text-2xl font-bold text-gray-800",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.p(
            "Estimate your net income and savings as a freelancer in Portugal under the D8 visa.",
            class_name="text-gray-500 mt-2",
        ),
        class_name="text-center py-8",
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            header(),
            rx.el.div(
                input_form(),
                output_display(),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto items-start",
            ),
            class_name="container mx-auto px-4",
        ),
        class_name="font-['Lora'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="violet", radius="large"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)