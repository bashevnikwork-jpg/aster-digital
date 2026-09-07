#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates parts/*.html — the page sections build.py stitches together."""

import pathlib

OUT = pathlib.Path(__file__).parent / "parts"
OUT.mkdir(exist_ok=True)

CHECK = ('<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 10.5 4 4 8-9"/></svg>')


def checks(items, indent=18):
    pad = " " * indent
    return "\n".join(f'{pad}<li>{CHECK}<span>{i}</span></li>' for i in items)


def write(name, html):
    (OUT / name).write_text(html, encoding="utf-8")
    print("  parts/" + name)


# ------------------------------------------------------------------ hero
write("hero.html", '''    <!-- ================= HERO ================= -->
    <section class="hero">
      <div class="shell">
        <div class="hero__inner" data-hero>
          <p class="pill">
            <span class="pill__dot" aria-hidden="true"></span>
            3–7 днів · від 9 999 ₴ · запуск реклами — безкоштовно
          </p>
          <h1>Сайт + Google Ads для бізнесу</h1>
          <p class="hero__sub lead">
            Запускаємо бізнес в інтернеті. Створюємо сучасний сайт, аналізуємо вашу нішу
            та запускаємо Google Ads, щоб ваш бізнес отримав <strong>перших клієнтів з інтернету</strong>.
          </p>
          <div class="hero__actions">
            <button class="btn btn--primary btn--lg" data-modal-open>Обговорити проєкт <span class="btn__arrow">→</span></button>
            <a class="btn btn--ghost btn--lg" href="portfolio.html">Переглянути роботи</a>
          </div>

          <div class="showcase">
            <div class="showcase__frame">
              <div class="showcase__bar" aria-hidden="true">
                <i></i><i></i><i></i>
                <span>aster-digital.com</span>
              </div>
              <div class="showcase__img">
                <img src="public/assets/screenshots/ferdinant.webp" alt="Приклад сайту, створеного Aster Digital" width="1600" height="740" />
              </div>
              <div class="showcase__note showcase__note--a" aria-hidden="true">
                <i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></i>
                <div><b>Google Ads</b><span>трафік за запитом клієнта</span></div>
              </div>
              <div class="showcase__note showcase__note--b showcase__note--ok" aria-hidden="true">
                <i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 13 4 4 10-11"/></svg></i>
                <div><b>Запуск за 3–7 днів</b><span>сайт + перша кампанія</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
''')

# ------------------------------------------------------------------ strip
PROJECTS = ["Ferdinant", "Noirveil", "Yes or Not", "SlimLab", "Kyparis", "Jaydee"]
ARROW_UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'
cells = "\n".join(
    f'          <a class="strip__cell" href="portfolio.html">{p} {ARROW_UP}</a>' for p in PROJECTS)
write("strip.html", f'''    <!-- ================= ПРОЄКТИ ================= -->
    <section>
      <div class="shell">
        <div class="strip" aria-label="Проєкти, які ми зробили">
{cells}
        </div>
      </div>
    </section>
''')

# ------------------------------------------------------------------ process
STEPS = [
    ("01", "Аналіз", "Ніша · конкуренти · аудиторія"),
    ("02", "Сайт", "Структура · дизайн · розробка"),
    ("03", "Реклама", "Google Ads · аналітика · запуск"),
    ("04", "Оптимізація", "Аналізуємо результати та покращуємо кампанії"),
]
step_cells = "\n".join(f'''          <article class="cell" data-reveal>
            <span class="cell__num">{n}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>''' for n, t, d in STEPS)

write("process.html", f'''    <!-- ================= ПРОЦЕС ================= -->
    <section class="section rule" id="process">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">Процес</span>
          <h2>Запускаємо бізнес в інтернеті під ключ. <span class="tt">Від аналізу ніші до перших звернень.</span></h2>
          <p class="lead">
            Аналізуємо вашу нішу та конкурентів, продумуємо структуру, створюємо сайт,
            налаштовуємо рекламу та допомагаємо запустити <strong>весь процес від ідеї до перших звернень</strong>.
          </p>
        </div>
      </div>
      <div class="shell shell--bleed">
        <div class="cells cells--4">
{step_cells}
        </div>
      </div>
      <div class="shell">
        <a class="section-link" href="#services" data-reveal>
          <span>Подивитися, що входить у кожну послугу</span>
          <span class="arrow-loop">→</span>
        </a>
      </div>
    </section>
''')

