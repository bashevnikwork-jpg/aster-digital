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
  var progress = document.getElementById('navProgress');

  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('is-stuck', window.scrollY > 8);
      if (progress) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        progress.style.transform = 'scaleX(' + (max > 0 ? window.scrollY / max : 0) + ')';
      }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
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

  /* ---------- 3. Scroll choreography ---------- */
  /* Split section headlines into words so they can set line by line. */
  function splitWords(el) {
    var frag = document.createDocumentFragment();
    var index = 0;

    var pushWords = function (text, target) {
      text.split(/(\s+)/).forEach(function (chunk) {
        if (!chunk) return;
        if (/^\s+$/.test(chunk)) { target.appendChild(document.createTextNode(' ')); return; }
        var word = document.createElement('span');
        word.className = 'w';
        var inner = document.createElement('i');
        inner.textContent = chunk;
        inner.style.setProperty('--i', index++);
        word.appendChild(inner);
        target.appendChild(word);
      });
    };

    Array.prototype.slice.call(el.childNodes).forEach(function (node) {
      if (node.nodeType === 3) {
        pushWords(node.textContent, frag);
      } else if (node.nodeType === 1) {
        // keep wrappers such as the grey second clause, split what's inside
        var clone = node.cloneNode(false);
        pushWords(node.textContent, clone);
        frag.appendChild(clone);
      }
    });

    el.textContent = '';
    el.appendChild(frag);
    el.setAttribute('data-split', '');
  }

  if (!reduceMotion) {
    document.querySelectorAll('.head h2, .page-head h1').forEach(splitWords);
  }

  /* Number the children of any group so CSS can cascade their delays. */
  function indexChildren(selector, childSelector) {
    document.querySelectorAll(selector).forEach(function (group) {
      Array.prototype.slice.call(group.querySelectorAll(childSelector)).forEach(function (child, i) {
        child.style.setProperty('--i', i);
      });
    });
  }

  indexChildren('.cells', '.cell');
  indexChildren('.strip', '.strip__cell');
  indexChildren('.faq', '.faq__item');
  indexChildren('.flow', '.flow__item');
  document.querySelectorAll('.cells .cell').forEach(function (cell) {
    var i = cell.style.getPropertyValue('--i');
    Array.prototype.slice.call(cell.children).forEach(function (child) {
      child.style.setProperty('--i', i);
    });
  });

  /* One observer drives every entrance. */
  var watched = document.querySelectorAll('[data-reveal], [data-split], .cells, .strip, .faq, .flow');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    watched.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.filter(function (e) { return e.isIntersecting; })
        .forEach(function (entry, i) {
          var el = entry.target;
          // siblings that appear together cascade rather than land as one block
          if (el.hasAttribute('data-reveal') && !el.style.getPropertyValue('--i')) {
            el.style.setProperty('--i', Math.min(i, 5));
          }
          el.classList.add('is-in');
          obs.unobserve(el);
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    watched.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- 3b. Mobile action bar ---------- */
  var bar = document.getElementById('actionBar');
  if (bar) {
    var closing = document.querySelector('.cta__panel');
    var update = function () {
      var past = window.scrollY > window.innerHeight * 0.7;
      // stand down where the page makes the same offer full size
      var atClosing = closing && closing.getBoundingClientRect().top < window.innerHeight;
      bar.classList.toggle('is-in', past && !atClosing);
    };
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
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
