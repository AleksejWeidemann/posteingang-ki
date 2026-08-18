import streamlit as st
import pandas as pd
from anthropic import Anthropic

MODELL = "claude-haiku-4-5-20251001"

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

st.title("Posteingang-KI")
st.caption("Dokumenten-Triage fuer Versicherungen - Demo")

datei = st.file_uploader("CSV mit Dokumenten hochladen", type="csv")

if datei is not None:
    df = pd.read_csv(datei)
    st.success(f"{len(df)} Dokumente hochgeladen.")
    st.dataframe(df)

    gewaehlte_id = st.selectbox("Dokument auswaehlen:", df["id"])
    dokument = df[df["id"] == gewaehlte_id]["text"].values[0]

    st.text_area("Ausgewaehlter Text:", dokument, height=150, disabled=True)

    if st.button("Dokument analysieren"):
        with st.spinner("Modell arbeitet..."):
            try:
                antwort = client.messages.create(
                    model=MODELL,
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": f"Worum geht es in diesem Versicherungsdokument? Antworte in zwei Saetzen.\n\n{dokument}"}
                    ],
                )
                st.write(antwort.content[0].text)
                st.caption(f"Tokens: {antwort.usage.input_tokens} rein, {antwort.usage.output_tokens} raus | stop_reason: {antwort.stop_reason}")
            except Exception as fehler:
                st.error(f"Der Modellaufruf ist fehlgeschlagen: {fehler}")
else:
    st.info("Bitte lade eine CSV-Datei mit den Spalten 'id' und 'text' hoch.")