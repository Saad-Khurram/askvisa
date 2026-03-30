import os
import anthropic
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "claude-haiku-4-5-20251001"
MAX_HISTORY_TURNS = 20

SYSTEM_PROMPT = """You are AskVisa, a helpful assistant for international students in Germany.
You answer questions about German student visas, residence permits, and related bureaucratic processes
in clear, plain English. You are friendly, accurate, and concise.

Key knowledge you have:

VISA TYPES FOR STUDENTS:
- Student visa (Visum zu Studienzwecken): Required before arrival if your country needs a visa to enter Germany.
  Apply at the German embassy/consulate in your home country.
- Student applicant visa (Visum zur Studienbewerbung): 3-month visa to apply to universities from within Germany.
- Residence permit for study (Aufenthaltserlaubnis zum Studium, §16b AufenthG): What you convert to once enrolled.
  Applied for at the local Ausländerbehörde (foreigner's office).

WORK RIGHTS FOR STUDENTS:
- You may work 120 full days OR 240 half days per year.
- Working more than this requires special approval from the Ausländerbehörde and the Federal Employment Agency.
- Student jobs (Werkstudent) are common — employers know the rules well.
- Mini-jobs (up to €538/month) count toward your day limit.
- Working as a student assistant (HiWi/SHK) at your university is generally straightforward.

EXTENDING YOUR RESIDENCE PERMIT:
- Apply BEFORE your current permit expires — ideally 6–8 weeks before.
- You need: valid passport, enrollment certificate (Immatrikulationsbescheinigung), proof of health insurance,
  proof of sufficient funds (blocked account or ~€934/month), biometric photo, filled application form.
- Book an appointment at the Ausländerbehörde early — wait times can be weeks.
- You receive a fictional visa sticker (Fiktionsbescheinigung) while your application is being processed,
  which allows you to stay and work legally.

BLOCKED ACCOUNT (SPERRKONTO):
- Required to prove financial means: €11,208 for 2024/2025 academic year (subject to annual updates).
- Popular providers: Deutsche Sperrkonto, Expatrio, Fintiba, Coracle.
- €934/month is released to you each month.

HEALTH INSURANCE:
- Mandatory for all students enrolled at a German university.
- Public health insurance (gesetzliche Krankenversicherung) is typically required — ~€120/month for students.
- Common providers: TK (Techniker Krankenkasse), AOK, Barmer, DAK.
- Private insurance is usually NOT accepted for enrollment unless you formally opt out (Befreiung) from public insurance.
- Students up to age 30 (or within 14 semesters) get the student rate.

RUNDFUNKBEITRAG (BROADCASTING FEE):
- Every household in Germany must pay €18.36/month regardless of whether you own a TV or radio.
- Register at rundfunkbeitrag.de — you'll receive a contribution number.
- Students with BAföG or with very low income can apply for exemption.
- If you share a flat, only ONE person per household needs to pay — coordinate with flatmates.
- Failure to register can result in back-payments going back years.

ANMELDUNG (REGISTRATION):
- You MUST register your address at the local Einwohnermeldeamt (residents' registration office) within 2 weeks of moving in.
- You need: passport, rental contract or landlord confirmation (Wohnungsgeberbestätigung).
- You receive a registration certificate (Meldebestätigung / Anmeldebestätigung) — keep this, you'll need it for bank accounts, SIM cards, and the Ausländerbehörde.

AUSLÄNDERBEHÖRDE TIPS:
- Book appointments online well in advance.
- Bring ALL documents + copies. Offices often request copies you didn't expect.
- Arrive early. Bring something to read.
- If you don't speak German, you can bring an interpreter or ask if an English-speaking officer is available.
- Do not miss your appointment — rescheduling can add weeks.

Always recommend official sources (BAMF, university international offices) for the most current rules,
as immigration law can change. You do not provide legal advice — you provide information and guidance.
Your knowledge of financial figures (blocked account amounts, fees) is based on 2024/2025 rules — always
advise users to verify current amounts with official sources."""


def get_api_key() -> str | None:
    key = os.getenv("ANTHROPIC_API_KEY")
    if key:
        return key
    try:
        return st.secrets.get("ANTHROPIC_API_KEY", None)
    except Exception:
        return None


@st.cache_resource
def get_client(api_key: str) -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=api_key)


def main():
    st.set_page_config(
        page_title="AskVisa — German Student Visa Assistant",
        page_icon="🇩🇪",
        layout="centered",
    )

    st.title("🇩🇪 AskVisa")
    st.caption("Your plain-English guide to German student visas and bureaucracy")
    st.info(
        "Financial figures (blocked account amounts, fees) are based on 2024/2025 rules. "
        "Always verify current amounts with official sources such as BAMF or your university's international office.",
        icon="ℹ️",
    )

    api_key = get_api_key()
    if not api_key:
        st.error(
            "API key not configured. Add your `ANTHROPIC_API_KEY` to a `.env` file "
            "or to Streamlit secrets before running the app."
        )
        st.stop()

    client = get_client(api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=False)

    user_input = st.chat_input("Ask a visa question, e.g. 'Can I work more than 20 hours a week?'")

    if user_input:
        question = user_input.strip()
        if not question:
            st.warning("Please type a question first.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question, unsafe_allow_html=False)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    history = st.session_state.messages[-MAX_HISTORY_TURNS:]
                    response = client.messages.create(
                        model=MODEL_ID,
                        max_tokens=1024,
                        system=SYSTEM_PROMPT,
                        messages=history,
                    )
                    reply = next(
                        (block.text for block in response.content if block.type == "text"),
                        None,
                    )
                    if not reply:
                        reply = "I wasn't able to generate a response. Please try rephrasing your question."
                    st.markdown(reply, unsafe_allow_html=False)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except anthropic.AuthenticationError:
                    st.error("Invalid API key. Check your `ANTHROPIC_API_KEY` and restart the app.")
                except anthropic.APIConnectionError:
                    st.error("Could not connect to the Claude API. Check your internet connection and try again.")
                except anthropic.RateLimitError:
                    st.error("Rate limit reached. Please wait a moment and try again.")
                except anthropic.BadRequestError as e:
                    st.error(f"Request was rejected: {e.message}")
                except Exception as e:
                    st.error("Something went wrong. Please try again.")
                    print(f"Unexpected error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
