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
