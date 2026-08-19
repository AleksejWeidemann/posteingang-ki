import os
from typing import Optional
from anthropic import Anthropic
from pydantic import BaseModel, Field

MODELL = "claude-haiku-4-5-20251001"

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

EXTRAKTION_PROMPT = """Du extrahierst Kerndaten aus Schadenmeldungen von Versicherungen.

Uebernimm nur Angaben, die woertlich im Text stehen. Rate nicht und leite nichts ab.
Fehlt eine Angabe, lass das Feld leer.

betrag ist die Hoehe des Schadens oder der Reparaturkosten.
Der Kaufpreis oder Neuwert eines Gegenstandes ist NICHT der Schadenbetrag.
datum ist der Zeitpunkt des Schadeneintritts, nicht das Datum des Schreibens.
Unbestimmte Zeitangaben wie gestern oder letztes Wochenende sind kein Datum."""


class Schadendaten(BaseModel):
    schadennummer: Optional[str] = Field(description="Aktenzeichen der Schadenmeldung")
    name: Optional[str] = Field(description="Name der meldenden Person")
    datum: Optional[str] = Field(description="Datum des Schadeneintritts")
    betrag: Optional[str] = Field(description="Schadenhoehe oder Reparaturkosten")


BEISPIEL = "Sehr geehrte Damen und Herren, hiermit melde ich einen Schaden an meinem Fahrzeug. Am 14.03.2026 gegen 17:30 Uhr wurde mein PKW auf dem Parkplatz des Einkaufszentrums Nordpassage im Bereich der Fahrertuer beschaedigt. Der Verursacher hat einen Zettel hinterlassen. Meine Schadennummer aus dem telefonischen Erstkontakt lautet KFZ-2026-44871. Der Kostenvoranschlag der Werkstatt belaeuft sich auf 2.340,00 EUR. Mit freundlichen Gruessen, Thomas Berger"


antwort = client.messages.parse(
    model=MODELL,
    max_tokens=400,
    system=EXTRAKTION_PROMPT,
    messages=[{"role": "user", "content": f"Extrahiere die Kerndaten.\n\n{BEISPIEL}"}],
    output_format=Schadendaten,
)

daten = antwort.parsed_output

for feld, wert in daten.model_dump().items():
    print(f"{feld}: {wert if wert else 'fehlt'}")

print()
print("stop_reason:", antwort.stop_reason)