KONFIDENZ_MIN = 0.7


def eskalationsgruende(kategorie, konfidenz, fehlende_angaben, datum):
    """Sammelt alle Gruende, warum ein Fall an einen Menschen geht."""
    gruende = []

    if konfidenz < KONFIDENZ_MIN:
        gruende.append("Konfidenz unter Schwelle")

    if kategorie == "Sonstiges":
        gruende.append("Kategorie Sonstiges")

    if kategorie == "Schadenmeldung" and datum == "fehlt":
        gruende.append("Datum fehlt")

    if (
        kategorie == "Kündigung"
        and "Vertragsnummer" in fehlende_angaben
        and "Name" in fehlende_angaben
    ):
        gruende.append("Kein Vertragsbezug")

    return gruende


def muss_geprueft_werden(kategorie, konfidenz, fehlende_angaben, datum):
    """True, wenn mindestens ein Eskalationsgrund vorliegt."""
    return len(eskalationsgruende(kategorie, konfidenz, fehlende_angaben, datum)) > 0


if __name__ == "__main__":
    faelle = [
        ("DOK-001", "Schadenmeldung", 0.95, "Vertragsnummer", "14.03.2026"),
        ("DOK-003", "Schadenmeldung", 0.95, "", "02.04.2026"),
        ("DOK-006", "Schadenmeldung", 0.95, "Vertragsnummer, Name, Schadennummer", "fehlt"),
        ("DOK-019", "Kündigung", 0.95, "", ""),
        ("DOK-023", "Kündigung", 0.95, "Vertragsnummer, Name", ""),
        ("DOK-027", "Vertragsanfrage", 0.65, "Datum, Schadennummer", ""),
        ("DOK-029", "Sonstiges", 0.95, "", ""),
    ]

    for kennung, kategorie, konfidenz, fehlend, datum in faelle:
        gruende = eskalationsgruende(kategorie, konfidenz, fehlend, datum)
        status = "PRUEFUNG" if gruende else "automatisch"
        print(f"{kennung}  {status:12}  {', '.join(gruende)}")