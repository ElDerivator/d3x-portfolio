#!/usr/bin/env python3
"""Pasada 'menos texto': acorta párrafos largos visibles (ES + data-en)
a una línea punchy. Reemplazos por string exacto."""
import pathlib
f = pathlib.Path("index.html"); h = f.read_text(encoding="utf-8"); n = 0

pairs = [
    # Hero summary (ES textContent)
    ("Construyo soluciones practicas para convertir trabajo repetitivo en procesos medibles:\n            automatizacion con Power Automate y Office Scripts, validacion de datos, reporting\n            operativo, dashboards, documentacion y soporte tecnico con enfoque en mejora continua.",
     "Convierto trabajo repetitivo en procesos medibles: automatización, validación de datos, reporting y dashboards."),
    # Hero summary (data-en)
    ("I build practical solutions that turn repetitive work into measurable processes: automation with Power Automate and Office Scripts, data validation, operational reporting, dashboards, documentation, and technical support with a continuous-improvement mindset.",
     "I turn repetitive work into measurable processes: automation, data validation, reporting and dashboards."),
    # Proyecto D3X
    ("Sistema de automatización y orquestación multi-nodo: memoria gobernada, pipelines de datos, dashboards operativos y agentes coordinados. Python, colas de trabajo y bases vectoriales/grafo.",
     "Automatización y orquestación multi-agente: memoria gobernada, pipelines, dashboards y agentes coordinados."),
    ("A multi-node automation and orchestration system: governed memory, data pipelines, operational dashboards and coordinated agents. Python, work queues, and vector/graph databases.",
     "Multi-agent automation & orchestration: governed memory, pipelines, dashboards, coordinated agents."),
    # Proyecto SHORBULL
    ("Plataforma de e-commerce y operación: catálogo, inventario, múltiples canales de venta, panel de control y reporting. Next.js + datos estructurados, desplegada en producción.",
     "E-commerce y operación: catálogo, inventario, multicanal y dashboard. Next.js, en producción."),
    ("An e-commerce and operations platform: catalog, inventory, multiple sales channels, control panel and reporting. Next.js + structured data, deployed to production.",
     "E-commerce & ops: catalog, inventory, multi-channel and dashboard. Next.js, in production."),
    # Proyecto POS
    ("Punto de venta y gestión para negocios locales: ventas, inventario y reporting operativo para varias unidades. Enfoque en quitar trabajo manual y dar visibilidad.",
     "Punto de venta y gestión para negocios locales: ventas, inventario y reporting multi-unidad."),
    ("Point-of-sale and management for local businesses: sales, inventory and operational reporting across several units. Focused on removing manual work and adding visibility.",
     "Point-of-sale & management for local businesses: sales, inventory and multi-unit reporting."),
    # Delitruck feature (ES, multilínea)
    ("Como emprendedor y operations manager, Delitruck me dio practica directa en logistica,\n              inventario, precios, promociones, servicio al cliente, proveedores, montaje de eventos\n              y ejecucion bajo presion. Esa experiencia aterriza mi forma de trabajar: entender el\n              proceso completo, detectar fricciones y convertirlas en sistemas mas claros.",
     "Operé un food-truck de punta a punta: logística, inventario, precios, clientes y ejecución bajo presión. Me enseñó a ver el proceso completo y convertir fricción en sistemas más claros."),
    ("As an entrepreneur and operations manager, Delitruck gave me direct practice in logistics, inventory, pricing, promotions, customer service, suppliers, event setup and execution under pressure. That experience grounds how I work: understand the whole process, spot friction and turn it into clearer systems.",
     "Ran a food-truck end to end: logistics, inventory, pricing, customers and execution under pressure. It taught me to see the whole process and turn friction into clearer systems."),
    # Proyectos intro (acortar)
    ("No solo analizo datos: diseño y opero los sistemas que los mueven. Estos son proyectos\n              propios, construidos con automatización, datos y criterio de operación.",
     "No solo analizo datos: diseño y opero los sistemas que los mueven."),
    ("I don't just analyze data: I design and run the systems that move it. These are my own projects.",
     "I don't just analyze data: I design and run the systems that move it."),
]
for old, new in pairs:
    if old in h:
        h = h.replace(old, new); n += 1
    else:
        print("NO:", old[:45])
f.write_text(h, encoding="utf-8"); print("Acortados:", n, "/", len(pairs))
