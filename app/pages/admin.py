import reflex as rx
from app.states.admin_state import AdminState
from app.states.auth_state import AuthState
from app.components.ui import card


def user_management_card() -> rx.Component:
    return card(
        rx.el.h2(
            "User Management", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "ID",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Email",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Role",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Actions",
                        class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AdminState.users,
                    lambda user: rx.el.tr(
                        rx.el.td(
                            user["id"],
                            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900",
                        ),
                        rx.el.td(
                            user["email"],
                            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                        ),
                        rx.el.td(
                            rx.cond(user["is_admin"], "Admin", "User"),
                            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                        ),
                        rx.el.td(
                            rx.el.button(
                                rx.icon("trash-2", size=16),
                                on_click=lambda: AdminState.delete_user(user["id"]),
                                disabled=user["is_admin"],
                                class_name="text-red-600 hover:text-red-800 disabled:text-gray-300",
                            ),
                            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
                        ),
                    ),
                ),
                class_name="bg-white divide-y divide-gray-200",
            ),
            class_name="min-w-full divide-y divide-gray-200",
        ),
    )


def tax_bracket_management_card() -> rx.Component:
    def bracket_editor() -> rx.Component:
        return rx.el.div(
            rx.el.h3("Edit Tax Bracket", class_name="text-md font-semibold"),
            rx.el.div(
                rx.el.label("Limit (€)"),
                rx.el.input(
                    default_value=AdminState.editing_bracket["limit"].to_string(),
                    on_change=lambda val: AdminState.handle_edit_bracket_change(
                        "limit", val
                    ),
                    class_name="w-full mt-1.5 flex h-10 rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.label("Rate (%)"),
                rx.el.input(
                    default_value=(
                        AdminState.editing_bracket["rate"] * 100
                    ).to_string(),
                    on_change=lambda val: AdminState.handle_edit_bracket_change(
                        "rate", val
                    ),
                    class_name="w-full mt-1.5 flex h-10 rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.button(
                    "Save",
                    on_click=AdminState.save_bracket,
                    class_name="px-4 py-2 text-sm font-medium text-white bg-violet-600 rounded-lg hover:bg-violet-700",
                ),
                rx.el.button(
                    "Cancel",
                    on_click=AdminState.cancel_edit_bracket,
                    class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300",
                ),
                class_name="flex gap-2 mt-4",
            ),
            class_name="p-4 bg-gray-50 rounded-lg mt-4 flex flex-col gap-4",
        )

    return card(
        rx.el.h2(
            "Tax Bracket Management",
            class_name="text-lg font-semibold text-gray-800 mb-4",
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Limit (€)",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Rate",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Actions",
                        class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AdminState.tax_brackets,
                    lambda bracket, index: rx.el.tr(
                        rx.el.td(
                            rx.cond(
                                bracket["limit"] == float("inf"),
                                "Above",
                                f"{bracket['limit']:.2f}",
                            ),
                            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900",
                        ),
                        rx.el.td(
                            f"{bracket['rate'] * 100:.2f}%",
                            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                        ),
                        rx.el.td(
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("copy", size=16),
                                    on_click=lambda: AdminState.start_edit_bracket(
                                        index
                                    ),
                                    class_name="text-blue-600 hover:text-blue-800",
                                ),
                                rx.el.button(
                                    rx.icon("trash-2", size=16),
                                    on_click=lambda: AdminState.remove_bracket(index),
                                    class_name="text-red-600 hover:text-red-800 ml-4",
                                ),
                                class_name="flex justify-end",
                            ),
                            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
                        ),
                    ),
                ),
                class_name="bg-white divide-y divide-gray-200",
            ),
            class_name="min-w-full divide-y divide-gray-200",
        ),
        rx.el.button(
            "Add New Bracket",
            on_click=AdminState.add_new_bracket,
            class_name="mt-4 px-4 py-2 text-sm font-medium text-white bg-violet-600 rounded-lg hover:bg-violet-700",
        ),
        rx.cond(AdminState.is_editing_bracket, bracket_editor(), rx.el.div()),
    )


def admin_page() -> rx.Component:
    from app.app import app_header, footer

    return rx.el.div(
        app_header(),
        rx.cond(
            AuthState.is_admin,
            rx.el.main(
                rx.el.h1(
                    "Admin Panel", class_name="text-3xl font-bold text-gray-800 mb-6"
                ),
                rx.el.div(
                    user_management_card(),
                    tax_bracket_management_card(),
                    class_name="flex flex-col gap-8",
                ),
                class_name="container mx-auto px-4 py-8",
            ),
            rx.el.main(
                rx.el.div(
                    rx.spinner(class_name="text-violet-500"),
                    class_name="flex justify-center items-center h-64",
                ),
                class_name="container mx-auto px-4 py-8",
            ),
        ),
        footer(),
        class_name="font-['Lora'] bg-gray-50 min-h-screen flex flex-col",
    )