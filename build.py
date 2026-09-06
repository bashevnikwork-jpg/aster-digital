#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static page builder for Astra Digital.

Topbar, nav, footer and the contact modal live here once and are stamped into
every page, so a header change no longer means editing three HTML files.

    python3 parts.py && python3 build.py
"""

import pathlib

ROOT = pathlib.Path(__file__).parent
PARTS = ROOT / "parts"

MARK_PATH = ("M 44.84 40.29 Q 45.20 21.60 52.01 2.04 Q 60.41 23.15 57.64 42.09 L 57.64 42.09 "
             "Q 75.52 36.66 96.23 37.09 Q 78.76 51.61 59.89 54.82 L 59.89 54.82 Q 70.58 70.15 "
             "76.56 89.98 Q 57.36 77.84 48.47 60.89 L 48.47 60.89 Q 37.19 75.80 20.18 87.62 "
             "Q 25.79 65.60 39.17 51.91 L 39.17 51.91 Q 21.51 45.79 5.01 33.27 Q 27.68 31.80 "
             "44.84 40.29 Z")

MARK = f'<svg viewBox="0 0 100 100" aria-hidden="true"><path d="{MARK_PATH}" fill="currentColor"/></svg>'

NAV_ITEMS = [
    ("Головна сторінка", "index.html", "index.html"),
    ("Наші послуги", "#services", "index.html"),
    ("Портфоліо", "portfolio.html", "portfolio.html"),
    ("Зв'язатися з нами", "contacts.html", "contacts.html"),
]

TOPICS = [
    "Сайт + Google Ads — 9 999 ₴",
    "Складний сайт + Google Ads — 18 999 ₴",
    "Тільки сайт",
    "Тільки Google Ads",
    "Motion Design",
    "Безкоштовний аналіз ніші",
]

NL = "\n"


def head(title, desc, extra=""):
    return f'''<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#FBFBF9" />
  <link rel="icon" href="public/favicon.svg" type="image/svg+xml" />
{extra}  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <script>document.documentElement.classList.add('js');</script>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="grain" aria-hidden="true"></div>
  <a class="skip-link" href="#main">Перейти до основного вмісту</a>
'''


def nav(current):
    links, sheet = [], []
    for label, href, page in NAV_ITEMS:
        target = href if (page == current or not href.startswith('#')) else 'index.html' + href
        cur = ' aria-current="page"' if (page == current and not href.startswith('#')) else ''
        links.append(f'          <a href="{target}"{cur}>{label}</a>')
        sheet.append(f'      <a href="{target}">{label}</a>')
    promo = ('#services' if current == 'index.html' else 'index.html#services')
    return f'''
  <div class="topbar">
    <a href="{promo}">Сайт + Google Ads від 9 999 ₴ — запуск реклами безкоштовно <span class="btn__arrow">→</span></a>
  </div>

  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="index.html" class="brand" aria-label="Astra Digital — на головну">
        <span class="brand__mark">{MARK}</span>
        <span class="brand__name">Astra Digital</span>
      </a>

      <nav class="nav__links" aria-label="Основна навігація">
{NL.join(links)}
      </nav>

      <div class="nav__right">
        <button class="btn btn--primary" data-modal-open>Обговорити проєкт <span class="btn__arrow">→</span></button>
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
    <button class="btn btn--primary btn--lg btn--wide" data-modal-open>Обговорити проєкт <span class="btn__arrow">→</span></button>
  </div>
'''


FOOTER = f'''
  <footer class="footer">
    <div class="shell">
      <div class="footer__grid">
        <div class="footer__about">
          <a href="index.html" class="brand">
            <span class="brand__mark">{MARK}</span>
            <span class="brand__name">Astra Digital</span>
          </a>
          <p>Створюємо сайти, налаштовуємо Google Ads і робимо motion — щоб бізнес отримував клієнтів з інтернету.</p>
          <button class="btn btn--ghost" data-modal-open>Обговорити проєкт <span class="btn__arrow">→</span></button>
        </div>
        <div class="footer__col">
          <h4>Сайт</h4>
          <a href="index.html">Головна сторінка</a>
          <a href="index.html#services">Наші послуги</a>
          <a href="index.html#packages">Пакети</a>
          <a href="portfolio.html">Портфоліо</a>
        </div>
        <div class="footer__col">
          <h4>Послуги</h4>
          <a href="index.html#services">Створення сайтів</a>
          <a href="index.html#services">Google Ads</a>
          <a href="index.html#services">Motion Design</a>
          <a href="index.html#faq">Часті запитання</a>
        </div>
        <div class="footer__col">
          <h4>Контакти</h4>
          <a href="mailto:hello@astradigital.agency">hello@astradigital.agency</a>
          <a href="https://t.me/astradigital" target="_blank" rel="noopener">Telegram</a>
          <a href="tel:+380000000000">+38 (000) 000-00-00</a>
          <a href="contacts.html">Форма заявки</a>
        </div>
      </div>
      <div class="footer__bottom">
        <span>© 2026 Astra Digital</span>
        <span>Київ · Працюємо з бізнесом по всій Україні</span>
      </div>
    </div>
  </footer>
'''


def form(prefix, note=True):
    opts = NL.join(f'            <option>{t}</option>' for t in TOPICS)
    tail = ('\n        <p class="form__note">Безкоштовна консультація · Без зобов\'язань</p>'
            if note else '')
    return f'''<div class="field">
          <label for="{prefix}Name">Ваше ім'я</label>
          <input id="{prefix}Name" name="name" type="text" autocomplete="name" required />
        </div>
        <div class="field">
          <label for="{prefix}Contact">Телефон або Telegram</label>
          <input id="{prefix}Contact" name="contact" type="text" autocomplete="tel" required />
        </div>
        <div class="field">
          <label for="{prefix}Topic">Що потрібно?</label>
          <select id="{prefix}Topic" name="topic">
{opts}
          </select>
        </div>
        <div class="field">
          <label for="{prefix}Message">Коротко про бізнес</label>
          <textarea id="{prefix}Message" name="message" rows="3"></textarea>
        </div>
        <button class="btn btn--primary btn--wide btn--lg" type="submit">Надіслати заявку <span class="btn__arrow">→</span></button>{tail}'''


MODAL = f'''
  <div class="modal" id="contactModal" role="dialog" aria-modal="true" aria-labelledby="modalTitle" hidden>
    <div class="modal__backdrop" data-modal-close></div>
    <div class="modal__dialog">
      <button class="modal__close" type="button" aria-label="Закрити вікно" data-modal-close>✕</button>
      <h2 id="modalTitle">Обговорити проєкт</h2>
      <p class="modal__lead">Залиште контакти — зв'яжемося протягом робочого дня та запропонуємо оптимальний варіант.</p>

      <form id="contactForm" novalidate>
        {form("f")}
        <p class="form__status" id="formStatus" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
'''

ACTIONBAR = '''
  <div class="actionbar" id="actionBar">
    <span class="actionbar__price"><span>Сайт + Google Ads</span><strong>від 9 999 ₴</strong></span>
    <button class="btn btn--primary" data-modal-open>Обговорити проєкт <span class="btn__arrow">→</span></button>
  </div>
'''

TAIL = ACTIONBAR + '''
  <script src="script.js" defer></script>
</body>
</html>
'''


def cta(heading):
    return f'''
    <section class="cta rule">
      <div class="shell">
        <div class="cta__panel" data-reveal>
          <span class="cta__mark">{MARK}</span>
          <h2>{heading}</h2>
          <p>Розкажіть нам про свій бізнес — ми проаналізуємо задачу та запропонуємо оптимальний варіант.</p>
          <div class="cta__actions">
            <button class="btn btn--on-ink btn--lg" data-modal-open>Обговорити проєкт <span class="btn__arrow">→</span></button>
            <a class="btn btn--on-ink-ghost btn--lg" href="contacts.html">Написати нам</a>
          </div>
          <p class="cta__note">Безкоштовна консультація · Без зобов'язань</p>
        </div>
      </div>
    </section>
'''


def part(name):
    return (PARTS / name).read_text(encoding="utf-8")


def build_index():
    return (
        head("Astra Digital — Створення сайтів та Google Ads для бізнесу",
             "Створюємо сучасні сайти для бізнесу, налаштовуємо Google Ads та створюємо "
             "motion-дизайн. Аналіз ніші, розробка, запуск і оптимізація під ключ. Від 9 999 ₴.",
             extra='  <meta property="og:type" content="website" />\n'
                   '  <meta property="og:title" content="Astra Digital — Створення сайтів та Google Ads для бізнесу" />\n'
                   '  <meta property="og:description" content="Сайт, реклама та motion під ключ. Від 9 999 ₴, запуск за 3–7 днів." />\n')
        + nav("index.html")
        + '\n  <main id="main">\n'
        + part("hero.html") + part("strip.html") + part("process.html") + part("bento.html")
        + part("system.html") + part("leadmagnet.html") + part("pricing.html")
        + part("services.html") + part("after.html") + part("faq.html")
        + cta("Готові запустити свій бізнес в інтернеті?")
        + '  </main>\n' + FOOTER + MODAL + TAIL
    )


def build_portfolio():
    return (
        head("Портфоліо — Astra Digital",
             "Роботи Astra Digital: сайти для бізнесу, e-commerce, медіакіти та лендинги "
             "з налаштованою рекламою Google Ads.")
        + nav("portfolio.html")
        + '\n  <main id="main">\n' + part("portfolio.html")
        + cta("Хочете такий самий результат?")
        + '  </main>\n' + FOOTER + MODAL + TAIL
    )


def build_contacts():
    body = f'''
    <section class="page-head">
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

    <section>
      <div class="shell">
        <div class="contact-grid">
          <div data-reveal>
            <h2 class="h-sm">Напишіть нам</h2>
            <ul class="contact-list">
              <li><a href="mailto:hello@astradigital.agency"><span class="k">Email</span><span class="v">hello@astradigital.agency</span></a></li>
              <li><a href="https://t.me/astradigital" target="_blank" rel="noopener"><span class="k">Telegram</span><span class="v">@astradigital</span></a></li>
              <li><a href="tel:+380000000000"><span class="k">Телефон</span><span class="v">+38 (000) 000-00-00</span></a></li>
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
        head("Зв'язатися з нами — Astra Digital",
             "Напишіть Astra Digital: безкоштовна консультація, аналіз ніші та розрахунок "
             "вартості сайту й Google Ads.")
        + nav("contacts.html")
        + '\n  <main id="main">\n' + body + '  </main>\n'
        + FOOTER + MODAL + TAIL
    )


if __name__ == "__main__":
    for name, builder in (("index.html", build_index),
                          ("portfolio.html", build_portfolio),
                          ("contacts.html", build_contacts)):
        (ROOT / name).write_text(builder(), encoding="utf-8")
        print("wrote", name)
