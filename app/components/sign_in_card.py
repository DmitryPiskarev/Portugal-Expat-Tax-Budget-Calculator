import reflex as rx
from app.states.auth_state import AuthState


def sign_in_card():
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Sign in to your account",
                class_name="font-semibold tracking-tight text-xl",
            ),
            rx.el.p(
                "Enter your email below to sign in to your account",
                class_name="text-sm text-gray-500 font-medium",
            ),
            class_name="flex flex-col text-center",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label("Email", class_name="text-sm font-medium leading-none"),
                rx.el.input(
                    type="email",
                    placeholder="user@example.com",
                    id="email",
                    required=True,
                    class_name="flex h-10 w-full rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.div(
                rx.el.label("Password", class_name="text-sm font-medium leading-none"),
                rx.el.input(
                    type="password",
                    id="password",
                    required=True,
                    class_name="flex h-10 w-full rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.button(
                "Sign in",
                class_name="w-full h-10 px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 font-medium",
            ),
            rx.el.div(
                rx.el.span(
                    "Don't have an account?",
                    class_name="text-sm text-gray-500 font-medium",
                ),
                rx.el.a(
                    "Sign up",
                    href="/sign-up",
                    class_name="text-sm text-violet-600 font-medium underline hover:text-violet-700 transition-colors",
                ),
                class_name="flex flex-row gap-2 justify-center",
            ),
            class_name="flex flex-col gap-4",
            on_submit=AuthState.sign_in,
        ),
        class_name="p-8 rounded-xl bg-white flex flex-col gap-6 shadow-lg border border-gray-200 text-gray-800 w-full max-w-md",
    )