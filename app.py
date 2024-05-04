def get_gemini_response(question):
    if "gemini" not in st.session_state:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        st.session_state["gemini"] = chat
    else:
        chat = st.session_state["gemini"]
    response = chat.send_message(question, stream=True)
    return response


def main():
    """Streamlit Application"""

    st.set_page_config(page_title="Q&A and Loan Support Demo")

    st.header("Smart Bank Assistant")

    chatbot = LoanSupportChatbot()

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_input = st.text_input("Input: ", key="input")
    submit_button = st.button("Ask the question")

    if submit_button and user_input:
        gemini_response = get_gemini_response(user_input)

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
            st.write("Please specify a loan type to get information.")