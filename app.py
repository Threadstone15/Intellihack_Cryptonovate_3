from dotenv import load_dotenv
load_dotenv()  # Optional, for Streamlit app configuration

import streamlit as st
import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"  # Replace with your Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class LoanSupportChatbot:
    def __init__(self):
        self.loans = {
            "Overdraft Facilities": {
                "description": "An overdraft is a way to manage cash flow with interest. It's linked to your current account and lets you use extra funds up to your limit. You can manage limits through online banking.",
                "features": [
                    "Quick and easy to arrange",
                    "Cash available when needed",
                    "Pay interest only on what you use",
                    "Sole proprietors can apply or adjust limits"
                ]
            },
            "Housing Loans": {
                "description": "We offer various housing loan schemes. Please select a scheme for more information.",
                "schemes": {
                    "Housing Loan Scheme": {
                        "description": "Provides financing for buying land, constructing a house, renovating, or purchasing a house/condominium.",
                        "quantum_of_loan": "Maximum of Rs. 50 Million",
                        "repayment_period": "Up to 25 years",
                        "eligibility": "Sri Lankan Citizen above 18, resident, not a defaulter, various professions",
                        "security_collateral": "Mortgage over the property",
                        "conditions_apply": "Contact the nearest branch or call centre for more information.",
                        "contact_info": "Please contact the relevant branch for more information."
                    },
                    "Housing Loan for University Staff": {
                        "description": "Offers a special loan for university staff with a minimum of 5 years of service.",
                        "quantum_of_loan": "Academic/Non-Academic Staff Grade: Rs. 2.0 Million, Non-Staff Grade: Rs. 1.0 Million",
                        "conditions_apply": "Smart Bank holds the authority to change or revise any condition."
                    },
                    "Housing Loan Scheme for Permanent Cadre Employees": {
                        "description": "Designed for Sri Lanka's permanent cadre salaried employees.",
                        "repayment_period": "Maximum 25 years",
                        "security_collateral": "Primary mortgage over the property to be developed",
                        "conditions_apply": "Smart Bank holds the authority to change or revise any condition."
                    }
                }
            },
            # Add other loan types here...
        }


def get_gemini_response(question, chat):
    response = chat.send_message(question, stream=True)
    return response, chat


def main():
    """Streamlit Application"""

    st.set_page_config(page_title="Q&A and Loan Support Demo")

    st.header("Smart Bank Assistant")

    chatbot = LoanSupportChatbot()

    # Initialize session state for chat history and chat object if they don't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'chat' not in st.session_state:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        st.session_state["chat"] = chat

    user_input = st.text_input("Input: ", key="input")
    submit_button = st.button("Ask the question")

    if submit_button and user_input:
        # Get the chat object from session state
        chat = st.session_state['chat']

        # Get the response and updated chat object
        gemini_response, chat = get_gemini_response(user_input, chat)

        # Update the chat object in session state
        st.session_state['chat'] = chat

        # Process Gemini response
        st.subheader("The Response is")
        for chunk in gemini_response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot (Gemini)", chunk.text))

        # Check if user query asks about loans
        if any(loan_type in user_input.lower() for loan_type in chatbot.loans.keys()):
            for loan_type, loan_info in chatbot.loans.items():
                if loan_type in user_input.lower():
                    st.subheader(f"{loan_type.title()} Information:")
                    st.write(loan_info["description"])
                    if "features" in loan_info:
                        st.subheader("Features:")
                        for feature in loan_info["features"]:
                            st.write(f"- {feature}")
                    if "schemes" in loan_info:
                        st.subheader("Available Schemes:")
                        for scheme, scheme_info in loan_info["schemes"].items():
                            st.write(f"- {scheme}: {scheme_info['description']}")
                            if "quantum_of_loan" in scheme_info:
                                st.write(f"Quantum of Loan: {scheme_info['quantum_of_loan']}")
                            if "repayment_period" in scheme_info:
                                st.write(f"Repayment Period: {scheme_info['repayment_period']}")
                            if "eligibility" in scheme_info:
                                st.write(f"Eligibility: {scheme_info['eligibility']}")
                            if "security_collateral" in scheme_info:
                                st.write(f"Security/Collateral: {scheme_info['security_collateral']}")
                            if "conditions_apply" in scheme_info:
                                st.write(f"Conditions Apply: {scheme_info['conditions_apply']}")
                    break
        else:
            st.write("Please specify a loan type to get information.")


if __name__ == "__main__":
    main()