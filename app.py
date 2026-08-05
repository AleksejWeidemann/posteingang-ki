import streamlit as st

st.title("Posteingang-KI")
st.caption("Dokumenten-Triage fuer Versicherungen - Demo")

text = st.text_area("Dokumententext hier einfuegen:", height=200)

if st.button("Dokument analysieren"):
    st.info(f"Empfangn: {len(text)} Zeichen. (KI folgt in Sitzung 3)")