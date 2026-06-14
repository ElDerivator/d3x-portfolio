#!/usr/bin/env python3
"""Fase 4 parte 3: párrafos multilínea. Inserta data-en en el <p>
que CONTIENE cada substring único (robusto para texto multilínea)."""
import pathlib
f = pathlib.Path("index.html")
html = f.read_text(encoding="utf-8")

# (substring_único_dentro_del_<p>, traducción_en)
T = [
    ("Base academica orientada a procesos",
     "Academic grounding in processes, resource coordination, business structure, service, costs and operational improvement."),
    ("Perspectiva util para soporte tecnico",
     "A useful lens for technical support, customer experience, teamwork, problem analysis and stakeholder communication."),
    ("Curse ambas areas y he orientado",
     "I studied both fields and channeled that base into operations, data, support and automation. The administrative graduation step remains pending due to social service, while my professional growth has continued through hands-on experience, technical certifications and applied projects."),
    ("Como emprendedor y operations manager",
     "As an entrepreneur and operations manager, Delitruck gave me direct practice in logistics, inventory, pricing, promotions, customer service, suppliers, event setup and execution under pressure. That experience grounds how I work: understand the whole process, spot friction and turn it into clearer systems."),
]

done, missing = 0, []
for sub, en in T:
    idx = html.find(sub)
    if idx == -1:
        missing.append(sub[:40]); continue
    p_open = html.rfind("<p", 0, idx)
    gt = html.find(">", p_open)
    if p_open == -1 or gt == -1 or "data-en=" in html[p_open:gt]:
        missing.append(sub[:40]); continue
    attr = ' data-en="' + en + '"'
    html = html[:gt] + attr + html[gt:]
    done += 1

f.write_text(html, encoding="utf-8")
print(f"Aplicados: {done}/{len(T)}")
for m in missing:
    print("  NO:", m)
