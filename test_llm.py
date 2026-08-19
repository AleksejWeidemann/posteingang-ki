import os
from typing import Literal
from anthropic import Anthropic
from pydantic import BaseModel, Field

# Modellname steht zentral. Ein Wechsel kostet nur eine Zeile.
MODELL = "claude-haiku-4-5-20251001"

# Der Schluessel kommt aus der Umgebung, nie aus dem Code.
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# Das Antwortschema. Das Modell muss genau in dieser Form antworten.
class DokumentAnalyse(BaseModel):
    # Literal laesst nur diese fuenf Werte zu.
    kategorie: Literal[
        "Schadenmeldung", "Beschwerde", "Vertragsanfrage", "Kündigung", "Sonstiges"
    ]
    dringlichkeit: Literal["hoch", "mittel", "niedrig"]
    # description wird ans Modell uebertragen und wirkt wie eine Anweisung.
    konfidenz: float = Field(description="Sicherheit der Einordnung, zwischen 0 und 1")
    begruendung: str = Field(description="Ein Satz zur Begruendung der Kategorie")
    fehlende_angaben: list[str] = Field(
        description="Nur Angaben, die im Text fehlen und ohne die eine Bearbeitung unmoeglich ist. Zulaessige Werte: Schadennummer, Name, Datum, Betrag, Vertragsnummer. Keine Anlagen wie Fotos oder Belege. Leere Liste, wenn nichts Wesentliches fehlt."
    )

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

# Testfall ist DOK-027, einer der bewusst uneindeutigen Faelle.
BEISPIEL = "Sehr geehrte Damen und Herren, hiermit melde ich einen Schaden an meinem Fahrzeug. Am 14.03.2026 gegen 17:30 Uhr wurde mein PKW auf dem Parkplatz des Einkaufszentrums Nordpassage im Bereich der Fahrertuer beschaedigt. Der Verursacher hat einen Zettel hinterlassen. Meine Schadennummer aus dem telefonischen Erstkontakt lautet KFZ-2026-44871. Der Kostenvoranschlag der Werkstatt belaeuft sich auf 2.340,00 EUR. Mit freundlichen Gruessen, Thomas Berger"

# parse schickt das Schema mit und validiert die Antwort.
antwort = client.messages.parse(
    model=MODELL,
    max_tokens=500,
    system=SYSTEM_PROMPT,
    messages=[
        {"role": "user", "content": f"Analysiere dieses Versicherungsdokument.\n\n{BEISPIEL}"}
    ],
    output_format=DokumentAnalyse,
)

# Fertiges Objekt. Es muss kein Text mehr zerlegt werden.
ergebnis = antwort.parsed_output

print("--- Objekt ---")
print(ergebnis)
print()
print("--- Einzelne Felder ---")
print("Kategorie:", ergebnis.kategorie)
print("Konfidenz:", ergebnis.konfidenz, "| Typ:", type(ergebnis.konfidenz))
print("Fehlende Angaben:", ergebnis.fehlende_angaben)
print()
# Bei max_tokens oder refusal passt die Antwort moeglicherweise nicht zum Schema.
print("stop_reason:", antwort.stop_reason)
print("Tokens:", antwort.usage.input_tokens, "rein,", antwort.usage.output_tokens, "raus")