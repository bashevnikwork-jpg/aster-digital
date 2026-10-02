#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static page builder for SkyBreeze.

Shell (topbar, nav, footer, contact modal, closing CTA) lives here once and is
stamped into every page. All editable business content is read from content/*.json
so it can be driven from Google Drive — see sync_drive.py and CONTENT-EDITING.md.

    python3 parts.py && python3 build.py
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent
PARTS = ROOT / "parts"
CONTENT = ROOT / "content"
NL = "\n"


def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


SITE = load("site.json")
GTM_ID = SITE["gtm_id"]

# The brand mark: two rounded parallelograms split by a diagonal negative-space
# channel, on the SkyBreeze blue gradient. Fixed colour (the wordmark carries the
# light/dark theme). The gradient id is shared; duplicate ids across inlined copies
# resolve to the first, which is intended — every mark takes the same gradient.
MARK = ('<svg class="mark" viewBox="0 0 110 96" aria-hidden="true">'
        '<defs><linearGradient id="sbMark" x1="0.05" y1="0" x2="0.5" y2="1">'
        '<stop offset="0" stop-color="#4C93FF"/><stop offset="0.55" stop-color="#2266EE"/>'
        '<stop offset="1" stop-color="#123FCC"/></linearGradient></defs>'
        '<g fill="url(#sbMark)" stroke="url(#sbMark)" stroke-width="6" stroke-linejoin="round">'
        '<polygon points="30,12 88,12 64,46 6,46"/>'
        '<polygon points="80,84 22,84 46,50 104,50"/></g>'
        '</svg>')


def logo(context="nav"):
    return (f'<a href="index.html" class="logo logo--{context}" aria-label="{SITE["brand"]} — на головну">'
            f'<span class="logo__mark">{MARK}</span>'
            f'<span class="logo__word">{SITE["brand"]}</span></a>')


GTM_HEAD = (
    '  <!-- Google Tag Manager -->\n'
    '  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({\'gtm.start\':\n'
    'new Date().getTime(),event:\'gtm.js\'});var f=d.getElementsByTagName(s)[0],\n'
    'j=d.createElement(s),dl=l!=\'dataLayer\'?\'&l=\'+l:\'\';j.async=true;j.src=\n'
    '\'https://www.googletagmanager.com/gtm.js?id=\'+i+dl;f.parentNode.insertBefore(j,f);\n'
    f'}})(window,document,\'script\',\'dataLayer\',\'{GTM_ID}\');</script>\n'
    '  <!-- End Google Tag Manager -->\n'
)
GTM_NOSCRIPT = (
    '  <!-- Google Tag Manager (noscript) -->\n'
    f'  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
    'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
    '  <!-- End Google Tag Manager (noscript) -->\n'
)


def head(title, desc, extra=""):
    return (f'''<!DOCTYPE html>
<html lang="{SITE["lang"]}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{GTM_HEAD}  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#0B0F14" />
  <link rel="icon" href="public/brand/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="public/apple-touch-icon.png" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{SITE["brand"]}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://{SITE["domain"]}/" />
  <meta property="og:image" content="https://{SITE["domain"]}/public/brand/og.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{SITE["brand"]} — сайт + Google Ads для бізнесу" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://{SITE["domain"]}/public/brand/og.png" />
{extra}  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <script>document.documentElement.classList.add('js');</script>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
{GTM_NOSCRIPT}  <div class="grain" aria-hidden="true"></div>
  <a class="skip-link" href="#main">Перейти до основного вмісту</a>
''')


def nav(current):
    links, sheet = [], []
    for item in SITE["nav"]:
        label, href, page = item["label"], item["href"], item["page"]
        target = href if (page == current or not href.startswith('#')) else 'index.html' + href
        cur = ' aria-current="page"' if (page == current and not href.startswith('#')) else ''
        links.append(f'          <a href="{target}"{cur}>{label}</a>')
        sheet.append(f'      <a href="{target}">{label}</a>')
    promo = ('#packages' if current == 'index.html' else 'index.html#packages')
    phone = SITE["phone"]; phone_href = SITE["phone_href"]
    return f'''
  <div class="topbar">
    <a href="{promo}">{SITE["topbar"]} <span class="btn__arrow">→</span></a>
  </div>

  <header class="nav" id="nav">
    <div class="nav__inner">
      {logo("nav")}

      <nav class="nav__links" aria-label="Основна навігація">
{NL.join(links)}
      </nav>

      <div class="nav__right">
        <a class="nav__phone" href="tel:{phone_href}" aria-label="Зателефонувати {phone}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.5 3h3l1.5 4-2 1.4a12 12 0 0 0 5.6 5.6L16 12l4 1.5v3a2 2 0 0 1-2.2 2A16.8 16.8 0 0 1 3 6.2 2 2 0 0 1 5 4z"/></svg><span>{phone}</span>
        </a>
        <button class="btn btn--primary" data-modal-open>{SITE["cta_button"]} <span class="btn__arrow">→</span></button>
        <button class="nav__burger" id="navBurger" aria-label="Відкрити меню" aria-expanded="false" aria-controls="navSheet">
          <span></span><span></span>
        </button>
      </div>
    </div>
    <span class="nav__progress" id="navProgress" aria-hidden="true"></span>
  </header>

  <div class="nav__sheet" id="navSheet">
    <nav aria-label="Мобільна навігація">
{NL.join(sheet)}
    </nav>
    <button class="btn btn--primary btn--lg btn--wide" data-modal-open>{SITE["cta_button"]} <span class="btn__arrow">→</span></button>
  </div>
'''


def footer():
    f = SITE["footer"]
    return f'''
  <footer class="footer band band--dark" data-nav-dark>
    <div class="shell">
      <div class="footer__grid">
        <div class="footer__about">
          {logo("footer")}
          <p>{f["about"]}</p>
          <button class="btn btn--primary" data-modal-open>{SITE["cta_button"]} <span class="btn__arrow">→</span></button>
        </div>
        <div class="footer__col">
          <h4>Сайт</h4>
          <a href="index.html">Головна сторінка</a>
          <a href="index.html#services">Наші послуги</a>
          <a href="index.html#mission">Місія</a>
          <a href="index.html#packages">Пакети</a>
          <a href="portfolio.html">Портфоліо</a>
        </div>
        <div class="footer__col">
          <h4>Послуги</h4>
          <a href="index.html#panel-web">Створення сайтів</a>
          <a href="index.html#panel-ads">Google Ads</a>
          <a href="index.html#panel-motion">Motion Design</a>
          <a href="index.html#panel-seo">SEO-оптимізація</a>
          <a href="index.html#panel-bots">Telegram-боти</a>
          <a href="index.html#panel-miniapp">Telegram Mini App</a>
        </div>
        <div class="footer__col">
          <h4>Контакти</h4>
          <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>
          <a href="{SITE["telegram_url"]}" target="_blank" rel="noopener">Telegram</a>
          <a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a>
          <a href="contacts.html">Форма заявки</a>
        </div>
      </div>
      <div class="footer__bottom">
        <span>{f["copyright"]}</span>
        <span>{f["location"]}</span>
      </div>
    </div>
  </footer>
'''


def form(prefix, note=True):
    opts = NL.join(f'            <option>{t}</option>' for t in SITE["form_topics"])
    tail = ('\n        <p class="form__note">Безкоштовна консультація · Без зобов\'язань</p>'
            if note else '')
    return f'''<div class="field">
          <label for="{prefix}Contact">Телефон або Telegram</label>
          <input id="{prefix}Contact" name="contact" type="text" autocomplete="tel" required />
        </div>
        <div class="field">
          <label for="{prefix}Topic">Що потрібно?</label>
          <select id="{prefix}Topic" name="topic">
{opts}
          </select>
        </div>
        <button class="btn btn--primary btn--wide btn--lg" type="submit">Надіслати заявку <span class="btn__arrow">→</span></button>{tail}'''


def modal():
    m = SITE["modal"]
    return f'''
  <div class="modal" id="contactModal" role="dialog" aria-modal="true" aria-labelledby="modalTitle" hidden>
    <div class="modal__backdrop" data-modal-close></div>
    <div class="modal__dialog">
      <button class="modal__close" type="button" aria-label="Закрити вікно" data-modal-close>✕</button>
      <h2 id="modalTitle">{m["title"]}</h2>
      <p class="modal__lead">{m["lead"]}</p>
      <form id="contactForm" novalidate>
        {form("f")}
        <p class="form__status" id="formStatus" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
'''


ACTIONBAR = f'''
  <div class="actionbar" id="actionBar">
    <span class="actionbar__price"><span>Сайт + Google Ads</span><strong>9 999 ₴</strong></span>
    <button class="btn btn--primary" data-modal-open>{SITE["cta_button"]} <span class="btn__arrow">→</span></button>
  </div>

  <a class="fab-call" href="tel:{SITE["phone_href"]}" aria-label="Зателефонувати {SITE["phone"]}">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.5 3h3l1.5 4-2 1.4a12 12 0 0 0 5.6 5.6L16 12l4 1.5v3a2 2 0 0 1-2.2 2A16.8 16.8 0 0 1 3 6.2 2 2 0 0 1 5 4z"/></svg>
  </a>
'''

TAIL = ACTIONBAR + '''
  <script src="script.js" defer></script>
</body>
</html>
'''


def cta(heading):
    c = SITE["cta"]
    return f'''
    <section class="cta band band--dark" data-nav-dark>
      <div class="channel channel--top" aria-hidden="true"></div>
      <div class="shell">
        <div class="cta__panel" data-reveal>
          <span class="cta__mark" aria-hidden="true">{MARK}</span>
          <h2>{heading}</h2>
          <p>{c["body"]}</p>
          <div class="cta__actions">
            <button class="btn btn--primary btn--lg" data-modal-open>{SITE["cta_button"]} <span class="btn__arrow">→</span></button>
            <a class="btn btn--line-ink btn--lg" href="contacts.html">Написати нам <span class="btn__arrow">→</span></a>
          </div>
          <p class="cta__note">{c["note"]}</p>
        </div>
      </div>
    </section>
'''


def part(name):
    return (PARTS / name).read_text(encoding="utf-8")


def build_index():
    return (
        head("SkyBreeze — Створення сайтів та Google Ads для бізнесу",
             "Створюємо сучасні сайти для бізнесу, налаштовуємо Google Ads та створюємо "
             "motion-дизайн. Аналіз ніші, розробка, запуск і оптимізація під ключ. Від 9 999 ₴.")
        + nav("index.html")
        + '\n  <main id="main">\n'
        + part("hero.html") + part("strip.html")
        + part("process.html") + part("bento.html") + part("system.html")
        + part("mission.html")
        + part("services.html") + part("pricing.html") + part("motion.html")
        + part("stack.html") + part("leadmagnet.html") + part("after.html") + part("faq.html")
        + cta(SITE["cta"]["index"])
        + '  </main>\n' + footer() + modal() + TAIL
    )


def build_portfolio():
    return (
        head("Портфоліо — SkyBreeze",
             "Роботи SkyBreeze: сайти для бізнесу, e-commerce, медіакіти та лендинги "
             "з налаштованою рекламою Google Ads.")
        + nav("portfolio.html")
        + '\n  <main id="main">\n' + part("portfolio.html")
        + cta(SITE["cta"]["portfolio"])
        + '  </main>\n' + footer() + modal() + TAIL
    )


def build_thanks():
    body = '''
    <section class="thanks band band--dark" data-nav-dark>
      <div class="shell">
        <div class="thanks__inner" data-hero>
          <span class="thanks__check" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>
          </span>
          <span class="tag tag--ok">Заявку прийнято</span>
          <h1>Дякуємо! <span class="tt">Ми вже отримали вашу заявку.</span></h1>
          <p class="lead">
            Зв’яжемося <strong>протягом робочого дня</strong> — уточнимо задачу та запропонуємо
            оптимальний варіант. Якщо питання термінове, телефонуйте просто зараз.
          </p>
          <div class="thanks__actions">
            <a class="btn btn--primary btn--lg" href="tel:''' + SITE["phone_href"] + '''">Зателефонувати <span class="btn__arrow">→</span></a>
            <a class="btn btn--line-ink btn--lg" href="''' + SITE["telegram_url"] + '''" target="_blank" rel="noopener">Написати в Telegram <span class="btn__arrow">→</span></a>
          </div>
        </div>
      </div>
    </section>

    <section class="section band band--light">
      <div class="shell shell--bleed">
        <ol class="flow">
          <li class="flow__item" data-reveal>
            <span class="flow__num">01</span>
            <div><h3>Читаємо заявку</h3><p>Дивимося, що ви написали про бізнес і яку задачу треба вирішити.</p></div>
          </li>
          <li class="flow__item" data-reveal>
            <span class="flow__num">02</span>
            <div><h3>Телефонуємо або пишемо</h3><p>Коротко уточнимо деталі — нішу, строки та що вже пробували.</p></div>
          </li>
          <li class="flow__item" data-reveal>
            <span class="flow__num">03</span>
            <div><h3>Надсилаємо пропозицію</h3><p>Формат роботи, строки та вартість — без зобов’язань з вашого боку.</p></div>
          </li>
        </ol>
      </div>
      <div class="shell">
        <a class="section-link" href="portfolio.html" data-reveal>
          <span>Поки чекаєте — подивіться наші роботи</span>
          <span class="arrow-loop">→</span>
        </a>
      </div>
    </section>
'''
    gate = (
        '  <meta name="robots" content="noindex, nofollow" />\n'
        "  <script>(function(){try{var raw=sessionStorage.getItem('skybreeze:lead');"
        "var ok=raw&&(Date.now()-parseInt(raw,10))<30*60*1000;"
        "if(!ok){location.replace('index.html');}}catch(e){}})();</script>\n"
    )
    return (
        head("Дякуємо за заявку — SkyBreeze",
             "Заявку прийнято. Зв'яжемося протягом робочого дня.",
             extra=gate)
        + nav("thanks.html")
        + '\n  <main id="main">\n' + body + '  </main>\n'
        + footer() + modal() + TAIL
    )


def build_contacts():
    body = f'''
    <section class="page-head band band--dark" data-nav-dark>
      <div class="shell">
        <div data-hero>
          <span class="tag">Контакти</span>
          <h1>Зв'язатися <span class="tt">з нами</span></h1>
          <p class="lead">
            Розкажіть про свій бізнес — ми безкоштовно проаналізуємо нішу, конкурентів
            та запропонуємо оптимальний варіант запуску.
          </p>
        </div>
      </div>
    </section>

    <section class="band band--light">
      <div class="shell">
        <div class="contact-grid">
          <div data-reveal>
            <h2 class="h-sm">Напишіть нам</h2>
            <ul class="contact-list">
              <li><a href="mailto:{SITE["email"]}"><span class="k">Email</span><span class="v">{SITE["email"]}</span></a></li>
              <li><a href="{SITE["telegram_url"]}" target="_blank" rel="noopener"><span class="k">Telegram</span><span class="v">{SITE["telegram_handle"]}</span></a></li>
              <li><a href="tel:{SITE["phone_href"]}"><span class="k">Телефон</span><span class="v">{SITE["phone"]}</span></a></li>
            </ul>
            <p class="small muted-note">
              Відповідаємо протягом робочого дня. Консультація безкоштовна та без зобов'язань.
            </p>
          </div>

          <div data-reveal>
            <h2 class="h-sm">Залишити заявку</h2>
            <p class="small form-card__lead">Заповніть коротку форму — ми зв'яжемося та запропонуємо рішення.</p>
            <form id="pageForm" novalidate>
              {form("p", note=False)}
              <p class="form__status" id="pageFormStatus" role="status" aria-live="polite"></p>
            </form>
          </div>
        </div>
      </div>
    </section>
'''
    return (
        head("Зв'язатися з нами — SkyBreeze",
             "Напишіть SkyBreeze: безкоштовна консультація, аналіз ніші та розрахунок "
             "вартості сайту й Google Ads.")
        + nav("contacts.html")
        + '\n  <main id="main">\n' + body + '  </main>\n'
        + footer() + modal() + TAIL
    )


if __name__ == "__main__":
    for name, builder in (("index.html", build_index),
                          ("portfolio.html", build_portfolio),
                          ("contacts.html", build_contacts),
                          ("thanks.html", build_thanks)):
        (ROOT / name).write_text(builder(), encoding="utf-8")
        print("wrote", name)