# ------------------------------------------------------------------ advantages
VIZ_SITE = '''            <div class="viz viz--demo" aria-hidden="true">
              <div class="viz__bar"><i></i><i></i><i></i></div>
              <div class="viz__body">
                <div class="viz__line viz__line--w70"></div>
                <div class="viz__line viz__line--w45 viz__line--accent"></div>
                <div class="viz__row"><span class="viz__box"></span><span class="viz__box"></span><span class="viz__box"></span></div>
                <div><span class="viz__cta">Залишити заявку</span></div>
              </div>
              <span class="viz__cursor">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 3l14 8-6.2 1.6L10 19 5 3z"/></svg>
              </span>
            </div>'''

VIZ_SEARCH = '''            <div class="viz" aria-hidden="true">
              <div class="viz__search">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
                барбершоп київ
              </div>
              <div class="viz__ad"><b>Реклама</b> ваш сайт · послуги та запис онлайн</div>
            </div>'''

VIZ_CHART = '''            <div class="viz" aria-hidden="true">
              <div class="viz__chart"><span></span><span></span><span></span><span></span><span></span></div>
            </div>'''

VIZ_PRICE = '''            <div class="viz" aria-hidden="true">
              <div class="viz__price"><span>Сайт + Google Ads</span><strong>9 999 ₴</strong></div>
            </div>'''

ADV = [
    ("""<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/></svg>""",
     "Не просто дизайн", "Створюємо сайт під конкретні цілі вашого бізнесу.", VIZ_SITE),
    ("""<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="2"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2"/></svg>""",
     "Все в одному місці",
     "Сайт, реклама, аналітика та motion без необхідності шукати кількох підрядників.",
     '''            <div class="chips">
              <span class="chip">Сайт</span><span class="chip">Google Ads</span>
              <span class="chip">Аналітика</span><span class="chip">Motion</span>
              <span class="chip">SEO-підготовка</span>
            </div>'''),
    ("""<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg>""",
     "Швидкий запуск", "Перший запуск сайту — від 3–7 днів для відповідних проєктів.", VIZ_CHART),
    ("""<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>""",
     "Прозора ціна", "Ви заздалегідь знаєте, що входить у вартість.", VIZ_PRICE),
]
adv_cells = "\n".join(f'''          <article class="cell" data-reveal>
            <span class="icon-tile" aria-hidden="true">{icon}</span>
            <h3>{t}</h3>
            <p>{d}</p>
{viz}
          </article>''' for icon, t, d, viz in ADV)

write("bento.html", f'''    <!-- ================= ПЕРЕВАГИ ================= -->
    <section class="section section--alt rule" id="why">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">Переваги</span>
          <h2>Чому саме ми? <span class="tt">Тому що сайт для нас — інструмент продажів, а не картинка.</span></h2>
          <p class="lead">
            В Aster Digital ми не обмежуємося візуальною подачею — продумуємо сайт як
            <strong>інструмент продажів</strong>: від структури та текстів до реклами й аналітики.
          </p>
        </div>
      </div>
      <div class="shell shell--bleed">
        <div class="cells cells--2">
{adv_cells}
        </div>
      </div>
      <div class="shell">
        <a class="section-link" href="#packages" data-reveal>
          <span>Переглянути пакети та ціни</span>
          <span class="arrow-loop">→</span>
        </a>
      </div>
    </section>
''')

