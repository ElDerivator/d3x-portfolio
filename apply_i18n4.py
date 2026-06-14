#!/usr/bin/env python3
"""Fase 4 cierre: sección de contacto/cotización (al final). Marca
los textos solo-texto (headings, tags, botón). Los <label> con input
dentro se dejan en ES (el form está al final, baja prioridad)."""
import pathlib
f = pathlib.Path("index.html")
html = f.read_text(encoding="utf-8")

# Reemplazos exactos (solo-texto)
R = [
    ('<p class="eyebrow">Diagnostico D3X</p>',
     '<p class="eyebrow" data-en="D3X Diagnostic">Diagnostico D3X</p>'),
    ('<h2 id="diagnostic-title">Cuentame donde se atora tu operacion.</h2>',
     '<h2 id="diagnostic-title" data-en="Tell me where your operation gets stuck.">Cuentame donde se atora tu operacion.</h2>'),
    ('<span>Procesos manuales</span>', '<span data-en="Manual processes">Procesos manuales</span>'),
    ('<span>Reportes</span>', '<span data-en="Reporting">Reportes</span>'),
    ('<span>Datos dispersos</span>', '<span data-en="Scattered data">Datos dispersos</span>'),
    ('<span>Automatizacion</span>', '<span data-en="Automation">Automatizacion</span>'),
    ('<p>Solicita un diagnostico inicial.</p>',
     '<p data-en="Request an initial diagnostic.">Solicita un diagnostico inicial.</p>'),
    ('<button type="submit">Solicitar diagnostico</button>',
     '<button type="submit" data-en="Request a diagnostic">Solicitar diagnostico</button>'),
    # Contacto (closing)
    ('<h2 id="contact-title" data-en="Let&#39;s talk with context.">Hablemos con contexto.</h2>',
     '<h2 id="contact-title" data-en="Let&#39;s talk with context.">Hablemos con contexto.</h2>'),  # ya marcado, no-op seguro
    ('<span>Respuesta humana</span>', '<span data-en="Human response">Respuesta humana</span>'),
    ('<span>Diagnostico primero</span>', '<span data-en="Diagnostic first">Diagnostico primero</span>'),
    ('<span>Sin acciones automaticas</span>', '<span data-en="No automatic actions">Sin acciones automaticas</span>'),
    ('<a href="#diagnostico">Ir al diagnostico</a>',
     '<a href="#diagnostico" data-en="Go to the diagnostic">Ir al diagnostico</a>'),
]
done, missing = 0, []
for old, new in R:
    if old in html:
        if old != new:
            html = html.replace(old, new); done += 1
    else:
        missing.append(old[:45])

# Párrafos multilínea por substring
T = [
    ("El formulario va primero",
     "This form lives at the end of the page. If you have manual reports, scattered data or repeated processes, here we can spot whether it's worth automating, tidying or measuring."),
    ("El formulario de diagnostico es la mejor entrada",
     "If you'd rather write directly, use these channels and share the problem, current tools and urgency."),
]
for sub, en in T:
    idx = html.find(sub)
    if idx == -1:
        missing.append(sub[:40]); continue
    p_open = html.rfind("<p", 0, idx)
    gt = html.find(">", p_open)
    if p_open == -1 or gt == -1 or "data-en=" in html[p_open:gt]:
        missing.append(sub[:40]); continue
    html = html[:gt] + ' data-en="' + en + '"' + html[gt:]
    done += 1

f.write_text(html, encoding="utf-8")
print(f"Aplicados: {done}")
for m in missing:
    print("  NO:", m)
