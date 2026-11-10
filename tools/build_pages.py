import sys, os, re, json, html
root = sys.argv[1]
def rd(n): return open(os.path.join(root, n), encoding='utf-8').read()
idx = rd('index.html')

def between(s, a, b):
    i = s.index(a); j = s.index(b, i)
    return s[i:j]

# ---- pieces taken from the main page
header = between(idx, '<header class="header" id="top">', '</header>') + '</header>'
footer = between(idx, '<footer class="footer">', '</footer>') + '</footer>'
assist = between(idx, '    <div class="assist">', '    <script>\n      /* Виджет сам прокручивает')
scrollfix = between(idx, '    <script>\n      /* Виджет сам прокручивает', '    <div class="widget-box" id="policyWidget">')
widget_tpl = between(idx, '    <div class="widget-box" id="policyWidget">', '    <div class="product-panel" id="kaskoPanel"')
fonts = re.findall(r'  <link rel="preload"[^\n]*\n', idx)
css_ver = re.search(r'styles\.css\?v=(\d+)', idx).group(1)
js_ver = re.search(r'script\.js\?v=(\d+)', idx).group(1)
cfg_ver = re.search(r'config\.js\?v=(\d+)', idx).group(1)

# header: absolute links, page-specific nav
header = header.replace('href="#top"', 'href="/"')
header = re.sub(r'<nav class="nav".*?</nav>', '''<nav class="nav" aria-label="Основная навигация">
      <a href="/#policy">Все виды страхования</a>
      <a href="#faq">Вопросы</a>
      <a href="/#why">Стать агентом</a>
    </nav>''', header, flags=re.S)
footer = footer.replace('href="#top"', 'href="/"').replace('href="privacy.html"', 'href="/privacy.html"').replace('href="consent.html"', 'href="/consent.html"')

TG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.5 4.3 18.4 19c-.2 1-.8 1.3-1.7.8l-4.6-3.4-2.2 2.1c-.3.3-.5.5-1 .5l.3-4.7 8.6-7.8c.4-.3-.1-.5-.6-.2L6.6 13 2 11.6c-1-.3-1-1 .2-1.5L20.1 3.2c.8-.3 1.6.2 1.4 1.1Z" fill="currentColor"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

ALL = [
    ('ОСАГО', '/osago/'), ('Страхование ипотеки', '/ipoteka/'), ('Путешествия', '/travel/'),
    ('Мини-КАСКО', '/#mini-kasko'), ('Квартира и дом', '/#kvartira'), ('Антиклещ', '/#antiklesh'),
    ('КАСКО', '/#kasko'), ('Титул', '/#titul'),
]