# ------------------------------------------------------------------ system
write("system.html", '''    <!-- ================= СИСТЕМА ЗАЛУЧЕННЯ ================= -->
    <section class="section rule" id="system">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">Навіщо сайт</span>
          <h2>Сайт без реклами ≠ система залучення клієнтів. <span class="tt">Порівняйте два шляхи клієнта.</span></h2>
          <p class="lead">
            Соцмережі можуть бути частиною продажів. Але власний сайт дає вам <strong>окрему точку контакту
            з клієнтом</strong>, яку можна використовувати в рекламі та пошуку.
          </p>
        </div>
      </div>
      <div class="shell shell--bleed">
        <div class="cells cells--2">
          <article class="cell path" data-reveal>
            <span class="path__tag">Тільки профіль у соцмережах</span>
            <ol class="path__steps">
              <li>Людина знаходить профіль</li>
              <li>Шукає потрібну інформацію серед постів</li>
              <li>Не бачить чіткої пропозиції та умов</li>
              <li>Відкладає рішення або йде далі</li>
            </ol>
            <p class="path__note">Ви залежите від того, наскільки зручно людині шукати відповіді у стрічці.</p>
          </article>

          <article class="cell path path--accent" data-reveal>
            <span class="path__tag">Сайт + Google Ads</span>
            <ol class="path__steps">
              <li>Людина шукає послугу в Google</li>
              <li>Бачить ваше оголошення за своїм запитом</li>
              <li>Потрапляє на сторінку з відповіддю на цей запит</li>
              <li>Бачить пропозицію та залишає заявку</li>
            </ol>
            <p class="path__note">Ви контролюєте пропозицію, шлях клієнта та бачите, звідки приходять заявки.</p>
          </article>
        </div>
      </div>
    </section>
''')

# ------------------------------------------------------------------ lead magnet
write("leadmagnet.html", '''    <!-- ================= ЛІД-МАГНІТ ================= -->
    <section class="section rule">
      <div class="shell">
        <div class="head head--center" data-reveal>
          <span class="tag tag--ok">Безкоштовно</span>
          <h2>Хочете дізнатися, як ваш бізнес виглядає <span class="tt">на фоні конкурентів?</span></h2>
          <p class="lead" style="margin-inline:auto">
            Безкоштовно проаналізуємо вашу нішу, конкурентів та присутність бізнесу в інтернеті.
            Покажемо, <strong>що можна покращити</strong> та з чого варто почати.
          </p>
          <p style="margin-top:28px">
            <button class="btn btn--accent btn--lg" data-modal-open data-modal-topic="Безкоштовний аналіз ніші">
              Отримайте безкоштовний аналіз
            </button>
          </p>
        </div>
      </div>
    </section>
''')

# ------------------------------------------------------------------ pricing
PKG1 = ["Аналіз ніші", "Аналіз конкурентів", "Сучасний адаптивний сайт", "Базова SEO-підготовка",
        "Налаштування Google Ads", "Запуск першої рекламної кампанії", "7 днів супроводу"]
PKG2 = ["Поглиблений аналіз ніші", "Складніша структура сайту", "Адаптивний дизайн",
        "Розширені функціональні можливості", "Поглиблене налаштування Google Ads",
        "Motion-анімації", "Аналітика"]

write("pricing.html", f'''    <!-- ================= ПАКЕТИ ================= -->
    <section class="section section--alt rule" id="packages">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">Пакети послуг</span>
          <h2>Оберіть, що потрібно вашому бізнесу. <span class="tt">Ціна відома заздалегідь.</span></h2>
        </div>
      </div>
      <div class="shell shell--bleed">
        <div class="pkgs">
          <article class="pkg pkg--featured" data-reveal>
            <span class="pkg__badge">РЕКОМЕНДОВАНО</span>
            <h3 class="pkg__title">Сайт + Google Ads</h3>
            <p class="pkg__price">
              <span class="pkg__amount">9 999 ₴</span>
              <span class="pkg__term">3–7 днів</span>
            </p>
            <ul class="checklist">
{checks(PKG1)}
            </ul>
            <p class="pkg__note">* Рекламний бюджет сплачується окремо.</p>
            <button class="btn btn--primary btn--wide btn--lg pkg__cta" data-modal-open data-modal-topic="Сайт + Google Ads — 9 999 ₴">Замовити</button>
          </article>

          <article class="pkg" data-reveal>
            <h3 class="pkg__title">Складний сайт + Google Ads</h3>
            <p class="pkg__price">
              <span class="pkg__amount">18 999 ₴</span>
              <span class="pkg__term">5–10 днів</span>
            </p>
            <ul class="checklist">
{checks(PKG2)}
            </ul>
            <button class="btn btn--ghost btn--wide btn--lg pkg__cta" data-modal-open data-modal-topic="Складний сайт + Google Ads — 18 999 ₴">Обговорити проєкт</button>
          </article>
        </div>
      </div>
    </section>
''')

