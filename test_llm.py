import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

antwort = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=300,
    messages=[{"role": "user", "content": "Antworte in genau einem Satz: Was ist eine Schadenmeldung?"}
    ],

)

print("--- Rohe Antwort ---")
print(antwort)
print()
print("--- Nur der Text ---")
print(antwort.content[0].text)
print()
print("--- Tokenverbrauch ---")
print("Eingabe:", antwort.usage.input_tokens)
print("Ausgabe:", antwort.usage.output_tokens)