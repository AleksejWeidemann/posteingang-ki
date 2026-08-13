# Referenzklassifikation (manuell)

Manuell erstellte Soll-Einordnung der 30 synthetischen Testdokumente.
Diese Datei wird **nicht** in die App geladen. Sie dient dem Abgleich der
Modellergebnisse ab Sitzung 4 und der Prüfung der Eskalationslogik in Sitzung 6.

Stand: Sitzung 2

---

## Eindeutige Fälle (25)

| ID | Kategorie | Anmerkung |
|---|---|---|
| DOK-001 | Schadenmeldung | Kfz, Parkschaden. Alle Pflichtfelder vorhanden |
| DOK-002 | Schadenmeldung | Leitungswasser. Keine Schadennummer, Datum nur vage ("gestern Abend") |
| DOK-003 | Schadenmeldung | Kfz, Unfall. Alle Pflichtfelder vorhanden, Betrag offen |
| DOK-004 | Schadenmeldung | Fahrraddiebstahl. Keine Schadennummer |
| DOK-005 | Schadenmeldung | Sturm/Dach. Keine Schadennummer, kein Betrag, Datum vage |
| DOK-006 | Schadenmeldung | Steinschlag. Kein Name, keine Nummer, kein Datum, kein Betrag |
| DOK-007 | Schadenmeldung | Hausrat, Transportschaden. Enthält zusätzlich eine Deckungsfrage |
| DOK-008 | Beschwerde | Bearbeitungsdauer, Eskalationsdrohung Ombudsmann |
| DOK-009 | Beschwerde | Verhalten Mitarbeiterin. Sehr kurz |
| DOK-010 | Beschwerde | Gutachtenhöhe, konkrete Forderung nach Neubewertung |
| DOK-011 | Beschwerde | Beitragserhöhung, umgangssprachlich |
| DOK-012 | Beschwerde | Prozess-/Postproblem |
| DOK-013 | Vertragsanfrage | Umzug, Anpassung Versicherungssumme |
| DOK-014 | Vertragsanfrage | Neuabschluss Haftpflicht |
| DOK-015 | Vertragsanfrage | Änderung Selbstbeteiligung |
| DOK-016 | Vertragsanfrage | Mitversicherung Kind |
| DOK-017 | Vertragsanfrage | Gewerbliche Nutzung, Deckungsfrage |
| DOK-018 | Vertragsanfrage | Umzug Ausland, umgangssprachlich |
| DOK-019 | Kündigung | Kfz, ordentlich, Vertragsnummer vorhanden |
| DOK-020 | Kündigung | Hausrat, sehr kurz, formal vollständig |
| DOK-021 | Kündigung | Sonderkündigungsrecht, **bedingt formuliert** (Rücknahme möglich) |
| DOK-022 | Kündigung | Fahrzeugverkauf, mit Beitragsrückforderung |
| DOK-023 | Kündigung | Ein Satz, keine Vertragsnummer, keine Sparte |
| DOK-029 | Sonstiges | Adressänderung |
| DOK-030 | Sonstiges | Kommunikationspräferenz, Werbewiderspruch |

---

## Bewusst uneindeutige Fälle (5)

Diese fünf sind die Demo für die Eskalationslogik aus Sitzung 6.
Erwartung: alle fünf landen im Topf "menschliche Prüfung".

| ID | Konflikt | Erwarteter Eskalationsgrund |
|---|---|---|
| DOK-024 | Schadenmeldung **und** Beschwerde **und** Kündigungsandrohung in einem Text | Niedrige Konfidenz |
| DOK-025 | Haftpflichtfall oder reine Deckungsanfrage? Absender fragt das selbst | Niedrige Konfidenz |
| DOK-026 | Widerspruch gegen Entscheidung: Beschwerde oder Vertragsanfrage (SF-Klasse)? | Niedrige Konfidenz |
| DOK-027 | Überlegung, keine Meldung. Umgangssprachlich, ohne jede Angabe | Konfidenz und/oder fehlende Pflichtfelder |
| DOK-028 | Reines Begleitschreiben ohne inhaltlichen Bezug | Kategorie "Sonstiges" |

---

## Grenzfälle in der eindeutigen Gruppe

Nicht als uneindeutig gezählt, aber im Abgleich beachten:

- **DOK-007** enthält neben der Schadenmeldung eine Deckungsfrage. Ein Modell kann
  hier plausibel auf "Vertragsanfrage" gehen. Sollte als Schadenmeldung eingeordnet
  werden, weil der Schaden bereits eingetreten ist.
- **DOK-021** ist eine Kündigung unter Vorbehalt. Fachlich ist sie wirksam,
  ein Modell könnte die Rücknahmeklausel überbewerten.
- **DOK-023** ist eine gültige Kündigung ohne jede Angabe zum Vertrag. Kategorie
  eindeutig, Bearbeitung nicht möglich. Guter Testfall für die Feldextraktion.

---

## Feldextraktion: Sollwerte für Schadenmeldungen

Prüfgrundlage für Sitzung 5. "fehlt" bedeutet: im Text nicht vorhanden.

| ID | Schadennummer | Name | Datum | Betrag |
|---|---|---|---|---|
| DOK-001 | KFZ-2026-44871 | Thomas Berger | 14.03.2026 | 2.340,00 EUR |
| DOK-002 | fehlt | Familie Kessler | vage ("gestern Abend") | ca. 4.800 EUR |
| DOK-003 | KFZ-2026-45102 | Marina Lorenz | 02.04.2026 | fehlt |
| DOK-004 | fehlt | S. Aydin | 20./21.04. | 3.100 EUR (Neuwert) |
| DOK-005 | fehlt | Dr. Anke Rieger | vage ("vergangenes Wochenende") | fehlt |
| DOK-006 | fehlt | fehlt | fehlt | fehlt |
| DOK-007 | fehlt | Jonas Petrovic | fehlt | 1.199 EUR (Kaufpreis, nicht Schadenhöhe) |

Hinweis: Bei DOK-004 und DOK-007 ist der genannte Betrag der Anschaffungswert,
nicht die Schadenhöhe. Ein Modell, das diese Unterscheidung nicht trifft,
liefert formal korrekte, fachlich irreführende Werte. Im Interview verwendbar.
