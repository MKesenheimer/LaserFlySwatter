# LFS - Laser Fly Swatter (Physik, Informatik)

# Einleitung
Mit dem Klimawandel und den wärmeren Temperaturen in Europa haben vermehrt Insekten Einzug, die hier vorher nicht heimisch waren und die im schlimmsten Fall gefährliche Tropenkrankheiten verbreiten können.
Deshalb wird es immer wichtiger effiziente Maßnahmen gegen Stechmücken zu entwickeln.
Da chemische Fallen Risiken für andere Tiere bergen, soll ein Gerät entwickelt werden, das Stechmücken ohne Risiken für andere Tiere und Menschen beseitigen kann.

Mit dem Projekt “Laser Fly Swatter” (LFS) soll ein “Proof-of-Concept” Modell einer laserbasierten Fliegenklatsche erstellt werden.
Mit dem LFS wollen wir Stechmücken über eine Kamera erkennen (Computer Vision) und mit einem gezielten Schuss aus einem Laser beseitigen.

Da der Umgang mit Hochleistungslasern gefährlich ist, führen wir unsere Experimente zuerst in einer Simulation und danach mit einer geeigneten Show-Laseranlage durch.
Die Leistung des Lasers lässt sich dabei problemlos auf ungefährliche Laserleistungen drosseln.
Da wir außerdem aus ethischen Gründen keine Versuche an echten Insekten durchführen können, wird für die Stechmücke ebenfalls ein Modell herangezogen.

## Voraussetzungen
* python
* openCV

## Installation
Installation nötiger Software:
```
pip install --user -r requirements.txt
```

Download des Projekts:
```
git clone https://github.com/MKesenheimer/LaserFlySwatter.git
git submodule update --init
```

Bauen der Bibliothek um die Showlaseranlage ansprechen zu können:
```
cd lumax
./make.sh <macOS|linux|windows>
```

## Benutzung
Ausführen der verschiedenen Programme, zum Beispiel:
```
python cv_tracking_test.py
```
