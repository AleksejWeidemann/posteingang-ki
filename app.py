import streamlit as st
import pandas as pd

st.title("Posteingang-KI")
st.caption("Dokumenten-Triage fuer Versicherungen - Demo")

datei = st.file_uploader("CSV mit Dokumenten hochladen", type=["csv"])

if datei is not None:
    df=pd.read_csv(datei)
    st.success(f"{len(df)} Dokumente hochgeladen.")
    st.dataframe(df)
else:
    st.info("Bitte lade eine CSV-Datei mit den Spalten 'id' und 'text' hoch.")