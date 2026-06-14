#!/usr/bin/env python3
"""Cierra puntos 1 y 3 del portfolio:
  1. Añade data-en (inglés) a los <p class="skills"> de credenciales.
  3. Corrige acentos del texto español en index.html y script.js.
No toca texto inglés (data-en) porque las grafías españolas con acento
no colisionan con sus equivalentes ingleses. 'esta/Esta' (demostrativos)
y 'menu-toggle' (clase CSS) se excluyen a propósito.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent

# --- Punto 1: skills ES -> data-en EN (match sobre texto SIN acentos) ---
SKILLS = {
    'Resolucion de problemas, Agile Methodologies, Product Ownership':
        'Problem solving, Agile methodologies, Product ownership',
    'Modelos estadisticos, Python, analisis de datos':
        'Statistical models, Python, data analysis',
    'Bases de datos, modelos estadisticos, data warehousing':
        'Databases, statistical models, data warehousing',
    'Project Management, resolucion de problemas, agile practices':
        'Project management, problem solving, agile practices',
    'Analisis de datos, visualizacion, fundamentos de reporting':
        'Data analysis, visualization, reporting fundamentals',
    'Modelos estadisticos, Python, analisis y visualizacion':
        'Statistical models, Python, analysis and visualization',
    'Modelos estadisticos, Python, data science':
        'Statistical models, Python, data science',
    'Data Science, modelos estadisticos, Python':
        'Data science, statistical models, Python',
    'Modelos estadisticos, analisis de clusters, data fundamentals':
        'Statistical models, cluster analysis, data fundamentals',
    'Modelos estadisticos, SQL, ETL, BI foundations':
        'Statistical models, SQL, ETL, BI foundations',
}

# --- Punto 3: mapa de acentos (clave sin acento -> con acento) ---
# Solo palabras inequívocamente españolas. Case-insensitive con preservación.
ACCENTS = {
    'senal': 'señal', 'senales': 'señales',
    'analisis': 'análisis',
    'resolucion': 'resolución',
    'visualizacion': 'visualización',
    'metodo': 'método',
    'automatizacion': 'automatización',
    'gestion': 'gestión',
    'atencion': 'atención',
    'comunicacion': 'comunicación',
    'titulacion': 'titulación',
    'administracion': 'administración',
    'psicologia': 'psicología',
    'formacion': 'formación',
    'educacion': 'educación',
    'diagnostico': 'diagnóstico',
    'pagina': 'página', 'paginas': 'páginas',
    'cotizacion': 'cotización',
    'operacion': 'operación', 'operaciones': 'operaciones',
    'presentacion': 'presentación',
    'tecnico': 'técnico', 'tecnica': 'técnica', 'tecnicos': 'técnicos',
    'rapido': 'rápido', 'rapida': 'rápida',
    'metricas': 'métricas', 'metrica': 'métrica',
    'practicas': 'prácticas', 'practica': 'práctica',
    'despues': 'después',
    'aqui': 'aquí',
    'mas': 'más',
    'quedo': 'quedó',
    'pertenecia': 'pertenecía',
}

def preserve_case(src, repl):
    if src.isupper():
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl

def apply_accents(text):
    n = 0
    for plain, acc in ACCENTS.items():
        pat = re.compile(r'\b' + plain + r'\b', re.IGNORECASE)
        def _r(m):
            nonlocal n
            n += 1
            return preserve_case(m.group(0), acc)
        text = pat.sub(_r, text)
    return text, n

# 'menu' -> 'menú' SOLO en texto español, nunca en class="menu-toggle"
def fix_menu(text):
    text = text.replace('presentacion, menu visible', 'presentación, menú visible')
    text = text.replace('Costos, menu, inventario', 'Costos, menú, inventario')
    text = text.replace('senal, ', 'señal, ')  # por si quedara suelto
    return text

# ---- index.html ----
idx = ROOT / 'index.html'
html = idx.read_text(encoding='utf-8')
skills_added = 0
for es, en in SKILLS.items():
    old = f'<p class="skills">{es}</p>'
    new = f'<p class="skills" data-en="{en}">{es}</p>'
    if old in html:
        html = html.replace(old, new)
        skills_added += 1
html = fix_menu(html)
html, idx_acc = apply_accents(html)
idx.write_text(html, encoding='utf-8')

# ---- script.js (minijuego: feedback dinámico ES) ----
js = ROOT / 'script.js'
jstxt = js.read_text(encoding='utf-8')
jstxt = fix_menu(jstxt)
jstxt, js_acc = apply_accents(jstxt)
js.write_text(jstxt, encoding='utf-8')

print(f'skills data-en añadidos: {skills_added}/10')
print(f'acentos index.html: {idx_acc}')
print(f'acentos script.js:  {js_acc}')
