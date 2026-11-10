/**
 * Уведомления в Telegram о шагах клиента в виджете Инссмарт (ПроСтрахАгент).
 *
 * Как работает: в настройках виджета Инссмарт (Аналитика → Postback) указан адрес
 * этого веб-приложения. На выбранных событиях Инссмарт вызывает его, а скрипт
 * отправляет короткое сообщение в Telegram через вашего бота.
 *
 * В Telegram уходит только тип события, номер заказа, вознаграждение и время —
 * без ФИО, телефонов и документов. Контакты клиента смотрите в кабинете Инссмарт.
 *
 * Свойства скрипта (Настройки проекта → Свойства скрипта):
 *   BOT_TOKEN — токен бота от @BotFather (вписываете сами, никому не пересылайте)
 *   CHAT_IDS  — кому слать, через запятую (узнать: функция findChats)
 */

var LABELS = {
  draft: '📝 Клиент начал оформление',
  has_offers: '📊 Клиент посмотрел предложения',
  offers: '📊 Клиент посмотрел предложения',
  select_offer: '👉 Клиент выбрал предложение',
  payment_link: '💳 Клиент получил ссылку на оплату',
  payment_success: '✅ Полис оплачен',
  payment_cancel: '⚠️ Оплата не прошла или отменена — можно дожать',
  create_application: '📨 Клиент оставил заявку'
};

function doGet(e) {
  return handle_((e && e.parameter) || {});
}

function doPost(e) {
  var p = {};
  var src = (e && e.parameter) || {};
  for (var k in src) p[k] = src[k];
  try {
    var body = JSON.parse(e.postData.contents);
    for (var b in body) if (!(b in p)) p[b] = body[b];
  } catch (err) { /* тело не JSON — хватит параметров из URL */ }
  return handle_(p);
}

function handle_(p) {
  var ev = String(p.event || p.eventName || '').toLowerCase().trim();
  if (!ev) return out_('no event');
  var lines = [LABELS[ev] || ('Событие виджета: ' + ev)];
  var order = p.orderId || p.order_id || p.contractId;
  if (order) lines.push('Заказ: ' + order);
  if (p.company) lines.push('Страховая: ' + p.company);
  if (p.price) lines.push('Стоимость полиса: ' + p.price + ' ₽');
  if (p.profit) lines.push('Вознаграждение: ' + p.profit + ' ₽');
  if (p.dateTime) lines.push('Время: ' + p.dateTime);
  lines.push('Контакты и новая ссылка на оплату — в кабинете: https://agents.inssmart.ru/contracts');
  send_(lines.join('\n'));
  return out_('ok');
}

function send_(text) {
  var props = PropertiesService.getScriptProperties();
  var token = props.getProperty('BOT_TOKEN');
  var chats = String(props.getProperty('CHAT_IDS') || '').split(',').map(function (s) { return s.trim(); }).filter(String);
  if (!token || !chats.length) return;
  chats.forEach(function (chatId) {
    UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
      method: 'post',
      payload: { chat_id: chatId, text: text, disable_web_page_preview: 'true' },
      muteHttpExceptions: true
    });
  });
}

function out_(s) {
  return ContentService.createTextOutput(s);
}

/** Запустите вручную после того, как нажали Start у бота: в журнале появятся chat_id. */
function findChats() {
  var token = PropertiesService.getScriptProperties().getProperty('BOT_TOKEN');
  if (!token) { Logger.log('Сначала добавьте свойство BOT_TOKEN'); return; }
  var me = JSON.parse(UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/getMe', { muteHttpExceptions: true }).getContentText());
  if (!me.ok) { Logger.log('Telegram не принял токен: ' + me.description); return; }
  Logger.log('Токен от бота @' + me.result.username);
  var res = JSON.parse(UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/getUpdates', { muteHttpExceptions: true }).getContentText());
  var seen = {};
  (res.result || []).forEach(function (u) {
    var m = u.message || u.my_chat_member || u.channel_post;
    if (m && m.chat && !seen[m.chat.id]) {
      seen[m.chat.id] = true;
      Logger.log(m.chat.id + ' — ' + (m.chat.username ? '@' + m.chat.username : (m.chat.title || m.chat.first_name || '')));
    }
  });
  if (!Object.keys(seen).length) Logger.log('Сообщений нет: нажмите Start у бота и запустите ещё раз');
}

/** Пробное уведомление. */
function testAlert() {
  handle_({ event: 'payment_cancel', orderId: 'TEST-123', profit: '1947', dateTime: new Date().toISOString() });
}