# ------------------------------------------------------------------ services (vertical tabs)
MOTION_SPLIT = '''            <div class="svc__split">
              <div class="svc__branch">
                <span class="svc__branch-tag">Напрям 1</span>
                <h4>Motion для сайту та бренду</h4>
                <p>Перетворюємо статичний бренд на єдину візуальну систему в русі. Анімуємо логотип,
                  елементи айдентики та графіку сайту так, щоб бренд виглядав цілісно — від першого
                  екрана до мікроанімацій.</p>
                <p class="svc__branch-why">Motion допомагає зробити взаємодію з брендом впізнаваною
                  та послідовною, а сайт — більш виразним і живим.</p>
              </div>
              <div class="svc__branch">
                <span class="svc__branch-tag">Напрям 2</span>
                <h4>Motion для реклами та соцмереж</h4>
                <p>Показуємо ваш продукт у русі, щоб його було легше помітити та зрозуміти. Створюємо
                  короткі анімовані рекламні ролики, product-анімації та контент для Reels, Stories
                  і рекламних кампаній.</p>
                <p class="svc__branch-why">Замість статичної картинки показуємо продукт, його функції
                  або переваги через рух і короткий сценарій: товар → відкривається → показуємо
                  функцію → демонструємо перевагу → CTA.</p>
              </div>
            </div>
'''

