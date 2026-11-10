(function () {
  "use strict";

  var CFG = window.SITE_CONFIG || {};
  document.documentElement.classList.add("js");

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fmt = function (n) { return Math.round(n).toLocaleString("ru-RU"); };
  var clean = function (u) { return String(u || "").replace(/^@/, "").replace(/^https?:\/\/t\.me\//, "").trim(); };

  /* ---------- storage (может быть недоступно) ---------- */
  function store(key, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem(key) || "null");
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
  }

  /* ---------- Метки трафика: UTM / click_id ---------- */
  var TRACK_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "click_id", "sub1", "sub2"];
  var params = new URLSearchParams(location.search);
  var fresh = {};
  TRACK_KEYS.forEach(function (k) { if (params.get(k)) fresh[k] = params.get(k); });
  ["clickid", "subid", "yclid", "gclid", "vkclid", "fbclid"].forEach(function (k) {
    if (!fresh.click_id && params.get(k)) fresh.click_id = params.get(k);
  });
  var CONSENT = window.PSConsent || { allowed: function () { return false; }, onGrant: function () {} };
  // Метки запоминаем между визитами только с согласия на cookie (consent.js)
  var track = Object.keys(fresh).length ? fresh : (CONSENT.allowed() && store("ps_track")) || {};
  function saveTrack() { if (Object.keys(fresh).length) store("ps_track", fresh); }
  if (CONSENT.allowed()) saveTrack(); else CONSENT.onGrant(saveTrack);

  /* ---------- Куда ведём в Telegram ----------
     1) бот с start-параметром (передаёт click_id/метки в бота)
     2) отдельная инвайт-ссылка канала под кампанию/источник
     3) обычная ссылка на канал */
  function startPayload() {
    var raw = track.click_id || [track.utm_source, track.utm_campaign, track.utm_content].filter(Boolean).join("_") || "direct";
    return raw.replace(/[^A-Za-z0-9_-]/g, "_").slice(0, 64);
  }
  function tgUrl() {
    var bot = clean(CFG.bot);
    if (bot) return "https://t.me/" + bot + "?start=" + encodeURIComponent(startPayload());
    var inv = CFG.inviteLinks || {};
    var byKey = inv[track.utm_campaign] || inv[track.utm_source] || inv["default"];
    if (byKey) return byKey;
    return "https://t.me/" + (clean(CFG.telegram) || "prostrahagent");
  }
  var TG = tgUrl();
  var MANAGER = clean(CFG.manager);

  $$(".js-tg").forEach(function (a) { a.href = TG; a.removeAttribute("target"); });
  $$(".js-tg-handle").forEach(function (a) { if (CFG.telegram) a.textContent = "@" + clean(CFG.telegram); });
  $$(".js-manager").forEach(function (a) {
    if (MANAGER) { a.href = "https://t.me/" + MANAGER; a.hidden = false; }
    else if (a.classList.contains("js-manager-always")) { a.href = TG; }
  });

  /* ---------- Реквизиты ---------- */
  var owner = CFG.owner || {};
  if (owner.name || owner.inn) {
    $$(".js-owner").forEach(function (el) {
      el.textContent = [owner.name, owner.inn && "ИНН " + owner.inn].filter(Boolean).join(", ") + ".";
      el.hidden = false;
    });
  }

  /* ---------- Аналитика: счётчики грузит consent.js после согласия ---------- */
  function goal(name) {
    if (!CONSENT.allowed()) return;
    try {
      if (CFG.metrikaId && window.ym) window.ym(+CFG.metrikaId, "reachGoal", name, track);
      if (CFG.vkPixelId && window._tmr) window._tmr.push({ type: "reachGoal", id: String(CFG.vkPixelId), goal: name });
    } catch (e) { /* noop */ }
  }
  function postback() {
    if (!CFG.postbackUrl || !track.click_id || !CONSENT.allowed()) return;
    try { if (sessionStorage.getItem("ps_pb")) return; sessionStorage.setItem("ps_pb", "1"); } catch (e) { /* noop */ }
    var url = CFG.postbackUrl.replace("{click_id}", encodeURIComponent(track.click_id));
    if (navigator.sendBeacon) navigator.sendBeacon(url); else new Image().src = url;
  }

  /* ---------- Клик в Telegram: цель → постбэк → переход ---------- */
  function goTelegram(href, goalName) {
    goal("tg_click");
    if (goalName) goal(goalName);
    postback();
    if (window.console) console.info("[tg] переход:", href, track);
    setTimeout(function () { location.href = href; }, 180); // даём метрике отправить цель
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest(".js-tg, .js-manager");
    if (a) {
      if (e.metaKey || e.ctrlKey || e.shiftKey) { goal("tg_click"); postback(); return; } // открытие в новой вкладке
      e.preventDefault();
      goTelegram(a.href, a.getAttribute("data-goal"));
      return;
    }
    if (e.target.closest(".js-tg-box")) { goTelegram(TG, "tg_mockup"); return; }
    var g = e.target.closest("[data-goal]");
    if (g) goal(g.getAttribute("data-goal"));
  });

  /* ---------- header ---------- */
  var header = $(".header");
  var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- калькулятор: полисы × вознаграждение ---------- */
  var RATES = Object.assign({ osago: 6000, kasko: 20000, ipoteka: 30000 }, CFG.rewards || {});
  Object.keys(RATES).forEach(function (k) {
    $$('[data-rate="' + k + '"]').forEach(function (el) { el.textContent = fmt(RATES[k]); });
  });
  var sliders = ["osago", "kasko", "ipoteka"].map(function (id) { return $("#" + id); });
  function fill(el) { el.style.setProperty("--fill", (el.value - el.min) / (el.max - el.min) * 100 + "%"); }
  function calc() {
    var total = 0;
    sliders.forEach(function (el) {
      $("#" + el.id + "Val").textContent = el.value;
      total += +el.value * RATES[el.id];
      fill(el);
    });
    $("#resultVal").textContent = fmt(total) + " ₽";
  }
  sliders.forEach(function (el) { el.addEventListener("input", calc); });
  calc();

  /* ---------- счётчик в макете кабинета ---------- */
  $$(".js-count").forEach(function (el) {
    var to = +el.dataset.to, start = null, dur = 1400;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    function step(t) {
      if (!start) start = t;
      var k = Math.min((t - start) / dur, 1);
      el.textContent = fmt(to * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });

  /* ---------- появление блоков ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en, i) {
        if (en.isIntersecting) {
          en.target.style.transitionDelay = (i % 6) * 60 + "ms";
          en.target.classList.add("in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- липкая кнопка на мобильном ---------- */
  // не показываем её поверх виджета оформления полиса
  var sticky = $("#stickyCta"), hero = $(".hero"), joinSec = $("#join"), policySec = $("#policy");
  if ("IntersectionObserver" in window && sticky) {
    var heroVisible = true, joinVisible = false, policyVisible = false;
    var upd = function () { sticky.classList.toggle("show", !heroVisible && !joinVisible && !policyVisible); };
    new IntersectionObserver(function (e) { heroVisible = e[0].isIntersecting; upd(); }).observe(hero);
    new IntersectionObserver(function (e) { joinVisible = e[0].isIntersecting; upd(); }, { threshold: 0.05 }).observe(joinSec);
    if (policySec) new IntersectionObserver(function (e) { policyVisible = e[0].isIntersecting; upd(); }).observe(policySec);
  }

  /* ---------- Виджет Инссмарт: вкладки продуктов ----------
     Загрузчик Инссмарт вставляет iframe на место своего <script>,
     поэтому при смене вкладки пересоздаём скрипт с другим data-product.
     Вкладка с data-panel (КАСКО) вместо виджета показывает блок «через менеджера». */
  var wBox = $("#inssmartWidget");
  if (wBox) {
    var first = $("script", wBox);
    var tpl = first ? Array.prototype.map.call(first.attributes, function (a) { return [a.name, a.value]; }) : null;
    var current = first ? first.getAttribute("data-product") : "";
    $$(".ptab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        if (tab.classList.contains("is-active") || !tpl) return;
        $$(".ptab").forEach(function (t) {
          var on = t === tab;
          t.classList.toggle("is-active", on);
          t.setAttribute("aria-selected", on ? "true" : "false");
        });
        try { tab.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "smooth" }); } catch (e) { /* noop */ }
        var panelId = tab.getAttribute("data-panel");
        $$(".product-panel").forEach(function (p) { p.hidden = p.id !== panelId; });
        wBox.hidden = !!panelId;
        if (panelId) return;
        var product = tab.getAttribute("data-product");
        if (product === current) return;
        current = product;
        var s = document.createElement("script");
        tpl.forEach(function (a) { s.setAttribute(a[0], a[1]); });
        s.setAttribute("data-product", product);
        wBox.innerHTML = "";
        wBox.appendChild(s);
      });
    });
  }

  $("#year").textContent = new Date().getFullYear();
})();
