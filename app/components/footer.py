import reflex as rx
import datetime


def footer_link(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name="text-sm text-gray-500 hover:text-gray-700 transition-colors",
    )


def footer_section(title: str, *links) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-sm font-semibold text-gray-800 mb-4"),
        rx.el.div(*links, class_name="flex flex-col gap-3"),
        class_name="flex flex-col",
    )


def footer() -> rx.Component:
    current_year = datetime.datetime.now().year
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("calculator", size=24, class_name="text-violet-600"),
                        rx.el.p(
                            "Portugal D8 Tax Calculator",
                            class_name="font-semibold text-gray-800",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.p(
                        "An intuitive tool to estimate your taxes and budget in Portugal.",
                        class_name="text-sm text-gray-500 mt-2",
                    ),
                ),
                rx.el.div(
                    footer_section(
                        "Navigation",
                        footer_link("Calculator", "/"),
                        footer_link("Tax Brackets", "/tax-brackets"),
                        footer_link("Tax Info", "/tax-info"),
                    ),
                    footer_section(
                        "Legal",
                        footer_link("Disclaimer", "#"),
                        footer_link("Privacy Policy", "#"),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 gap-8",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-12",
            ),
            rx.el.div(class_name="border-t border-gray-200 mt-12 pt-8"),
            rx.el.div(
                rx.el.p(
                    f"© {current_year} Portugal D8 Tax Calculator. Built by ",
                    rx.el.a(
                        "Dmitry Piskarev",
                        href="https://www.linkedin.com/in/dmitry-piskarev/",
                        target="_blank",
                        class_name="text-blue-600 hover:underline",
                    ),
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center gap-2 py-4",
            ),
            class_name="container mx-auto px-6 lg:px-8",
        ),
        class_name="py-12 bg-white border-t border-gray-200 mt-auto",
    )
