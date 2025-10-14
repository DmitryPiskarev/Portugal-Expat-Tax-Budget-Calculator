import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "© 2024 Portugal D8 Tax Calculator. All rights reserved.",
                    class_name="text-sm text-gray-500",
                ),
                rx.el.div(
                    rx.el.a(
                        "Home",
                        href="/",
                        class_name="text-sm text-gray-500 hover:text-gray-700",
                    ),
                    rx.el.a(
                        "Tax Brackets",
                        href="/tax-brackets",
                        class_name="text-sm text-gray-500 hover:text-gray-700",
                    ),
                    rx.el.a(
                        "Tax Info",
                        href="/tax-info",
                        class_name="text-sm text-gray-500 hover:text-gray-700",
                    ),
                    class_name="flex items-center gap-4",
                ),
            ),
            class_name="container mx-auto px-4 flex justify-between items-center",
        ),
        class_name="py-6 border-t border-gray-200 bg-gray-50 mt-12",
    )