#!/usr/bin/env python3
"""Genera páginas de detalle por proyecto reutilizando el design system (styles.css + console.css).
Cada página: header/footer del sitio, tema+idioma (enhancements.js), hero del proyecto, stack, cuerpo y media."""
from pathlib import Path

ROOT = Path(__file__).parent

HEAD = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{meta}" />
    <meta name="theme-color" content="#0a8f8a" />
    <title>{title} | D3X · Luis Rivero</title>
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%23121418'/%3E%3Ctext x='32' y='39' text-anchor='middle' font-family='Arial' font-size='22' font-weight='800' fill='white'%3ED3X%3C/text%3E%3C/svg%3E" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="styles.css" />
    <link rel="stylesheet" href="console.css" />
    <script>(function(){try{var t=localStorage.getItem("d3x-theme");if(!t)t=(window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches)?"dark":"light";document.documentElement.dataset.theme=t;}catch(e){}})();</script>
  </head>
  <body>
    <header class="site-header" aria-label="Navegacion principal">
      <a class="brand" href="index.html" aria-label="D3X inicio">
        <span class="brand-mark">D3X</span>
        <span class="brand-text">Data &middot; Automation &middot; Operations</span>
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span> Menu</button>
      <nav class="nav-links" id="site-nav" aria-label="Secciones">
        <a href="index.html#work" data-en="Experience">Trabajo</a>
        <a href="index.html#projects" data-en="Projects">Proyectos</a>
        <a href="index.html#game" data-en="Mini-game">Minijuego</a>
        <a href="index.html#education" data-en="Education">Educación</a>
        <a href="index.html#contact" data-en="Contact">Contacto</a>
      </nav>
      <div class="console-controls">
        <button class="console-btn lang-btn" type="button" data-lang-toggle aria-label="Switch language">EN</button>
        <button class="console-btn" type="button" data-theme-toggle aria-pressed="false" aria-label="Cambiar a modo oscuro"><span class="ico" aria-hidden="true">☾</span><span class="txt">Dark</span></button>
      </div>
    </header>
    <main class="project-page">
      <section class="section">
        <a class="proj-back" href="index.html#projects" data-en="&larr; Back to projects">&larr; Volver a proyectos</a>
        <p class="eyebrow" data-en="{eyebrow_en}">{eyebrow}</p>
        <h1 class="proj-title">{name}</h1>
        <p class="proj-tagline" data-en="{tagline_en}">{tagline}</p>
        <div class="proj-tags">{tags}</div>
        <div class="proj-actions">{actions}</div>
      </section>
      <section class="section proj-body">
        {body}
      </section>
      {media}
    </main>
    <footer class="site-footer">
      <div><strong>D3X &middot; d3x.biz</strong><span data-en="Portfolio for data, automation and operations work.">Portafolio de trabajo en datos, automatización y operaciones.</span></div>
      <a href="index.html" data-en="Back to home">Volver al inicio</a>
    </footer>
    <script src="enhancements.js"></script>
    <script>(function(){var h=document.querySelector(".site-header"),b=document.querySelector(".menu-toggle");if(b)b.addEventListener("click",function(){var o=h.classList.toggle("is-open");b.setAttribute("aria-expanded",String(o));});})();</script>
  </body>
