const header = document.querySelector(".site-header");
const progressBar = document.querySelector(".page-progress i");
const menuToggle = document.querySelector(".menu-toggle");
const navItems = [...document.querySelectorAll(".nav-links a[href^='#']")];
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const D3X_WORKSPACE_LEAD_ENDPOINT = "";
const navSections = navItems
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

function updateHeaderShadow() {
  header?.classList.toggle("is-scrolled", window.scrollY > 10);
}

function updateScrollState() {
  updateHeaderShadow();
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
  if (progressBar) progressBar.style.setProperty("--scroll-progress", `${progress}%`);

  const passedSections = navSections.filter(
    (section) => section.getBoundingClientRect().top <= window.innerHeight * 0.35,
  );
  const activeSection = passedSections[passedSections.length - 1];

  navItems.forEach((link) => {
    link.classList.toggle("is-active", activeSection?.id === link.getAttribute("href").slice(1));
  });
}

window.addEventListener("scroll", updateScrollState, { passive: true });
window.addEventListener("resize", updateScrollState);
updateScrollState();

function setMenuOpen(open) {
  header?.classList.toggle("is-open", open);
  menuToggle?.setAttribute("aria-expanded", String(open));
  document.body.classList.toggle("menu-open", open);
}

menuToggle?.addEventListener("click", () => {
  setMenuOpen(!header?.classList.contains("is-open"));
});

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const target = document.querySelector(link.getAttribute("href"));
    if (!target) return;
    event.preventDefault();
    setMenuOpen(false);
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

const revealTargets = document.querySelectorAll(
  ".section-grid, .section-heading, .stack-section, .method-shell, .method-steps article, .value-shell, .value-grid article, .project-focus, .project-card, .game-shell, .career-arc, .experience-feature, .timeline article, .education-shell, .education-grid article, .credential-map article, .credential-card, .contact-section, .contact-form",
);

function animateCount(element) {
  if (element.dataset.counted === "true") return;
  element.dataset.counted = "true";
  const target = Number(element.dataset.count || element.textContent);
  const duration = 900;
  const start = performance.now();

  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    element.textContent = Math.round(target * eased);
    if (progress < 1) {
      window.requestAnimationFrame(tick);
    } else {
      element.textContent = target;
    }
  }

  window.requestAnimationFrame(tick);
}

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      });
    },
    { threshold: 0.14 },
  );

  revealTargets.forEach((target, index) => {
    target.classList.add("reveal");
    target.style.transitionDelay = `${Math.min(index % 6, 5) * 55}ms`;
    revealObserver.observe(target);
  });

  const countObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        animateCount(entry.target);
        countObserver.unobserve(entry.target);
      });
    },
    { threshold: 0.5 },
  );

  document.querySelectorAll(".dashboard-visual [data-count]").forEach((counter) => {
    counter.textContent = "0";
    countObserver.observe(counter);
  });
} else {
  revealTargets.forEach((target) => target.classList.add("is-visible"));
  document.querySelectorAll(".dashboard-visual [data-count]").forEach(animateCount);
}