PAGES = [
  dict(slug='osago', product='/eosago', crumb='ОСАГО',
    title='ОСАГО онлайн — рассчитать и оформить электронный полис | ПроСтрахАгент',
    desc='Рассчитайте ОСАГО онлайн и сравните цены страховых компаний. Электронный полис приходит на e-mail и действует так же, как бумажный. Не получается — поможет менеджер.',
    h1='ОСАГО онлайн: рассчитайте и оформите полис',
    lead='Сравните цены страховых компаний на ОСАГО и оформите электронный полис онлайн. Он придёт на почту и действует так же, как бумажный.',
    chips=['Расчёт бесплатный', 'Цены нескольких страховых сразу', 'Электронный полис на e-mail'],
    facts_title='Что понадобится',
    facts=[
      ('Паспорт', 'Собственника машины — и страхователя, если это другой человек.'),
      ('СТС или ПТС', 'Данные машины: марка, модель, мощность, VIN или номер кузова.'),
      ('Права водителей', 'Всех, кто будет за рулём. Или выберите полис без ограничений.'),
      ('Госномер', 'С него начинается расчёт. Можно рассчитать и без номера.'),
    ],
    note='Диагностическая карта для личного легкового автомобиля при покупке ОСАГО не нужна.',
    faq=[
      ('Почему у страховых разные цены?', 'Центробанк задаёт тарифный коридор, а каждая страховая выбирает в нём свою базовую ставку. Итоговая цена ещё зависит от региона, мощности машины, возраста и стажа водителей и скидки за безаварийную езду (КБМ). Поэтому одна и та же машина у разных страховых стоит по-разному.'),
      ('Сохранится ли скидка, если сменить страховую?', 'Да. Скидка за безаварийную езду (КБМ) хранится в общей базе и привязана к водителю, а не к страховой компании.'),
      ('Нужно ли распечатывать электронный полис?', 'Нет. Сотрудник ГИБДД проверяет полис по базе. Файл на телефоне или распечатку можно держать при себе на всякий случай.'),
      ('С ограничением или без ограничений по водителям?', 'Полис с ограниченным списком дешевле, но за руль могут садиться только вписанные в него водители. Без ограничений машину может водить любой человек с правами, но такой полис дороже.'),
      ('Что делать при ДТП?', 'Если пострадали только машины и у обоих водителей есть ОСАГО, обращайтесь в свою страховую — она урегулирует убыток. Если нет пострадавших и разногласий, аварию можно оформить по европротоколу без ГИБДД, в том числе онлайн через Госуслуги.'),
    ]),
  dict(slug='ipoteka', product='/mortgage', crumb='Страхование ипотеки',
    title='Страхование ипотеки онлайн — калькулятор полиса для банка | ПроСтрахАгент',
    desc='Рассчитайте страхование ипотеки онлайн: имущество, жизнь и титул. Сравните цены страховых для вашего банка — часто это дешевле, чем продлевать полис в банке.',
    h1='Страхование ипотеки онлайн: полис для банка',
    lead='Рассчитайте полис для ипотеки и сравните цены страховых, подходящих для вашего банка. Часто это дешевле, чем продлевать страховку в самом банке.',
    chips=['Имущество, жизнь и титул', 'С учётом вашего банка', 'Полис на e-mail'],
    facts_title='Что важно знать',
    facts=[
      ('Квартиру страховать обязательно', 'Если жильё в залоге у банка, по закону его нужно застраховать от гибели и повреждения.'),
      ('Жизнь и титул — добровольно', 'Но без них банк может повысить ставку по кредиту. Условия — в вашем кредитном договоре.'),
      ('Не обязательно покупать в банке', 'Подойдёт полис любой страховой, которую принимает ваш банк.'),
      ('Полис продлевается каждый год', 'При продлении можно выбрать другую страховую, если она дешевле.'),
    ],
    note='Для расчёта понадобятся банк и остаток долга, дата кредитного договора, ваша дата рождения и данные жилья: тип, год постройки, регион.',
    faq=[
      ('Почему в калькуляторе может быть дешевле, чем в банке?', 'Банк обычно предлагает страховку своих партнёров, и её цена не всегда самая низкая. Калькулятор показывает предложения нескольких страховых — можно сравнить и выбрать.'),
      ('Можно сменить страховую, если полис уже куплен в банке?', 'Обычно да, при очередном продлении: оформите новый полис в подходящей страховой и отправьте его в банк до окончания старого. Точный порядок — в вашем кредитном договоре.'),
      ('Что отправить в банк?', 'Полис и документ об оплате. Как именно отправлять — через личный кабинет банка или в отделении — зависит от банка.'),
      ('Обязательно ли страховать жизнь?', 'По закону нет, это добровольно. Но банк вправе повысить ставку, если вы откажетесь, — посмотрите условия в кредитном договоре.'),
    ]),
  dict(slug='travel', product='/travel', crumb='Путешествия',
    title='Страховка для путешествий за границу онлайн — для визы и поездки | ПроСтрахАгент',
    desc='Оформите медицинскую страховку для поездки за границу онлайн: сравните цены страховых, полис для визы приходит на e-mail сразу после оплаты.',
    h1='Страховка для путешествий за границу',
    lead='Медицинская страховка для поездки: сравните цены страховых и оформите полис онлайн — он придёт на почту сразу после оплаты.',
    chips=['Подходит для визы', 'Расчёт бесплатный', 'Полис на e-mail'],
    facts_title='Перед покупкой',
    facts=[
      ('Для Шенгена — от 30 000 €', 'Для шенгенской визы нужен полис с покрытием не меньше 30 000 € на всю поездку и все страны Шенгена.'),
      ('Требования зависят от страны', 'Уточните их на сайте консульства или у туроператора.'),
      ('Активный отдых — отдельно', 'Горные лыжи, дайвинг и другой активный отдых выбирайте отдельной опцией: обычный полис их может не покрывать.'),
      ('Сохраните телефон ассистанса', 'Он есть в полисе. Если заболели, звоните туда до обращения к врачу.'),
    ],
    note='',
    faq=[
      ('Нужна ли страховка, если для страны не нужна виза?', 'Для въезда может не требоваться, но без полиса лечение за границей вы оплачиваете сами, а оно бывает очень дорогим.'),
      ('Какую сумму покрытия выбрать?', 'Для Шенгена — минимум 30 000 €. Для других стран смотрите их требования; для дальних поездок и активного отдыха обычно берут больше.'),
      ('Что делать, если заболели в поездке?', 'Позвоните в сервисную компанию по телефону из полиса: там скажут, в какую клинику обратиться, и согласуют оплату. Если обратились к врачу сами, сохраните все чеки и документы.'),
    ]),
]

