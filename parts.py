#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates parts/*.html — the page sections build.py stitches together.

All copy is read from content/*.json, so the site can be driven from Google
Drive (see sync_drive.py). This file owns structure and markup only.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "parts"
CONTENT = ROOT / "content"
OUT.mkdir(exist_ok=True)


def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


SECT = load("sections.json")

CHECK = ('<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 10.5 4 4 8-9"/></svg>')
ARROW_UP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>')


def checks(items, indent=18):
    pad = " " * indent
    return "\n".join(f'{pad}<li>{CHECK}<span>{i}</span></li>' for i in items)


# The brand mark, for decorative hero/section geometry (currentColor fill).
MARK = ('<svg class="mark" viewBox="8 48 161 88" fill="currentColor" aria-hidden="true">'
        '<path d="M101.141 53H136.632C151.023 53 162.689 64.6662 162.689 79.0573V112.904H148.112V79.0573C148.112 78.7105 148.098 78.3662 148.072 78.0251L112.581 112.898C112.701 112.902 112.821 112.904 112.941 112.904H148.112V126.672H112.941C98.5504 126.672 86.5638 114.891 86.5638 100.5V66.7434H101.141V100.5C101.141 101.15 101.191 101.792 101.289 102.422L137.56 66.7816C137.255 66.7563 136.945 66.7434 136.632 66.7434H101.141V53Z"/>'
        '<path d="M65.2926 124.136L14 66.7372H34.6355L64.7495 100.436V66.7372H80.1365V118.47C80.1365 126.278 70.4953 129.958 65.2926 124.136Z"/>'
        '</svg>')


def write(name, html):
    (OUT / name).write_text(html, encoding="utf-8")
    print("  parts/" + name)


def head_block(d, center=False, ok=False):
    """Standard section head: kicker tag + two-tone headline + optional lead."""
    cls = "head head--center" if center else "head"
    tagcls = "tag tag--ok" if ok else "tag"
    tt = f' <span class="tt">{d["title_2"]}</span>' if d.get("title_2") else ""
    lead = f'\n          <p class="lead">{d["lead"]}</p>' if d.get("lead") else ""
    return f'''        <div class="{cls}" data-reveal>
          <span class="{tagcls}">{d["tag"]}</span>
          <h2>{d["title"]}{tt}</h2>{lead}
        </div>'''


def section_link(href, label, tag="a", attrs=""):
    return f'''        <{tag} class="section-link" href="{href}" data-reveal{attrs}>
          <span>{label}</span>
          <span class="arrow-loop">→</span>
        </{tag}>'''


# ================================================================= HERO
h = SECT["hero"]
flow = "".join(
    f'<span class="hero__step">{s}</span>' + ('<span class="hero__link" aria-hidden="true"></span>' if i < len(h["flow"]) - 1 else '')
    for i, s in enumerate(h["flow"]))
write("hero.html", f'''    <!-- ================= HERO ================= -->
    <section class="hero band band--dark" data-nav-dark>
      <div class="hero__field" aria-hidden="true">
        <span class="hero__mark hero__mark--a">{MARK}</span>
        <span class="hero__mark hero__mark--b">{MARK}</span>
        <span class="hero__grid"></span>
      </div>
      <div class="shell">
        <div class="hero__inner" data-hero>
          <p class="pill">
            <span class="pill__dot" aria-hidden="true"></span>
            {h["pill"]}
          </p>
          <h1>{h["title"]} <span class="hero__channel">{h["title_channel"]}</span></h1>
          <p class="hero__sub lead">{h["sub"]}</p>
          <div class="hero__actions">
            <button class="btn btn--primary btn--lg" data-modal-open>{h["primary_cta"]} <span class="btn__arrow">→</span></button>
            <a class="btn btn--line-ink btn--lg" href="portfolio.html">{h["secondary_cta"]} <span class="btn__arrow">→</span></a>
          </div>
          <div class="hero__flow" aria-label="Аналіз, сайт, реклама, зростання">
            {flow}
          </div>
        </div>
      </div>
    </section>
''')

# ================================================================= PROOF STRIP
p = SECT["proof"]
cells = "\n".join(
    f'          <a class="strip__cell" href="portfolio.html">{name} {ARROW_UP}</a>' for name in p["projects"])
write("strip.html", f'''    <!-- ================= ПРОЄКТИ ================= -->
    <section class="strip-section band band--dark" data-nav-dark>
      <div class="shell">
        <div class="strip" aria-label="{p["label"]}">
{cells}
        </div>
      </div>
    </section>
''')

# ================================================================= PROCESS
pr = SECT["process"]
step_cells = "\n".join(f'''          <article class="cell" data-reveal>
            <span class="cell__num">{s["n"]}</span>
            <h3>{s["title"]}</h3>
            <p>{s["desc"]}</p>
          </article>''' for s in pr["steps"])
write("process.html", f'''    <!-- ================= ПРОЦЕС ================= -->
    <section class="section band band--light rule" id="process">
      <div class="shell">
{head_block(pr)}
      </div>
      <div class="shell shell--bleed">
        <div class="cells cells--4 cells--flow">
{step_cells}
        </div>
      </div>
      <div class="shell">
{section_link("#services", pr["link"])}
      </div>
    </section>
''')

# ================================================================= ADVANTAGES
ad = SECT["advantages"]
adv_cells = "\n".join(f'''          <article class="cell" data-reveal>
            <span class="cell__num">0{i+1}</span>
            <h3>{it["title"]}</h3>
            <p>{it["desc"]}</p>
          </article>''' for i, it in enumerate(ad["items"]))
write("bento.html", f'''    <!-- ================= ПЕРЕВАГИ ================= -->
    <section class="section band band--dark rule" id="why" data-nav-dark>
      <div class="shell">
{head_block(ad)}
      </div>
      <div class="shell shell--bleed">
        <div class="cells cells--4">
{adv_cells}
        </div>
      </div>
      <div class="shell">
{section_link("#packages", ad["link"])}
      </div>
    </section>
''')

# ================================================================= SYSTEM (two paths)
sy = SECT["system"]
paths = []
for pth in sy["paths"]:
    acc = " path--accent" if pth["accent"] else ""
    steps = "\n".join(f'              <li>{s}</li>' for s in pth["steps"])
    paths.append(f'''          <article class="cell path{acc}" data-reveal>
            <span class="path__tag">{pth["tag"]}</span>
            <ol class="path__steps">
{steps}
            </ol>
            <p class="path__note">{pth["note"]}</p>
          </article>''')
write("system.html", f'''    <!-- ================= СИСТЕМА ЗАЛУЧЕННЯ ================= -->
    <section class="section band band--light rule" id="system">
      <div class="shell">
{head_block(sy)}
      </div>
      <div class="shell shell--bleed">
        <div class="cells cells--2">
{chr(10).join(paths)}
        </div>
      </div>
    </section>
''')

# ================================================================= MISSION (new)
mi = SECT["mission"]
pillars = "\n".join(f'''          <article class="mission__pillar" data-reveal>
            <span class="mission__num">{pl["n"]}</span>
            <h3>{pl["title"]}</h3>
            <p>{pl["desc"]}</p>
          </article>''' for pl in mi["pillars"])
write("mission.html", f'''    <!-- ================= МІСІЯ ================= -->
    <section class="section mission band band--dark rule" id="mission" data-nav-dark>
      <div class="channel channel--top" aria-hidden="true"></div>
      <div class="shell">
        <div class="mission__head" data-reveal>
          <span class="tag">{mi["tag"]}</span>
          <h2>{mi["title"]} <span class="tt">{mi["title_2"]}</span></h2>
          <p class="lead">{mi["lead"]}</p>
        </div>
      </div>
      <div class="shell shell--bleed">
        <div class="mission__grid">
{pillars}
        </div>
      </div>
      <div class="shell">
        <p class="mission__statement" data-reveal>{mi["statement"]}</p>
      </div>
    </section>
''')

# ================================================================= SERVICES (vtabs)
sv = load("services.json")
rail = "\n".join(
    f'''            <button class="vtabs__btn" id="tab-{s["id"]}" role="tab" aria-controls="panel-{s["id"]}"
              aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">
              <span class="vtabs__idx">{s["index"]}</span>{s["nav"]}<small>{s["navsub"]}</small>
            </button>''' for i, s in enumerate(sv["items"]))

panels = []
for i, s in enumerate(sv["items"]):
    note = f'\n                <p class="svc__note">{s["note"]}</p>' if s.get("note") else ""
    branches = ""
    if s.get("branches"):
        cols = "\n".join(f'''              <div class="svc__branch">
                <span class="svc__branch-tag">{b["tag"]}</span>
                <h4>{b["title"]}</h4>
                <p>{b["desc"]}</p>
                <p class="svc__branch-why">{b["why"]}</p>
              </div>''' for b in s["branches"])
        branches = f'''            <div class="svc__split">
{cols}
            </div>
'''
    extra_price = ""
    if s.get("extra_price"):
        ep = s["extra_price"]
        extra_price = f'''
              <div class="svc__second">
                <div>
                  <span class="svc__second-label">{ep["label"]}</span>
                  <p>{ep["desc"]}</p>
                </div>
                <strong>{ep["price"]}</strong>
              </div>'''
    panels.append(f'''            <div class="vtabs__panel" id="panel-{s["id"]}" role="tabpanel" aria-labelledby="tab-{s["id"]}" tabindex="0"{"" if i == 0 else " hidden"}>
              <span class="svc__ghost" aria-hidden="true">{s["index"]}</span>
              <div class="svc__top">
                <div>
                  <span class="svc__index">{s["index"]} — {s["code"]}</span>
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

{branches}              <div class="svc__grid">
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
{extra_price}
              <div class="svc__foot">
                <p class="svc__from"><span>Вартість</span><strong>{s["price"]}</strong></p>
                <button class="btn btn--primary btn--lg" data-modal-open data-modal-topic="{s["topic"]}">{s["cta"]} <span class="btn__arrow">→</span></button>
              </div>
            </div>''')

write("services.html", f'''    <!-- ================= ПОСЛУГИ ================= -->
    <section class="section band band--light rule" id="services">
      <div class="shell">
{head_block(sv)}
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

# ================================================================= PRICING
pc = load("pricing.json")
pkgs = []
for pk in pc["packages"]:
    feat = " pkg--featured" if pk["featured"] else ""
    badge = f'\n            <span class="pkg__badge">{pk["badge"]}</span>' if pk.get("badge") else ""
    note = f'\n            <p class="pkg__note">{pk["note"]}</p>' if pk.get("note") else ""
    btn = "btn--primary" if pk["featured"] else "btn--line"
    pkgs.append(f'''          <article class="pkg{feat}" data-reveal>{badge}
            <h3 class="pkg__title">{pk["title"]}</h3>
            <p class="pkg__price">
              <span class="pkg__amount">{pk["amount"]}</span>
              <span class="pkg__term">{pk["term"]}</span>
            </p>
            <ul class="checklist">
{checks(pk["items"])}
            </ul>{note}
            <button class="btn {btn} btn--wide btn--lg pkg__cta" data-modal-open data-modal-topic="{pk["topic"]}">{pk["cta"]} <span class="btn__arrow">→</span></button>
          </article>''')
write("pricing.html", f'''    <!-- ================= ПАКЕТИ ================= -->
    <section class="section band band--dark rule" id="packages" data-nav-dark>
      <div class="shell">
{head_block({"tag": pc["tag"], "title": pc["title"], "title_2": pc.get("title_2")})}
      </div>
      <div class="shell shell--bleed">
        <div class="pkgs">
{chr(10).join(pkgs)}
        </div>
      </div>
    </section>
''')

# ================================================================= MOTION
mo = load("motion.json")
notes = "\n".join(f'''            <div class="motion__note">
              <h3>{n["title"]}</h3>
              <p>{n["desc"]}</p>
            </div>''' for n in mo["notes"])
mcards = []
for c in mo["cards"]:
    tagcls = "tag tag--plain" if c.get("tag_plain") else "tag"
    mcards.append(f'''          <article class="cell" data-reveal>
            <span class="{tagcls}">{c["tag"]}</span>
            <h3>{c["title"]}</h3>
            <p>{c["desc"]}</p>
            <p class="cell__price"><span>{c["price_label"]}</span><strong>{c["price"]}</strong></p>
          </article>''')
write("motion.html", f'''    <!-- ================= MOTION У ДІЇ ================= -->
    <section class="section band band--light rule" id="motion">
      <div class="shell">
{head_block(mo, center=True)}
      </div>

      <div class="shell shell--bleed">
        <div class="mv">
          <figure class="mv__side">
            <figcaption>
              <span class="tag tag--plain">{mo["before_tag"]}</span>
              <span>{mo["before_desc"]}</span>
            </figcaption>
            <div class="mv__frame">
              <video src="public/assets/motion/logo-reveal.mp4" muted playsinline
                     preload="auto" data-freeze="0.9"
                     aria-label="Статичний кадр логотипа"></video>
            </div>
          </figure>

          <figure class="mv__side mv__side--live">
            <figcaption>
              <span class="tag">{mo["after_tag"]}</span>
              <span>{mo["after_desc"]}</span>
            </figcaption>
            <div class="mv__frame">
              <video src="public/assets/motion/logo-reveal.mp4" autoplay muted loop playsinline
                     preload="metadata" aria-label="Анімація логотипа SkyBreeze"></video>
            </div>
          </figure>
        </div>

        <div class="motion is-motion" id="motionDemo">
          <div class="motion__bar">
            <div class="seg" role="group" aria-label="Режим показу">
              <button type="button" class="seg__btn" data-motion="off">Без анімацій</button>
              <button type="button" class="seg__btn is-on" data-motion="on" aria-pressed="true">З анімаціями</button>
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
                  <span class="reel__cta">Замовити <span class="reel__arrow">→</span></span>
                </div>
              </div>
            </figure>
          </div>

          <div class="motion__notes">
{notes}
          </div>
        </div>
      </div>

      <div class="shell shell--bleed">
        <div class="cells cells--2">
{chr(10).join(mcards)}
        </div>
      </div>

      <div class="shell">
{section_link("#panel-motion", mo["link"])}
      </div>
    </section>
''')

# ================================================================= TECH STACK
st = load("stack.json")


def stack_row(items, indent=12):
    pad = " " * indent
    one = "\n".join(
        f'{pad}<li class="tick__item"><span class="tick__tile">{code}</span>'
        f'<span class="tick__name">{name}</span></li>' for code, name in items)
    dup = one.replace('<li class="tick__item">', '<li class="tick__item" aria-hidden="true">')
    return one + "\n" + dup


row1 = stack_row(st["row1"])
row2 = stack_row(st["row2"])
tt = f' <span class="tt">{st["title_2"]}</span>' if st.get("title_2") else ""
write("stack.html", f'''    <!-- ================= ТЕХНОЛОГІЇ ================= -->
    <section class="stack band band--dark rule" id="stack" data-nav-dark>
      <div class="shell">
        <div class="stack__head" data-reveal>
          <span class="tag">{st["tag"]}</span>
          <h2>{st["title"]}{tt}</h2>
          <p class="lead">{st["lead"]}</p>
          <a class="btn btn--primary btn--lg" href="#services">{st["cta"]} <span class="btn__arrow">→</span></a>
        </div>
      </div>

      <div class="shell shell--bleed">
        <div class="tick" aria-label="Технології, з якими ми працюємо">
          <div class="tick__row">
            <ul class="tick__track">
{row1}
            </ul>
          </div>
          <div class="tick__row tick__row--back">
            <ul class="tick__track">
{row2}
            </ul>
          </div>
        </div>
      </div>
    </section>
''')

# ================================================================= LEAD MAGNET
lm = SECT["leadmagnet"]
write("leadmagnet.html", f'''    <!-- ================= ЛІД-МАГНІТ ================= -->
    <section class="section band band--light rule">
      <div class="shell">
        <div class="head head--center" data-reveal>
          <span class="tag tag--ok">{lm["tag"]}</span>
          <h2>{lm["title"]} <span class="tt">{lm["title_2"]}</span></h2>
          <p class="lead" style="margin-inline:auto">{lm["lead"]}</p>
          <p style="margin-top:28px">
            <button class="btn btn--primary btn--lg" data-modal-open data-modal-topic="{lm["topic"]}">
              {lm["cta"]} <span class="btn__arrow">→</span>
            </button>
          </p>
        </div>
      </div>
    </section>
''')

# ================================================================= AFTER
af = SECT["after"]
after_rows = "\n".join(f'''          <li class="flow__item" data-reveal>
            <span class="flow__num">{s["n"]}</span>
            <div>
              <h3>{s["title"]}</h3>
              <p>{s["desc"]}</p>
            </div>
          </li>''' for s in af["steps"])
write("after.html", f'''    <!-- ================= ПІСЛЯ ЗАЯВКИ ================= -->
    <section class="section band band--dark rule" id="after" data-nav-dark>
      <div class="shell">
{head_block(af)}
      </div>
      <div class="shell shell--bleed">
        <ol class="flow">
{after_rows}
        </ol>
      </div>
    </section>
''')

# ================================================================= FAQ
fq = load("faq.json")
faq_rows = "\n".join(f'''          <div class="faq__item">
            <h3><button class="faq__q" aria-expanded="false" aria-controls="faq-a{i}" id="faq-q{i}">{it["q"]}<span class="faq__icon" aria-hidden="true"></span></button></h3>
            <div class="faq__a" id="faq-a{i}" role="region" aria-labelledby="faq-q{i}"><div><p>{it["a"]}</p></div></div>
          </div>''' for i, it in enumerate(fq["items"], 1))
tt = f' <span class="tt">{fq["title_2"]}</span>' if fq.get("title_2") else ""
write("faq.html", f'''    <!-- ================= FAQ ================= -->
    <section class="section band band--light rule" id="faq">
      <div class="shell">
        <div class="head" data-reveal>
          <span class="tag">{fq["tag"]}</span>
          <h2>{fq["title"]}{tt}</h2>
        </div>
      </div>
      <div class="shell shell--bleed">
        <div class="faq">
{faq_rows}
        </div>
      </div>
      <div class="shell">
{section_link("#", "Не знайшли відповідь? Запитайте нас напряму", tag="button", attrs=" data-modal-open")}
      </div>
    </section>
''')

# ================================================================= PORTFOLIO
pf = load("portfolio.json")
EXT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
       '<path d="M7 17 17 7M9 7h8v8"/></svg>')


def work_card(c):
    n, t = c["name"], c["tag"]
    live, clip, slug, l = c.get("live"), c.get("video"), c["slug"], c["loading"]
    if clip:
        shot = (f'<div class="work__shot work__shot--video">'
                f'<video src="{clip}" autoplay muted loop playsinline preload="metadata" '
                f'aria-label="{n} — запис сайту"></video></div>')
        cta = f'\n              <a class="work__live" href="{live}" target="_blank" rel="noopener">Дивитися сайт {EXT}</a>'
    elif live:
        shot = (f'<a class="work__shot work__shot--link" href="{live}" target="_blank" rel="noopener">'
                f'<b>{n}</b><span>Відкрити сайт у новій вкладці</span></a>')
        cta = f'\n              <a class="work__live" href="{live}" target="_blank" rel="noopener">Дивитися сайт {EXT}</a>'
    else:
        shot = (f'<div class="work__shot"><img src="public/assets/screenshots/{slug}.webp" '
                f'alt="{n} — проєкт SkyBreeze" loading="{l}" /></div>')
        cta = ''
    return f'''          <article class="work" data-reveal>
            {shot}
            <div class="work__body">
              <span class="work__tag">{t}</span>
              <h3>{n}</h3>
              <dl class="case">
                <dt>Задача</dt><dd>{c["task"]}</dd>
                <dt>Рішення</dt><dd>{c["solution"]}</dd>
                <dt>Результат</dt><dd>{c["result"]}</dd>
              </dl>{cta}
            </div>
          </article>'''


work_cells = "\n".join(work_card(c) for c in pf["cases"])
tt = f' <span class="tt">{pf["title_2"]}</span>' if pf.get("title_2") else ""
write("portfolio.html", f'''    <section class="page-head band band--dark" data-nav-dark>
      <div class="shell">
        <div data-hero>
          <span class="tag">{pf["tag"]}</span>
          <h1>{pf["title"]}{tt}</h1>
          <p class="lead">{pf["lead"]}</p>
        </div>
      </div>
    </section>

    <section class="band band--light">
      <div class="shell">
        <div class="works">
{work_cells}
        </div>
      </div>
    </section>
''')

print("done")
