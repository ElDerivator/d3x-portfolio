/* enhancements.js — D3X Operations Console
   Tema claro/oscuro + idioma ES/EN. Independiente de script.js. */
(function () {
  "use strict";
  var root = document.documentElement;
  var THEME_KEY = "d3x-theme";
  var LANG_KEY = "d3x-lang";

  /* ---------------- TEMA ---------------- */
  function systemPrefersDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function resolveTheme() {
    var s = null;
    try { s = localStorage.getItem(THEME_KEY); } catch (e) {}
    if (s === "dark" || s === "light") return s;
    return systemPrefersDark() ? "dark" : "light";
  }
  function applyTheme(theme) {
    root.dataset.theme = theme;
    var btn = document.querySelector("[data-theme-toggle]");
    if (btn) {
      var dark = theme === "dark";
      btn.setAttribute("aria-pressed", String(dark));
      btn.setAttribute("aria-label", dark ? "Cambiar a modo claro" : "Cambiar a modo oscuro");
      var ico = btn.querySelector(".ico"), txt = btn.querySelector(".txt");
      if (ico) ico.textContent = dark ? "☀" : "☾";
      if (txt) txt.textContent = dark ? "Light" : "Dark";
    }
  }
  function setTheme(t) { applyTheme(t); try { localStorage.setItem(THEME_KEY, t); } catch (e) {} }

  /* ---------------- IDIOMA ---------------- */
  function resolveLang() {
    var s = null;
    try { s = localStorage.getItem(LANG_KEY); } catch (e) {}
    if (s === "en" || s === "es") return s;
    return (navigator.language || "es").toLowerCase().indexOf("en") === 0 ? "en" : "es";
  }
  function applyLang(lang) {
    var nodes = document.querySelectorAll("[data-en]");
    nodes.forEach(function (el) {
      if (!("es" in el.dataset)) el.dataset.es = el.textContent.trim();
      el.textContent = lang === "en" ? el.dataset.en : el.dataset.es;
    });
    root.lang = lang;
    var btn = document.querySelector("[data-lang-toggle]");
    if (btn) {
      btn.textContent = lang === "en" ? "ES" : "EN";   // muestra idioma DESTINO
      btn.setAttribute("aria-label", lang === "en" ? "Cambiar a español" : "Switch to English");
    }
  }
  function setLang(l) { applyLang(l); try { localStorage.setItem(LANG_KEY, l); } catch (e) {} }

  /* Aplicar tema temprano (anti-flash) */
  applyTheme(resolveTheme());

  document.addEventListener("DOMContentLoaded", function () {
    applyTheme(root.dataset.theme || resolveTheme());
    applyLang(resolveLang());

    var themeBtn = document.querySelector("[data-theme-toggle]");
    if (themeBtn) themeBtn.addEventListener("click", function () {
      setTheme(root.dataset.theme === "dark" ? "light" : "dark");
    });

    var langBtn = document.querySelector("[data-lang-toggle]");
    if (langBtn) langBtn.addEventListener("click", function () {
      setLang(root.lang === "en" ? "es" : "en");
    });

    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (e) {
        var s = null; try { s = localStorage.getItem(THEME_KEY); } catch (err) {}
        if (!s) applyTheme(e.matches ? "dark" : "light");
      });
    }
  });
})();

/* "Ir al diagnóstico": abre el <details> colapsado + scroll suave */
(function () {
  function openDiag(e) {
    var sec = document.getElementById('diagnostico');
    if (!sec) return;
    var det = sec.querySelector('details');
    if (det) det.open = true;
    if (e) { e.preventDefault(); sec.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  }
  function wire() {
    document.querySelectorAll('a[href="#diagnostico"]').forEach(function (a) {
      a.addEventListener('click', openDiag);
    });
    if (location.hash === '#diagnostico') openDiag();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wire);
  else wire();
})();

/* Cintilla seamless: duplica el contenido hasta superar 2× el ancho visible
   (mantiene mitades idénticas para que la animación -50% no muestre hueco). */
(function () {
  function fillMarquee() {
    var track = document.querySelector('.stack-track');
    if (!track) return;
    var section = track.parentElement;
    var guard = 0;
    while (track.scrollWidth < section.clientWidth * 2 + 200 && guard < 5) {
      var kids = Array.prototype.slice.call(track.children);
      for (var i = 0; i < kids.length; i++) track.appendChild(kids[i].cloneNode(true));
      guard++;
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fillMarquee);
  else fillMarquee();
})();
