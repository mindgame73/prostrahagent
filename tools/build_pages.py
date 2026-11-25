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
footer = footer.replace('href="#top"', 'href="/"').replace('href="privacy.html"', 'href="/privacy.html"').replace('href="consent.html"', 'href="/consent.html"').replace('href="terms.html"', 'href="/terms.html"')

TG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.5 4.3 18.4 19c-.2 1-.8 1.3-1.7.8l-4.6-3.4-2.2 2.1c-.3.3-.5.5-1 .5l.3-4.7 8.6-7.8c.4-.3-.1-.5-.6-.2L6.6 13 2 11.6c-1-.3-1-1 .2-1.5L20.1 3.2c.8-.3 1.6.2 1.4 1.1Z" fill="currentColor"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

ALL = [
    ('Проверка КБМ', '/kbm/'), ('ОСАГО', '/osago/'), ('Страхование ипотеки', '/ipoteka/'), ('Путешествия', '/travel/'),
    ('Мини-КАСКО', '/kasko/'), ('Квартира и дом', '/#kvartira'), ('Антиклещ', '/#antiklesh'),
    ('КАСКО', '/kasko/'), ('Титул', '/#titul'),
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
  dict(slug='kasko', product='/mini-kasko', crumb='КАСКО',
    title='КАСКО и мини-КАСКО онлайн — рассчитать стоимость полиса | ПроСтрахАгент',
    desc='Мини-КАСКО можно рассчитать онлайн и сравнить цены страховых. Полное КАСКО подберёт менеджер: запросит расчёты в нескольких страховых и поможет выбрать.',
    h1='КАСКО и мини-КАСКО: рассчитать и оформить',
    lead='Мини-КАСКО считается онлайн прямо на этой странице. Полное КАСКО подбираем через менеджера: цена сильно зависит от машины, водителей и франшизы.',
    chips=['Мини-КАСКО онлайн', 'Полное КАСКО через менеджера', 'Полис на e-mail'],
    facts_title='Что выбрать',
    facts=[
      ('Полное КАСКО', 'Защищает от угона, ущерба в ДТП, стихии и вандализма. Расчёт делает менеджер: напишите марку и год машины, город и кто будет за рулём.'),
      ('Мини-КАСКО', 'Дешевле полного: покрывает ограниченный набор случаев с лимитом выплаты. Подойдёт, если нужна защита своей машины после ДТП по вашей вине.'),
      ('ОСАГО свою машину не чинит', 'ОСАГО платит только тем, кому вы причинили ущерб. Ремонт своей машины после ДТП по вашей вине покрывает КАСКО или мини-КАСКО.'),
      ('Франшиза снижает цену', 'Это часть ущерба, которую вы оплачиваете сами. Чем она больше, тем дешевле полис.'),
    ],
    note='Калькулятор ниже считает мини-КАСКО. Точные риски и лимит выплаты смотрите в условиях выбранной страховой перед оплатой.',
    faq=[
      ('Чем мини-КАСКО отличается от полного КАСКО?', 'Полное КАСКО покрывает много рисков: угон, ДТП, стихию, вандализм, и выплата обычно до стоимости машины. Мини-КАСКО покрывает меньше случаев и с лимитом выплаты, зато стоит в разы дешевле. Что именно входит, зависит от страховой и указано в условиях полиса.'),
      ('Нужно ли КАСКО, если есть ОСАГО?', 'ОСАГО обязательно, но оно платит только пострадавшим. Если ДТП произошло по вашей вине, ремонт своей машины ОСАГО не оплатит. Для этого и нужно КАСКО или мини-КАСКО.'),
      ('Обязательно ли КАСКО при автокредите?', 'По закону нет, но банк по кредитному договору часто требует полное КАСКО. Полис не обязательно покупать в банке: подойдёт страховая, которую банк принимает. Требования смотрите в договоре.'),
      ('От чего зависит цена КАСКО?', 'От марки, года и стоимости машины, возраста и стажа водителей, региона, набора рисков, франшизы и противоугонной системы. Поэтому полное КАСКО лучше считать с менеджером: он запросит цены в нескольких страховых.'),
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
    kbm_link = '    <p class="kbm-hint">Не знаете свою скидку за безаварийность? <a class="link" href="/kbm/" data-goal="kbm_from_osago">Проверьте КБМ бесплатно →</a></p>\n' if p['slug'] == 'osago' else ''
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
{kbm_link}{a_assist}{scrollfix}{widget}    <p class="widget-note">Вводя данные, вы соглашаетесь, что они будут переданы ООО «МК Групп» (ИНН 7805730637) и страховым компаниям для расчёта и оформления полиса — на условиях <a class="link" href="https://inssmart.ru/policypersonald" target="_blank" rel="noopener">их политики обработки персональных данных</a>. Подробнее — в <a class="link" href="/privacy.html#widget">нашей политике</a>.</p>
    <p class="widget-note widget-note--mediator"><b>Кто оформляет полис.</b> Расчёт и оформление выполняются через онлайн-платформу ООО «МК Групп» (ИНН 7805730637) на основании её договоров со страховыми компаниями. Договор страхования вы заключаете напрямую со страховой компанией, которую выбрали при расчёте, — она выпускает полис. Владелец сайта денежные средства за полисы не принимает. Наименование страховщика, его лицензия Банка России и правила страхования доступны в калькуляторе до оплаты. При страховом случае обращайтесь в страховую компанию, указанную в полисе.</p>
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
<script src="/consent.js?v=3"></script>
<script src="/script.js?v={js_ver}"></script>
</body>
</html>
'''

# ---------------- страница «Стать агентом» (/agent/) ----------------
steps_html = between(idx, '    <ol class="steps">', '    </ol>') + '    </ol>\n'

AGENT = dict(
    title='Как стать страховым агентом онлайн — без опыта и вложений | ПроСтрахАгент',
    desc='Станьте страховым агентом онлайн: бесплатное обучение с куратором, вознаграждение за каждый оформленный полис. Без опыта, из любого города. Честно о плюсах и минусах.',
    h1='Как стать страховым агентом онлайн',
    lead='Страховой агент оформляет полисы для клиентов и получает вознаграждение за каждый. Обучение с куратором и оформление — онлайн, из любого города. Это не работа по найму с окладом, а ваше дело.',
    chips=['Бесплатный старт', 'Без опыта', 'Из любого города'],
    what=[
      ('Находит клиентов', 'Родственники, знакомые, коллеги, соцсети, автомобилисты и ипотечники вашего города.'),
      ('Считает варианты', 'В личном кабинете сравнивает цены разных страховых и подбирает подходящий полис.'),
      ('Оформляет полис онлайн', 'Клиент оплачивает полис, а электронный полис приходит ему на почту.'),
      ('Получает вознаграждение', 'За каждый оформленный полис. Ставка зависит от вида страхования и страховой компании.'),
    ],
    fit=[
      ('Подработка в своём темпе', 'Можно совмещать с основной работой, учёбой или декретом.'),
      ('Много знакомых', 'Если вас часто спрашивают про ОСАГО или ипотеку — это готовые первые клиенты.'),
      ('Есть аудитория', 'Блог, канал, чат дома или автоклуба — там тоже нужны полисы.'),
      ('Хотите своё дело', 'Без вложений и офиса: доход растёт вместе с числом клиентов.'),
    ],
    cons=[
      ('Нет оклада', 'Доход зависит только от числа оформленных полисов.'),
      ('Клиентов ищете сами', 'Мы подсказываем, где искать и как отвечать на возражения, но продаёте вы.'),
      ('Нужно время', 'Новичкам на первые продажи обычно требуется несколько недель.'),
    ],
    faq=[
      ('Это трудоустройство?', 'Нет. Вы работаете как самостоятельный страховой агент по агентскому договору с онлайн-платформой: его вы принимаете при регистрации на платформе, вознаграждение начисляется и выплачивается по её правилам. Трудового договора и оклада нет. Мы помогаем разобраться и начать: обучение и куратор.'),
      ('Нужен ли опыт?', 'Нет. Куратор присылает уроки в личные сообщения и помогает до первого оформленного полиса.'),
      ('Нужно ли что-то платить?', 'Нет. Регистрация и обучающие материалы бесплатные.'),
      ('Сколько можно заработать?', 'Зависит от того, сколько полисов вы оформите и каких. Ориентир можно прикинуть в калькуляторе дохода на главной — это оценка, а не гарантия.'),
      ('Как выводить вознаграждение?', 'Вознаграждение зачисляется на баланс в личном кабинете агента, оттуда его выводят на свой счёт.'),
      ('Где брать клиентов?', 'Начните с себя и близких: ваша машина, квартира, ипотека, потом родственники и знакомые. Дальше — соцсети и рекомендации. Куратор поможет составить первое сообщение.'),
    ],
)

def agent_page(a):
    url = 'https://prostrahagent.ru/agent/'
    hdr = re.sub(r'<nav class="nav".*?</nav>', '''<nav class="nav" aria-label="Основная навигация">
      <a href="#what">Чем занимается агент</a>
      <a href="#steps">Как начать</a>
      <a href="#faq">Вопросы</a>
      <a href="/#policy">Рассчитать полис</a>
    </nav>''', header, flags=re.S)
    cards = lambda items: ''.join(f'<article class="fact"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>' for t, d in items)
    chips = ''.join(f'<li>{CHECK}{html.escape(c)}</li>' for c in a['chips'])
    cons = ''.join(f'<li><b>{html.escape(t)}</b><span>{html.escape(d)}</span></li>' for t, d in a['cons'])
    faq_html = ''.join(f'''      <details class="faq__item"{' open' if i == 0 else ''}>
        <summary>{html.escape(q)}</summary>
        <p>{html.escape(t)}</p>
      </details>
''' for i, (q, t) in enumerate(a['faq']))
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in a['faq']]}
    ld_crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://prostrahagent.ru/"},
        {"@type": "ListItem", "position": 2, "name": "Стать агентом", "item": url}]}
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(a["title"])}</title>
  <meta name="description" content="{html.escape(a["desc"])}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0B1736">
  <meta property="og:title" content="{html.escape(a["h1"])}">
  <meta property="og:description" content="{html.escape(a["desc"])}">
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

{hdr}

<main>

<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Навигация"><a href="/">Главная</a><span aria-hidden="true">›</span><span>Стать агентом</span></nav>
    <h1 class="page-hero__title">{html.escape(a["h1"])}</h1>
    <p class="page-hero__lead">{html.escape(a["lead"])}</p>
    <ul class="chips">{chips}</ul>
    <div class="page-hero__cta">
      <a class="btn btn--accent btn--lg js-tg" href="https://t.me/prostrahagent" data-goal="tg_agent_hero">{TG} Начать в Telegram</a>
      <a class="btn btn--ghost btn--lg" href="/#calc">Посчитать доход</a>
    </div>
    <p class="page-hero__note"><a class="link js-manager" href="https://t.me/prostrahagent" data-goal="curator_agent_hero" hidden>Готовы сразу? Напишите куратору</a> <span class="sep">·</span> Нет Telegram? <a class="link" href="https://max.ru/join/tF0KNwrT1PTsww7vG0NTL_VBi3YXHXQv3bgCNp18fi8" target="_blank" rel="noopener" data-goal="max_agent_hero"><img class="max-ico" src="/img/max.png" alt="" width="18" height="18">Канал в Max</a></p>
  </div>
</section>

<section class="section section--tight-top" id="what">
  <div class="container">
    <div class="section__head section__head--left"><h2 class="h2">Чем занимается страховой агент</h2></div>
    <div class="facts">{cards(a["what"])}</div>
  </div>
</section>

<section class="section section--tight-top">
  <div class="container">
    <div class="section__head section__head--left"><h2 class="h2">Кому подходит</h2></div>
    <div class="facts">{cards(a["fit"])}</div>
  </div>
</section>

<section class="section section--tight-top" id="steps">
  <div class="container">
    <div class="section__head section__head--left"><h2 class="h2">Четыре шага до первого вознаграждения</h2></div>
{steps_html}    <div class="steps__cta">
      <a class="btn btn--accent btn--lg js-tg" href="https://t.me/prostrahagent" data-goal="tg_agent_steps">{TG} Начать с шага 1 — в Telegram</a>
    </div>
    <p class="cta-alt"><a class="link js-manager" href="https://t.me/prostrahagent" data-goal="curator_agent_steps" hidden>Готовы сразу? Напишите куратору →</a></p>
  </div>
</section>

<section class="section section--tight-top">
  <div class="container">
    <div class="section__head section__head--left">
      <h2 class="h2">Честно о минусах</h2>
      <p class="section__lead">Чтобы вы заранее понимали, на что идёте.</p>
    </div>
    <ul class="cons">{cons}</ul>
  </div>
</section>

<section class="section section--tight-top" id="faq">
  <div class="container faq">
    <div class="section__head section__head--left">
      <span class="eyebrow">Частые вопросы</span>
      <h2 class="h2">Отвечаем честно</h2>
      <p class="section__lead">Не нашли ответ? Напишите в <a class="link js-manager js-manager-always" href="https://t.me/prostrahagent" data-goal="tg_agent_faq">Telegram</a> — ответим.</p>
    </div>
    <div class="faq__list">
{faq_html}    </div>
  </div>
</section>

<section class="section section--tight-top">
  <div class="container">
    <div class="agent-band">
      <div>
        <h2>Пошаговый старт — в Telegram</h2>
        <p>Как устроена работа агента, план первой недели, какие продукты проще новичку и где искать первых клиентов.</p>
      </div>
      <a class="btn btn--accent btn--lg js-tg" href="https://t.me/prostrahagent" data-goal="tg_agent_band">{TG} Перейти в Telegram</a>
    </div>
    <p class="client-link">Нужна страховка, а не работа? <a href="/#policy">Рассчитайте полис онлайн →</a></p>
  </div>
</section>

</main>

{footer}

<script src="/config.js?v={cfg_ver}"></script>
<script src="/consent.js?v=3"></script>
<script src="/script.js?v={js_ver}"></script>
</body>
</html>
'''


RESULT = [
  dict(slug='spasibo', goal='policy_paid', title='Спасибо! Полис оплачен | ПроСтрахАгент',
    h1='Спасибо! Полис оплачен',
    lead='Полис придёт на e-mail, который вы указали при оформлении. Обычно это занимает несколько минут.',
    items=[('Письма нет?', 'Проверьте папку «Спам». Если полиса нет больше часа, напишите менеджеру, проверим.'),
           ('Сохраните полис', 'Электронный полис действует так же, как бумажный. Удобно держать файл в телефоне.'),
           ('Напомним о продлении', 'Напишите менеджеру слово «Продление», и за месяц до окончания полиса мы пришлём новый расчёт.')],
    cta_title='Понравилось оформлять онлайн?',
    cta_text='Так же можно помогать знакомым с ОСАГО, КАСКО и страховкой ипотеки и получать комиссию за каждый полис. Обучение бесплатное.',
    cta=('/agent/', 'Стать агентом', 'agent_from_thanks')),
  dict(slug='oplata-ne-proshla', goal='payment_failed', title='Оплата не прошла | ПроСтрахАгент',
    h1='Оплата не прошла',
    lead='Так бывает: банк отклонил платёж, не пришёл код или прервалась связь. Попробуйте ещё раз или напишите нам, поможем оформить.',
    items=[('Попробуйте другую карту', 'Иногда банк блокирует оплату в интернете. Подойдёт карта другого банка.'),
           ('Деньги списались, а полиса нет?', 'Не оплачивайте повторно. Напишите менеджеру, проверим платёж и полис.'),
           ('Не получается оформить сами?', 'Менеджер сделает расчёт и пришлёт ссылку на оплату.')],
    cta_title='Попробовать ещё раз',
    cta_text='Вернитесь к расчёту: данные можно ввести заново за пару минут.',
    cta=('/#policy', 'К расчёту полиса', 'retry_after_fail')),
  dict(slug='404', goal='page_404', title='Страница не найдена | ПроСтрахАгент',
    h1='Такой страницы нет',
    lead='Возможно, ссылка устарела или в адресе опечатка. Всё основное есть на главной.',
    items=[('Рассчитать полис', 'ОСАГО, мини-КАСКО, ипотека, путешествия и другое: на главной в разделе «Рассчитать страховку».'),
           ('Стать агентом', 'Как устроена работа агента, обучение и куратор: страница «Стать агентом».'),
           ('Нужна помощь?', 'Напишите менеджеру в Telegram, подскажем.')],
    cta_title='Вернуться на сайт',
    cta_text='Главная страница ПроСтрахАгент.',
    cta=('/', 'На главную', 'home_from_404')),
]

def result_page(r):
    items = ''.join(f'<article class="fact"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>' for t, d in r['items'])
    href, label, g = r['cta']
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(r["title"])}</title>
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#0B1736">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{''.join(f.replace('href="fonts/', 'href="/fonts/') for f in fonts)}  <link rel="stylesheet" href="/styles.css?v={css_ver}">
</head>
<body class="product-page" data-goal-onload="{r["goal"]}">

{header}

<main>
<section class="page-hero">
  <div class="container">
    <h1 class="page-hero__title">{html.escape(r["h1"])}</h1>
    <p class="page-hero__lead">{html.escape(r["lead"])}</p>
    <div class="page-hero__cta">
      <a class="btn btn--tg btn--lg js-manager js-manager-always" href="https://t.me/prostrahagent" data-goal="tg_{r["slug"].replace("-", "_")}">{TG} Написать менеджеру</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="facts">{items}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2 class="h2">{html.escape(r["cta_title"])}</h2>
    <p class="section__lead">{html.escape(r["cta_text"])}</p>
    <div class="page-hero__cta"><a class="btn btn--accent btn--lg" href="{href}" data-goal="{g}">{html.escape(label)}</a></div>
  </div>
</section>
</main>

{footer}

<script src="/config.js?v={cfg_ver}"></script>
<script src="/consent.js?v=3"></script>
<script src="/script.js?v={js_ver}"></script>
</body>
</html>
'''

# ---------------- страница «Проверка КБМ» (/kbm/) ----------------
KBM_API = 'https://functions.yandexcloud.net/d4e3e3v52nob2rn4k038'
KBM = dict(
  title='Проверка КБМ онлайн бесплатно по базе РСА | ПроСтрахАгент',
  desc='Проверьте КБМ (скидку за безаварийность) по базе РСА онлайн и бесплатно: ФИО, дата рождения и номер прав. Узнайте, сохранилась ли скидка, и рассчитайте ОСАГО с ней.',
  h1='Проверка КБМ онлайн: узнайте свою скидку на ОСАГО',
  lead='КБМ — это скидка за езду без аварий. Она может доходить до 54%, а может «потеряться» после замены прав или ошибки в базе. Проверьте за минуту.',
  chips=['Бесплатно', 'По базе РСА', 'Данные не храним'],
  facts=[
    ('От 0,46 до 3,92', 'Таков диапазон КБМ. Меньше 1 — скидка, больше 1 — повышение цены. Каждый год без аварий снижает коэффициент.'),
    ('1,17 — стартовый класс', 'Его получают новые водители. Если вы ездите давно, а видите 1,17, скорее всего, скидка не подтянулась из базы.'),
    ('Скидка не «сгорает» при смене страховой', 'КБМ хранится в общей базе РСА и привязан к водителю, а не к компании.'),
    ('Скидку можно вернуть', 'Если КБМ посчитан неверно, страховая обязана исправить его по обращению. Мы поможем пройти это бесплатно.'),
  ],
  faq=[
    ('Что такое КБМ?', 'Коэффициент бонус-малус — множитель в цене ОСАГО за аварийность. Чем дольше вы ездите без аварий по своей вине, тем он ниже и тем дешевле полис. После аварии КБМ растёт.'),
    ('Почему у меня КБМ 1,17, хотя я езжу без аварий?', 'Чаще всего база не связала вас с прошлыми полисами: вы меняли права и в новом полисе не указали старые, полис был «без ограничений» (тогда скидка учитывается у собственника), или в прошлом полисе была ошибка в ФИО или номере прав.'),
    ('Как восстановить КБМ?', 'Нужно обратиться в страховую с заявлением о пересчёте и подтвердить прошлые полисы. Страховая обязана исправить КБМ в базе. Оставьте заявку — подскажем, куда и что написать, и посчитаем ОСАГО уже с правильной скидкой.'),
    ('Какие данные нужны для проверки?', 'ФИО, дата рождения, серия и номер водительского удостоверения — как в правах. Если права меняли, проверьте и по старым.'),
    ('Как часто обновляется КБМ?', 'Класс пересчитывается раз в год, на 1 апреля, по данным о страховых случаях за прошлый год. В течение года при оформлении нового полиса применяется текущий класс.'),
    ('Вы сохраняете мои данные?', 'Нет. Данные передаются только для проверки в базе РСА через партнёрскую платформу и не сохраняются. Подробнее — в политике обработки персональных данных.'),
  ],
)

def kbm_page(k):
    url = 'https://prostrahagent.ru/kbm/'
    hdr = re.sub(r'<nav class="nav".*?</nav>', '''<nav class="nav" aria-label="Основная навигация">
      <a href="#check">Проверить КБМ</a>
      <a href="#faq">Вопросы</a>
      <a href="/osago/">Рассчитать ОСАГО</a>
    </nav>''', header, flags=re.S)
    chips = ''.join(f'<li>{CHECK}{html.escape(c)}</li>' for c in k['chips'])
    facts = ''.join(f'<article class="fact"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>' for t, d in k['facts'])
    faq_html = ''.join(f'''      <details class="faq__item"{' open' if i == 0 else ''}>
        <summary>{html.escape(q)}</summary>
        <p>{html.escape(a)}</p>
      </details>
''' for i, (q, a) in enumerate(k['faq']))
    cross = ''.join(f'<a class="ptab" href="{h}">{html.escape(n)}</a>' for n, h in ALL if h != '/kbm/')
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in k['faq']]}
    ld_crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://prostrahagent.ru/"},
        {"@type": "ListItem", "position": 2, "name": "Проверка КБМ", "item": url}]}
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(k["title"])}</title>
  <meta name="description" content="{html.escape(k["desc"])}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0B1736">
  <meta property="og:title" content="{html.escape(k["h1"])}">
  <meta property="og:description" content="{html.escape(k["desc"])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="ПроСтрахАгент">
  <meta property="og:locale" content="ru_RU">
  <script type="application/ld+json">{json.dumps(ld_crumbs, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{''.join(f.replace('href="fonts/', 'href="/fonts/') for f in fonts)}  <link rel="stylesheet" href="/styles.css?v={css_ver}">
  <style>
    .kbm-card {{ background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); padding: 28px; max-width: 640px; margin-top: 28px; }}
    .kbm-form {{ display: grid; gap: 16px; }}
    .kbm-form label {{ display: grid; gap: 6px; font-weight: 700; font-size: 15px; }}
    .kbm-form label span {{ font-weight: 500; color: var(--muted); font-size: 13px; }}
    .kbm-form input[type=text], .kbm-form input[type=tel] {{ font: inherit; font-size: 17px; padding: 14px 16px; border: 1px solid var(--line); border-radius: var(--radius-sm); background: var(--bg); color: var(--ink); width: 100%; }}
    .kbm-form input:focus {{ outline: none; border-color: var(--blue); box-shadow: 0 0 0 4px rgba(47, 91, 255, .15); background: #fff; }}
    .kbm-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    @media (max-width: 560px) {{ .kbm-row {{ grid-template-columns: 1fr; }} .kbm-card {{ padding: 20px; }} }}
    .kbm-consent {{ display: flex !important; grid-template-columns: none; gap: 10px !important; align-items: flex-start; font-weight: 500 !important; font-size: 13px !important; color: var(--muted); }}
    .kbm-consent input {{ margin-top: 3px; width: 18px; height: 18px; flex: none; }}
    .kbm-hp {{ position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }}
    .kbm-err {{ color: #C62828; font-weight: 600; font-size: 14px; min-height: 1em; }}
    .kbm-res {{ display: none; }}
    .kbm-res.is-on {{ display: block; }}
    .kbm-big {{ font-family: var(--font-head); font-weight: 600; font-size: clamp(40px, 7vw, 64px); letter-spacing: -.03em; line-height: 1; }}
    .kbm-badge {{ display: inline-block; padding: 6px 14px; border-radius: 999px; font-weight: 800; font-size: 14px; margin: 10px 0 14px; }}
    .kbm-badge--good {{ background: var(--accent); color: var(--ink); }}
    .kbm-badge--warn {{ background: #FFE3A3; color: #6A4A00; }}
    .kbm-badge--bad {{ background: #FFD4D4; color: #8A1C1C; }}
    .kbm-res p {{ color: var(--muted); margin-bottom: 18px; }}
    .kbm-actions {{ display: flex; flex-wrap: wrap; gap: 12px; }}
    .kbm-lead {{ margin-top: 22px; padding-top: 22px; border-top: 1px solid var(--line); }}
    .kbm-lead h3 {{ font-family: var(--font-head); font-weight: 600; font-size: 20px; margin-bottom: 6px; }}
    .kbm-again {{ background: none; border: 0; color: var(--blue); font: inherit; font-weight: 700; cursor: pointer; padding: 0; margin-top: 16px; }}
    .kbm-hint {{ margin: 14px 0 0; font-weight: 600; }}
    .btn[disabled] {{ opacity: .6; pointer-events: none; }}
  </style>
</head>
<body class="product-page">

{hdr}

<main>

<section class="page-hero" id="check">
  <div class="container">
    <nav class="crumbs" aria-label="Навигация"><a href="/">Главная</a><span aria-hidden="true">›</span><span>Проверка КБМ</span></nav>
    <h1 class="page-hero__title">{html.escape(k["h1"])}</h1>
    <p class="page-hero__lead">{html.escape(k["lead"])}</p>
    <ul class="chips">{chips}</ul>

    <div class="kbm-card">
      <form class="kbm-form" id="kbmForm" novalidate>
        <label>Фамилия, имя и отчество<span>Как в водительском удостоверении</span>
          <input type="text" name="fio" autocomplete="name" placeholder="Иванов Иван Иванович" required></label>
        <div class="kbm-row">
          <label>Дата рождения
            <input type="text" name="birth" inputmode="numeric" autocomplete="bday" placeholder="31.05.1986" maxlength="10" required></label>
          <label>Серия и номер прав<span>10 знаков, пункт 5</span>
            <input type="text" name="license" autocomplete="off" placeholder="99 12 345678" maxlength="12" autocapitalize="characters" required></label>
        </div>
        <div class="kbm-hp" aria-hidden="true"><label>Сайт<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <label class="kbm-consent"><input type="checkbox" name="agree" required> <span>Согласен на обработку персональных данных для проверки КБМ: они передаются ООО «МК Групп» (ИНН 7805730637) для запроса в базу РСА и не сохраняются. <a class="link" href="/privacy.html#kbm" target="_blank">Политика</a></span></label>
        <div class="kbm-err" id="kbmErr" role="alert"></div>
        <button class="btn btn--accent btn--lg" type="submit" id="kbmBtn" data-goal="kbm_check">Проверить КБМ</button>
      </form>

      <div class="kbm-res" id="kbmRes" aria-live="polite">
        <div class="kbm-big" id="kbmVal">—</div>
        <div class="kbm-badge" id="kbmBadge"></div>
        <p id="kbmText"></p>
        <div class="kbm-actions" id="kbmActions"></div>
        <div class="kbm-lead" id="kbmLeadBox">
          <h3 id="kbmLeadTitle">Вернём скидку бесплатно</h3>
          <p id="kbmLeadText">Оставьте телефон: подскажем, как восстановить КБМ, и посчитаем ОСАГО уже с правильной скидкой.</p>
          <form class="kbm-form" id="leadForm" novalidate>
            <div class="kbm-row">
              <label>Имя<input type="text" name="name" autocomplete="given-name" placeholder="Иван"></label>
              <label>Телефон<input type="tel" name="phone" autocomplete="tel" placeholder="+7 900 000-00-00" required></label>
            </div>
            <label class="kbm-consent"><input type="checkbox" name="agree" required> <span>Согласен, чтобы со мной связались по этой заявке. <a class="link" href="/privacy.html#kbm" target="_blank">Политика</a></span></label>
            <div class="kbm-err" id="leadErr" role="alert"></div>
            <button class="btn btn--accent btn--lg" type="submit" id="leadBtn" data-goal="kbm_lead">Оставить заявку</button>
          </form>
        </div>
        <button class="kbm-again" type="button" id="kbmAgain">↺ Проверить другого водителя</button>
      </div>
    </div>
    <p class="widget-note">Проверка идёт через партнёрскую платформу ООО «МК Групп» по базе Российского союза автостраховщиков. Мы не храним введённые данные.</p>
  </div>
</section>

<section class="section section--tight-top">
  <div class="container">
    <div class="section__head section__head--left"><h2 class="h2">Что важно знать о КБМ</h2></div>
    <div class="facts">{facts}</div>
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
    <h2 class="h3-title">Рассчитать полис</h2>
    <div class="ptabs ptabs--left">{cross}</div>
  </div>
</section>

</main>

{footer}

<script src="/config.js?v={cfg_ver}"></script>
<script src="/consent.js?v=3"></script>
<script src="/script.js?v={js_ver}"></script>
<script>
(function () {{
  var API = '{KBM_API}';
  var src = (new URLSearchParams(location.search).get('utm_source') || new URLSearchParams(location.search).get('src') || 'site').slice(0, 20);
  var $ = function (id) {{ return document.getElementById(id); }};
  var form = $('kbmForm'), res = $('kbmRes'), lastFactor = null;
  var birth = form.birth;
  birth.addEventListener('input', function () {{
    var d = birth.value.replace(/\\D/g, '').slice(0, 8), o = d.slice(0, 2);
    if (d.length > 2) o += '.' + d.slice(2, 4);
    if (d.length > 4) o += '.' + d.slice(4);
    birth.value = o;
  }});
  // Номер прав: сами ставим пробелы «99 12 345678» (серия бывает с буквами у старых прав)
  var lic = form.license;
  lic.addEventListener('input', function () {{
    var v = lic.value.toUpperCase().replace(/[^0-9А-ЯЁ]/g, '').slice(0, 10), o = v.slice(0, 2);
    if (v.length > 2) o += ' ' + v.slice(2, 4);
    if (v.length > 4) o += ' ' + v.slice(4);
    lic.value = o;
  }});
  function post(api, body) {{
    return fetch(API + '?api=' + api, {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(body) }})
      .then(function (r) {{ return r.json().catch(function () {{ return {{ ok: false, error: 'Ошибка сервера' }}; }}); }});
  }}
  function goal(g) {{ try {{ if (window.PS && PS.goal) PS.goal(g); }} catch (e) {{}} }}
  form.addEventListener('submit', function (e) {{
    e.preventDefault();
    var err = $('kbmErr'), btn = $('kbmBtn');
    err.textContent = '';
    if (!form.agree.checked) {{ err.textContent = 'Отметьте согласие на обработку данных.'; return; }}
    btn.disabled = true; btn.textContent = 'Проверяем в базе РСА…';
    post('kbm', {{ fio: form.fio.value, birth: form.birth.value, license: form.license.value, website: form.website.value, src: src }})
      .then(function (r) {{
        btn.disabled = false; btn.textContent = 'Проверить КБМ';
        if (!r.ok) {{ err.textContent = r.error || 'Не получилось проверить. Попробуйте ещё раз.'; return; }}
        show(r);
      }})
      .catch(function () {{ btn.disabled = false; btn.textContent = 'Проверить КБМ'; err.textContent = 'Нет связи с сервером. Попробуйте ещё раз.'; }});
  }});
  function show(r) {{
    var val = $('kbmVal'), badge = $('kbmBadge'), text = $('kbmText'), act = $('kbmActions');
    var leadT = $('kbmLeadTitle'), leadP = $('kbmLeadText');
    form.style.display = 'none'; res.classList.add('is-on');
    act.innerHTML = '';
    if (!r.found) {{
      lastFactor = null;
      val.textContent = 'Не нашли';
      badge.className = 'kbm-badge kbm-badge--warn'; badge.textContent = 'Нет данных в базе РСА';
      text.textContent = 'Проверьте ФИО и номер прав — точно как в удостоверении. Если права меняли, попробуйте старые. Или оставьте телефон, проверим сами.';
      leadT.textContent = 'Проверим КБМ за вас'; leadP.textContent = 'Оставьте телефон: проверим по старым правам и прошлым полисам.';
      return;
    }}
    lastFactor = r.factor;
    val.textContent = 'КБМ ' + String(r.factor).replace('.', ',');
    if (r.kind === 'discount') {{
      badge.className = 'kbm-badge kbm-badge--good'; badge.textContent = 'Скидка ' + r.discount + '%';
      text.textContent = 'Отлично: скидка за безаварийность на месте. Посчитайте ОСАГО — цена в калькуляторе уже учтёт её.';
      act.innerHTML = '<a class="btn btn--accent btn--lg" href="/osago/#policy" data-goal="kbm_to_osago">Посчитать ОСАГО со скидкой</a>';
      leadT.textContent = 'Хотите, посчитаем за вас?'; leadP.textContent = 'Оставьте телефон: сравним цены во всех страховых и пришлём лучшую.';
    }} else if (r.kind === 'neutral') {{
      badge.className = 'kbm-badge kbm-badge--warn'; badge.textContent = 'Скидки пока нет';
      text.textContent = 'Каждый год без аварий снижает КБМ. Если вы водите дольше, чем говорит база, проверим и вернём скидку.';
      act.innerHTML = '<a class="btn btn--ghost btn--lg" href="/osago/#policy" data-goal="kbm_to_osago">Посчитать ОСАГО</a>';
    }} else if (r.kind === 'base') {{
      badge.className = 'kbm-badge kbm-badge--warn'; badge.textContent = 'Стартовый класс, как у новичка';
      text.textContent = 'Если вы водите давно без аварий, скорее всего, база не связала вас с прошлыми полисами: права меняли, полис был «без ограничений» или в нём ошибка. Скидку можно вернуть, и ОСАГО станет дешевле.';
      act.innerHTML = '<a class="btn btn--ghost btn--lg" href="/osago/#policy" data-goal="kbm_to_osago">Всё равно посчитать ОСАГО</a>';
    }} else {{
      badge.className = 'kbm-badge kbm-badge--bad'; badge.textContent = 'Повышенный КБМ';
      text.textContent = 'Так бывает после аварий по вашей вине. Если аварий не было, это ошибка в базе, и её можно исправить.';
      act.innerHTML = '<a class="btn btn--ghost btn--lg" href="/osago/#policy" data-goal="kbm_to_osago">Посчитать ОСАГО</a>';
    }}
    goal('kbm_result_' + (r.kind || 'none'));
  }}
  $('leadForm').addEventListener('submit', function (e) {{
    e.preventDefault();
    var f = e.target, err = $('leadErr'), btn = $('leadBtn');
    err.textContent = '';
    if (!f.agree.checked) {{ err.textContent = 'Отметьте согласие.'; return; }}
    btn.disabled = true; btn.textContent = 'Отправляем…';
    post('lead', {{ name: f.name.value, phone: f.phone.value, factor: lastFactor, want: lastFactor !== null && lastFactor < 1 ? 'calc' : 'restore', src: src }})
      .then(function (r) {{
        btn.disabled = false; btn.textContent = 'Оставить заявку';
        if (!r.ok) {{ err.textContent = r.error || 'Не получилось отправить.'; return; }}
        $('kbmLeadBox').innerHTML = '<h3>Спасибо! Заявка у нас</h3><p>Свяжемся с вами в течение дня. Если удобнее, напишите сами в <a class="link js-manager js-manager-always" href="https://t.me/agentstrah">Telegram</a>.</p>';
        goal('kbm_lead_sent');
      }})
      .catch(function () {{ btn.disabled = false; btn.textContent = 'Оставить заявку'; err.textContent = 'Нет связи с сервером. Попробуйте ещё раз.'; }});
  }});
  $('kbmAgain').addEventListener('click', function () {{
    res.classList.remove('is-on'); form.style.display = ''; form.license.value = ''; form.fio.focus();
  }});
}})();
</script>
</body>
</html>
'''

for p in PAGES:
    d = os.path.join(root, p['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(p))
    print('wrote', p['slug'])

os.makedirs(os.path.join(root, 'agent'), exist_ok=True)
open(os.path.join(root, 'agent', 'index.html'), 'w', encoding='utf-8').write(agent_page(AGENT))
print('wrote agent')

for r in RESULT:
    if r['slug'] == '404':
        open(os.path.join(root, '404.html'), 'w', encoding='utf-8').write(result_page(r))
        print('wrote 404.html')
        continue
    d = os.path.join(root, r['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(result_page(r))
    print('wrote', r['slug'])

os.makedirs(os.path.join(root, 'kbm'), exist_ok=True)
open(os.path.join(root, 'kbm', 'index.html'), 'w', encoding='utf-8').write(kbm_page(KBM))
print('wrote kbm')
