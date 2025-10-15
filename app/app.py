import reflex as rx
from app.states.auth_state import AuthState
from app.components.input_form import income_input, expenses_input
from app.components.output_display import output_display, budget_output
from app.pages.sign_in import sign_in
from app.pages.sign_up import sign_up
from app.pages.tax_brackets import tax_brackets_page
from app.pages.tax_info import tax_info_page
from app.pages.admin import admin_page
from app.components.footer import footer
from app.states.admin_state import AdminState


def navigation_item(text: str, href: str) -> rx.Component:
    is_active = (AuthState.router.page.path == href) | (href == "/") & (
        AuthState.router.page.path == ""
    )
    return rx.el.a(
        text,
        href=href,
        class_name=rx.cond(
            is_active,
            "px-3 py-2 rounded-md bg-violet-100 text-violet-700 font-medium text-sm",
            "px-3 py-2 rounded-md text-gray-500 hover:bg-gray-100 hover:text-gray-700 font-medium text-sm",
        ),
    )


def app_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("calculator", size=32, class_name="text-violet-600"),
                        rx.el.h1(
                            "Portugal D8 Visa Tax & Budget Calculator",
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    href="/",
                ),
                rx.el.nav(
                    navigation_item("Calculator", "/"),
                    navigation_item("Tax Brackets", "/tax-brackets"),
                    navigation_item("Tax Info", "/tax-info"),
                    rx.cond(
                        AuthState.is_admin,
                        navigation_item("Admin", "/admin"),
                        rx.el.div(),
                    ),
                    class_name="flex items-center gap-2",
                ),
            ),
            rx.cond(
                AuthState.is_logged_in,
                rx.el.button(
                    "Logout",
                    on_click=AuthState.sign_out,
                    class_name="px-4 py-2 text-sm font-medium text-white bg-violet-600 rounded-lg hover:bg-violet-700",
                ),
                rx.el.a(
                    "Login",
                    href="/sign-in",
                    class_name="px-4 py-2 text-sm font-medium text-violet-700 bg-violet-100 rounded-lg hover:bg-violet-200",
                ),
            ),
            class_name="container mx-auto px-4 flex justify-between items-center",
        ),
        class_name="py-4 border-b border-gray-200 bg-white/80 backdrop-blur-md sticky top-0 z-10",
    )


def index() -> rx.Component:
    return rx.el.div(
        app_header(),
        rx.el.main(
            rx.el.div(
                rx.el.p(
                    "Estimate your net income and savings as a freelancer in Portugal under the D8 visa.",
                    class_name="text-gray-500 mt-2 text-center",
                ),
                class_name="py-8",
            ),
            rx.el.div(
                rx.el.div(
                    income_input(),
                    output_display(),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start",
                ),
                rx.el.div(class_name="py-4 lg:py-6"),
                rx.divider(margin_bottom="1em"),
                rx.el.div(
                    expenses_input(),
                    budget_output(),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start",
                ),
                class_name="flex flex-col max-w-6xl mx-auto",
            ),
            class_name="container mx-auto px-4",
        ),
        footer(),
        class_name="font-['Lora'] bg-gray-50 min-h-screen flex flex-col",
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
app.add_page(index, on_load=AuthState.check_session, route="/")
app.add_page(sign_in, route="/sign-in")
app.add_page(sign_up, route="/sign-up")
app.add_page(tax_brackets_page, route="/tax-brackets", on_load=AuthState.check_session)
app.add_page(tax_info_page, route="/tax-info", on_load=AuthState.check_session)
app.add_page(
    admin_page,
    route="/admin",
    on_load=[AuthState.check_admin, AdminState.on_load_admin],
)
