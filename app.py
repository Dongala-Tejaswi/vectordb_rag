import streamlit as st
from query import query_db

st.set_page_config(page_title="Vector DB Assistant")

st.title("AI Knowledge Assistant")

query = st.text_input("Ask your question:")

if query:
    answer, docs = query_db(query)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Source Documents")
    for d in docs:
        st.write(d.page_content[:300] + "...")
