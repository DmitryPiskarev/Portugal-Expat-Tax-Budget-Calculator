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

    def external_link(url: str, text: str) -> rx.Component:
        return rx.el.a(
            rx.el.div(
                rx.icon("external-link", size=14, class_name="text-violet-600"),
                rx.el.span(text),
                class_name="flex items-center gap-1 text-violet-600 hover:underline font-medium",
            ),
            href=url,
            target="_blank",
            rel="noopener noreferrer",
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
            # ✅ New section: official visa portals and guidance
            info_section(
                "Visa Registration & Application Portals",
                rx.el.p(
                    "To start your D-type (Digital Nomad) visa application, use the official Portuguese Ministry of Foreign Affairs platforms below. These are the legitimate systems where you register, upload documents, and book your consular appointments."
                ),
                rx.el.ul(
                    rx.el.li(
                        rx.text.strong("E-Visa Portal: "),
                        "Create your account (‘Registo Único’), confirm your token, log in, and choose the National (D) visa type. ",
                        external_link(
                            "https://pedidodevistos.mne.gov.pt/",
                            "pedidodevistos.mne.gov.pt",
                        ),
                        rx.el.p(
                            "After logging in, select your Consulate (e.g., Moscow / Russian Federation) and upload the required documents for your Digital Nomad visa.",
                            class_name="mt-1 text-gray-500",
                        ),
                    ),
                    rx.el.li(
                        rx.text.strong("Consular Appointments System: "),
                        "If your Consulate requires an in-person appointment for document drop-off, use the scheduling portal: ",
                        external_link(
                            "https://agendamentos.mne.gov.pt/en/register",
                            "agendamentos.mne.gov.pt",
                        ),
                        rx.el.p(
                            "Register with your basic info (name, email, phone), then book or confirm your appointment slot.",
                            class_name="mt-1 text-gray-500",
                        ),
                    ),
                    rx.el.li(
                        rx.text.strong("General Visa Guidance: "),
                        "Official Ministry page describing procedures and required documents: ",
                        external_link(
                            "https://vistos.mne.gov.pt/",
                            "vistos.mne.gov.pt",
                        ),
                    ),
                    class_name="list-disc list-inside space-y-3 mt-3",
                ),
                rx.el.div(
                    rx.el.p(
                        "If you see a message like “this visa type is not available for your consular post,” slots might be temporarily closed. Try again later or email the Consular Section in Moscow at ",
                        rx.el.a(
                            "sconsular.moscovo@mne.pt",
                            href="mailto:sconsular.moscovo@mne.pt",
                            class_name="text-violet-600 hover:underline",
                        ),
                        " for guidance.",
                    ),
                    class_name="bg-violet-50 border border-violet-200 rounded-lg p-3 mt-3 text-sm text-gray-700",
                ),
                rx.el.p(
                    "Before you register, make sure you have: passport scans, proof of remote income, health insurance, CV/cover letter, and passport photo files in the required format.",
                    class_name="mt-3 text-gray-600 italic",
                ),
            ),
                        info_section(
                "Applicants Outside Russia (US / UK / Other Countries)",
                rx.el.p(
                    "If you’re applying from another country (for example the US or UK), the same visa type applies but the submission method and required documents vary slightly by region."
                ),
                rx.el.ul(
                    rx.el.li(
                        rx.text.strong("United States: "),
                        "Applications are made through the ",
                        rx.el.a(
                            "VFS Global Portugal centres",
                            href="https://www.vfsglobal.com/one-pager/portugal/usa/english/",
                            target="_blank",
                            class_name="text-blue-600 hover:underline",
                        ),
                        ". All D-type visa applications must be submitted in person."
                    ),
                    rx.el.li(
                        rx.text.strong("United Kingdom: "),
                        "Apply via your local Portuguese Consulate. Working remotely for a non-Portuguese company is allowed under the D8 regime, but always check your regional Consulate’s website for availability.",
                    ),
                    rx.el.li(
                        rx.text.strong("Other Countries: "),
                        "The same E-Visa portal is used. Contact your nearest Portuguese Embassy or Consulate if the D-type visa option doesn’t appear for your jurisdiction.",
                    ),
                    class_name="list-disc list-inside space-y-2 mt-2",
                ),
                rx.el.p(
                    "Before applying, ensure you have: passport scan, proof of income, health insurance, criminal record certificate (with apostille if applicable), and accommodation proof. Processing time can take 4–8 weeks or longer depending on your consular post."
                ),
                rx.el.p(
                    "Helpful sources: ",
                    rx.el.a(
                        "gov.uk (for UK applicants)",
                        href="https://www.gov.uk/guidance/travel-to-portugal-for-work",
                        target="_blank",
                        class_name="text-blue-600 hover:underline",
                    ),
                    ", ",
                    rx.el.a(
                        "Wise D8 Visa Guide",
                        href="https://wise.com/us/blog/portugal-d8-visa",
                        target="_blank",
                        class_name="text-blue-600 hover:underline",
                    ),
                    ", ",
                    rx.el.a(
                        "OysterHR D8 Overview",
                        href="https://www.oysterhr.com/library/portugal-digital-nomad-visa",
                        target="_blank",
                        class_name="text-blue-600 hover:underline",
                    ),
                    ".",
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
