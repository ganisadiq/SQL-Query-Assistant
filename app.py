import streamlit as st
from src.agent import SQLQueryAssistant

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="SQL Query Assistant",
    page_icon="💻",
    layout="centered"
)

# ---------------- Session State ----------------
if "assistant" not in st.session_state:
    st.session_state.assistant = SQLQueryAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Custom CSS ----------------
st.markdown("""
<style>

/* Light grey background */
.stApp {
    background-color: #f5f5f5;
}

/* Center page */
.main > div {
    max-width: 800px;
    margin: auto;
}

/* Center title */
h1 {
    text-align: center;
}

div[data-testid="stCaptionContainer"] {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.title("💻 SQL Query Assistant")
st.caption("Ask me to generate an SQL query...")

st.divider()

# ---------------- Chat History ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- Chat Input ----------------
if prompt := st.chat_input("Describe the SQL query you need..."):

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response (only once)
    response = st.session_state.assistant.get_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )