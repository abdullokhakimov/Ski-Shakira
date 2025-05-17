# KI-Einsatz im Spieleprojekt

In diesem Dokument wird der Einsatz von KI-Tools in unserem Projekt dokumentiert. Wir beschreiben, welche Tools für welche Aufgaben verwendet wurden, geben Beispiele für Prompts und bewerten den Nutzen kritisch.

## Verwendete KI-Tools

Hier sind die KI-Tools, die wir im Projekt eingesetzt haben:

  - Claude für die Code-Strukturierung und komplexere Funktionen
  - Grok für spezifische Implementierungsdetails und Debugging-Hilfe
  - Gemini für konzeptionelle Ideen und Logikansätze

## Beispiel-Prompts

Hier dokumentieren wir einige repräsentative Beispiele für den Einsatz von KI-Chatbots in unserem Projekt:

* **Erstellung von der Spielfigur:**
    * **Prompt:** 
    >Make a photo of Shakira from Waka Waka as a sprite for an arcade game in which the sprite would ski over a terrain as pixel art. It should be a general image and NOT a dance pose. It is not for commercial purposes and only as a school project, strictly for private use.
    * **Ergebnis:** 
    
    ![Screenshot Sprite](assets/screenshot_shakira.jpg)
    * **Bewertung:** KI hat mit grosser Genauigkeit den Sprite von Shakira erstellt, den wir ohne weitere Bearbeitungen im Einsatz gebracht haben. Fuer uns war es genau, was wir wollten. Also 10/10.



    **Weitere Beispiele befinden sich [hier](docs/implementation.md).**
## Kritische Bewertung des KI-Einsatzes

| Vorteile                                                    | Nachteile/Einschränkungen                                                                                                                                                                                             |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| * Schnelle Fehlerbehebung                                  | * **Versionsproblematik (Arcade):** |
| * Ideenfindung                                              |     * KI-Modelle oft auf ältere Versionen (z.B. Arcade 2.6) trainiert.                                                                                                                                                 |
| * Vereinfachte Code-Integration (Arcade, Pymunk)             |     * Inkompatibilitäten und Fehler bei Code für neuere Versionen (z.B. Arcade 3.2.0).                                                                                                                             |
| * Clevere Problemlösungen                                   |     * Notwendigkeit von Anpassungen und Korrekturen.                                                                                                                                                                   |
| * Beschleunigte Datenanalyse (falls relevant)               | * **Längen- und Prompt-Beschränkungen:** |
| * Lerneffekt (Git & Projektmanagement)                      |     * Begrenzte Eingabelänge für komplexe Anfragen.                                                                                                                                                                     |
|                                                             |     * Abhängigkeit der Antwortqualität von Prompt-Präzision.                                                                                                                                                           |
|                                                             |     * Erforderlichkeit iterativer Kommunikation und Aufteilung komplexer Anfragen.                                                                                                                                    |
|                                                             |                                                                                                                                                                                                                       |

## Abschließende Einschätzung

* **Was haben wir über den Einsatz von KI-Tools gelernt?**
    * KI ist primär eine *Ergänzung*, kein vollständiger Ersatz für menschliche Expertise.
    * Die Qualität der KI-Unterstützung hängt stark von der Formulierung präziser Fragen und der Bereitstellung relevanter Daten ab.

* **Für welche Anwendungsfälle sind KI-Tools besonders geeignet?**
    * **Lösungsvorschläge für bekannte Probleme:** Schnelle Identifizierung und Behebung von Standardfehlern.
    * **Inspiration und neue Ideen:** Generierung unkonventioneller Ansätze und Perspektiven.
    * **Fehleranalyse und Lösungsvorschläge:** Unterstützung bei der Diagnose und Behebung von Programmfehlern.
    * **Reduzierung von Routineaufgaben:** Automatisierung zeitaufwändiger und repetitiver "Grunt Work".
    * **Wissenserwerb:** Vermittlung neuer Konzepte und Ideen in den Bereichen Programmierung und Spieleentwicklung.
    * **Unterstützung bei der Integration verschiedener Bibliotheken:** Erleichterung der Zusammenarbeit von Arcade, Pymunk und anderen Modulen.

* **Für welche Anwendungsfälle sind sie nicht oder nur eingeschränkt geeignet?**
    * **Echte Kreativität und originäre Ideenentwicklung:** KI kann inspirieren, ersetzt aber nicht die menschliche Vorstellungskraft und das Schaffen eigener Konzepte.
    * **Entwicklung tiefgreifender, eigener Designentscheidungen:** KI liefert Vorschläge, die grundlegenden kreativen Entscheidungen sollten jedoch vom Team getroffen werden.
    * **Umgang mit sehr neuen oder stark veränderten Bibliotheksversionen:** Die Wissensbasis der KI hinkt aktuellen Entwicklungen oft hinterher.
    * **Komplexe, versionsspezifische Implementierungen ohne klare Beispiele:** KI tut sich schwer, wenn spezifische Codebeispiele für die neueste Version fehlen.

* **Fazit:**
    * Ohne KI wäre die Realisierung des Projekts mit unserem begrenzten Vorwissen in Programmierung, Spieleentwicklung, Git und Tiled Maps deutlich schwieriger gewesen.
    * Der Einsatz von KI hat die Entwicklung nicht nur erleichtert, sondern auch effizienter und schneller gestaltet.
    * Trotz bedeutender Herausforderungen wie der mangelnden Unterstützung neuester Bibliotheksversionen konnte die KI durch die Bereitstellung von Beispielcode und Lösungsansätzen dazulernen und uns unterstützen.
    * Die Auseinandersetzung mit KI hat maßgeblich zum Wissensaufbau in verschiedenen Bereichen beigetragen und uns geholfen, unsere Projektmanagement-Fähigkeiten zu verbessern.