# **Git Dokumentation**

Hier schreibt der Git-Meister Abdulloh Khakimov.

## **Repository-Struktur**

Unser Git-Repository ist einfach und übersichtlich aufgebaut. Die Hauptbestandteile sind:

    .idea/                → Projektkonfigurationsdateien (von IDE generiert)  
    assets/               → Bilder, Musik und andere Medienressourcen  
    docs/                 → Dokumentation und Präsentationsmaterialien  
    map/                  → Kartendateien und Level-Informationen  
    Ski_Shakira_main.py   → Hauptdatei des Spiels mit der Spiel-Logik  
    requirements.txt      → Liste der benötigten Python-Bibliotheken  
Wir haben keine klassische Branch-Strategie verwendet. Stattdessen hat jede*r Teammitglied Änderungen lokal vorgenommen, indem sie eine Kopie der Datei erstellt und daran gearbeitet haben. Am Ende des Projekts wurden alle Änderungen zusammengeführt, unnötige Kopien entfernt und die finale Hauptdatei (Ski_Shakira_main.py) im Repository belassen.

## **Workflow**

Unser Team bestand aus **fünf Mitgliedern**, und **alle haben aktiv zum Repository beigetragen**.

Die Arbeit mit Git erfolgte hauptsächlich über **das Terminal mit klassischen Git-Kommandos** wie git add, git commit und git push. Es wurde direkt mit dem GitLab-Remote-Repository gearbeitet.

Alle Teammitglieder haben regelmäßig gepusht.

Die aktive Entwicklungsphase dauerte von **20. März bis 16. Mai**.

Insgesamt gab es **71 Commits**, was einem Durchschnitt von **1,2 Commits pro Tag** entspricht.

Ein Großteil der Entwicklung fand **gemeinsam vor Ort in der Bibliothek** statt. Die Aufgabenverteilung war klar strukturiert, sodass jede*r für eine bestimmte Komponente des Spiels zuständig war. Bei Überschneidungen oder gemeinsamer Arbeit an bestimmten Modulen wurde das **finale Merge-Ergebnis von der Person entschieden**, die für den entsprechenden Teil verantwortlich war. Andere Teammitglieder konnten Feedback oder Verbesserungsvorschläge geben.

## **Statistiken**
Insgesamt wurden **71 Commits** während des Projekts durchgeführt. Die Beiträge der einzelnen Teammitglieder verteilten sich wie folgt:

|**Name**| **GitLab-Handle** |**Commits** |**Verantwortungsbereich**|
|--|--|--|--|
| Abdulloh Khakimov | @akhakiym | 9 | Git-Meister; Level Designer |
| Elizaveta Chichkanov | @chiliza | 14 | Game Designer |
| Koustav Agrawal | @koustavagr2005 | 21 | Lead Developer |
| Juanita Giraldo | @juanisg | 2 | Grafik Designer |
| Aanjneya Moudgil| @aanjneya | 3 | Test und Fehlermanagement |

Obwohl jede*r eine bestimmte Rolle hatte, wurde im Team viel **interdisziplinär zusammengearbeitet**. In verschiedenen Phasen des Projekts unterstützten sich die Mitglieder gegenseitig mit ihrem Wissen, z. B. beim Beheben von Fehlern oder beim Feintuning des Leveldesigns.

## Best Practices

Während der Entwicklung unseres Projekts haben wir versucht, möglichst viele **Git Best Practices** umzusetzen:

-   **Aussagekräftige Commit-Nachrichten**: Wir haben darauf geachtet, klare und verständliche Beschreibungen zu schreiben, die die Änderungen gut zusammenfassen.
    
-   **Sinnvolle Commit-Frequenz**: Statt nach jeder Kleinigkeit zu committen, haben wir versucht, abgeschlossene Arbeitsblöcke zu committen.
    
-   **Verwendung von .gitignore**: Die virtuelle Umgebung (venv/) wurde bewusst ignoriert, um das Repository sauber zu halten. Stattdessen haben wir eine requirements.txt-Datei gepflegt.
    
-   **Regelmäßige Commits und Teamarbeit**: Alle Teammitglieder haben regelmäßig gepusht und gut zusammengearbeitet.
    
-   **Sehr wenige Konflikte**: Durch klare Aufgabenteilung und gute Kommunikation gab es kaum Merge-Konflikte.
  

### **Was wir beim nächsten Projekt verbessern würden:**

-   **Verwendung einer Branch-Strategie**: Das Arbeiten mit Feature-Branches hätte die Zusammenarbeit strukturierter gemacht und wäre skalierbarer für größere Projekte.
    
-   **Automatisierte Tests und Linting**: Einfache Unit-Tests oder Code-Checks hätten uns geholfen, Fehler frühzeitig zu erkennen.
    
-   **Bessere Dokumentation während des Prozesses**: Eine laufende Dokumentation hätte uns bei der Präsentation und Nachverfolgung geholfen.
