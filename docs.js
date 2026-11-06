/* Подстановка реквизитов из config.js в privacy.html / consent.html.
   Пустое поле остаётся жёлтой плашкой «заполните …» — сразу видно, чего не хватает.
   Блоки с data-if="metrikaId|vkPixelId|postbackUrl|bot" видны, только если поле задано. */
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
  Array.prototype.forEach.call(document.querySelectorAll("[data-if]"), function (el) {
    el.hidden = !CFG[el.getAttribute("data-if")];
  });
})();
