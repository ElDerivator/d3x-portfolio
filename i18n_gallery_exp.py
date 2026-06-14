#!/usr/bin/env python3
"""i18n de galería Delitruck + cajas de experiencia (lo que faltaba bilingüe).
Convención del sitio: texto visible = español, data-en = inglés.
Para la caption dinámica de la galería se añade data-gallery-text-en.
"""
import pathlib
idx = pathlib.Path(__file__).parent / 'index.html'
h = idx.read_text(encoding='utf-8')

R = [
 # figcaption inicial
 ('<figcaption data-gallery-caption>Evento nocturno, montaje y atención en punto de venta.</figcaption>',
  '<figcaption data-gallery-caption data-en="Night event, setup and on-site service.">Evento nocturno, montaje y atención en punto de venta.</figcaption>'),
 # captions dinámicas: añadir data-gallery-text-en junto a cada data-gallery-text
 ('data-gallery-text="Evento nocturno, montaje y atención en punto de venta."',
  'data-gallery-text="Evento nocturno, montaje y atención en punto de venta."\n                data-gallery-text-en="Night event, setup and on-site service."'),
 ('data-gallery-text="Operación con alta afluencia, coordinacion de servicio y ritmo de venta."',
  'data-gallery-text="Operación con alta afluencia, coordinación de servicio y ritmo de venta."\n                data-gallery-text-en="High-traffic operation, service coordination and sales pace."'),
 ('data-gallery-text="Producto, presentación, menú visible y control de preparacion."',
  'data-gallery-text="Producto, presentación, menú visible y control de preparación."\n                data-gallery-text-en="Product, presentation, visible menu and prep control."'),
 # labels de thumbnails
 ('<span>Evento</span>', '<span data-en="Event">Evento</span>'),
 ('<span>Operación</span>', '<span data-en="Operation">Operación</span>'),
 ('<span>Producto</span>', '<span data-en="Product">Producto</span>'),
 # experience-points (estaban solo en inglés -> español visible + data-en)
 ('<span>Event operations</span>', '<span data-en="Event operations">Operación de eventos</span>'),
 ('<span>Customer experience</span>', '<span data-en="Customer experience">Experiencia de cliente</span>'),
 ('<span>Inventory control</span>', '<span data-en="Inventory control">Control de inventario</span>'),
 ('<span>Pricing &amp; promotions</span>', '<span data-en="Pricing &amp; promotions">Precios y promociones</span>'),
 # experience-metrics: Field ops / Live demand / Business control
 ('<strong>Field ops</strong>', '<strong data-en="Field ops">Operación de campo</strong>'),
 ('<span>Montaje, servicio y cierre en eventos.</span>',
  '<span data-en="Setup, service and event teardown.">Montaje, servicio y cierre en eventos.</span>'),
 ('<strong>Live demand</strong>', '<strong data-en="Live demand">Demanda en vivo</strong>'),
 ('<span>Ajustes de producto, ritmo y comunicación.</span>',
  '<span data-en="Product adjustments, pace and communication.">Ajustes de producto, ritmo y comunicación.</span>'),
 ('<strong>Business control</strong>', '<strong data-en="Business control">Control del negocio</strong>'),
 ('<span>Costos, menú, inventario y promociones.</span>',
  '<span data-en="Costs, menu, inventory and promotions.">Costos, menú, inventario y promociones.</span>'),
]
miss = []
for old, new in R:
    if old in h:
        h = h.replace(old, new, 1)
    else:
        miss.append(old[:50])
idx.write_text(h, encoding='utf-8')
print('aplicados:', len(R) - len(miss), '/', len(R))
for m in miss:
    print('  NO ENCONTRADO:', m)
