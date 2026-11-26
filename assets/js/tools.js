/* LegalPundits.com — free legal tools */
(function () {
  'use strict';
  var doc = document, ROOT = doc.documentElement.getAttribute('data-root') || '';
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var num = function (id) { var v = parseFloat(($('#' + id) || {}).value); return isFinite(v) ? v : 0; };
  var money = function (v) { return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(Math.round(v)); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var DAY = 864e5;
  var fmtDate = function (d) { return d.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }); };
  var parseDate = function (s) { if (!s) return null; var p = s.split('-'); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); };
  var todayUTC = function () { var n = new Date(); return new Date(Date.UTC(n.getFullYear(), n.getMonth(), n.getDate())); };
  function show(form, html) { var r = $('[data-result]', form.parentNode); r.innerHTML = html; r.hidden = false; r.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
  function cta(issue, src, label) {
    return '<p style="margin-top:14px"><a class="btn btn-gold" href="' + ROOT + 'case-review/?issue=' + issue + '&src=' + src + '">' + (label || 'Get a free case review') + '</a></p>';
  }

  /* 1. Settlement estimator */
  var se = $('form[data-calc="settlement"]');
  if (se) se.addEventListener('submit', function (e) {
    e.preventDefault();
    var med = num('se-med'), fmed = num('se-fmed'), wages = num('se-wages'), other = num('se-other');
    var m = parseFloat($('#se-sev').value), fault = Math.min(100, Math.max(0, num('se-fault'))), rule = $('#se-rule').value;
    var limit = num('se-limit'), fee = Math.min(50, Math.max(0, num('se-fee'))) / 100;
    var medTotal = med + fmed, econ = medTotal + wages + other;
    var lowM = Math.max(1, m - 0.5), highM = m + 0.5;
    var low = econ + medTotal * lowM, mid = econ + medTotal * m, high = econ + medTotal * highM;
    var factor = 1, barred = false, f = fault / 100;
    if (rule === 'pure') factor = 1 - f;
    else if (rule === 'mod50') { if (fault >= 50) barred = true; else factor = 1 - f; }
    else if (rule === 'mod51') { if (fault >= 51) barred = true; else factor = 1 - f; }
    else if (rule === 'contrib') { if (fault > 0) barred = true; }
    if (barred) factor = 0;
    var adj = function (v) { var x = v * factor; return limit > 0 ? Math.min(x, limit) : x; };
    var aLow = adj(low), aMid = adj(mid), aHigh = adj(high), feeAmt = aMid * fee, net = aMid - feeAmt;
    var html = '<p class="eyebrow">Estimated claim range</p><p class="big">' + money(aLow) + ' – ' + money(aHigh) + '</p>' +
      '<table><tbody>' +
      '<tr><td>Economic damages (medical, wages, costs)</td><td>' + money(econ) + '</td></tr>' +
      '<tr><td>Non-economic damages (medical × ' + m + ')</td><td>' + money(medTotal * m) + '</td></tr>' +
      '<tr><td>Gross value before fault</td><td>' + money(mid) + '</td></tr>' +
      '<tr><td>After your ' + fault + '% fault</td><td>' + money(mid * factor) + '</td></tr>' +
      (limit > 0 ? '<tr><td>Capped at policy limit</td><td>' + money(Math.min(mid * factor, limit)) + '</td></tr>' : '') +
      '<tr><td>Attorney fee (' + Math.round(fee * 1000) / 10 + '%)</td><td>− ' + money(feeAmt) + '</td></tr>' +
      '<tr><td><strong>Estimated net before costs &amp; liens</strong></td><td><strong>' + money(net) + '</strong></td></tr>' +
      '</tbody></table>';
    if (barred) html += '<div class="danger">Under the fault rule you selected, your share of fault could bar recovery entirely. Fault percentages are often disputed, so get a lawyer’s view before giving up on a claim.</div>';
    if (limit > 0 && mid * factor > limit) html += '<div class="warn">Your estimate exceeds the at-fault policy limit. Underinsured-motorist coverage, umbrella policies or other responsible parties may matter. A lawyer can investigate.</div>';
    html += '<p class="small muted">Educational estimate using the multiplier method. Real values depend on evidence, venue, insurance and negotiation. Not legal advice.</p>';
    html += cta('injury', 'settlement-estimator', 'Get a free review of my claim');
    show(se, html);
  });

  /* 2. Statute of limitations deadline finder */
  var dl = $('form[data-calc="deadline"]');
  if (dl) {
    var SOL = JSON.parse($('#sol-data').textContent), byCode = {};
    SOL.forEach(function (s) { byCode[s.c] = s; });
    dl.addEventListener('submit', function (e) {
      e.preventDefault();
      var s = byCode[$('#dl-state').value], d = parseDate($('#dl-date').value), type = $('#dl-type').value;
      if (!s || !d) { show(dl, '<div class="warn">Choose a state and the date of injury.</div>'); return; }
      var end = new Date(Date.UTC(d.getUTCFullYear() + s.y, d.getUTCMonth(), d.getUTCDate()));
      if (end.getUTCMonth() !== d.getUTCMonth()) end = new Date(Date.UTC(d.getUTCFullYear() + s.y, d.getUTCMonth() + 1, 0));
      var left = Math.round((end - todayUTC()) / DAY);
      var html = '<p class="eyebrow">' + esc(s.n) + ' · general personal injury deadline: ' + s.y + ' year' + (s.y === 1 ? '' : 's') + '</p>' +
        '<p class="big">' + fmtDate(end) + '</p>';
      if (left < 0) html += '<div class="danger">This general deadline appears to have passed ' + Math.abs(left) + ' days ago. Exceptions can apply (late discovery, minors, a defendant’s absence). Speak with a lawyer promptly.</div>';
      else if (left < 180) html += '<div class="danger"><strong>' + left + ' days left.</strong> Lawyers need time to investigate and file. Act now.</div>';
      else html += '<p><strong>' + left + ' days left</strong> under the general rule.</p>';
      if (s.note) html += '<div class="warn">' + esc(s.note) + '</div>';
      if (type === 'gov') html += '<div class="danger">Claims against a government entity usually require a written <strong>notice of claim</strong> within a much shorter window, often 30 to 180 days, before you can sue.</div>';
      if (type === 'med') html += '<div class="warn">Medical malpractice deadlines are often shorter, may run from discovery, and usually have an outer limit (statute of repose).</div>';
      if (type === 'minor') html += '<div class="warn">Many states pause (toll) the deadline until the child turns 18, so the real deadline may be later. Parents’ own claims for medical bills may follow the normal deadline.</div>';
      if (s.contrib) html += '<p class="small">Note: ' + esc(s.n) + ' follows contributory negligence, so any fault on your part can bar recovery.</p>';
      html += '<p class="small muted">General rule for negligence-based personal injury claims, last reviewed November 2026. Exceptions and other claim types (property, contract, wrongful death) differ. Confirm with a licensed attorney.</p>';
      html += cta('injury', 'deadline-finder', 'Check my deadline with a lawyer (free)');
      show(dl, html);
    });
  }

  /* 3. Contingency fee calculator */
  var cf = $('form[data-calc="contingency"]');
  if (cf) {
    $('#cf-stage').addEventListener('change', function () { $('#cf-pct').value = this.value === 'pre' ? '33.33' : '40'; });
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      var A = num('cf-amt'), p = Math.min(50, Math.max(0, num('cf-pct'))) / 100, c = num('cf-costs'), L = num('cf-liens');
      var basis = ($('input[name="cf-basis"]:checked') || {}).value || 'gross';
      var fee = basis === 'gross' ? A * p : Math.max(0, A - c) * p;
      var net = A - fee - c - L, share = A > 0 ? Math.max(0, net) / A * 100 : 0;
      var html = '<p class="eyebrow">Your estimated take-home</p><p class="big">' + money(Math.max(0, net)) + '</p>' +
        '<div class="meter" aria-hidden="true"><span style="width:' + Math.min(100, share) + '%;background:linear-gradient(90deg,var(--teal),var(--gold))"></span></div>' +
        '<p class="small">That’s about <strong>' + share.toFixed(1) + '%</strong> of the gross recovery.</p>' +
        '<table><tbody><tr><td>Gross settlement</td><td>' + money(A) + '</td></tr>' +
        '<tr><td>Attorney fee (' + (p * 100).toFixed(2) + '% of ' + (basis === 'gross' ? 'gross' : 'net of costs') + ')</td><td>− ' + money(fee) + '</td></tr>' +
        '<tr><td>Case costs</td><td>− ' + money(c) + '</td></tr><tr><td>Medical liens / bills</td><td>− ' + money(L) + '</td></tr>' +
        '<tr><td><strong>You receive</strong></td><td><strong>' + money(net) + '</strong></td></tr></tbody></table>';
      if (net < 0) html += '<div class="danger">Costs and liens exceed the recovery. Lawyers can often negotiate liens down; ask about reductions before settling.</div>';
      else if (L > 0) html += '<div class="warn">Medical liens are frequently negotiable. Even a 20% reduction would add ' + money(L * 0.2) + ' to your share.</div>';
      html += '<p class="small muted">Your signed fee agreement controls the real math. Not legal advice.</p>' + cta('injury', 'contingency-fee-calculator');
      show(cf, html);
    });
  }

  /* 4. Court deadline days calculator */
  function nthWeekday(y, m, wd, n) { var d = new Date(Date.UTC(y, m, 1)); var add = (wd - d.getUTCDay() + 7) % 7; return new Date(Date.UTC(y, m, 1 + add + (n - 1) * 7)); }
  function lastWeekday(y, m, wd) { var d = new Date(Date.UTC(y, m + 1, 0)); var sub = (d.getUTCDay() - wd + 7) % 7; return new Date(Date.UTC(y, m, d.getUTCDate() - sub)); }
  function observed(d) { var w = d.getUTCDay(); if (w === 6) return new Date(d - DAY); if (w === 0) return new Date(+d + DAY); return d; }
  var holCache = {};
  function holidays(y) {
    if (holCache[y]) return holCache[y];
    var list = [
      ['New Year’s Day', observed(new Date(Date.UTC(y, 0, 1)))], ['Martin Luther King Jr. Day', nthWeekday(y, 0, 1, 3)],
      ['Washington’s Birthday', nthWeekday(y, 1, 1, 3)], ['Memorial Day', lastWeekday(y, 4, 1)],
      ['Juneteenth', observed(new Date(Date.UTC(y, 5, 19)))], ['Independence Day', observed(new Date(Date.UTC(y, 6, 4)))],
      ['Labor Day', nthWeekday(y, 8, 1, 1)], ['Columbus Day', nthWeekday(y, 9, 1, 2)],
      ['Veterans Day', observed(new Date(Date.UTC(y, 10, 11)))], ['Thanksgiving Day', nthWeekday(y, 10, 4, 4)],
      ['Christmas Day', observed(new Date(Date.UTC(y, 11, 25)))]
    ];
    var map = {}; list.forEach(function (h) { map[h[1].toISOString().slice(0, 10)] = h[0]; });
    holCache[y] = map; return map;
  }
  function holidayName(d) {
    var k = d.toISOString().slice(0, 10);
    return holidays(d.getUTCFullYear())[k] || holidays(d.getUTCFullYear() + 1)[k] || null;
  }
  function isBusiness(d) { var w = d.getUTCDay(); return w !== 0 && w !== 6 && !holidayName(d); }
  var cd = $('form[data-calc="days"]');
  if (cd) cd.addEventListener('submit', function (e) {
    e.preventDefault();
    var start = parseDate($('#cd-start').value), n = Math.max(1, Math.round(num('cd-n'))), mode = $('#cd-mode').value;
    var dir = $('#cd-dir').value === 'b' ? -1 : 1, roll = $('#cd-roll').checked;
    if (!start) { show(cd, '<div class="warn">Choose a start date.</div>'); return; }
    var d = new Date(+start), skipped = [];
    if (mode === 'cal') d = new Date(+start + dir * n * DAY);
    else { var c = 0; while (c < n) { d = new Date(+d + dir * DAY); if (isBusiness(d)) c++; else if (holidayName(d)) skipped.push(holidayName(d) + ' (' + d.toISOString().slice(0, 10) + ')'); } }
    var rolled = '';
    if (roll && !isBusiness(d)) {
      var orig = new Date(+d);
      while (!isBusiness(d)) d = new Date(+d + dir * DAY);
      rolled = '<div class="warn">Day ' + n + ' landed on ' + fmtDate(orig) + (holidayName(orig) ? ' (' + holidayName(orig) + ')' : ' (weekend)') + ', so it moves to the ' + (dir > 0 ? 'next' : 'previous') + ' business day.</div>';
    }
    var html = '<p class="eyebrow">' + n + ' ' + (mode === 'cal' ? 'calendar' : 'business') + ' days ' + (dir > 0 ? 'after' : 'before') + ' ' + fmtDate(start) + '</p><p class="big">' + fmtDate(d) + '</p>' + rolled;
    if (skipped.length) html += '<p class="small">Federal holidays skipped: ' + esc(skipped.join(', ')) + '.</p>';
    html += '<p class="small muted">Uses US federal holidays only. Local court rules, state holidays, court closures and extra days for mail service can change the result. Confirm with the court or a lawyer.</p>';
    show(cd, html);
  });

  /* 5. Demand letter generator */
  var ml = $('form[data-calc="letter"]');
  if (ml) {
    ml.addEventListener('submit', function (e) {
      e.preventDefault();
      var g = function (id) { return ($('#' + id).value || '').trim(); };
      var type = g('ml-type'), you = g('ml-you') || '[Your name]', ya = g('ml-youaddr') || '[Your address]';
      var them = g('ml-them') || '[Recipient name]', ta = g('ml-themaddr') || '[Recipient address]';
      var amt = num('ml-amt'), when = g('ml-date'), facts = g('ml-facts') || '[Briefly describe what happened.]', days = g('ml-days'), st = g('ml-state');
      var today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
      var dueD = new Date(Date.now() + days * DAY).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
      var whenTxt = when ? parseDate(when).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }) : '[date]';
      var amtTxt = amt ? money(amt).replace('$', '$') : '$[amount]';
      var subj = { money: 'Demand for Payment of Money Owed', deposit: 'Demand for Return of Security Deposit', damage: 'Demand for Payment for Property Damage', refund: 'Demand for Refund' }[type];
      var body = {
        money: 'On or about ' + whenTxt + ', you agreed to pay me ' + amtTxt + '. Despite my previous requests, this amount remains unpaid.',
        deposit: 'I was your tenant and my tenancy ended on or about ' + whenTxt + '. I returned possession of the premises and provided my forwarding address. To date, my security deposit has not been returned' + (st ? ' as required by the laws of ' + st : ' as required by law') + ', and I have not received a proper itemized statement of deductions. I demand return of ' + amtTxt + '.',
        damage: 'On or about ' + whenTxt + ', my property was damaged as a result of your actions or negligence. The cost to repair or replace the damaged property is ' + amtTxt + '.',
        refund: 'On or about ' + whenTxt + ', I purchased goods or services from you. They were defective or not provided as agreed, and you have not issued a refund. I demand a refund of ' + amtTxt + '.'
      }[type];
      var letter = you + '\n' + ya + '\n\n' + today + '\n\nSENT BY CERTIFIED MAIL / EMAIL\n\n' + them + '\n' + ta + '\n\nRe: ' + subj + '\n\nDear ' + them + ',\n\n' +
        body + '\n\nThe facts are as follows:\n' + facts + '\n\n' +
        'I request payment of ' + amtTxt + ' no later than ' + dueD + ' (' + days + ' days from the date of this letter). Payment may be made by [check / bank transfer / other method] to the address above.\n\n' +
        'If I do not receive payment by that date, I intend to pursue all available legal remedies, which may include filing a claim in ' + (st ? st + ' ' : '') + 'small claims court to recover the amount owed plus court costs and any other amounts permitted by law, without further notice.\n\n' +
        'I would prefer to resolve this matter without going to court. Please contact me promptly to arrange payment.\n\nSincerely,\n\n\n' + you + '\n\nEnclosures: [copies of receipts, agreements, photos, correspondence]';
      $('#ml-out').value = letter;
      var r = $('[data-result]', ml.parentNode); r.hidden = false; r.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    doc.addEventListener('click', function (e) {
      var c = e.target.closest('[data-copy]'), p = e.target.closest('[data-print-letter]'), d = e.target.closest('[data-download]');
      var ta = $('#ml-out'); if (!ta) return;
      if (c) { ta.select(); (navigator.clipboard ? navigator.clipboard.writeText(ta.value) : Promise.resolve(doc.execCommand('copy'))).then(function () { c.textContent = 'Copied!'; setTimeout(function () { c.textContent = 'Copy'; }, 1500); }); }
      if (p) { var w = window.open('', '_blank'); if (w) { w.document.write('<pre style="font:14px/1.6 Georgia,serif;white-space:pre-wrap;max-width:700px;margin:40px auto">' + esc(ta.value) + '</pre>'); w.document.close(); w.focus(); w.print(); } }
      if (d) { var a = doc.createElement('a'); a.href = URL.createObjectURL(new Blob([ta.value], { type: 'text/plain' })); a.download = 'demand-letter.txt'; a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000); }
    });
  }

  /* 6. Do I need a lawyer quiz */
  var nl = $('form[data-calc="needlawyer"]');
  if (nl) nl.addEventListener('submit', function (e) {
    e.preventDefault();
    var total = 0, missing = false, issue = 'other';
    ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'].forEach(function (q) {
      var c = $('input[name="' + q + '"]:checked', nl);
      if (!c) missing = true; else { total += +c.value; if (q === 'q1') issue = c.getAttribute('data-issue'); }
    });
    if (missing) { show(nl, '<div class="warn">Please answer all six questions.</div>'); return; }
    var max = 17, pct = Math.round(total / max * 100), level, text;
    if (total >= 11) { level = 'High: talk to a lawyer now'; text = 'Your answers point to serious stakes, a near deadline or an opponent with professional help. Speaking to an attorney quickly is strongly recommended, and many offer free consultations.'; }
    else if (total >= 6) { level = 'Moderate: get a consultation soon'; text = 'A short consultation could clarify your options and protect deadlines. Our guides and tools can help you prepare.'; }
    else { level = 'Lower: self-help may work'; text = 'You may be able to handle this yourself with good information, for example in small claims court. A quick consultation is still wise if anything changes.'; }
    var html = '<p class="eyebrow">Your urgency score: ' + total + ' / ' + max + '</p><p class="big">' + level + '</p><div class="meter" aria-hidden="true"><span style="width:' + pct + '%"></span></div><p>' + text + '</p>';
    html += cta(issue, 'do-i-need-a-lawyer', total >= 6 ? 'Start my free case review' : 'Ask for a free review anyway');
    html += '<p class="small"><a href="' + ROOT + 'legal-aid/">Low income? Find free legal aid →</a></p>';
    show(nl, html);
  });
})();
