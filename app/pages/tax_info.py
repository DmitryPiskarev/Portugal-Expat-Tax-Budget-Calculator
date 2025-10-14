import reflex as rx
from app.components.ui import card


def tax_info_page() -> rx.Component:
    from app.app import app_header, footer

    def info_section(title: str, *content) -> rx.Component:
        return card(
            rx.el.h2(title, class_name="text-xl font-semibold text-gray-800 mb-4"),
            rx.el.div(*content, class_name="prose prose-sm max-w-none text-gray-600"),
            class_name="mb-6",
        )

    return rx.el.div(
        app_header(),
        rx.el.main(
            rx.el.h1(
                "Portuguese Tax Information for Freelancers",
                class_name="text-3xl font-bold text-gray-800 mb-6",
            ),
            info_section(
                "Taxable Income Calculation (Simplified Regime)",
                rx.el.p(
                    "Under the simplified regime for freelancers (recibos verdes), your taxable income is not your full gross income. Instead, a coefficient is applied. For most services, this coefficient is 0.75."
                ),
                rx.el.p(
                    "The formula to determine the taxable base for IRS (income tax) is:"
                ),
                rx.el.div(
                    rx.el.code(
                        "Taxable Income = (Gross Annual Income * 0.75) - Social Security Contributions"
                    ),
                    class_name="p-2 bg-gray-100 rounded-md my-2",
                ),
                rx.el.p(
                    "Note: This calculator uses the standard calculation where Social Security is based on 70% of your income from the previous reporting period. The formula used here is a common estimation: (G * 0.75) - (G * 0.7 * SS_Rate)."
                ),
            ),
            info_section(
                "Social Security (Segurança Social)",
                rx.el.p(
                    "As a freelancer in Portugal, you are generally required to make social security contributions. The standard rate for self-employed individuals is 21.4%."
                ),
                rx.el.p(
                    "Contributions are calculated based on your 'relevant income,' which is typically 70% of the gross income from the previous quarter. This calculator uses a simplified estimation based on your current monthly income to project your annual liability."
                ),
                rx.el.ul(
                    rx.el.li(
                        rx.text.strong("First-Year Exemption: "),
                        "New freelancers are exempt from social security payments for the first 12 months of their activity.",
                    ),
                    rx.el.li(
                        rx.text.strong("Contribution Base: "),
                        "The contribution is not on your full gross income but on a determined percentage (usually 70%).",
                    ),
                    rx.el.li(
                        rx.text.strong("Default Rate: "),
                        "This calculator defaults to the standard 21.4% rate, which you can adjust in the 'Advanced Options' on the main calculator page.",
                    ),
                    class_name="list-disc list-inside space-y-2 mt-2",
                ),
            ),
            info_section(
                "IRS (Personal Income Tax)",
                rx.el.p(
                    "This is a progressive tax applied to your taxable income. The rates are divided into brackets. As your income increases, the portion of income in higher brackets is taxed at a higher rate."
                ),
                rx.el.p(
                    "The 'Tax Brackets' tab in this app shows the progressive rates for the current year."
                ),
            ),
            info_section(
                "Important Note on Tax Regimes",
                rx.el.p(
                    "This calculator is specifically designed for freelancers under the ",
                    rx.text.strong("simplified tax regime"),
                    ". Portugal has other tax regimes, such as organized accounting (contabilidade organizada), which may be mandatory or beneficial depending on your income level and business complexity.",
                ),
                rx.el.p(
                    "The simplified regime is generally available for freelancers with an annual gross income below €200,000. Above this threshold, organized accounting is usually required."
                ),
            ),
            info_section(
                "Disclaimer",
                rx.el.p(
                    "This calculator provides an estimation for informational purposes only. It is not financial advice. Tax laws can change and individual circumstances vary. Always consult with a qualified accountant or tax advisor in Portugal for accurate financial planning."
                ),
            ),
            class_name="container mx-auto px-4 py-8",
        ),
        footer(),
        class_name="font-['Lora'] bg-gray-50 min-h-screen flex flex-col",
    )