# 🎿 Ski Shakira

Willkommen bei **Ski Shakira** – einem aufregenden 2D-Platformer-Spiel, das als Teamprojekt im Studienkolleg entwickelt wurde. In diesem Spiel steuerst du eine Skifahrerin durch verschneite Levels voller Herausforderungen, Licht- und Schatteneffekte und sammelst dabei möglichst viele Punkte durch akrobatische Stunts.

---

## 🕹️ Spielbeschreibung

**Ski Shakira** ist ein Level-basiertes Platformer-Game mit zwei unterschiedlichen Karten:

* **Level 1:** Einführung in Steuerung und Gameplay. Leichte Hindernisse und gute Sichtbarkeit.
* **Level 2:** Dunkleres Level mit eingeschränkter Sicht und anspruchsvolleren Hindernissen.

Ziel des Spiels ist es, Hindernisse zu überwinden, Münzen zu sammeln und das Ziel möglichst schnell und unbeschadet zu erreichen.

---

## 🎮 Steuerung

* **Pfeiltasten links/rechts:** Bewegung
* **Pfeiltasten oben/unten:** Salto
* **Leertaste:** Springen
* **R:** Level neu starten
* **N:** Zum nächsten Level wechseln

---

## ⚠️ Bekannte Einschränkungen

* Terrain-Physik ist in Level 2 teilweise eingeschränkt, da Arcade keine perfekte Bodenrotation bei hügeligen Flächen unterstützt.
* Es gibt keine Pausenfunktion.

---

## 🖼️ Screenshot

![Screenshot Level 1](assets/screenshot.png)

---

## 🛠️ Installation

### Voraussetzungen

* Python **3.10+**
* Arcade **3.1+**
* Pymunk

### Schritte

1. Repository herunterladen:

```bash
git clone https://git.tu-berlin.de/mittagspuase/platformer.git
cd platformer
```

2. Virtuelle Umgebung einrichten (optional aber empfohlen):

```bash
python -m venv venv
source venv/bin/activate  # für macOS/Linux
venv\Scripts\activate  # für Windows
```

3. Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

4. Spiel starten:

```bash
python Ski_Shakira_main.py
```

---

## 📘 Projektübersicht

* Entwickelt im Rahmen des Softwareprojekts am Studienkolleg Berlin
* Aufgabenstellung: Umsetzung eines Platformer Games mit Python und der Arcade-Bibliothek

---

## 👥 Team

* **Abdulloh Khakimov (@akhakiym)** – Git, Level Design
* **Elizaveta Chichkanov (@chiliza)** – Game Design
* **Koustav Agrawal (@koustavagr2005)** – Hauptprogrammierung
* **Aanjneya Moudgil (@aanjneya)** – Testmanagement
* **Juanita Giraldo Foronda (@juanisg)** – Grafikdesign

> Obwohl jede\:r eine bestimmte Rolle hatte, unterstützte das Team sich gegenseitig bei der Entwicklung aller Bestandteile.


## 📄 Weitere Informationen zum Projekt
- Unser [Game Design](docs/game-design.md) mit Story, Konzept, Mechaniken, Spielfigur.
- [Level Design](docs/level-design.md): Tilesets, Karten, Gestaltung
- [Programmierung](docs/implementation.md): Alles zum Python Sourcecode
- Und [so verwenden wir git](docs/git.md)!
- [Dokumentation des Projektmanagements](docs/project-management.md).
- [Test und Fehlerbehebung](docs/test.md)
- Übersicht über die verwendeten [KI-Tools](docs/ai.md)
- Tabellarische Übersicht über [externe Quellen](docs/references.md)

