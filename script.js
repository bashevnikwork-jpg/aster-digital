/* ============================================================
   ASTRA DIGITAL — interactions
   nav state · mobile sheet · staggered scroll reveal
   tabs · faq · modal · forms
   ============================================================ */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Nav: hairline appears once the page moves ---------- */
  var nav = document.getElementById('nav');
  if (nav) {
    var setStuck = function () { nav.classList.toggle('is-stuck', window.scrollY > 8); };
    setStuck();
    window.addEventListener('scroll', setStuck, { passive: true });
  }

  /* ---------- 2. Mobile sheet ---------- */
  var burger = document.getElementById('navBurger');
  var sheet = document.getElementById('navSheet');

  if (burger && sheet) {
    var setSheet = function (open) {
      if (open && nav) sheet.style.top = Math.round(nav.getBoundingClientRect().height) + 'px';
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Закрити меню' : 'Відкрити меню');
      sheet.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };

    burger.addEventListener('click', function () {
      setSheet(burger.getAttribute('aria-expanded') !== 'true');
    });
    sheet.addEventListener('click', function (e) {
      if (e.target.closest('a, button')) setSheet(false);
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && sheet.classList.contains('is-open')) setSheet(false);
    });
  }

  /* ---------- 3. Scroll reveal with sibling stagger ---------- */
  var revealables = document.querySelectorAll('[data-reveal]');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var observer = new IntersectionObserver(function (entries, obs) {
      // Group entries that land in the same frame so a row of cards cascades.
      var incoming = entries.filter(function (e) { return e.isIntersecting; });
      incoming.forEach(function (entry, i) {
        var el = entry.target;
        el.style.transitionDelay = Math.min(i, 5) * 90 + 'ms';
        el.classList.add('is-in');
        obs.unobserve(el);
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -10% 0px' });

    revealables.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- 4. FAQ disclosures ---------- */
  document.querySelectorAll('.faq__q').forEach(function (btn) {
    var item = btn.closest('.faq__item');
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      item.classList.toggle('is-open', !open);
    });
  });

  /* ---------- 5. Service rail (vertical tabs) ---------- */
  var railList = document.querySelector('.vtabs__rail[role="tablist"]');

  if (railList) {
    var tabs = Array.prototype.slice.call(railList.querySelectorAll('[role="tab"]'));

    var selectTab = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
      });
      if (focus) tab.focus();
    };

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () { selectTab(tab, false); });
    });

    railList.addEventListener('keydown', function (e) {
      var i = tabs.indexOf(document.activeElement);
      if (i === -1) return;
      // The rail is vertical on desktop and horizontal once it collapses,
      // so both axes move between tabs.
      var next = null;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') next = (i + 1) % tabs.length;
      else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') next = (i - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') next = 0;
      else if (e.key === 'End') next = tabs.length - 1;
      if (next === null) return;
      e.preventDefault();
      selectTab(tabs[next], true);
    });

    /* #panel-ads in the URL opens that service. */
    var hash = window.location.hash;
    if (hash.indexOf('#panel-') === 0) {
      var wanted = tabs.filter(function (t) { return '#' + t.getAttribute('aria-controls') === hash; })[0];
      if (wanted) selectTab(wanted, false);
    }
  }

  /* ---------- 6. Modal ---------- */
  var modal = document.getElementById('contactModal');

  if (modal) {
    var dialog = modal.querySelector('.modal__dialog');
    var topicSelect = document.getElementById('fTopic');
    var lastFocused = null;

    var focusables = function () {
      return Array.prototype.filter.call(
        dialog.querySelectorAll('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'),
        function (el) { return !el.disabled && el.offsetParent !== null; }
      );
    };

    var openModal = function (trigger) {
      lastFocused = trigger || document.activeElement;
      modal.hidden = false;
      document.body.style.overflow = 'hidden';

      var topic = trigger && trigger.getAttribute('data-modal-topic');
      if (topic && topicSelect) {
        Array.prototype.forEach.call(topicSelect.options, function (opt) {
          if (opt.text === topic) topicSelect.value = opt.value;
        });
      }

      var first = focusables()[0];
      if (first) first.focus();
    };

    var closeModal = function () {
      modal.hidden = true;
      document.body.style.overflow = '';
      if (lastFocused) lastFocused.focus();
    };

    document.querySelectorAll('[data-modal-open]').forEach(function (btn) {
      btn.addEventListener('click', function () { openModal(btn); });
    });
    modal.querySelectorAll('[data-modal-close]').forEach(function (btn) {
      btn.addEventListener('click', closeModal);
    });

    document.addEventListener('keydown', function (e) {
      if (modal.hidden) return;
      if (e.key === 'Escape') { closeModal(); return; }
      if (e.key !== 'Tab') return;

      var items = focusables();
      if (!items.length) return;
      var first = items[0];
      var last = items[items.length - 1];

      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    var modalForm = document.getElementById('contactForm');
    if (modalForm) bindForm(modalForm, document.getElementById('formStatus'), closeModal);
  }

  /* ---------- 7. Forms (front-end only, no backend yet) ---------- */
  function bindForm(form, status, done) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (status) status.textContent = 'Дякуємо! Ми зв\'яжемося з вами найближчим часом.';
      form.reset();
      if (done) {
        setTimeout(function () {
          if (status) status.textContent = '';
          done();
        }, 2200);
      }
    });
  }

  var pageForm = document.getElementById('pageForm');
  if (pageForm) bindForm(pageForm, document.getElementById('pageFormStatus'), null);
})();
