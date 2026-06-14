#!/usr/bin/env python3
"""Hace bilingüe el minijuego en script.js: inserta diccionario ES->EN
+ helper tr(), y enruta los textos dinámicos por él."""
import pathlib
f = pathlib.Path("script.js")
s = f.read_text(encoding="utf-8")

block = '''const GAME_I18N = {
  "Automatizacion": "Automation", "Validacion": "Validation", "Escalacion": "Escalation", "Dashboard": "Dashboard",
  "El reporte semanal se copia a mano cada lunes": "The weekly report is copied by hand every Monday",
  "La misma hoja, el mismo mensaje y los mismos destinatarios se repiten cada semana.": "Same sheet, same message, same recipients repeat every week.",
  "Bien visto. El trabajo manual recurrente pertenece a un flujo automatizado.": "Well spotted. Recurring manual work belongs in an automated flow.",
  "El CSV de asistencia no coincide con el archivo maestro": "The attendance CSV doesn't match the master file",
  "Dos fuentes no coinciden en IDs de empleados y fechas de turno.": "Two sources disagree on employee IDs and shift dates.",
  "Ruta correcta. Validar antes evita decisiones con datos rotos.": "Right call. Validating first avoids decisions on broken data.",
  "Un caso tecnico falla despues del diagnostico estandar": "A technical case fails after standard diagnostics",
  "El procedimiento normal ya se completo, pero la causa sigue sin estar clara.": "The normal procedure is done, but the cause is still unclear.",
  "Correcto. Los casos complejos necesitan una escalacion controlada.": "Correct. Complex cases need a controlled escalation.",
  "El equipo pide visibilidad diaria de nivel de servicio": "The team asks for daily service-level visibility",
  "La metrica se revisa seguido y debe ser facil de escanear.": "The metric is checked often and must be easy to scan.",
  "Exacto. Las metricas recurrentes deben estar visibles, no escondidas en archivos.": "Exactly. Recurring metrics should be visible, not hidden in files.",
  "Un reporte muestra registros duplicados despues de exportar": "A report shows duplicate records after export",
  "El volumen cambio, pero el responsable esperaba el mismo conteo.": "The volume changed, but the owner expected the same count.",
  "Bien. Los duplicados son una senal de calidad antes de ser problema de reporte.": "Good. Duplicates are a data-quality signal before they become a reporting problem.",
  "Supervisores envian el mismo recordatorio cada turno": "Supervisors send the same reminder every shift",
  "Horario, audiencia y mensaje son predecibles.": "Timing, audience and message are predictable.",
  "Muy bien. La comunicacion repetible es candidata clara para automatizar.": "Great. Repeatable communication is a clear candidate for automation.",
  "Productividad se revisa en cada reunion operativa": "Productivity is reviewed in every operations meeting",
  "El equipo necesita ver tendencias, no abrir otra hoja estatica.": "The team needs to see trends, not open another static sheet.",
  "Buena ruta. Las tendencias que guian reuniones merecen dashboard.": "Good route. Trends that drive meetings deserve a dashboard.",
  "Un proceso manual rompe una regla de cumplimiento": "A manual process breaks a compliance rule",
  "El riesgo afecta calidad de servicio y necesita responsable claro.": "The risk affects service quality and needs a clear owner.",
  "Correcto. Un riesgo operativo necesita ownership antes de optimizarse.": "Correct. An operational risk needs ownership before optimization.",
  "Corriendo": "Running",
  "Manda la senal a la capa correcta.": "Send the signal to the right layer.",
  "Jugar de nuevo": "Play again",
  "Run terminado. La operacion quedo mas clara que al inicio.": "Run over. The operation ended clearer than it started.",
  "Run terminado. La friccion todavia pesa en el flujo.": "Run over. Friction still weighs on the flow.",
};
function GLANG() { return document.documentElement.lang === "en" ? "en" : "es"; }
function tr(t) { return GLANG() === "en" ? (GAME_I18N[t] || t) : t; }

function renderGame() {'''

s = s.replace("function renderGame() {", block, 1)

reps = [
    ("gameEls.type.textContent = game.current.type;", "gameEls.type.textContent = tr(game.current.type);"),
    ("gameEls.title.textContent = game.current.title;", "gameEls.title.textContent = tr(game.current.title);"),
    ("gameEls.description.textContent = game.current.description;", "gameEls.description.textContent = tr(game.current.description);"),
    ("gameEls.feedback.textContent = game.current.success;", "gameEls.feedback.textContent = tr(game.current.success);"),
    ('gameEls.start.textContent = "Corriendo";', 'gameEls.start.textContent = tr("Corriendo");'),
    ('gameEls.feedback.textContent = "Manda la senal a la capa correcta.";', 'gameEls.feedback.textContent = tr("Manda la senal a la capa correcta.");'),
    ('gameEls.start.textContent = "Jugar de nuevo";', 'gameEls.start.textContent = tr("Jugar de nuevo");'),
    ('? "Run terminado. La operacion quedo mas clara que al inicio."', '? tr("Run terminado. La operacion quedo mas clara que al inicio.")'),
    (': "Run terminado. La friccion todavia pesa en el flujo.";', ': tr("Run terminado. La friccion todavia pesa en el flujo.");'),
    ('gameEls.feedback.textContent = `Casi. Esta senal pertenecia a ${game.current.answer}.`;',
     'gameEls.feedback.textContent = GLANG() === "en" ? `Close. That signal belonged to ${game.current.answer}.` : `Casi. Esta senal pertenecia a ${game.current.answer}.`;'),
]
n = 0
for old, new in reps:
    if old in s:
        s = s.replace(old, new); n += 1
    else:
        print("NO encontrado:", old[:50])

f.write_text(s, encoding="utf-8")
print("Reemplazos:", n, "/ dict insertado:", "GAME_I18N" in s)
