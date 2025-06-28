# KI-Agent lernt Super Mario Bros zu spielen

Von Niklas, Leevi, Kenan und Malik

## Libraries installieren
Unsere verwendeten Libraries sind in `requirements.txt`  
Mithilfe von pip können diese einfach installiert werden. Wir empfehlen, ein virtual environment (venv) für die Libraries zu benutzen.
```bash
$ python -m venv venv
```
Dann kann alles installiert werden:
```bash
$ pip install -r requirements.txt
```

## Ausführen
Training:
```bash
python main.py
```
Visualisierung:
```bash
python visualize_map.py
python visualize_metrics.py
```

## State/Action Space

Der Action Space sind die Inputs, die eigentlich der Spieler auf dem Controller drückt. 
```python
RIGHT_ONLY = [
    ['NOOP'],            # Nichts tun
    ['right'],           # Nach rechts gehen
    ['right', 'A'],      # Nach rechts gehen und springen
    ['right', 'B'],      # Nach rechts gehen und sprinten
    ['right', 'A', 'B']] # Nach rechts sprinten und springe]
```

Wir haben den State Space an die x/y Position von Mario gebunden. Dazu haben wir eine Art Raster benutzt, um die Anzahl von Zuständen so klein wie möglich zu halten.



## Exploration Strategie
Mit der klassischen $\epsilon$-greedy Strategie mit globaler linearer Abnahme haben wir leider nur mittelmäßige Ergebnisse erziehlt. Das lag vor allem daran, dass der Agent in bereits bekannten Bereichen unnötigt exploriert hat. Deswegen haben wir uns etwas neues einfallen lassen: Der Epsilon Wert ist nun abhängig davon wie bekannt dem Agent der aktuelle Bereich ist. Er grenzt also in bereits bekannten Bereichen an 0, und ist höher in unbekannten Bereichen.

$\epsilon_n = max(min(0.005 * x - 0.005*(x_{last \varnothing}-35), 0.3), 0.001)$
