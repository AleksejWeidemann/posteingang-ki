import time

import pandas as pd
import streamlit as st
from anthropic import Anthropic
from pydantic import BaseModel, Field
from typing import Literal

MODELL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """Du ordnest eingehende Versicherungsdokumente einer Kategorie zu.

Kategorien:
Schadenmeldung: Ein Schaden ist eingetreten und wird gemeldet.
Beschwerde: Unzufriedenheit mit Bearbeitung, Personal, Beitrag oder Entscheidung.
Vertragsanfrage: Frage zu Konditionen, Deckung, Aenderung oder Neuabschluss.
Kündigung: Ausdruecklicher Wunsch, einen Vertrag zu beenden.
Sonstiges: Alles andere, etwa Adressaenderungen oder reine Begleitschreiben.

Die Konfidenz bewertet die Eindeutigkeit des Dokuments, nicht deine Formulierungssicherheit.
Vergib unter 0.7, wenn eines zutrifft:
Der Text passt auf mehrere Kategorien.
Der Absender ist selbst unsicher, was er will.
Der Text ist zu knapp oder zu vage fuer eine sichere Zuordnung.
Es ist kein Anliegen erkennbar."""

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


class DokumentAnalyse(BaseModel):
    kategorie: Literal[
        "Schadenmeldung", "Beschwerde", "Vertragsanfrage", "Kündigung", "Sonstiges"
    ]
    dringlichkeit: Literal["hoch", "mittel", "niedrig"]
    konfidenz: float = Field(description="Sicherheit der Einordnung, zwischen 0 und 1")
    begruendung: str = Field(description="Ein Satz zur Begruendung der Kategorie")
    fehlende_angaben: list[str] = Field(
        description="Nur Angaben, die im Text fehlen und ohne die eine Bearbeitung unmoeglich ist. Zulaessige Werte: Schadennummer, Name, Datum, Betrag, Vertragsnummer. Keine Anlagen wie Fotos oder Belege. Leere Liste, wenn nichts Wesentliches fehlt."
    )


def analysiere(text):
    """Schickt einen Dokumententext ans Modell und gibt Analyse und Tokenverbrauch zurueck."""
    antwort = client.messages.parse(
        model=MODELL,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Analysiere dieses Versicherungsdokument.\n\n{text}"}
        ],
        output_format=DokumentAnalyse,
    )
    return antwort.parsed_output, antwort.usage


st.title("Posteingang-KI")
st.caption("Dokumenten-Triage fuer Versicherungen - Demo")

datei = st.file_uploader("CSV mit Dokumenten hochladen", type="csv")

if datei is not None:
    df = pd.read_csv(datei)
    st.success(f"{len(df)} Dokumente hochgeladen.")

    if st.button("Alle Dokumente analysieren"):
        zeilen = []
        tokens_rein = 0
        tokens_raus = 0
        fortschritt = st.progress(0, text="Analyse laeuft...")

        for i, zeile in df.iterrows():
            try:
                ergebnis, verbrauch = analysiere(zeile["text"])
                zeilen.append(
                    {
                        "id": zeile["id"],
                        "kategorie": ergebnis.kategorie,
                        "dringlichkeit": ergebnis.dringlichkeit,
                        "konfidenz": ergebnis.konfidenz,
                        "fehlende_angaben": ", ".join(ergebnis.fehlende_angaben),
                        "begruendung": ergebnis.begruendung,
                    }
                )
                tokens_rein += verbrauch.input_tokens
                tokens_raus += verbrauch.output_tokens
            except Exception as fehler:
                zeilen.append(
                    {
                        "id": zeile["id"],
                        "kategorie": "FEHLER",
                        "dringlichkeit": "",
                        "konfidenz": 0.0,
                        "fehlende_angaben": "",
                        "begruendung": str(fehler),
                    }
                )

            fortschritt.progress(
                (i + 1) / len(df), text=f"Analysiert: {i + 1} von {len(df)}"
            )
            time.sleep(0.3)

        fortschritt.empty()
        st.session_state["ergebnisse"] = pd.DataFrame(zeilen)
        st.session_state["tokens"] = (tokens_rein, tokens_raus)

    if "ergebnisse" in st.session_state:
        st.dataframe(st.session_state["ergebnisse"])
        rein, raus = st.session_state["tokens"]
        kosten = rein / 1_000_000 * 1.0 + raus / 1_000_000 * 5.0
        st.caption(
            f"Tokenverbrauch gesamt: {rein} rein, {raus} raus | geschaetzte Kosten: {kosten:.4f} USD"
        )
else:
    st.info("Bitte lade eine CSV-Datei mit den Spalten 'id' und 'text' hoch.")