SERVICES = [
    dict(id="web", index="01 — WEB", nav="Створення сайтів", navsub="Landing page та складні проєкти",
         title="Створення сайтів",
         tagline="Сайти, які працюють на залучення клієнтів, а не просто красиво виглядають.",
         price="від 9 999 ₴", term="3–7 днів",
         what="В Aster Digital ми продумуємо сайт як інструмент продажів: формуємо сильну пропозицію, "
              "вибудовуємо структуру, додаємо необхідні елементи довіри та скорочуємо шлях клієнта від "
              "першого відвідування до заявки. Після запуску можемо підключити Google Ads і приводити "
              "потенційних клієнтів прямо на розроблений для вас сайт.",
         why="Сайт стає вашою власною точкою контакту з клієнтом, де ви контролюєте пропозицію, "
             "інформацію про бізнес та шлях до заявки.",
         gets=["Структуру сторінки під вашу пропозицію",
               "Сучасний адаптивний дизайн під мобільні та десктоп",
               "Тексти та блоки довіри: послуги, роботи, контакти",
               "Форми заявки та зручні способи звʼязку",
               "Базову SEO-підготовку під пошук",
               "Готовність підключити Google Ads одразу після запуску"],
         result="Ви отримуєте власний майданчик, на який можна вести рекламний і пошуковий трафік, "
                "і де клієнту зрозуміло, що ви пропонуєте та як залишити заявку.",
         note=None, cta="Замовити сайт", topic="Тільки сайт", extra=""),

    dict(id="ads", index="02 — ADS", nav="Google Ads", navsub="Реклама в пошуку під запит клієнта",
         title="Google Ads",
         tagline="Допомагаємо потенційним клієнтам знаходити ваш бізнес саме тоді, коли вони шукають послугу.",
         price="від 5 999 ₴", term="запуск під ключ",
         what="Аналізуємо нішу та попит, налаштовуємо рекламні кампанії, підключаємо аналітику та "
              "направляємо рекламний трафік на сторінку, яка відповідає запиту клієнта.",
         why="Якщо людина вже шукає вашу послугу, реклама дозволяє показати їй вашу пропозицію "
             "саме в цей момент, а не чекати, поки вона випадково знайде ваш бізнес.",
         gets=["Аналіз ніші, попиту та конкурентів",
               "Пошукові запити й мінус-слова під ваші послуги",
               "Налаштовані та запущені кампанії в Google Ads",
               "Підключену аналітику та відстеження заявок",
               "Звʼязку «запит → оголошення → відповідна сторінка»",
               "Подальшу оптимізацію за результатами перших тижнів"],
         result="Працюємо на залучення цільового трафіку та заявок: вашу пропозицію бачать люди "
                "з активним запитом, а рішення щодо кампаній ухвалюємо на основі аналітики.",
         note="Рекламний бюджет сплачується окремо напряму в Google. Кількість клієнтів залежить "
              "від ніші, попиту та бюджету, тому ми не обіцяємо гарантованих цифр.",
         cta="Замовити рекламу", topic="Тільки Google Ads", extra=""),

    dict(id="motion", index="03 — MOTION", nav="Motion Design", navsub="Анімації для бренду та реклами",
         title="Motion Design",
         tagline="Оживляємо бренд і продукт: від айдентики сайту до рекламних роликів і контенту для соцмереж.",
         price="від 4 999 ₴", term="за проєкт",
         what="Motion у нас — це два напрями: анімація бренду та інтерфейсу сайту, а також короткі "
              "анімовані ролики для реклами, Reels і Stories.",
         why="Рух робить бренд впізнаваним і послідовним, а продукт — зрозумілішим: замість "
             "статичної картинки людина бачить, як він працює.",
         gets=["Анімований логотип та елементи айдентики",
               "Мікроанімації та переходи для сайту",
               "Product-анімації, що показують функції та переваги",
               "Короткі рекламні ролики за сценарієм",
               "Формати під Reels, Stories та рекламні кампанії"],
         result="Бренд виглядає цілісно в русі, а рекламні матеріали легше помітити та зрозуміти "
                "за перші секунди перегляду.",
         note=None, cta="Замовити Motion", topic="Motion Design", extra=MOTION_SPLIT),
]

rail = "\n".join(
    f'''            <button class="vtabs__btn" id="tab-{s["id"]}" role="tab" aria-controls="panel-{s["id"]}"
              aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">
              {s["nav"]}<small>{s["navsub"]}</small>
            </button>''' for i, s in enumerate(SERVICES))

panels = []
for i, s in enumerate(SERVICES):
    note = f'\n                <p class="svc__note">{s["note"]}</p>' if s["note"] else ""
    panels.append(f'''            <div class="vtabs__panel" id="panel-{s["id"]}" role="tabpanel" aria-labelledby="tab-{s["id"]}" tabindex="0"{"" if i == 0 else " hidden"}>
              <div class="svc__top">
                <div>
                  <span class="svc__index">{s["index"]}</span>
                  <h3 class="svc__title">{s["title"]}</h3>
                  <p class="svc__tagline">{s["tagline"]}</p>
                </div>
                <p class="svc__price"><strong>{s["price"]}</strong><span>{s["term"]}</span></p>
              </div>

              <div class="svc__grid">
                <div class="svc__col">
                  <h4>Що це</h4>
                  <p>{s["what"]}</p>
                </div>
                <div class="svc__col">
                  <h4>Навіщо це бізнесу</h4>
                  <p>{s["why"]}</p>
                </div>
              </div>

{s["extra"]}              <div class="svc__grid">
                <div class="svc__col">
                  <h4>Що ви отримаєте</h4>
                  <ul class="checklist">
{checks(s["gets"], 20)}
                  </ul>
                </div>
                <div class="svc__col">
                  <h4>Який результат це має дати</h4>
                  <p>{s["result"]}</p>{note}
                </div>
              </div>

              <div class="svc__foot">
                <p class="svc__from"><span>Вартість</span><strong>{s["price"]}</strong></p>
                <button class="btn btn--primary btn--lg" data-modal-open data-modal-topic="{s["topic"]}">{s["cta"]} <span class="btn__arrow">→</span></button>
              </div>
            </div>''')