</html>
"""

def tag(t): return f'<span class="proj-tag">{t}</span>'
def block(h_es, h_en, p_es, p_en):
    return (f'<div class="proj-block"><h2 data-en="{h_en}">{h_es}</h2>'
            f'<p data-en="{p_en}">{p_es}</p></div>')
def btn(href, es, en, cls="primary"):
    return f'<a class="button {cls}" href="{href}" target="_blank" rel="noopener" data-en="{en}">{es}</a>'

PROJECTS = {
  "proyecto-exocortex.html": dict(
    title="Exocortex", meta="Exocortex — governed memory and agent orchestration system.",
    eyebrow="Sistema cognitivo", eyebrow_en="Cognitive system", name="Exocortex",
    tagline="Memoria gobernada, grafo de verdad temporal y orquestación de agentes local-first.",
    tagline_en="Governed memory, a temporal truth graph and local-first agent orchestration.",
    tags="".join(tag(t) for t in ["Python","FalkorDB","Qdrant","DAG runner","Local-first","Multi-agente"]),
    actions='<span class="proj-note" data-en="Private system &mdash; shown via screenshots">Sistema privado &mdash; se muestra con capturas</span>',
    body=(
      block("Qué es","What it is",
        "Una extensión cognitiva: un sistema de memoria que sabe qué sabe, por qué lo sabe, qué resultado lo confirmó y cuándo cambió. Construido para correr en hardware modesto (Raspberry Pi) bajo restricciones reales de cómputo y costo.",
        "A cognitive extension: a memory system that knows what it knows, why, what outcome confirmed it and when it changed. Built to run on modest hardware (Raspberry Pi) under real compute and cost constraints.")+
      block("Qué construí","What I built",
        "Grafo de verdad temporal bi-temporal (283 edges en FalkorDB), memoria gobernada con validación determinista, pipelines con checkpoint/resume/replay y un gate que protege la capa core. Lectura matemática sin LLM en el hot-path; escritura propuesta por LLM y decidida por gates y resultados.",
        "A bi-temporal truth graph (283 edges in FalkorDB), governed memory with deterministic validation, pipelines with checkpoint/resume/replay, and a gate protecting the core layer. Math-based reads with no LLM in the hot path; LLM-proposed writes decided by gates and outcomes.")+
      block("Resultado","Outcome",
        "Un loop de memoria que corre solo, se autocorrige y puede explicar su propio conocimiento — cero alucinación como principio rector.",
        "A memory loop that runs on its own, self-corrects and can explain its own knowledge — zero hallucination as a guiding principle.")),
    media=""),
  "proyecto-shorbull.html": dict(
    title="SHORBULL", meta="SHORBULL CommerceOps — e-commerce and operations platform.",
    eyebrow="CommerceOps", eyebrow_en="CommerceOps", name="SHORBULL",
    tagline="Plataforma de e-commerce y operación: catálogo, inventario, multicanal y dashboard.",
    tagline_en="E-commerce and operations platform: catalog, inventory, multi-channel and dashboard.",
    tags="".join(tag(t) for t in ["Next.js","FastAPI","SQLite","359 productos","Multicanal","Dashboard"]),
    actions=btn("https://github.com/ElDerivator/d3x-shorbull","Ver repositorio","View repository"),
    body=(
      block("Qué es","What it is",
        "Sistema de operaciones de comercio de punta a punta: gestiona un catálogo de 359 productos, inventario, precios, 12 canales de venta y pago contra entrega, con panel de administración y reportes.",
        "An end-to-end commerce operations system: manages a 359-product catalog, inventory, pricing, 12 sales channels and cash-on-delivery, with an admin panel and reports.")+
      block("Qué construí","What I built",
        "Frontend Next.js + backend FastAPI, historial de precios, export a XLSX, dashboard de operación y un bot de mensajería como patrón reutilizable. Todo diseñado para que un dueño-operador controle la tienda sin fricción.",
        "A Next.js frontend + FastAPI backend, price history, XLSX export, an operations dashboard and a messaging bot as a reusable pattern. Designed so an owner-operator runs the store without friction.")+
      block("Resultado","Outcome",
        "Un CommerceOps completo que demuestra capacidad de construir producto real, no solo prototipos.",
        "A complete CommerceOps that proves the ability to build real product, not just prototypes.")),
    media=""),
  "proyecto-pos.html": dict(
    title="POS Multi-unidad", meta="POS — multi-unit point of sale and management for local businesses.",
    eyebrow="Punto de venta", eyebrow_en="Point of sale", name="POS · Gestión de unidades",
    tagline="Punto de venta y gestión multi-unidad para negocios locales: ventas, inventario y reporting.",
    tagline_en="Multi-unit point of sale and management for local businesses: sales, inventory and reporting.",
    tags="".join(tag(t) for t in ["FastAPI","42 tests","Multi-unidad","Inventario","Dashboard","LAN"]),
    actions=btn("https://github.com/ElDerivator/d3x-family","Ver repositorio","View repository"),
    body=(
      block("Qué es","What it is",
        "Plataforma de punto de venta y gestión para tres unidades de negocio reales (abarrotes, ferretería, ropa de bebé): ventas, inventario y reporting consolidado por unidad.",
        "A point-of-sale and management platform for three real business units (groceries, hardware, baby clothes): sales, inventory and consolidated per-unit reporting.")+
      block("Qué construí","What I built",
        "API FastAPI con 42 tests, catálogo multi-unidad, economía por unidad, dashboard y CLI. Pensado para operar en LAN, robusto y verificable.",
        "A FastAPI API with 42 tests, multi-unit catalog, per-unit economics, dashboard and CLI. Built to run on LAN, robust and verifiable.")+
      block("Resultado","Outcome",
        "Un sistema operativo de tienda con disciplina de pruebas — la base de cómo construyo: verificable de punta a punta.",
        "A store operations system with test discipline — the basis of how I build: verifiable end to end.")),
    media=""),
  "proyecto-videos.html": dict(
    title="Creación de videos con IA", meta="AI video creation — branding, product demos and social content.",
    eyebrow="Video con IA", eyebrow_en="AI video", name="Creación de videos con IA",
    tagline="Generación de video con IA: branding, demos de producto y contenido para social.",
    tagline_en="AI video generation: branding, product demos and social content.",
    tags="".join(tag(t) for t in ["IA generativa","Branding","Demos de producto","Social","Prompt-to-render"]),
    actions='<a class="button secondary" href="index.html#projects" data-en="Back to projects">Volver a proyectos</a>',
    body=(
      block("Qué es","What it is",
        "Pipeline propio de creación de video con IA: de un prompt a un render listo para social, aplicado a branding y demostraciones de producto.",
        "An in-house AI video creation pipeline: from a prompt to a social-ready render, applied to branding and product demos.")+
      block("Qué construí","What I built",
        "Flujo de generación, marca y montaje para producir piezas cortas de forma repetible. Abajo, ejemplos reales.",
        "A generation, branding and editing flow to produce short pieces repeatably. Real examples below.")),
    media='<section class="section"><div class="video-grid">'+
      "".join(f'<figure><video controls preload="metadata" playsinline src="assets/videos/{f}"></video><figcaption>{c}</figcaption></figure>'
        for f,c in [("Personal_derivatorcondex.mp4","D3X · personal"),("Derivatorviendoadex.mp4","D3X · operación"),
                    ("SHORBULL_parrilla.mp4","SHORBULL · producto"),("SHORBULL_Reclutamiento.mp4","SHORBULL · reclutamiento"),
                    ("SHORBULL_Senora.mp4","SHORBULL · campaña")])+
      '</div></section>'),
}

for fname, p in PROJECTS.items():
    out = HEAD
    for k, v in p.items():
        out = out.replace("{" + k + "}", v)
    (ROOT / fname).write_text(out, encoding="utf-8")
    print("escrito:", fname)
