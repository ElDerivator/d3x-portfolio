#!/usr/bin/env python3
"""Inyecta data-en="..." en elementos de solo-texto del index.html.
El español queda como contenido; enhancements.js togglea ES<->EN.
Reemplazos por string EXACTO y único (seguro, sin regex genérico)."""
import sys, pathlib

f = pathlib.Path("index.html")
html = f.read_text(encoding="utf-8")

# (old_exacto, new_exacto) — el new añade data-en con la traducción
R = [
    # --- Nav ---
    ('<a href="#work">Trabajo</a>', '<a href="#work" data-en="Experience">Trabajo</a>'),
    ('<a href="#projects">Proyectos</a>', '<a href="#projects" data-en="Projects">Proyectos</a>'),
    ('<a href="#game">Minijuego</a>', '<a href="#game" data-en="Mini-game">Minijuego</a>'),
    ('<a href="#education">Educacion</a>', '<a href="#education" data-en="Education">Educacion</a>'),
    ('<a href="#credentials">Credenciales</a>', '<a href="#credentials" data-en="Credentials">Credenciales</a>'),
    ('<a href="#contact">Contacto</a>', '<a href="#contact" data-en="Contact">Contacto</a>'),
    # --- Hero ---
    ('<p class="eyebrow">Mexico City &middot; Remote / Hybrid</p>',
     '<p class="eyebrow" data-en="Mexico City &middot; Remote / Hybrid">Mexico City &middot; Remote / Hybrid</p>'),
    ('<p class="hero-summary">',
     '<p class="hero-summary" data-en="I build practical solutions that turn repetitive work into measurable processes: automation with Power Automate and Office Scripts, data validation, operational reporting, dashboards, documentation, and technical support with a continuous-improvement mindset.">'),
    ('<a class="button primary" href="assets/LGRA_CV.pdf" download>Descargar CV</a>',
     '<a class="button primary" href="assets/LGRA_CV.pdf" download data-en="Download CV">Descargar CV</a>'),
    ('<a class="button secondary" href="#work">Ver experiencia</a>',
     '<a class="button secondary" href="#work" data-en="View experience">Ver experiencia</a>'),
    ('<a class="button ghost" href="#projects">Proyectos</a>',
     '<a class="button ghost" href="#projects" data-en="Projects">Proyectos</a>'),
    ('<span>anos en datos, soporte y operaciones</span>',
     '<span data-en="years in data, support &amp; operations">anos en datos, soporte y operaciones</span>'),
    ('<span>credenciales documentadas</span>',
     '<span data-en="documented credentials">credenciales documentadas</span>'),
    ('<span>arquitectura propia para automatizacion</span>',
     '<span data-en="self-built automation architecture">arquitectura propia para automatizacion</span>'),
    # --- Proyectos (headings) ---
    ('<p class="eyebrow">Proyectos construidos</p>',
     '<p class="eyebrow" data-en="Built projects">Proyectos construidos</p>'),
    ('<h2 id="client-value-title">Sistemas que diseñé y construí de punta a punta.</h2>',
     '<h2 id="client-value-title" data-en="Systems I designed and built end to end.">Sistemas que diseñé y construí de punta a punta.</h2>'),
    # --- Experiencia (headings) ---
    ('<p class="eyebrow">Carrera</p>', '<p class="eyebrow" data-en="Career">Carrera</p>'),
    ('<h2 id="work-title">Experiencia profesional</h2>',
     '<h2 id="work-title" data-en="Professional experience">Experiencia profesional</h2>'),
    ('<summary>Ver historial completo</summary>',
     '<summary data-en="View full history">Ver historial completo</summary>'),
    # --- Educacion ---
    ('<p class="eyebrow">Formacion academica</p>',
     '<p class="eyebrow" data-en="Education">Formacion academica</p>'),
    ('<h2 id="education-title">Negocio, personas y operaciones como base de trabajo.</h2>',
     '<h2 id="education-title" data-en="Business, people and operations as a working foundation.">Negocio, personas y operaciones como base de trabajo.</h2>'),
    # --- Credenciales ---
    ('<p class="eyebrow">Aprendizaje</p>', '<p class="eyebrow" data-en="Learning">Aprendizaje</p>'),
    ('<h2 id="credentials-title">Credenciales destacadas</h2>',
     '<h2 id="credentials-title" data-en="Featured credentials">Credenciales destacadas</h2>'),
    ('<summary>Ver las 11 credenciales documentadas</summary>',
     '<summary data-en="View all 11 documented credentials">Ver las 11 credenciales documentadas</summary>'),
    # --- Contacto ---
    ('<p class="eyebrow">Contacto</p>', '<p class="eyebrow" data-en="Contact">Contacto</p>'),
    ('<h2 id="contact-title">Hablemos con contexto.</h2>',
     '<h2 id="contact-title" data-en="Let&#39;s talk with context.">Hablemos con contexto.</h2>'),
]

missing = []
for old, new in R:
    if old in html:
        html = html.replace(old, new, 1) if old != '<a class="button secondary" href="#work">Ver experiencia</a>' else html.replace(old, new)
        # nota: 'Ver experiencia' puede aparecer 2x (hero+proyectos); ambos reciben data-en
    else:
        missing.append(old[:60])

f.write_text(html, encoding="utf-8")
print(f"Aplicados: {len(R)-len(missing)}/{len(R)}")
if missing:
    print("NO encontrados:")
    for m in missing:
        print("  -", m)
