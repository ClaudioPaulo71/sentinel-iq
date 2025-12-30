import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Sentinel IQ - Contracts Assistant", page_icon="🛡️")

st.title("🛡️ Sentinel IQ")
st.subheader("Intelligent Analysis of Contractual Documents")

# Barra lateral para ações
with st.sidebar:
    st.header("Commands")
    if st.button("🔄 Index New Documents"):
        with st.spinner("Reading PDFs..."):
            response = requests.post("http://localhost:8000/ingest")
            if response.status_code == 200:
                st.success("Brain updated!")
            else:
                st.error("Error indexing.")

# Área de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Ask something about the contracts..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing clauses..."):
            try:
                response = requests.post(
                    "http://localhost:8000/ask",
                    json={"text": prompt}
                )
                answer = response.json().get("answer", "No response.")
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Connection error: {e}")