if (!reduceMotion) {
  document.querySelectorAll(".hero-proof article, .profile-snapshot article, .method-steps article, .value-grid article, .project-focus, .project-card, .credential-map article, .credential-card, .timeline article, .experience-copy, .education-grid article, .contact-form").forEach((card) => {
    card.addEventListener("pointermove", (event) => {
      const rect = card.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      const rotateX = ((event.clientY - rect.top) / rect.height - 0.5) * -3;
      const rotateY = ((event.clientX - rect.left) / rect.width - 0.5) * 3;
      card.style.setProperty("--mx", `${x}%`);
      card.style.setProperty("--my", `${y}%`);
      card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-3px)`;
      card.classList.add("is-tilting");
    });

    card.addEventListener("pointerleave", () => {
      card.style.removeProperty("transform");
      card.classList.remove("is-tilting");
    });
  });
}

const workspaceLeadForm = document.querySelector("[data-workspace-lead-form]");
const workspaceLeadStatus = document.querySelector("[data-workspace-lead-status]");
const workspaceEndpointAllowedPrefix = "https://script.google.com/";
const fallbackLeadMessage = "Formulario preparado. Por ahora puedes escribir a administracion@d3x.biz.";

function setLeadFormStatus(message, type = "") {
  if (!workspaceLeadStatus) return;
  workspaceLeadStatus.classList.remove("is-ok", "is-error");
  if (type) workspaceLeadStatus.classList.add(type);
  workspaceLeadStatus.textContent = message;
}

function getLeadField(name) {
  return workspaceLeadForm?.elements.namedItem(name);
}

function validateLeadForm() {
  const name = getLeadField("name")?.value.trim();
  const email = getLeadField("email")?.value.trim();
  const processProblem = getLeadField("process_problem")?.value.trim();
  const consent = getLeadField("consent")?.checked === true;
  const emailField = getLeadField("email");

  if (!name) return "Agrega tu nombre para solicitar el diagnóstico.";
  if (!email || !emailField?.checkValidity()) return "Agrega un email valido.";
  if (!processProblem) return "Describe brevemente el problema de proceso.";
  if (!consent) return "Confirma el consentimiento antes de enviar.";
  return "";
}

function buildWorkspaceLeadPayload() {
  const tools = getLeadField("current_tools")?.value
    .split(",")
    .map((tool) => tool.trim())
    .filter(Boolean) || [];
  const consentText = "Acepto que D3X use estos datos para responder mi solicitud.";

  return {
    source: "d3x.biz",
    source_channel: "public_website",
    name: getLeadField("name")?.value.trim(),
    company: getLeadField("company")?.value.trim() || null,
    email: getLeadField("email")?.value.trim(),
    phone: getLeadField("phone")?.value.trim() || null,
    business_type: getLeadField("business_type")?.value || null,
    process_problem: getLeadField("process_problem")?.value.trim(),
    current_tools: tools,
    urgency: getLeadField("urgency")?.value || "unknown",
    budget_range: getLeadField("budget_range")?.value || "unknown",
    consent: {
      provided: true,
      text: consentText,
      provided_at: new Date().toISOString(),
    },
  };
}

workspaceLeadForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (getLeadField("website")?.value) {
    setLeadFormStatus(fallbackLeadMessage);
    return;
  }

  const validationMessage = validateLeadForm();
  if (validationMessage) {
    setLeadFormStatus(validationMessage, "is-error");
    return;
  }

  if (!D3X_WORKSPACE_LEAD_ENDPOINT) {
    setLeadFormStatus(fallbackLeadMessage);
    return;
  }

  if (!D3X_WORKSPACE_LEAD_ENDPOINT.startsWith(workspaceEndpointAllowedPrefix)) {
    console.warn("Lead intake endpoint blocked: only Google Apps Script endpoints are allowed.");
    setLeadFormStatus("No se pudo enviar el formulario por configuracion segura del sitio.", "is-error");
    return;
  }

  const submitButton = workspaceLeadForm.querySelector("button[type='submit']");
  submitButton.disabled = true;
  setLeadFormStatus("Enviando solicitud a Google Workspace...");

  try {
    await fetch(D3X_WORKSPACE_LEAD_ENDPOINT, {
      method: "POST",
      mode: "no-cors",
      headers: {
        "Content-Type": "text/plain;charset=utf-8",
      },
      body: JSON.stringify(buildWorkspaceLeadPayload()),
    });
    workspaceLeadForm.reset();
    setLeadFormStatus("Solicitud recibida. Revisaremos tu diagnóstico antes de cualquier accion externa.", "is-ok");
  } catch (error) {
    setLeadFormStatus("No se pudo enviar. Puedes escribir a administracion@d3x.biz.", "is-error");
  } finally {
    submitButton.disabled = false;
  }
});

const galleryImage = document.querySelector("[data-gallery-image]");
const galleryCaption = document.querySelector("[data-gallery-caption]");
const galleryButtons = [...document.querySelectorAll("[data-gallery-src]")];
const galleryPrev = document.querySelector("[data-gallery-prev]");
const galleryNext = document.querySelector("[data-gallery-next]");
let galleryIndex = 0;

function setGalleryFallback() {
  galleryImage?.classList.add("is-missing");
  if (galleryCaption) {
    galleryCaption.textContent = "Agrega las fotos en assets/delitruck-01.jpeg a assets/delitruck-03.jpeg para activar esta galeria.";
  }
}

if (galleryImage) {
  galleryImage.addEventListener("error", setGalleryFallback);
}

function showGalleryImage(index) {
  if (!galleryImage || !galleryCaption || !galleryButtons.length) return;
  galleryIndex = (index + galleryButtons.length) % galleryButtons.length;
  const button = galleryButtons[galleryIndex];
  galleryButtons.forEach((item) => item.classList.remove("is-active"));
  button.classList.add("is-active");
  galleryImage.classList.remove("is-missing");
  galleryImage.classList.add("is-switching");

  window.setTimeout(() => {
    galleryImage.src = button.dataset.gallerySrc;
    galleryImage.alt = button.dataset.galleryAlt;
    const galLangEn = document.documentElement.lang === "en";
    galleryCaption.textContent = (galLangEn && button.dataset.galleryTextEn) || button.dataset.galleryText;
    galleryImage.classList.remove("is-switching");
  }, 160);
}

galleryButtons.forEach((button, index) => {
  button.addEventListener("click", () => showGalleryImage(index));
});

galleryPrev?.addEventListener("click", () => showGalleryImage(galleryIndex - 1));
galleryNext?.addEventListener("click", () => showGalleryImage(galleryIndex + 1));

const game = {
  duration: 45,
  timeLeft: 45,
  score: 0,
  friction: 0,
  streak: 0,
  active: false,
  timer: null,
  current: null,
  queue: [],     // señales pendientes (barajadas) en este run
  total: 0,      // total de señales del run
  solved: 0,     // cuántas se han resuelto
};

const signals = [
  {
    type: "Automatización",
    title: "El reporte semanal se copia a mano cada lunes",
    description: "La misma hoja, el mismo mensaje y los mismos destinatarios se repiten cada semana.",
    answer: "automate",
    success: "Bien visto. El trabajo manual recurrente pertenece a un flujo automatizado.",
  },
  {
    type: "Validacion",
    title: "El CSV de asistencia no coincide con el archivo maestro",
    description: "Dos fuentes no coinciden en IDs de empleados y fechas de turno.",
    answer: "validate",
    success: "Ruta correcta. Validar antes evita decisiones con datos rotos.",
  },
  {
    type: "Escalacion",
    title: "Un caso técnico falla después del diagnóstico estandar",
    description: "El procedimiento normal ya se completo, pero la causa sigue sin estar clara.",
    answer: "escalate",
    success: "Correcto. Los casos complejos necesitan una escalacion controlada.",
  },
  {
    type: "Dashboard",
    title: "El equipo pide visibilidad diaria de nivel de servicio",
    description: "La métrica se revisa seguido y debe ser facil de escanear.",
    answer: "dashboard",
    success: "Exacto. Las métricas recurrentes deben estar visibles, no escondidas en archivos.",
  },
  {
    type: "Validacion",
    title: "Un reporte muestra registros duplicados después de exportar",
    description: "El volumen cambio, pero el responsable esperaba el mismo conteo.",
    answer: "validate",
    success: "Bien. Los duplicados son una señal de calidad antes de ser problema de reporte.",
  },
  {
    type: "Automatización",
    title: "Supervisores envian el mismo recordatorio cada turno",
    description: "Horario, audiencia y mensaje son predecibles.",
    answer: "automate",
    success: "Muy bien. La comunicación repetible es candidata clara para automatizar.",
  },
  {
    type: "Dashboard",
    title: "Productividad se revisa en cada reunion operativa",
    description: "El equipo necesita ver tendencias, no abrir otra hoja estatica.",
    answer: "dashboard",
    success: "Buena ruta. Las tendencias que guian reuniones merecen dashboard.",
  },
  {
    type: "Escalacion",
    title: "Un proceso manual rompe una regla de cumplimiento",
    description: "El riesgo afecta calidad de servicio y necesita responsable claro.",
    answer: "escalate",
    success: "Correcto. Un riesgo operativo necesita ownership antes de optimizarse.",
  },
  {
    type: "Automatización",
    title: "Cada cierre de mes consolidas seis hojas a mano",
    description: "Mismas columnas, mismo formato, distinto periodo.",
    answer: "automate",
    success: "Eso. Una consolidación repetible es trabajo para un flujo, no para tus manos.",
  },
  {
    type: "Validacion",
    title: "Dos tableros reportan cifras distintas para el mismo KPI",
    description: "Nadie sabe cual es la fuente de verdad.",
    answer: "validate",
    success: "Correcto. Sin fuente validada, cada tablero cuenta una historia distinta.",
  },
  {
    type: "Escalacion",
    title: "Un cliente reporta una falla que afecta facturacion",
    description: "El impacto crece y supera tu alcance de decision.",
    answer: "escalate",
    success: "Bien. Un riesgo que toca dinero necesita responsable arriba, rapido.",
  },
  {
    type: "Dashboard",
    title: "Direccion pide el estado del proyecto cada manana por chat",
    description: "La misma pregunta, todos los dias, en tiempo real.",
    answer: "dashboard",
    success: "Exacto. Una pregunta diaria y repetible merece una vista, no otro mensaje.",
  },
  { type: "Automatización", answer: "automate",
    title: "Cada viernes exportas el mismo reporte y lo pegas en tres correos",
    title_en: "Every Friday you export the same report and paste it into three emails",
    description: "Mismo origen, mismos destinatarios, mismo formato.",
    description_en: "Same source, same recipients, same format.",
    success: "Eso. Una salida repetible debe dispararse sola.",
    success_en: "That's it. A repeatable output should fire on its own." },
  { type: "Automatización", answer: "automate",
    title: "Renombrar doscientos archivos sigue un patron fijo cada mes",
    title_en: "Renaming two hundred files follows a fixed pattern every month",
    description: "La regla nunca cambia, solo el lote.",
    description_en: "The rule never changes, only the batch.",
    success: "Bien. Reglas fijas sobre lotes son trabajo de script.",
    success_en: "Good. Fixed rules over batches are script work." },
  { type: "Automatización", answer: "automate",
    title: "El alta de un cliente repite los mismos seis pasos manuales",
    title_en: "Onboarding a client repeats the same six manual steps",
    description: "Cada alta es identica salvo los datos.",
    description_en: "Every onboarding is identical except the data.",
    success: "Correcto. Un proceso identico y repetido pide un flujo.",
    success_en: "Correct. An identical, repeated process asks for a flow." },
  { type: "Validacion", answer: "validate",
    title: "Las sumas del cierre no cuadran con el sistema contable",
    title_en: "Closing totals don't match the accounting system",
    description: "Dos fuentes dan cifras distintas para el mismo periodo.",
    description_en: "Two sources give different figures for the same period.",
    success: "Bien. Sin cuadrar fuentes, el cierre no es confiable.",
    success_en: "Good. Without reconciling sources, the close isn't trustworthy." },
  { type: "Validacion", answer: "validate",
    title: "Un import dejo fechas en dos formatos distintos",
    title_en: "An import left dates in two different formats",
    description: "Parte del archivo usa DD/MM y otra MM/DD.",
    description_en: "Part of the file uses DD/MM and another MM/DD.",
    success: "Correcto. Formatos mezclados rompen cualquier analisis.",
    success_en: "Correct. Mixed formats break any analysis." },
  { type: "Validacion", answer: "validate",
    title: "El total de unidades vendidas supera el inventario inicial",
    title_en: "Total units sold exceeds the starting inventory",
    description: "El numero es imposible: algo se conto dos veces.",
    description_en: "The number is impossible: something was counted twice.",
    success: "Bien visto. Un imposible logico es una alerta de datos.",
    success_en: "Well spotted. A logical impossibility is a data alert." },
  { type: "Escalacion", answer: "escalate",
    title: "Una caida de servicio afecta a varios clientes a la vez",
    title_en: "A service outage affects several clients at once",
    description: "El alcance supera lo que puedes resolver solo.",
    description_en: "The scope is beyond what you can fix alone.",
    success: "Correcto. Un incidente amplio necesita responsable y coordinacion.",
    success_en: "Correct. A broad incident needs an owner and coordination." },
  { type: "Escalacion", answer: "escalate",
    title: "Detectas un posible acceso no autorizado a un panel",
    title_en: "You detect a possible unauthorized access to a panel",
    description: "Hay riesgo de seguridad y no es tu decision contenerlo solo.",
    description_en: "There's a security risk and containing it isn't yours alone.",
    success: "Bien. La seguridad se escala de inmediato, no se improvisa.",
    success_en: "Good. Security escalates immediately, it isn't improvised." },
  { type: "Escalacion", answer: "escalate",
    title: "Un cambio rompio produccion y no hay rollback claro",
    title_en: "A change broke production and there's no clear rollback",
    description: "El impacto crece mientras se busca la causa.",
    description_en: "Impact grows while the cause is being found.",
    success: "Correcto. Sin rollback claro, necesitas mas manos y ownership.",
    success_en: "Correct. With no clear rollback, you need more hands and ownership." },
  { type: "Dashboard", answer: "dashboard",
    title: "Operaciones pregunta el avance de tickets varias veces al dia",
    title_en: "Ops asks for ticket progress several times a day",
    description: "La misma metrica, consultada en bucle.",
    description_en: "The same metric, queried in a loop.",
    success: "Exacto. Una metrica consultada en bucle merece estar a la vista.",
    success_en: "Exactly. A metric queried in a loop deserves to be on display." },
  { type: "Dashboard", answer: "dashboard",
    title: "Finanzas quiere ver el gasto por area en vivo",
    title_en: "Finance wants to see spend by area live",
    description: "Necesitan tendencia, no un export de fin de mes.",
    description_en: "They need a trend, not a month-end export.",
    success: "Buena ruta. Las tendencias que guian decisiones van en dashboard.",
    success_en: "Good route. Trends that drive decisions belong in a dashboard." },
  { type: "Dashboard", answer: "dashboard",
    title: "El SLA de soporte se revisa en cada standup",
    title_en: "The support SLA is reviewed in every standup",
    description: "El equipo necesita el numero sin abrir otra hoja.",
    description_en: "The team needs the number without opening another sheet.",
    success: "Correcto. Un numero recurrente de equipo va visible, no escondido.",
    success_en: "Correct. A recurring team number goes visible, not hidden." },
];
const gameEls = {
  timer: document.querySelector("#game-timer"),
  score: document.querySelector("#game-score"),
  friction: document.querySelector("#game-friction"),
  streak: document.querySelector("#game-streak"),
  type: document.querySelector("#signal-type"),
  title: document.querySelector("#signal-title"),
  description: document.querySelector("#signal-description"),
  card: document.querySelector("#signal-card"),
  meter: document.querySelector("#game-meter-fill"),
  start: document.querySelector("#game-start"),
  feedback: document.querySelector("#game-feedback"),
  buttons: document.querySelectorAll("[data-decision]"),
};

const GAME_I18N = {
  "Automatización": "Automation", "Validacion": "Validation", "Escalacion": "Escalation", "Dashboard": "Dashboard",
  "El reporte semanal se copia a mano cada lunes": "The weekly report is copied by hand every Monday",
  "La misma hoja, el mismo mensaje y los mismos destinatarios se repiten cada semana.": "Same sheet, same message, same recipients repeat every week.",
  "Bien visto. El trabajo manual recurrente pertenece a un flujo automatizado.": "Well spotted. Recurring manual work belongs in an automated flow.",
  "El CSV de asistencia no coincide con el archivo maestro": "The attendance CSV doesn't match the master file",
  "Dos fuentes no coinciden en IDs de empleados y fechas de turno.": "Two sources disagree on employee IDs and shift dates.",
  "Ruta correcta. Validar antes evita decisiones con datos rotos.": "Right call. Validating first avoids decisions on broken data.",
  "Un caso técnico falla después del diagnóstico estandar": "A technical case fails after standard diagnostics",
  "El procedimiento normal ya se completo, pero la causa sigue sin estar clara.": "The normal procedure is done, but the cause is still unclear.",
  "Correcto. Los casos complejos necesitan una escalacion controlada.": "Correct. Complex cases need a controlled escalation.",
  "El equipo pide visibilidad diaria de nivel de servicio": "The team asks for daily service-level visibility",
  "La métrica se revisa seguido y debe ser facil de escanear.": "The metric is checked often and must be easy to scan.",
  "Exacto. Las métricas recurrentes deben estar visibles, no escondidas en archivos.": "Exactly. Recurring metrics should be visible, not hidden in files.",
  "Un reporte muestra registros duplicados después de exportar": "A report shows duplicate records after export",
  "El volumen cambio, pero el responsable esperaba el mismo conteo.": "The volume changed, but the owner expected the same count.",
  "Bien. Los duplicados son una señal de calidad antes de ser problema de reporte.": "Good. Duplicates are a data-quality signal before they become a reporting problem.",
  "Supervisores envian el mismo recordatorio cada turno": "Supervisors send the same reminder every shift",
  "Horario, audiencia y mensaje son predecibles.": "Timing, audience and message are predictable.",
  "Muy bien. La comunicación repetible es candidata clara para automatizar.": "Great. Repeatable communication is a clear candidate for automation.",
  "Productividad se revisa en cada reunion operativa": "Productivity is reviewed in every operations meeting",
  "El equipo necesita ver tendencias, no abrir otra hoja estatica.": "The team needs to see trends, not open another static sheet.",
  "Buena ruta. Las tendencias que guian reuniones merecen dashboard.": "Good route. Trends that drive meetings deserve a dashboard.",
  "Un proceso manual rompe una regla de cumplimiento": "A manual process breaks a compliance rule",
  "El riesgo afecta calidad de servicio y necesita responsable claro.": "The risk affects service quality and needs a clear owner.",
  "Correcto. Un riesgo operativo necesita ownership antes de optimizarse.": "Correct. An operational risk needs ownership before optimization.",
  "Cada cierre de mes consolidas seis hojas a mano": "Every month-end you consolidate six sheets by hand",
  "Mismas columnas, mismo formato, distinto periodo.": "Same columns, same format, different period.",
  "Eso. Una consolidación repetible es trabajo para un flujo, no para tus manos.": "That's it. A repeatable consolidation is work for a flow, not your hands.",
  "Dos tableros reportan cifras distintas para el mismo KPI": "Two dashboards report different figures for the same KPI",
  "Nadie sabe cual es la fuente de verdad.": "Nobody knows which is the source of truth.",
  "Correcto. Sin fuente validada, cada tablero cuenta una historia distinta.": "Correct. With no validated source, each dashboard tells a different story.",
  "Un cliente reporta una falla que afecta facturacion": "A client reports a failure that affects billing",
  "El impacto crece y supera tu alcance de decision.": "The impact grows and exceeds your decision scope.",
  "Bien. Un riesgo que toca dinero necesita responsable arriba, rapido.": "Good. A risk that touches money needs an owner up the chain, fast.",
  "Direccion pide el estado del proyecto cada manana por chat": "Leadership asks for project status every morning by chat",
  "La misma pregunta, todos los dias, en tiempo real.": "The same question, every day, in real time.",
  "Exacto. Una pregunta diaria y repetible merece una vista, no otro mensaje.": "Exactly. A daily, repeatable question deserves a view, not another message.",
  "Corriendo": "Running",
  "Manda la señal a la capa correcta.": "Send the signal to the right layer.",
  "Jugar de nuevo": "Play again",
  "Señal": "Signal",
  "Run terminado. La operación quedó más clara que al inicio.": "Run over. The operation ended clearer than it started.",
  "Run terminado. La friccion todavia pesa en el flujo.": "Run over. Friction still weighs on the flow.",
  "Despejaste todas las señales sin un solo error. Operación impecable.": "You cleared every signal with zero errors. Flawless operation.",
  "Despejaste todas las señales, pero la fricción dejó marca. Hay que afinar el criterio.": "You cleared every signal, but friction left a mark. Sharpen the judgment.",
  "Se acabó el tiempo. Quedaron señales en la cola.": "Time's up. Signals were left in the queue.",
};
function GLANG() { return document.documentElement.lang === "en" ? "en" : "es"; }
function tr(t) { return GLANG() === "en" ? (GAME_I18N[t] || t) : t; }
// Campo bilingüe de una señal: usa <key>_en si existe (tarjetas nuevas), si no cae al diccionario.
function trField(obj, key) {
  if (GLANG() === "en") return obj[key + "_en"] || GAME_I18N[obj[key]] || obj[key];
  return obj[key];
}

let _timeDeltaEl = null;
function flashTimeDelta(amount) {
  if (!gameEls.timer) return;
  if (!_timeDeltaEl) {
    _timeDeltaEl = document.createElement("span");
    _timeDeltaEl.className = "time-delta";
    _timeDeltaEl.style.cssText = "margin-left:.4em;font-weight:800;opacity:0;transition:opacity .25s ease;";
    gameEls.timer.insertAdjacentElement("afterend", _timeDeltaEl);
  }
  _timeDeltaEl.textContent = (amount > 0 ? "+" : "") + amount + "s";
  _timeDeltaEl.style.color = amount > 0 ? "#1aa179" : "#e0796b";  // verde acierto / rojo error
  _timeDeltaEl.style.opacity = "1";
  clearTimeout(_timeDeltaEl._t);
  _timeDeltaEl._t = setTimeout(() => { _timeDeltaEl.style.opacity = "0"; }, 750);
}

function renderGame() {
  if (!gameEls.timer) return;
  gameEls.timer.textContent = `${game.timeLeft}s`;
  gameEls.score.textContent = game.score;
  gameEls.friction.textContent = game.friction;
  gameEls.streak.textContent = game.streak;
  // El #signal-type ya NO muestra la categoría (delataba la respuesta): muestra progreso.
  if (gameEls.type && game.total) {
    gameEls.type.textContent = `${tr("Señal")} ${Math.min(game.solved + 1, game.total)}/${game.total}`;
  }
  if (gameEls.meter) {
    gameEls.meter.style.width = `${Math.max((game.timeLeft / game.duration) * 100, 0)}%`;
  }
}

function bumpScore(element) {
  const card = element?.closest("article");
  if (!card) return;
  card.classList.remove("is-bumping");
  window.requestAnimationFrame(() => card.classList.add("is-bumping"));
}

function setDecisionEnabled(enabled) {
  gameEls.buttons.forEach((button) => {
    button.disabled = !enabled;
  });
}

function nextSignal() {
  if (!game.queue.length) {     // se acabaron las tarjetas → fin por completar
    finishGame("cleared");
    return;
  }
  game.current = game.queue.shift();
  gameEls.title.textContent = trField(game.current, "title");
  gameEls.description.textContent = trField(game.current, "description");
  gameEls.card.classList.remove("is-correct", "is-wrong");
  gameEls.card.classList.remove("is-entering");
  window.requestAnimationFrame(() => gameEls.card.classList.add("is-entering"));
  renderGame();
}

function finishGame(reason) {
  clearInterval(game.timer);
  game.active = false;
  game.current = null;
  setDecisionEnabled(false);
  gameEls.start.textContent = tr("Jugar de nuevo");
  if (reason === "cleared") {
    gameEls.feedback.textContent = game.friction === 0
      ? tr("Despejaste todas las señales sin un solo error. Operación impecable.")
      : tr("Despejaste todas las señales, pero la fricción dejó marca. Hay que afinar el criterio.");
  } else if (reason === "timeout") {
    gameEls.feedback.textContent = tr("Se acabó el tiempo. Quedaron señales en la cola.");
  } else {
    gameEls.feedback.textContent =
      game.score >= game.friction
        ? tr("Run terminado. La operación quedó más clara que al inicio.")
        : tr("Run terminado. La friccion todavia pesa en el flujo.");
  }
}

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function startGame() {
  clearInterval(game.timer);
  game.timeLeft = game.duration;
  game.score = 0;
  game.friction = 0;
  game.streak = 0;
  game.solved = 0;
  game.queue = shuffle(signals);   // cada run baraja todas las señales, sin repetir
  game.total = game.queue.length;
  game.active = true;
  gameEls.start.textContent = tr("Corriendo");
  gameEls.feedback.textContent = tr("Manda la señal a la capa correcta.");
  setDecisionEnabled(true);
  nextSignal();
  renderGame();

  game.timer = setInterval(() => {
    game.timeLeft -= 1;
    renderGame();
    if (game.timeLeft <= 0) finishGame("timeout");
  }, 1000);
}

function handleDecision(decision) {
  if (!game.active || !game.current) return;
  const correct = decision === game.current.answer;

  if (correct) {
    game.streak += 1;
    game.score += 10 + Math.min(game.streak * 2, 10);
    game.timeLeft += 2;                 // acierto: +2 segundos
    flashTimeDelta(2);
    gameEls.card.classList.add("is-correct");
    gameEls.feedback.textContent = trField(game.current, "success");
    bumpScore(gameEls.score);
    bumpScore(gameEls.streak);
  } else {
    game.streak = 0;
    game.friction += 8;
    game.timeLeft = Math.max(game.timeLeft - 2, 0);   // error: -2 segundos
    flashTimeDelta(-2);
    gameEls.card.classList.add("is-wrong");
    gameEls.feedback.textContent = GLANG() === "en" ? `Close. That signal belonged to ${game.current.answer}.` : `Casi. Esta señal pertenecía a ${game.current.answer}.`;
    bumpScore(gameEls.friction);
  }

  game.solved += 1;
  renderGame();
  if (game.timeLeft <= 0) { finishGame("timeout"); return; }   // el -2 pudo agotar el tiempo
  window.setTimeout(() => {
    if (game.active) nextSignal();
  }, 450);
}

if (gameEls.start) {
  setDecisionEnabled(false);
  renderGame();
  gameEls.start.addEventListener("click", startGame);
  gameEls.buttons.forEach((button) => {
    button.addEventListener("click", () => handleDecision(button.dataset.decision));
  });
}

