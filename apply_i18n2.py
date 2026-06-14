#!/usr/bin/env python3
"""Fase 4 parte 2: marca las CARDS (proyectos, timeline, experiencia,
educación) con data-en. Strings de una sola línea, exactos y únicos."""
import pathlib
f = pathlib.Path("index.html")
html = f.read_text(encoding="utf-8")

R = [
    # ---- Cards de Proyectos ----
    ('<h3>D3X — Orquestación multi-agente</h3>',
     '<h3 data-en="D3X — Multi-agent orchestration">D3X — Orquestación multi-agente</h3>'),
    ('<p>Sistema de automatización y orquestación multi-nodo: memoria gobernada, pipelines de datos, dashboards operativos y agentes coordinados. Python, colas de trabajo y bases vectoriales/grafo.</p>',
     '<p data-en="A multi-node automation and orchestration system: governed memory, data pipelines, operational dashboards and coordinated agents. Python, work queues, and vector/graph databases.">Sistema de automatización y orquestación multi-nodo: memoria gobernada, pipelines de datos, dashboards operativos y agentes coordinados. Python, colas de trabajo y bases vectoriales/grafo.</p>'),
    ('<h3>SHORBULL — CommerceOps</h3>',
     '<h3 data-en="SHORBULL — CommerceOps">SHORBULL — CommerceOps</h3>'),
    ('<p>Plataforma de e-commerce y operación: catálogo, inventario, múltiples canales de venta, panel de control y reporting. Next.js + datos estructurados, desplegada en producción.</p>',
     '<p data-en="An e-commerce and operations platform: catalog, inventory, multiple sales channels, control panel and reporting. Next.js + structured data, deployed to production.">Plataforma de e-commerce y operación: catálogo, inventario, múltiples canales de venta, panel de control y reporting. Next.js + datos estructurados, desplegada en producción.</p>'),
    ('<h3>POS — Gestión de unidades</h3>',
     '<h3 data-en="POS — Multi-unit management">POS — Gestión de unidades</h3>'),
    ('<p>Punto de venta y gestión para negocios locales: ventas, inventario y reporting operativo para varias unidades. Enfoque en quitar trabajo manual y dar visibilidad.</p>',
     '<p data-en="Point-of-sale and management for local businesses: sales, inventory and operational reporting across several units. Focused on removing manual work and adding visibility.">Punto de venta y gestión para negocios locales: ventas, inventario y reporting operativo para varias unidades. Enfoque en quitar trabajo manual y dar visibilidad.</p>'),
    # ---- Timeline (descripciones) ----
    ('<p>10–20 interacciones diarias con ~90% de resolución bajo métricas en tiempo real; documentación en CRM, diagnóstico root-cause y detección de patrones para oportunidades de automatización.</p>',
     '<p data-en="10–20 daily customer interactions with a ~90% resolution rate under real-time metrics; CRM documentation, root-cause diagnostics, and pattern detection for automation opportunities.">10–20 interacciones diarias con ~90% de resolución bajo métricas en tiempo real; documentación en CRM, diagnóstico root-cause y detección de patrones para oportunidades de automatización.</p>'),
    ('<p>Cuenta The Coca-Cola Company: análisis y reporting de Net Revenue Sales del Caribe. Resolví un blocker automatizando la integración de headers desde un ticketing tipo Jira, eliminando captura manual.</p>',
     '<p data-en="The Coca-Cola Company account: Net Revenue Sales analysis and reporting for the Caribbean. Resolved a blocker by automating header integration from a Jira-like ticketing system, removing manual data entry.">Cuenta The Coca-Cola Company: análisis y reporting de Net Revenue Sales del Caribe. Resolví un blocker automatizando la integración de headers desde un ticketing tipo Jira, eliminando captura manual.</p>'),
    ('<p>Analítica WFM para una operación de 500 agentes. Diseñé un ETL completo (Oracle SQL → distribución por correo vía Power Automate) y automaticé la rotación diaria de asientos de 3–4 h a ~30 min. Una auditoría de piso descubrió un abuso del sistema de ruteo de llamadas.</p>',
     '<p data-en="WFM analytics for a 500-agent operation. Designed a full ETL pipeline (Oracle SQL → automated email distribution via Power Automate) and automated the daily seat-rotation from 3–4 h to ~30 min. A floor audit uncovered abuse of the call-routing system.">Analítica WFM para una operación de 500 agentes. Diseñé un ETL completo (Oracle SQL → distribución por correo vía Power Automate) y automaticé la rotación diaria de asientos de 3–4 h a ~30 min. Una auditoría de piso descubrió un abuso del sistema de ruteo de llamadas.</p>'),
    ('<p>Tomaba requerimientos de áreas cross-funcionales y construía soluciones de datos. Construí un ETL que automatizó un reporte de status antes mantenido por un equipo de 5 personas, entregando a cada PM una vista consolidada y pre-filtrada. 3.5 años de datos operativos en telecom.</p>',
     '<p data-en="Took in requests from cross-functional teams and built custom data solutions. Built an ETL that automated a status report previously maintained by a 5-person team, delivering each PM a consolidated, pre-filtered view. 3.5 years of operational data in telecom.">Tomaba requerimientos de áreas cross-funcionales y construía soluciones de datos. Construí un ETL que automatizó un reporte de status antes mantenido por un equipo de 5 personas, entregando a cada PM una vista consolidada y pre-filtrada. 3.5 años de datos operativos en telecom.</p>'),
    ('<p>Operé un food-truck de punta a punta: operación, logística, servicio al cliente, marketing y expansión.</p>',
     '<p data-en="Ran a food-truck end to end: operations, logistics, customer service, marketing and expansion.">Operé un food-truck de punta a punta: operación, logística, servicio al cliente, marketing y expansión.</p>'),
    ('<p>Seguimiento operativo, comunicación y resolución de problemas.</p>',
     '<p data-en="Operational tracking, communication and problem-solving.">Seguimiento operativo, comunicación y resolución de problemas.</p>'),
    ('<p>Servicio al cliente, soporte administrativo y manejo de front desk.</p>',
     '<p data-en="Customer service, administrative support and front-desk management.">Servicio al cliente, soporte administrativo y manejo de front desk.</p>'),
    # ---- Experience summary (3 cards) ----
    ('<span>Soporte tecnico</span>', '<span data-en="Technical support">Soporte tecnico</span>'),
    ('<p>Diagnostico, documentacion CRM y escalaciones con lectura de patrones repetitivos.</p>',
     '<p data-en="Diagnostics, CRM documentation and escalations with an eye for repetitive patterns.">Diagnostico, documentacion CRM y escalaciones con lectura de patrones repetitivos.</p>'),
    ('<span>Datos y sistemas</span>', '<span data-en="Data &amp; systems">Datos y sistemas</span>'),
    ('<p>Analisis operativo, reporting, workforce, requerimientos y visibilidad para equipos.</p>',
     '<p data-en="Operational analysis, reporting, workforce, requirements and visibility for teams.">Analisis operativo, reporting, workforce, requerimientos y visibilidad para equipos.</p>'),
    ('<span>Operacion real</span>', '<span data-en="Real operations">Operacion real</span>'),
    ('<p>Eventos, inventario, pricing, clientes, proveedores y ejecucion bajo presion.</p>',
     '<p data-en="Events, inventory, pricing, customers, suppliers and execution under pressure.">Eventos, inventario, pricing, clientes, proveedores y ejecucion bajo presion.</p>'),
    # ---- Education (headings de una línea) ----
    ('<span>Administracion de Empresas</span>', '<span data-en="Business Administration">Administracion de Empresas</span>'),
    ('<h3>Formacion en gestion, operacion y toma de decisiones.</h3>',
     '<h3 data-en="Training in management, operations and decision-making.">Formacion en gestion, operacion y toma de decisiones.</h3>'),
    ('<span>Psicologia</span>', '<span data-en="Psychology">Psicologia</span>'),
    ('<h3>Formacion en comportamiento, comunicacion y lectura de personas.</h3>',
     '<h3 data-en="Training in behavior, communication and reading people.">Formacion en comportamiento, comunicacion y lectura de personas.</h3>'),
    ('<span>Trayectoria academica</span>', '<span data-en="Academic path">Trayectoria academica</span>'),
    ('<h3>Formacion cursada con enfoque profesional aplicado.</h3>',
     '<h3 data-en="Studies completed with an applied professional focus.">Formacion cursada con enfoque profesional aplicado.</h3>'),
    # ---- Delitruck feature ----
    ('<p class="eyebrow">Experiencia de campo</p>', '<p class="eyebrow" data-en="Field experience">Experiencia de campo</p>'),
    ('<h3>Delitruck: operaciones reales, clientes reales, decisiones en tiempo real.</h3>',
     '<h3 data-en="Delitruck: real operations, real customers, real-time decisions.">Delitruck: operaciones reales, clientes reales, decisiones en tiempo real.</h3>'),
]

missing = []
for old, new in R:
    if old in html:
        html = html.replace(old, new)
    else:
        missing.append(old[:55])
f.write_text(html, encoding="utf-8")
print(f"Aplicados: {len(R)-len(missing)}/{len(R)}")
for m in missing:
    print("  NO:", m)