FAQ_MANAGER = ('Не получается оформить онlайн?'.replace('онlайн', 'онлайн'),
               'Напишите менеджеру в Telegram — он сделает расчёт и поможет оформить полис.')

def page(p):
    url = f'https://prostrahagent.ru/{p["slug"]}/'
    widget = widget_tpl.replace('data-product="/eosago"', f'data-product="{p["product"]}"')
    assert f'data-product="{p["product"]}"' in widget
    chips = ''.join(f'<li>{CHECK}{html.escape(c)}</li>' for c in p['chips'])
    facts = ''.join(f'<article class="fact"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>' for t, d in p['facts'])
    note = f'<p class="facts__note">{html.escape(p["note"])}</p>' if p['note'] else ''
    faq_items = list(p['faq'])
    faq_html = ''
    for i, (q, a) in enumerate(faq_items):
        faq_html += f'''      <details class="faq__item"{' open' if i == 0 else ''}>
        <summary>{html.escape(q)}</summary>
        <p>{html.escape(a)}</p>
      </details>
'''
    faq_html += f'''      <details class="faq__item">
        <summary>{FAQ_MANAGER[0]}</summary>
        <p>Напишите менеджеру в <a class="link js-manager js-manager-always" href="https://t.me/prostrahagent" data-goal="tg_{p["slug"]}_faq">Telegram</a> — он сделает расчёт и поможет оформить полис.</p>
      </details>
'''
    cross = ''.join(f'<a class="ptab" href="{h}">{html.escape(n)}</a>' for n, h in ALL if h != f'/{p["slug"]}/')
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]}
    ld_crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://prostrahagent.ru/"},
        {"@type": "ListItem", "position": 2, "name": p['crumb'], "item": url}]}
    a_assist = assist.replace('data-goal="tg_policy_manager"', f'data-goal="tg_{p["slug"]}_manager"')
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(p["title"])}</title>
  <meta name="description" content="{html.escape(p["desc"])}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0B1736">
  <meta property="og:title" content="{html.escape(p["h1"])}">
  <meta property="og:description" content="{html.escape(p["desc"])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="ПроСтрахАгент">
  <meta property="og:locale" content="ru_RU">
  <script type="application/ld+json">{json.dumps(ld_crumbs, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{''.join(f.replace('href="fonts/', 'href="/fonts/') for f in fonts)}  <link rel="stylesheet" href="/styles.css?v={css_ver}">
</head>
<body class="product-page">

{header}

<main>

<section class="page-hero section--policy" id="policy">
  <div class="container">
    <nav class="crumbs" aria-label="Навигация"><a href="/">Главная</a><span aria-hidden="true">›</span><span>{html.escape(p["crumb"])}</span></nav>
    <h1 class="page-hero__title">{html.escape(p["h1"])}</h1>
    <p class="page-hero__lead">{html.escape(p["lead"])}</p>
    <ul class="chips">{chips}</ul>
{a_assist}{scrollfix}{widget}    <p class="widget-note">Данные, которые вы вводите в форму или передаёте менеджеру, получают сервис расчёта полисов и страховая компания — подробнее в <a class="link" href="/privacy.html#widget">политике</a>.</p>
  </div>
</section>

<section class="section section--tight-top">
  <div class="container">
    <div class="section__head section__head--left">
      <h2 class="h2">{html.escape(p["facts_title"])}</h2>
    </div>
    <div class="facts">{facts}</div>
    {note}
  </div>
</section>

<section class="section section--tight-top" id="faq">
  <div class="container faq">
    <div class="section__head section__head--left">
      <span class="eyebrow">Частые вопросы</span>
      <h2 class="h2">Коротко о главном</h2>
    </div>
    <div class="faq__list">
{faq_html}    </div>
  </div>
</section>

<section class="section section--tight-top">
  <div class="container">
    <h2 class="h3-title">Другие виды страхования</h2>
    <div class="ptabs ptabs--left">{cross}</div>
  </div>
</section>

<section class="section section--tight-top">
  <div class="container">
    <div class="agent-band">
      <div>
        <h2>Оформляете полисы родным и знакомым?</h2>
        <p>Станьте агентом и получайте вознаграждение за каждый полис — бесплатно, онлайн и без опыта. Это не работа с окладом, а ваше дело.</p>
      </div>
      <a class="btn btn--accent btn--lg js-tg" href="https://t.me/prostrahagent" data-goal="tg_{p["slug"]}_agent">{TG} Стать агентом</a>
    </div>
  </div>
</section>

</main>

{footer}

<script src="/config.js?v={cfg_ver}"></script>
<script src="/consent.js"></script>
<script src="/script.js?v={js_ver}"></script>
</body>
</html>
'''

for p in PAGES:
    d = os.path.join(root, p['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(p))
    print('wrote', p['slug'])
