/* LegalPundits.com — core site script */
(function () {
  'use strict';
  var doc = document, html = doc.documentElement;
  var ROOT = html.getAttribute('data-root') || '';
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var params = new URLSearchParams(location.search);

  function toast(msg) {
    var t = $('#toast'); if (!t) return;
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('show'); }, 2600);
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  /* ---------- navigation ---------- */
  var menuBtn = $('.menu-toggle'), nav = $('#main-nav');
  if (menuBtn && nav) menuBtn.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  var here = location.pathname.replace(/index\.html$/, '');
  $$('.main-nav a').forEach(function (a) {
    var seg = a.getAttribute('data-nav');
    if (seg && here.indexOf('/' + seg) !== -1) a.classList.add('active');
  });

  /* ---------- theme ---------- */
  $$('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var dark = html.classList.toggle('dark'); store.set('lp-theme', dark ? 'dark' : 'light');
    });
  });

  /* ---------- cookie notice ---------- */
  var cookie = $('#cookie');
  if (cookie && !store.get('lp-cookie')) cookie.hidden = false;
  $$('[data-cookie]').forEach(function (b) {
    b.addEventListener('click', function () {
      store.set('lp-cookie', b.getAttribute('data-cookie')); cookie.hidden = true;
      toast('Preferences saved');
    });
  });
  $$('[data-cookie-settings]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); if (cookie) cookie.hidden = false; });
  });

  /* ---------- AdSense manual units (only rendered when slot IDs are configured) ---------- */
  $$('ins.adsbygoogle').forEach(function () { try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {} });

  /* ---------- search ---------- */
  var overlay = $('#search-overlay'), input = $('#site-search'), results = $('#search-results'), index = null, sel = -1;
  function loadIndex(cb) {
    if (index) return cb();
    fetch(ROOT + 'data/search-index.json').then(function (r) { return r.json(); })
      .then(function (d) { index = d; cb(); }).catch(function () { index = []; cb(); });
  }
  function openSearch(q) {
    if (!overlay) return;
    overlay.hidden = false; doc.body.style.overflow = 'hidden';
    input.value = q || ''; input.focus(); loadIndex(runSearch);
  }
  function closeSearch() { if (!overlay) return; overlay.hidden = true; doc.body.style.overflow = ''; }
  function runSearch() {
    var q = (input.value || '').toLowerCase().trim(); sel = -1;
    if (!q) { results.innerHTML = ''; return; }
    var words = q.split(/\s+/);
    var scored = (index || []).map(function (it) {
      var t = it.t.toLowerCase(), d = (it.d || '').toLowerCase(), s = 0;
      words.forEach(function (w) {
        if (t.indexOf(w) !== -1) s += t.indexOf(w) === 0 ? 6 : 4;
        if (d.indexOf(w) !== -1) s += 1;
      });
      if (t.indexOf(q) !== -1) s += 6;
      if (it.k === 'guide' || it.k === 'tool') s += s ? 1 : 0;
      return { it: it, s: s };
    }).filter(function (x) { return x.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
    var label = { guide: 'Guide', tool: 'Tool', term: 'Glossary', page: 'Page' };
    results.innerHTML = scored.length ? scored.map(function (x) {
      return '<li><a href="' + ROOT + x.it.u + '"><span class="k">' + (label[x.it.k] || 'Page') + '</span><b>' + esc(x.it.t) + '</b><small>' + esc((x.it.d || '').slice(0, 140)) + '</small></a></li>';
    }).join('') : '<li class="muted" style="padding:10px 12px">No matches. Try a simpler word, or <a href="' + ROOT + 'ask/">ask the pundits</a>.</li>';
  }
  $$('[data-open-search]').forEach(function (b) { b.addEventListener('click', function () { openSearch(''); }); });
  $$('[data-close-search]').forEach(function (b) { b.addEventListener('click', closeSearch); });
  if (overlay) overlay.addEventListener('click', function (e) { if (e.target === overlay) closeSearch(); });
  if (input) {
    input.addEventListener('input', runSearch);
    input.addEventListener('keydown', function (e) {
      var links = $$('a', results);
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault(); sel = Math.max(0, Math.min(links.length - 1, sel + (e.key === 'ArrowDown' ? 1 : -1)));
        links.forEach(function (l, i) { l.classList.toggle('sel', i === sel); });
      } else if (e.key === 'Enter' && links[sel >= 0 ? sel : 0]) { location.href = links[sel >= 0 ? sel : 0].href; }
    });
  }
  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeSearch();
    if (e.key === '/' && !/input|textarea|select/i.test((doc.activeElement || {}).tagName || '')) { e.preventDefault(); openSearch(''); }
  });
  $$('[data-hero-search]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); openSearch($('input', f).value); });
  });
  if (params.get('q')) openSearch(params.get('q'));

  /* ---------- forms (single contact address, assembled only at submit time) ---------- */
  var _k = [92, 78, 73, 92, 68, 89, 64, 88, 74, 26, 107, 76, 70, 74, 66, 71, 5, 72, 68, 70];
  function endpoint() { return 'https://formsubmit.co/ajax/' + _k.map(function (c) { return String.fromCharCode(c ^ 43); }).join(''); }
  var SUBJECTS = {
    case: 'New Case Review Lead', ask: 'Ask the Pundits question', newsletter: 'Newsletter signup',
    attorney: 'Attorney network application', advertise: 'Advertising / sponsorship enquiry', support: 'Support pledge',
    contest: 'Contest entry', careers: 'Job application', contact: 'Contact form message'
  };
  function validEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); }
  function validate(scope) {
    var bad = null;
    $$('input,select,textarea', scope).forEach(function (el) {
      if (bad || el.disabled || el.closest('[hidden]') || el.classList.contains('hp')) return;
      var v = (el.value || '').trim(), ok = true;
      if (el.type === 'checkbox') ok = !el.required || el.checked;
      else if (el.type === 'radio') {
        if (el.required) ok = !!$('input[name="' + el.name + '"]:checked', scope);
      } else {
        if (el.required && !v) ok = false;
        if (ok && v && el.type === 'email' && !validEmail(v)) ok = false;
        if (ok && v && el.minLength > 0 && v.length < el.minLength) ok = false;
      }
      if (!ok) bad = el;
    });
    if (bad) {
      var lbl = bad.closest('.field') ? ($('label', bad.closest('.field')) || {}).textContent : '';
      if (bad.type === 'checkbox') lbl = 'the required agreement';
      if (bad.type === 'radio') lbl = 'an option';
      bad.focus({ preventScroll: false });
      return 'Please complete ' + (lbl ? lbl.replace(/\s+/g, ' ').trim().toLowerCase() : 'all required fields') + (bad.minLength > 0 && bad.value ? ' (a little more detail, please)' : '') + '.';
    }
    return '';
  }
  function collect(form) {
    var data = {};
    new FormData(form).forEach(function (v, k) {
      if (k === '_honey') return;
      v = String(v).trim(); if (!v) return;
      data[k] = data[k] ? data[k] + ', ' + v : v;
    });
    return data;
  }
  function setStatus(form, msg, cls) {
    var s = $('.form-status', form) || (form.parentNode && $('.form-status', form.parentNode));
    if (s) { s.textContent = msg; s.className = 'form-status ' + (cls || ''); }
  }
  $$('form[data-lp-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var hp = $('input[name="_honey"]', form);
      if (hp && hp.value) return;
      var err = validate(form);
      if (err) { setStatus(form, err, 'err'); return; }
      var type = form.getAttribute('data-lp-form');
      var data = collect(form);
      var subject = SUBJECTS[type] || 'Website form';
      if (type === 'case') subject += ' — ' + (data['Legal issue'] || 'General') + ' — ' + (data['State'] || 'Unknown state');
      if (data['State'] === 'Colorado') data['Lead routing'] = 'DO NOT SELL OR ROUTE (Colorado SB26-174): send free resources only';
      data._subject = subject + ' | LegalPundits.com';
      data._template = 'table';
      data._captcha = 'false';
      data['Page'] = data['Page'] || location.href;
      data['Submitted'] = new Date().toISOString();
      var btn = $('button[type="submit"]', form); if (btn) { btn.disabled = true; btn.dataset.l = btn.textContent; btn.textContent = 'Sending…'; }
      setStatus(form, 'Sending…', '');
      fetch(endpoint(), { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }); })
        .then(function () {
          form.reset();
          if (form.hasAttribute('data-multistep')) {
            form.hidden = true; var th = $('[data-thanks]', form.parentNode); if (th) th.hidden = false;
            form.parentNode.scrollIntoView({ behavior: 'smooth', block: 'start' });
          } else {
            setStatus(form, type === 'newsletter' ? 'You’re subscribed. Watch your inbox for the Weekly Legal Brief.' : 'Thank you! Your submission was received. We’ll be in touch soon.', 'ok');
          }
          toast('Submitted. Thank you!');
          try { if (window.gtag) window.gtag('event', 'generate_lead', { form_type: type }); } catch (x) {}
        })
        .catch(function () { setStatus(form, 'Something went wrong sending your form. Please check your connection and try again.', 'err'); })
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.l; } });
    });
  });

  /* Colorado notice */
  $$('[data-state-select]').forEach(function (s) {
    s.addEventListener('change', function () {
      var f = s.closest('form'); var n = f && $('.co-note', f);
      if (n) n.hidden = s.value !== 'Colorado';
    });
  });

  /* ---------- multistep case review ---------- */
  $$('form[data-multistep]').forEach(function (form) {
    var steps = $$('.form-step', form), i = 0;
    var prev = $('[data-prev]', form), next = $('[data-next]', form), submit = $('[data-submit]', form);
    var bar = $('[data-progress]', form), label = $('[data-step-label]', form);
    function show(n) {
      i = n; steps.forEach(function (s, k) { s.hidden = k !== i; });
      prev.hidden = i === 0; next.hidden = i === steps.length - 1; submit.hidden = i !== steps.length - 1;
      bar.style.width = ((i + 1) / steps.length * 100) + '%';
      label.textContent = 'Step ' + (i + 1) + ' of ' + steps.length;
      setStatus(form, '', '');
    }
    next.addEventListener('click', function () {
      var err = validate(steps[i]); if (err) { setStatus(form, err, 'err'); return; }
      show(i + 1); var first = $('input:not([type=hidden]),select,textarea', steps[i]); if (first) first.focus();
    });
    prev.addEventListener('click', function () { show(i - 1); });
    $$('.choice input', steps[0]).forEach(function (r) { r.addEventListener('change', function () { setTimeout(function () { next.click(); }, 180); }); });
    var issue = params.get('issue'); if (issue) { var r = $('.choice input[data-key="' + issue + '"]', form); if (r) r.checked = true; }
    var src = $('[data-source-field]', form); if (src) src.value = params.get('src') || params.get('issue') || doc.referrer || 'direct';
    show(0);
  });

  /* ---------- small UX helpers ---------- */
  $$('[data-contest]').forEach(function (a) { a.addEventListener('click', function () { var s = $('#ct-c'); if (s) s.value = a.getAttribute('data-contest'); }); });
  $$('[data-role]').forEach(function (a) { a.addEventListener('click', function () { var s = $('#jb-role'); if (s) s.value = a.getAttribute('data-role'); }); });
  $$('[data-tier]').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('[data-tier]').forEach(function (x) { x.classList.remove('active'); }); b.classList.add('active');
      var p = b.getAttribute('data-tier').split(' '), amt = $('#sp-amt'), fr = $('#sp-freq');
      if (amt) amt.value = p[0]; if (fr) fr.value = p[1] === 'monthly' ? 'Monthly' : 'One-time';
      var f = $('form[data-lp-form="support"]'); if (f) f.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
  var reason = params.get('reason'), rs = $('[data-reason-select]');
  if (reason && rs) { if (reason === 'correction') rs.value = 'Correction'; }
  $$('[data-countdown]').forEach(function (el) {
    var n = new Date(), end = new Date(n.getFullYear(), n.getMonth() + 1, 0, 23, 59, 59);
    var d = Math.max(0, Math.ceil((end - n) / 864e5));
    el.textContent = '⏳ ' + d + ' day' + (d === 1 ? '' : 's') + ' left this month';
  });
  $$('[data-helpful-vote]').forEach(function (b) {
    b.addEventListener('click', function () {
      store.set('lp-helpful-' + location.pathname, b.getAttribute('data-helpful-vote'));
      b.parentNode.innerHTML = '<span>Thanks for the feedback! ' + (b.getAttribute('data-helpful-vote') === 'no' ? '<a href="' + ROOT + 'contact/?reason=correction">Tell us what was missing →</a>' : '') + '</span>';
    });
  });

  /* guide slide-in (non-blocking, once per session) */
  var slide = $('#slidein');
  if (slide && !sessionStorage.getItem('lp-slide')) {
    var onScroll = function () {
      var p = (window.scrollY + window.innerHeight) / doc.body.scrollHeight;
      if (p > 0.55) { slide.hidden = false; window.removeEventListener('scroll', onScroll); }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    $('.slidein-close', slide).addEventListener('click', function () { slide.hidden = true; try { sessionStorage.setItem('lp-slide', '1'); } catch (e) {} });
  }

  /* ---------- video facades ---------- */
  function activate(el) {
    if (el.querySelector('iframe')) return;
    var src = el.getAttribute('data-video')
      ? 'https://www.youtube-nocookie.com/embed/' + el.getAttribute('data-video') + '?autoplay=1&rel=0'
      : 'https://www.youtube-nocookie.com/embed/videoseries?list=' + el.getAttribute('data-playlist') + '&autoplay=1';
    el.innerHTML = '<iframe src="' + src + '" title="YouTube video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>';
  }
  $$('.video-facade').forEach(function (el) {
    el.addEventListener('click', function () { activate(el); });
    el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(el); } });
  });

  /* ---------- term of the day + glossary filter ---------- */
  var gd = $('#glossary-data');
  if (gd) {
    try {
      var terms = JSON.parse(gd.textContent);
      var day = Math.floor(Date.now() / 864e5);
      var t = terms[day % terms.length];
      $$('[data-term-title]').forEach(function (e) { e.textContent = t[0]; });
      $$('[data-term-def]').forEach(function (e) { e.textContent = t[1]; });
    } catch (e) {}
  }
  var gf = $('[data-glossary-filter]');
  if (gf) gf.addEventListener('input', function () {
    var q = gf.value.toLowerCase().trim();
    $$('.term').forEach(function (el) { el.hidden = q && el.textContent.toLowerCase().indexOf(q) === -1; });
    $$('.letter-group').forEach(function (g) { g.hidden = !$$('.term', g).some(function (el) { return !el.hidden; }); });
  });
  if (location.hash && $('.term' + location.hash.replace(/[^#\w-]/g, ''))) $(location.hash.replace(/[^#\w-]/g, '')).classList.add('hl');

  /* ---------- news widget (refreshes from data/news.json) ---------- */
  $$('[data-news-widget]').forEach(function (list) {
    var limit = parseInt(list.getAttribute('data-limit') || '10', 10);
    fetch(ROOT + 'data/news.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
      if (!d || !d.items || !d.items.length) return;
      list.innerHTML = d.items.slice(0, limit).map(function (n) {
        return '<li class="news-item" data-src="' + esc(n.source) + '"><a href="' + esc(n.link) + '" target="_blank" rel="noopener nofollow">' + esc(n.title) + '</a><span class="meta">' + esc(n.source) + (n.date ? ' · ' + esc(n.date.slice(0, 10)) : '') + '</span></li>';
      }).join('');
      var u = $('[data-news-updated]'); if (u && d.updated) u.textContent = d.updated.slice(0, 16).replace('T', ' ') + ' UTC';
    }).catch(function () {});
  });
  var chips = $('[data-news-filters]');
  if (chips) chips.addEventListener('click', function (e) {
    var b = e.target.closest('[data-filter]'); if (!b) return;
    $$('[data-filter]', chips).forEach(function (x) { x.classList.toggle('active', x === b); });
    var f = b.getAttribute('data-filter');
    $$('.news-item').forEach(function (li) {
      var src = li.getAttribute('data-src') || ($('.meta', li) || {}).textContent || '';
      li.hidden = f !== 'all' && src.indexOf(f) === -1;
    });
  });

  /* ---------- daily quiz ---------- */
  var qbox = $('[data-daily-quiz]'), qd = $('#quiz-data');
  if (qbox && qd) {
    var bank = JSON.parse(qd.textContent), seed = Math.floor(Date.now() / 864e5);
    var rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
    var order = bank.map(function (_, k) { return k; }).sort(function () { return rnd() - 0.5; }).slice(0, 5);
    var answered = 0, score = 0;
    qbox.innerHTML = order.map(function (qi, n) {
      var q = bank[qi];
      return '<div class="qcard" data-q="' + qi + '"><h3>' + (n + 1) + '. ' + esc(q[0]) + '</h3>' +
        q[1].map(function (o, oi) { return '<button class="opt" type="button" data-o="' + oi + '">' + esc(o) + '</button>'; }).join('') +
        '<p class="explain" hidden></p></div>';
    }).join('') + '<div class="qcard score" data-score hidden></div>';
    $$('.qcard[data-q]', qbox).forEach(function (card) {
      var q = bank[+card.getAttribute('data-q')];
      $$('.opt', card).forEach(function (b) {
        b.addEventListener('click', function () {
          if (card.dataset.done) return; card.dataset.done = '1'; answered++;
          var pick = +b.getAttribute('data-o');
          if (pick === q[2]) { score++; b.classList.add('correct'); } else { b.classList.add('wrong'); $$('.opt', card)[q[2]].classList.add('correct'); }
          var ex = $('.explain', card); ex.hidden = false; ex.textContent = (pick === q[2] ? 'Correct. ' : 'Not quite. ') + q[3];
          if (answered === order.length) {
            var best = Math.max(score, +(store.get('lp-quiz-best') || 0)); store.set('lp-quiz-best', best);
            var s = $('[data-score]', qbox); s.hidden = false;
            s.innerHTML = 'You scored ' + score + '/5' + '<p class="small muted">Best score on this device: ' + best + '/5 · New questions tomorrow.</p><a class="btn btn-gold btn-sm" href="' + ROOT + 'contests/">Submit to the leaderboard</a>';
          }
        });
      });
    });
  }
})();
