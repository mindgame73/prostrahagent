/* ==========================================================
   Согласие на cookie и аналитику (152-ФЗ)

   Яндекс.Метрика, пиксель VK и постбэк в трекер включаются
   только после «Принять». До этого на устройство посетителя
   ничего рекламного не пишется и никуда не отправляется.
   Баннер показывается, только если в config.js задан хотя бы
   один из metrikaId / vkPixelId / postbackUrl.

   Наружу: window.PSConsent = { allowed(), onGrant(fn), open() }
   ========================================================== */
(function () {
  "use strict";

  var CFG = window.SITE_CONFIG || {};
  var KEY = "ps_consent";
  var NEEDED = !!(CFG.metrikaId || CFG.vkPixelId || CFG.postbackUrl);
  var listeners = [];
  var started = false;

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { return null; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, JSON.stringify({ v: v, at: new Date().toISOString() })); } catch (e) { /* noop */ }
  }
  var state = read();

  function allowed() { return !!(state && state.v === "all"); }

  /* ---------- Счётчики ---------- */
  function startAnalytics() {
    if (started) return;
    started = true;
    if (CFG.metrikaId) {
      (function (m, e, t, r, i, k, a) {
        m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
        m[i].l = 1 * new Date();
        k = e.createElement(t); a = e.getElementsByTagName(t)[0];
        k.async = 1; k.src = r; a.parentNode.insertBefore(k, a);
      })(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
      window.ym(+CFG.metrikaId, "init", { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: true });
    }
    if (CFG.vkPixelId) {
      var _tmr = window._tmr || (window._tmr = []);
      _tmr.push({ id: String(CFG.vkPixelId), type: "pageView", start: Date.now() });
      var s = document.createElement("script");
      s.async = true; s.src = "https://top-fwz1.mail.ru/js/code.js";
      document.head.appendChild(s);
    }
    listeners.forEach(function (fn) { try { fn(); } catch (e) { /* noop */ } });
  }

  // Стираем метки рекламы и то, что успели записать счётчики
  function purge() {
    try {
      Object.keys(localStorage).forEach(function (k) {
        if (k === "ps_track" || /^(_ym|_tmr|tmr_)/.test(k)) localStorage.removeItem(k);
      });
      sessionStorage.removeItem("ps_pb");
    } catch (e) { /* noop */ }
    document.cookie.split(";").forEach(function (c) {
      var name = c.split("=")[0].trim();
      if (/^(_ym|_tmr|tmr_)/.test(name)) {
        ["", "; domain=" + location.hostname, "; domain=." + location.hostname.replace(/^www\./, "")].forEach(function (d) {
          document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + d;
        });
      }
    });
  }

  /* ---------- Баннер ---------- */
  var banner;
  function close() { if (banner) banner.hidden = true; }
  function decide(v) {
    state = { v: v };
    write(v);
    close();
    if (v === "all") startAnalytics();
    else {
      purge();
      // Загруженный счётчик выгрузить нельзя — перезагружаем страницу без него
      if (started) location.reload();
    }
  }
  function build() {
    banner = document.createElement("div");
    banner.className = "consent";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-live", "polite");
    banner.setAttribute("aria-label", "Согласие на cookie");
    var tools = [CFG.metrikaId && "Яндекс.Метрика (с Вебвизором)", CFG.vkPixelId && "пиксель VK Рекламы", CFG.postbackUrl && "трекер рекламы"].filter(Boolean).join(", ");
    banner.innerHTML =
      '<div class="consent__inner">' +
        '<p class="consent__text">Мы хотим использовать cookie и сервисы аналитики (' + tools + '), ' +
        'чтобы понимать, откуда приходят посетители и какая реклама работает. Без вашего согласия они не включатся. ' +
        'Подробнее — в <a class="link" href="privacy.html">политике</a> и ' +
        '<a class="link" href="consent.html">тексте согласия</a>.</p>' +
        '<div class="consent__actions">' +
          '<button type="button" class="btn btn--sm btn--ghost js-consent-no">Отклонить</button>' +
          '<button type="button" class="btn btn--sm btn--primary js-consent-yes">Принять</button>' +
        '</div>' +
      '</div>';
    banner.querySelector(".js-consent-yes").addEventListener("click", function () { decide("all"); });
    banner.querySelector(".js-consent-no").addEventListener("click", function () { decide("necessary"); });
    document.body.appendChild(banner);
  }
  function open() {
    if (!NEEDED) return;
    if (!banner) build();
    banner.hidden = false;
  }

  window.PSConsent = {
    allowed: allowed,
    onGrant: function (fn) { if (started) fn(); else listeners.push(fn); },
    open: open
  };

  function init() {
    // Ссылка «Настройки cookie» в подвале — только если есть что настраивать
    Array.prototype.forEach.call(document.querySelectorAll(".js-cookie-settings"), function (el) {
      if (!NEEDED) { el.hidden = true; return; }
      el.hidden = false;
      el.addEventListener("click", function (e) { e.preventDefault(); open(); });
    });
    // Ссылка на текст согласия — тоже только при подключённых счётчиках
    Array.prototype.forEach.call(document.querySelectorAll(".js-consent-doc"), function (el) { el.hidden = !NEEDED; });
    if (!NEEDED) return;
    if (allowed()) startAnalytics();
    else if (!state) open();
    else purge(); // отказ: подчищаем то, что счётчик мог дописать при уходе со страницы
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
