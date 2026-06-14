#!/usr/bin/env python3
"""Formulario 100% bilingüe. Labels: envuelve el texto en <span data-en>
(regex tolerante a indentación). Options/spans: data-en directo."""
import re, pathlib
f = pathlib.Path("index.html")
html = f.read_text(encoding="utf-8")
n = 0

# --- Labels: (texto_es, en, ancla_campo) ---
labels = [
    ("Nombre", "Name", '<input name="name"'),
    ("Empresa o proyecto", "Company or project", '<input name="company"'),
    ("Email", "Email", '<input name="email"'),
    ("Telefono", "Phone", '<input name="phone"'),
    ("Tipo de negocio", "Business type", '<select name="business_type"'),
    ("Urgencia", "Urgency", '<select name="urgency"'),
    ("Problema de proceso", "Process problem", "<textarea name=\"process_problem\""),
    ("Herramientas actuales", "Current tools", '<input name="current_tools"'),
    ("Rango de presupuesto", "Budget range", '<select name="budget_range"'),
]
for es, en, anchor in labels:
    pat = re.compile(r'(\n(\s*))' + re.escape(es) + r'(\n\s*' + re.escape(anchor) + r')')
    new, k = pat.subn(r'\1<span data-en="' + en + r'">' + es + r'</span>\3', html)
    if k:
        html = new; n += k

# --- Options: (texto_es, en) ---
options = [
    ("Seleccionar", "Select"), ("Negocio local", "Local business"),
    ("Servicios profesionales", "Professional services"), ("Equipo operativo", "Operations team"),
    ("Ecommerce", "E-commerce"), ("Startup", "Startup"),
    ("Equipo empresarial", "Enterprise team"), ("Individual", "Individual"), ("Otro", "Other"),
    ("No estoy seguro", "Not sure"), ("Baja", "Low"), ("Media", "Medium"),
    ("Alta", "High"), ("Urgente", "Urgent"),
    ("No definido", "Not defined"), ("Menos de 500 USD", "Under 500 USD"),
    ("500 a 1,500 USD", "500 to 1,500 USD"), ("1,500 a 5,000 USD", "1,500 to 5,000 USD"),
    ("5,000 a 15,000 USD", "5,000 to 15,000 USD"), ("15,000+ USD", "15,000+ USD"),
]
for es, en in options:
    old = ">" + es + "</option>"
    new = ' data-en="' + en + '">' + es + "</option>"
    if old in html:
        html = html.replace(old, new); n += 1

# --- Spans / textos sueltos ---
singles = [
    ('<span>Acepto que D3X use estos datos para responder mi solicitud.</span>',
     '<span data-en="I agree that D3X may use this data to respond to my request.">Acepto que D3X use estos datos para responder mi solicitud.</span>'),
    ('              Website\n',  # honeypot label text (oculto) — lo dejamos
     '              Website\n'),
]
for old, new in singles:
    if old in html and old != new:
        html = html.replace(old, new); n += 1

# --- placeholder Herramientas (no se traduce textContent, es atributo) skip ---

# --- status y note (multilínea, por substring) ---
multil = [
    ("Formulario preparado. Por ahora puedes escribir",
     "Form ready. For now you can write to administracion@d3x.biz."),
    ("Tus datos se usan unicamente para responder",
     "Your data is used only to respond to your diagnostic or quote request. D3X takes no external actions without human review."),
]
for sub, en in multil:
    idx = html.find(sub)
    if idx == -1: continue
    open_tag = html.rfind("<", 0, idx)
    # buscar el inicio del tag contenedor (span/small) antes del texto
    tstart = html.rfind("<span", 0, idx)
    tstart2 = html.rfind("<small", 0, idx)
    tstart = max(tstart, tstart2)
    gt = html.find(">", tstart)
    if tstart != -1 and gt != -1 and "data-en=" not in html[tstart:gt]:
        html = html[:gt] + ' data-en="' + en + '"' + html[gt:]; n += 1

f.write_text(html, encoding="utf-8")
print("Cambios aplicados:", n)
