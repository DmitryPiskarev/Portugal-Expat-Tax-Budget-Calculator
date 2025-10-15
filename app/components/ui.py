import reflex as rx


def card(*children, **props) -> rx.Component:
    base_class = "bg-white border border-gray-200 rounded-xl p-6 shadow-sm"
    if "class_name" in props:
        props["class_name"] = f"{base_class} {props['class_name']}"
    else:
        props["class_name"] = base_class
    return rx.el.div(*children, **props)


def metric_card(title: str, value: rx.Var | str, icon: str, **props) -> rx.Component:
    return card(
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.icon(icon, class_name="text-gray-400", size=20),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(value, class_name="text-2xl font-semibold text-gray-800 mt-1"),
        **props,
    )


def input_field(label: str, icon: str, **props) -> rx.Component:
    # Extract custom class_name if provided
    input_class = props.pop(
        "class_name",
        "flex h-10 w-full rounded-lg border border-gray-300 bg-transparent "
        "pl-9 pr-6 py-2 text-sm transition-colors focus-visible:outline-none "
        "focus-visible:ring-2 focus-visible:ring-violet-500 text-gray-800",
    )

    return rx.el.div(
        rx.el.label(
            label,
            class_name="text-sm font-medium text-gray-700 mb-1.5 block",
        ),
        rx.el.div(
            # Left-side icon (calculator, home, etc.)
            rx.el.span(
                rx.icon(icon, size=18, class_name="text-gray-400"),
                class_name="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none",
            ),
            # Right-side euro sign, placed *inside* input without spacing gap
            rx.el.span(
                "€",
                class_name=(
                    "absolute inset-y-0 right-2 flex items-center "
                    "text-gray-500 text-sm font-medium pointer-events-none"
                ),
            ),
            # Input field
            rx.el.input(
                class_name=input_class,
                style={"paddingRight": "1.75rem"},  # 👈 ensures tight alignment
                **props,
            ),
            class_name="relative",
        ),
        class_name="w-full",
    )