write("services.html", f'''    <!-- ================= ПОСЛУГИ ================= -->
    <section class="section rule" id="services">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">Наші послуги</span>
          <h2>Що вам потрібно? <span class="tt">Оберіть напрям — і побачите повну картку послуги.</span></h2>
          <p class="lead">
            Усередині кожної картки: що це, навіщо це бізнесу, <strong>що саме ви отримаєте</strong>,
            якого результату очікувати та скільки це коштує.
          </p>
        </div>
      </div>
      <div class="shell shell--bleed">
        <div class="vtabs">
          <div class="vtabs__rail" role="tablist" aria-label="Наші послуги" aria-orientation="vertical">
{rail}
          </div>
          <div class="vtabs__panels">
{chr(10).join(panels)}
          </div>
        </div>
      </div>
    </section>
''')

# ------------------------------------------------------------------ after
AFTER = [
    ("01", "Розбираємося у вашому бізнесі", "Що продаєте, кому, як зараз приходять клієнти та що вже пробували."),
    ("02", "Аналізуємо нішу та задачу", "Дивимося на попит, конкурентів і те, як вас бачить клієнт у пошуку."),
    ("03", "Пропонуємо оптимальний формат", "Показуємо, що доцільно зробити першим кроком, зі строками та вартістю."),
    ("04", "Створюємо та запускаємо", "Робимо сайт, налаштовуємо рекламу й аналітику, узгоджуємо на кожному етапі."),
    ("05", "Аналізуємо перші результати", "Дивимося на дані після запуску та коригуємо сторінку й кампанії."),
]
after_rows = "\n".join(f'''          <li class="flow__item" data-reveal>
            <span class="flow__num">{n}</span>
            <div>
              <h3>{t}</h3>
              <p>{d}</p>
            </div>
          </li>''' for n, t, d in AFTER)

write("after.html", f'''    <!-- ================= ПІСЛЯ ЗАЯВКИ ================= -->
    <section class="section section--alt rule" id="after">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">Далі</span>
          <h2>Що відбувається після заявки? <span class="tt">Ніяких зобовʼязань на першому кроці.</span></h2>
          <p class="lead">
            Спочатку розбираємося в задачі, а вже потім пропонуємо <strong>формат і вартість</strong>.
          </p>
        </div>
      </div>
      <div class="shell shell--bleed">
        <ol class="flow">
{after_rows}
        </ol>
      </div>
    </section>
''')

# ------------------------------------------------------------------ faq
FAQ = [
    ("Скільки коштує сайт?",
     "Створення сайту — від 9 999 ₴. Точна вартість залежить від структури, функціональності та обсягу роботи."),
    ("Скільки часу займає розробка?",
     "Типовий сайт запускаємо приблизно за 3–7 днів. Складніші проєкти можуть потребувати більше часу."),
    ("Чи входить рекламний бюджет?",
     "Ні. У вартість входить повне налаштування та ведення реклами. Рекламний бюджет сплачується "
     "окремо напряму в Google, і ви завжди бачите, скільки витрачено."),
    ("Чи можна замовити тільки сайт?",
     "Так. Також можна замовити тільки рекламу на вже існуючий сайт або тільки motion-анімації."),
    ("Чи працюєте ви з існуючими сайтами?",
     "Так. Можемо доопрацювати структуру та сторінки під рекламу або підключити Google Ads "
     "до сайту, який у вас уже є."),
    ("Чи можна замовити тільки рекламу?",
     "Так — від 5 999 ₴. Перед запуском подивимося, чи готова сторінка приймати трафік, "
     "і скажемо, що варто підправити."),
    ("Чи можна зробити motion для мого бренду?",
     "Так. Анімуємо логотип та айдентику, робимо мікроанімації для сайту, а також ролики "
     "для реклами, Reels і Stories."),
    ("Чи гарантуєте ви кількість клієнтів?",
     "Ні, і не обіцяємо цифр наперед: результат залежить від ніші, попиту та бюджету. "
     "Ми працюємо на залучення цільового трафіку та заявок і ухвалюємо рішення на основі аналітики."),
]
faq_rows = "\n".join(f'''          <div class="faq__item">
            <h3><button class="faq__q" aria-expanded="false" aria-controls="faq-a{i}" id="faq-q{i}">{q}<span class="faq__icon" aria-hidden="true"></span></button></h3>
            <div class="faq__a" id="faq-a{i}" role="region" aria-labelledby="faq-q{i}"><div><p>{a}</p></div></div>
          </div>''' for i, (q, a) in enumerate(FAQ, 1))

write("faq.html", f'''    <!-- ================= FAQ ================= -->
    <section class="section rule" id="faq">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">FAQ</span>
          <h2>Часті запитання. <span class="tt">Відповідаємо прямо.</span></h2>
        </div>
      </div>
      <div class="shell shell--bleed">
        <div class="faq">
{faq_rows}
        </div>
      </div>
      <div class="shell">
        <button class="section-link" data-modal-open data-reveal>
          <span>Не знайшли відповідь? Запитайте нас напряму</span>
          <span class="arrow-loop">→</span>
        </button>
      </div>
    </section>
''')

# ------------------------------------------------------------------ portfolio
CASES = [
    ('ferdinant', 'Ferdinant Barbershop', 'Сайт · Google Ads',
     'Барбершопу потрібна була власна точка контакту з клієнтом замість профілю в соцмережах.',
     'Зробили сайт-візитівку з чіткою пропозицією, послугами, роботами майстрів і онлайн-записом, '
     'та підготували сторінку під пошукову рекламу.',
     'Клієнт бачить умови й записується прямо на сайті, а сторінка готова приймати рекламний трафік.',
     'eager'),
    ('noirveil', 'Noirveil', 'E-commerce · Motion',
     'Бренду одягу був потрібен магазин, який передає характер бренду й не гальмує на мобільних.',
     'Побудували каталог із швидкою навігацією, вибудували картку товару та додали motion-переходи в айдентиці бренду.',
     'Єдина візуальна подача бренду й зрозумілий шлях від каталогу до кошика.', 'eager'),
    ('yesornot', 'Yes or Not', 'E-commerce',
     'Streetwear-бренд заходив переважно з мобільного трафіку соцмереж.',
     'Спроєктували структуру під продажі: акцент на добірках, короткий шлях до товару, адаптив під мобільний екран у пріоритеті.',
     'Мобільний користувач доходить від першого екрана до товару за кілька кроків.', 'lazy'),
    ('slimlab', 'SlimLab', 'Сайт · Аналітика',
     'У медичному напрямі клієнту важливо швидко зрозуміти суть послуги та умови.',
     'Розклали послуги зрозумілими блоками, додали елементи довіри й форми запису, підключили наскрізну аналітику.',
     'Заявки приходять із зафіксованим джерелом, тому видно, які сторінки працюють.', 'lazy'),
    ('kyparis', 'Kyparis', 'Сайт · SEO',
     'Бренду був потрібен іміджевий сайт, який добре виглядає й індексується пошуком.',
     'Зробили стриману типографічну подачу та базову SEO-підготовку: структура заголовків, метадані, швидкість завантаження.',
     'Сайт коректно віддається пошуку й тримає єдиний візуальний стиль бренду.', 'lazy'),
    ('jaydee', 'Jaydee Mediakit', 'Landing · Motion',
     'Інфлюенсеру потрібно було показувати статистику й формати співпраці рекламодавцям.',
     'Зібрали цифровий медіакіт: динамічна подача цифр, кейси та формати розміщення на одній сторінці.',
     'Замість файлу-презентації — посилання, яке можна відправити рекламодавцю в будь-який момент.', 'lazy'),
]
work_cells = "\n".join(f'''          <article class="work" data-reveal>
            <div class="work__shot"><img src="public/assets/screenshots/{s}.webp" alt="{n} — проєкт Aster Digital" loading="{l}" /></div>
            <div class="work__body">
              <span class="work__tag">{t}</span>
              <h3>{n}</h3>
              <dl class="case">
                <dt>Задача</dt><dd>{task}</dd>
                <dt>Рішення</dt><dd>{sol}</dd>
                <dt>Результат</dt><dd>{res}</dd>
              </dl>
            </div>
          </article>''' for s, n, t, task, sol, res, l in CASES)

write("portfolio.html", f'''    <section class="page-head">
      <div class="shell">
        <div data-hero>
          <span class="tag">Портфоліо</span>
          <h1>Роботи, створені <span class="tt">під конкретні бізнес-задачі</span></h1>
          <p class="lead">
            Для кожного проєкту показуємо, з якою задачею прийшов клієнт, що ми зробили
            та що це дало. <strong>Без вигаданих цифр</strong> — лише те, що можемо підтвердити.
          </p>
        </div>
      </div>
    </section>

    <section>
      <div class="shell">
        <div class="works">
{work_cells}
        </div>
      </div>
    </section>
''')

print("done")

# ------------------------------------------------------------------ motion demo
# The stage is built in code so the comparison is honest. To show real work,
# drop files into public/assets/motion/ and swap .stage__shot / .reel__screen
# for <video autoplay muted loop playsinline poster="...">.
write("motion.html", '''    <!-- ================= MOTION У ДІЇ ================= -->
    <section class="section rule" id="motion">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">Motion у дії</span>
          <h2>Один і той самий екран. <span class="tt">Перемкніть — і побачите різницю.</span></h2>
          <p class="lead">
            Motion не про «красиво рухається». Він веде око по сторінці, показує продукт у дії
            та <strong>підказує, куди натиснути</strong>. Нижче — той самий блок без анімації та з нею.
          </p>
        </div>
      </div>

      <div class="shell shell--bleed">
        <div class="motion is-motion" id="motionDemo">
          <div class="motion__bar">
            <div class="seg" role="group" aria-label="Режим показу">
              <button type="button" class="seg__btn" data-motion="off">Без motion</button>
              <button type="button" class="seg__btn is-on" data-motion="on" aria-pressed="true">З motion</button>
            </div>
            <p class="motion__hint">Сцена повторюється по колу</p>
          </div>

          <div class="motion__grid">
            <figure class="stage">
              <figcaption class="stage__cap">Перший екран сайту</figcaption>
              <div class="stage__frame">
                <div class="stage__bar" aria-hidden="true"><i></i><i></i><i></i></div>
                <div class="stage__shot" aria-hidden="true">
                  <span class="stage__tag">Барбершоп у Києві</span>
                  <span class="stage__h l1"></span>
                  <span class="stage__h l2"></span>
                  <span class="stage__pic"></span>
                  <span class="stage__cta">Записатися</span>
                  <span class="stage__chip">Вільно сьогодні</span>
                </div>
              </div>
            </figure>

            <figure class="reel">
              <figcaption class="stage__cap">Ролик для Reels та реклами</figcaption>
              <div class="reel__phone">
                <div class="reel__screen" aria-hidden="true">
                  <span class="reel__step s1">Товар</span>
                  <span class="reel__box"></span>
                  <span class="reel__step s2">Функція</span>
                  <span class="reel__step s3">Перевага</span>
                  <span class="reel__cta">Замовити →</span>
                </div>
              </div>
            </figure>
          </div>

          <div class="motion__notes">
            <div class="motion__note">
              <h3>Без motion</h3>
              <p>Усе з’являється одночасно. Око саме шукає, з чого почати й що тут головне.</p>
            </div>
            <div class="motion__note">
              <h3>З motion</h3>
              <p>Сцена веде за собою: спершу пропозиція, далі продукт, наприкінці — кнопка.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="shell">
        <a class="section-link" href="#panel-motion" data-reveal>
          <span>Подивитися, що входить у Motion Design</span>
          <span class="arrow-loop">→</span>
        </a>
      </div>
    </section>
''')
