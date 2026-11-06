/* Подстановка реквизитов из config.js в privacy.html / consent.html.
   Пустое поле остаётся жёлтой плашкой «заполните …» — сразу видно, чего не хватает.
   Блоки с data-if="metrikaId|vkPixelId|postbackUrl|bot|tracking" видны, только если поле задано;
   data-if="!tracking" — наоборот, только когда счётчиков нет. */
(function () {
  "use strict";
  var CFG = window.SITE_CONFIG || {};
  var o = CFG.owner || {};
  var fields = {
    name: o.name,
    inn: o.inn,
    email: o.email,
    telegram: CFG.telegram && "@" + String(CFG.telegram).replace(/^@/, "")
  };
  Array.prototype.forEach.call(document.querySelectorAll("[data-op]"), function (el) {
    var v = fields[el.getAttribute("data-op")];
    if (v) {
      el.classList.remove("doc__fill");
      if (el.getAttribute("data-op") === "email") el.innerHTML = '<a class="link" href="mailto:' + v + '">' + v + "</a>";
      else el.textContent = v;
    }
  });
  // tracking — подключён хотя бы один счётчик (тогда же показывается баннер cookie)
  var flags = Object.assign({}, CFG, { tracking: !!(CFG.metrikaId || CFG.vkPixelId || CFG.postbackUrl) });
  Array.prototype.forEach.call(document.querySelectorAll("[data-if]"), function (el) {
    var key = el.getAttribute("data-if"), neg = key.charAt(0) === "!";
    var on = !!flags[neg ? key.slice(1) : key];
    el.hidden = neg ? on : !on;
  });
})();
