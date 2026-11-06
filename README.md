# ПроСтрахование — прелендинг для перелива трафика в Telegram

Статичный сайт без сборки: `index.html`, `styles.css`, `script.js`, `config.js`, `favicon.svg`.
Все кнопки ведут в Telegram-канал. Формы на сайте нет: заявку человек оставляет уже в канале.

## Настройка — `config.js`

| Поле | Что это |
|---|---|
| `telegram` | Ник канала без `@`. Все кнопки ведут сюда |
| `manager` | Ваш ник для связи — появится кнопка «Написать нам» |
| `inssmartRef` | Ваша реферальная ссылка Инссмарт — появятся кнопки «Зарегистрироваться на Инссмарт» |
| `owner` | ФИО и ИНН для подвала |
| `rewards` | Вознаграждение за полис для калькулятора (ОСАГО / КАСКО / ипотека) — сверьте с кабинетом |
| `inviteLinks` | Отдельные инвайт-ссылки канала под кампании/источники (ключ = `utm_campaign` или `utm_source`, плюс `default`). В статистике ссылок в Telegram видно, сколько подписчиков дал каждый источник |
| `bot` | Ник бота. Если задан, кнопки ведут в `t.me/<bot>?start=<click_id>`: бот получает click_id и может слать постбэк при подписке |
| `postbackUrl` | Постбэк в трекер при клике «в Telegram», `{click_id}` подставится |
| `metrikaId`, `vkPixelId` | Яндекс.Метрика и пиксель VK Рекламы |

Приоритет: `bot` → `inviteLinks` → `telegram`.

## Метки

Берутся из URL: `utm_*`, `sub1`, `sub2`, `click_id` (также `clickid`, `subid`, `yclid`, `gclid`, `vkclid`, `fbclid`) и запоминаются в браузере.

Цели: `tg_click` — любой переход в TG; по кнопкам — `tg_header`, `tg_hero`, `tg_calc`, `tg_geo`, `tg_main`, `tg_sticky`, `tg_footer`, `tg_faq`, `tg_mockup`, `tg_manager`.

## Локальный просмотр

```bash
python3 -m http.server 8765
```

## Деплой на GitHub Pages

Залить файлы в репозиторий → Settings → Pages → Deploy from branch `main` / root.
