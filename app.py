import os

import streamlit as st

from answerer import answer
from checklist import build_checklist
from retriever import retrieve

st.set_page_config(page_title="BUFS Admissions Assistant", page_icon="🎓")
st.title("🎓 BUFS Admissions Assistant")
st.caption(
    "Ask in any language. Answers are grounded in official BUFS admissions documents."
)

if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "OPENAI_API_KEY is not configured. Add it to .env locally or Streamlit "
        "Secrets when deploying."
    )
    st.stop()

chat_tab, checklist_tab = st.tabs(["Ask a question", "My document checklist"])

with chat_tab:
    question = st.text_input("Your question (any language)")
    if st.button("Ask", type="primary") and question.strip():
        try:
            with st.spinner("Searching official documents..."):
                result = answer(question, retrieve(question))
            st.write(result["text"])
            if result["citations"]:
                st.caption(
                    "Retrieved sources: "
                    + ", ".join(
                        f"{item['source']} p.{item['page']}"
                        for item in result["citations"]
                    )
                )
        except Exception as exc:
            st.error(f"Could not answer the question: {exc}")

with checklist_tab:
    level = st.selectbox("Program level", ["undergraduate", "graduate"])
    program = st.text_input("Program / major", "Korean Language")
    applicant_type = st.selectbox("Applicant type", ["new", "transfer"])
    language = st.text_input("Answer language", "English")
    if st.button("Build my checklist"):
        try:
            with st.spinner("Building your checklist..."):
                result = build_checklist(
                    level, program, applicant_type, language
                )
            st.write(result["text"])
            if result["citations"]:
                st.caption(
                    "Retrieved sources: "
                    + ", ".join(
                        f"{item['source']} p.{item['page']}"
                        for item in result["citations"]
                    )
                )
        except Exception as exc:
            st.error(f"Could not build the checklist: {exc}")
