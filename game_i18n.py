#!/usr/bin/env python3
"""Minijuego: marca textos FIJOS con data-en. Los dinámicos
(timer, score, signal, feedback) los maneja script.js → no se tocan."""
import pathlib
f = pathlib.Path("index.html")
html = f.read_text(encoding="utf-8")
n = 0
R = [
    ('<strong id="game-title">D3X Carrera de Senales</strong>',
     '<strong id="game-title" data-en="D3X Signal Run">D3X Carrera de Senales</strong>'),
    ('<em>Jugar</em>', '<em data-en="Play">Jugar</em>'),
    ('<h2>D3X Carrera de Senales</h2>', '<h2 data-en="D3X Signal Run">D3X Carrera de Senales</h2>'),
    ('<span>D3X Carrera de Senales</span>', '<span data-en="D3X Signal Run">D3X Carrera de Senales</span>'),
    ('<span>Claridad</span>', '<span data-en="Clarity">Claridad</span>'),
    ('<span>Friccion</span>', '<span data-en="Friction">Friccion</span>'),
    ('<span>Racha</span>', '<span data-en="Streak">Racha</span>'),
    ('<button type="button" data-decision="automate">Automatizar</button>',
     '<button type="button" data-decision="automate" data-en="Automate">Automatizar</button>'),
    ('<button type="button" data-decision="validate">Validar</button>',
     '<button type="button" data-decision="validate" data-en="Validate">Validar</button>'),
    ('<button type="button" data-decision="escalate">Escalar</button>',
     '<button type="button" data-decision="escalate" data-en="Escalate">Escalar</button>'),
]
for old, new in R:
    if old in html:
        html = html.replace(old, new); n += 1

# descripción multilínea por substring
sub = "Clasifica senales operativas"
en = "Classify operational signals before they become manual work. Each correct decision increases clarity; each mistake adds friction to the system."
idx = html.find(sub)
if idx != -1:
    p_open = html.rfind("<p", 0, idx)
    gt = html.find(">", p_open)
    if p_open != -1 and gt != -1 and "data-en=" not in html[p_open:gt]:
        html = html[:gt] + ' data-en="' + en + '"' + html[gt:]; n += 1

f.write_text(html, encoding="utf-8")
print("Minijuego cambios:", n)
