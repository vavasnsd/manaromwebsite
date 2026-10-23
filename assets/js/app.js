/* =========================================================
   Manarom website — interactions
   Plain JavaScript, no framework. Each block is independent:
   if a page does not have the element, the block does nothing.
   ========================================================= */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.remove("no-js");
  root.classList.add("js");
  var LANG = root.lang === "en" ? "en" : "th";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  var T = {
    th: {
      required: "กรุณากรอกช่องนี้",
      choose: "กรุณาเลือกอย่างน้อย 1 ข้อ",
      email: "รูปแบบอีเมลไม่ถูกต้อง เช่น name@email.com",
      phone: "กรุณากรอกเบอร์โทร 9–10 หลัก เช่น 0812345678",
      consent: "กรุณายอมรับนโยบายข้อมูลส่วนบุคคลก่อนส่ง",
      date: "กรุณาเลือกวันที่ตั้งแต่วันนี้เป็นต้นไป",
      fix: "ยังมีช่องที่ต้องแก้ไข",
      sending: "กำลังส่ง…",
      failed: "ส่งข้อมูลไม่สำเร็จ กรุณาลองใหม่ หรือโทรหาเรา",
      copied: "คัดลอกแล้ว",
      copyFail: "คัดลอกไม่ได้ ลองเลือกข้อความแล้วคัดลอกเอง",
      linkCopied: "คัดลอกลิงก์บทความแล้ว",
      answerAll: "ตอบข้อนี้ก่อนไปข้อถัดไป",
      subscribed: "สมัครรับข่าวสารแล้ว ขอบคุณค่ะ",
      count: function (a, b) { return "ข้อ " + a + " จาก " + b; },
      none: "—"
    },
    en: {
      required: "Please fill in this field",
      choose: "Please choose at least one option",
      email: "Please enter a valid email, e.g. name@email.com",
      phone: "Please enter a 9–10 digit phone number, e.g. 0812345678",
      consent: "Please accept the privacy policy before sending",
      date: "Please pick today or a later date",
      fix: "Some fields still need attention",
      sending: "Sending…",
      failed: "We couldn't send this. Please try again or call us.",
      copied: "Copied",
      copyFail: "Couldn't copy. Select the text and copy it manually.",
      linkCopied: "Article link copied",
      answerAll: "Please answer this question first",
      subscribed: "You're subscribed. Thank you!",
      count: function (a, b) { return "Question " + a + " of " + b; },
      none: "—"
    }
  }[LANG];

  /* ---------- Toast ---------- */
  var toastEl;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg;
    toastEl.classList.add("is-show");
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.classList.remove("is-show"); }, 2600);
  }

  /* ---------- Header, scroll progress, back to top ---------- */
  var header = $(".hdr") || $(".header"), bar = $(".progress"), reading = $(".reading"), totop = $(".totop");
  var ticking = false;
  function onScroll() {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    var p = h > 0 ? Math.min(1, y / h) : 0;
    if (header) header.classList.toggle("is-scrolled", y > 10);
    if (bar) bar.style.transform = "scaleX(" + p + ")";
    if (totop) totop.classList.toggle("is-show", y > 600);
    if (reading) {
      var art = $(".article");
      if (art) {
        var r = art.getBoundingClientRect(), total = r.height - window.innerHeight * .5;
        var rp = Math.max(0, Math.min(1, -r.top / Math.max(1, total)));
        reading.style.transform = "scaleX(" + rp + ")";
      }
    }
    ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();
  if (totop) totop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- Mobile drawer ---------- */
  var drawer = $(".drawer"), burger = $(".burger");
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
    drawer.setAttribute("aria-hidden", String(!open));
    document.body.style.overflow = open ? "hidden" : "";
    $$("nav a", drawer).forEach(function (a, i) { a.style.transitionDelay = open ? (80 + i * 40) + "ms" : "0ms"; });
    if (open) { var c = $(".drawer__close", drawer); if (c) c.focus(); } else if (burger) { burger.focus(); }
  }
  if (burger && drawer) {
    burger.addEventListener("click", function () { setDrawer(!drawer.classList.contains("is-open")); });
    $$("[data-close-drawer]", drawer).forEach(function (el) { el.addEventListener("click", function () { setDrawer(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("is-open")) setDrawer(false); });
    window.addEventListener("resize", function () { if (window.innerWidth > 1180 && drawer.classList.contains("is-open")) setDrawer(false); });
  }

  /* ---------- Floating helper: Nong Jaidee ---------- */
  var fab = $(".fab");
  var bubble = $("#jd-bubble");
  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }
  var typer = { timer: null, rot: null, i: 0, msgs: [] };
  try { typer.msgs = JSON.parse(($("#jd-msgs") || {}).textContent || "[]"); } catch (e) { typer.msgs = []; }
  function typeText(el, text, done) {
    clearTimeout(typer.timer);
    if (reduce) { el.textContent = text; if (done) done(); return; }
    var n = 0; el.textContent = "";
    bubble.classList.remove("is-done");
    (function step() { el.textContent = text.slice(0, ++n); if (n < text.length) typer.timer = setTimeout(step, 38); else if (done) done(); })();
  }
  function rotate() {
    if (!bubble || !typer.msgs.length) return;
    var txt = $(".jd-bubble__text", bubble);
    typeText(txt, typer.msgs[typer.i % typer.msgs.length], function () {
      typer.rot = setTimeout(function () { typer.i++; if (!bubble.hidden && !bubble.classList.contains("has-reply")) rotate(); }, 4200);
    });
  }
  function showBubble() { if (!bubble) return; bubble.hidden = false; clearTimeout(typer.rot); if (!bubble.classList.contains("has-reply")) rotate(); }
  function hideBubble() { if (!bubble) return; bubble.hidden = true; clearTimeout(typer.timer); clearTimeout(typer.rot); }
  if (fab) {
    var fabBtn = $(".fab__main", fab);
    fabBtn.addEventListener("click", function () {
      var open = !fab.classList.contains("is-open");
      fab.classList.toggle("is-open", open);
      fabBtn.setAttribute("aria-expanded", String(open));
      if (open) showBubble();
    });
    document.addEventListener("click", function (e) { if (!fab.contains(e.target)) { fab.classList.remove("is-open"); fabBtn.setAttribute("aria-expanded", "false"); } });
    if (bubble) {
      $(".jd-bubble__x", bubble).addEventListener("click", function () { hideBubble(); store("jd-closed", "1"); });
      if (!store("jd-closed")) setTimeout(function () { if (bubble.hidden) showBubble(); }, 3000);
    }
  }

  /* ---------- Reveal on scroll ---------- */
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target;
      el.classList.remove("is-pending");
      el.classList.add("is-in");
      if (el.hasAttribute("data-count")) runCounter(el);
      io.unobserve(el);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }) : null;

  function inView(el) { var r = el.getBoundingClientRect(); return r.top < window.innerHeight && r.bottom > 0; }
  $$(".reveal, .step, [data-count]").forEach(function (el) {
    if (!io || reduce || inView(el)) { el.classList.add("is-in"); return; }
    if (el.classList.contains("reveal")) el.classList.add("is-pending");
    if (el.hasAttribute("data-count")) el.textContent = "0";
    io.observe(el);
  });

  function runCounter(el) {
    var end = parseInt(el.getAttribute("data-count"), 10) || 0, start = performance.now(), dur = 1400;
    (function frame(now) {
      var t = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(end * e).toLocaleString();
      if (t < 1) requestAnimationFrame(frame);
    })(start);
  }

  /* ---------- Carousel ---------- */
  $$(".carousel").forEach(function (c) {
    var slides = $$(".carousel__slide", c), dots = $$(".carousel__dot", c), i = 0, timer, dur = 5200;
    if (slides.length < 2) return;
    c.style.setProperty("--dur", dur + "ms");
    function go(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle("is-active", k === i); s.setAttribute("aria-hidden", String(k !== i)); });
      dots.forEach(function (d, k) {
        d.classList.remove("is-active");
        d.classList.toggle("is-done", k < i);
        d.setAttribute("aria-current", String(k === i));
      });
      void (dots[i] && dots[i].offsetWidth);
      if (dots[i]) dots[i].classList.add("is-active");
      schedule();
    }
    function schedule() { clearTimeout(timer); if (!reduce && !c.classList.contains("is-paused")) timer = setTimeout(function () { go(i + 1); }, dur); }
    var prev = $("[data-prev]", c), next = $("[data-next]", c);
    if (prev) prev.addEventListener("click", function () { go(i - 1); });
    if (next) next.addEventListener("click", function () { go(i + 1); });
    dots.forEach(function (d, k) { d.addEventListener("click", function () { go(k); }); });
    c.addEventListener("mouseenter", function () { c.classList.add("is-paused"); clearTimeout(timer); });
    c.addEventListener("mouseleave", function () { c.classList.remove("is-paused"); schedule(); });
    c.addEventListener("focusin", function () { c.classList.add("is-paused"); clearTimeout(timer); });
    c.addEventListener("focusout", function () { c.classList.remove("is-paused"); schedule(); });
    var sx = null;
    c.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    c.addEventListener("touchend", function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1)); sx = null; });
    document.addEventListener("visibilitychange", function () { if (document.hidden) clearTimeout(timer); else schedule(); });
    go(0);
  });

  /* ---------- Mood check-in ---------- */
  var mood = $(".mood");
  if (mood) {
    var ans = $(".mood__answer", mood), text = $("[data-mood-text]", mood), link = $("[data-mood-link]", mood), linkLabel = $("[data-mood-link-label]", mood);
    $$(".mood__opt", mood).forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".mood__opt", mood).forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        text.textContent = b.getAttribute("data-msg");
        link.setAttribute("href", b.getAttribute("data-href"));
        linkLabel.textContent = b.getAttribute("data-cta");
        ans.classList.add("is-open");
        ans.setAttribute("aria-hidden", "false");
      });
    });
  }

  /* ---------- Mood check-in v2 (section + Nong Jaidee bubble) ---------- */
  var MOODS = [];
  try { MOODS = JSON.parse(($("#mood-data") || {}).textContent || "[]"); } catch (e) { MOODS = []; }
  function moodBy(k) { return MOODS.filter(function (m) { return m.key === k; })[0]; }
  function faceSvg(k) { var b = document.querySelector('.mood__opt[data-mood="' + k + '"] svg, .jd-mood[data-mood="' + k + '"] svg'); return b ? b.outerHTML : ""; }
  var READ = LANG === "en" ? "Read on manarom.com" : "อ่านบน manarom.com";
  var EXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>';
  function esc(x) { var d = document.createElement("div"); d.textContent = x; return d.innerHTML; }
  $$(".mood2").forEach(function (sec) {
    var ans = $(".mood__answer", sec), text = $("[data-mood-text]", sec), arts = $("[data-mood-arts]", sec), extra = $("[data-mood-extra]", sec);
    $$(".mood__opt", sec).forEach(function (btn) {
      btn.addEventListener("click", function () {
        var m = moodBy(btn.getAttribute("data-mood")); if (!m) return;
        $$(".mood__opt", sec).forEach(function (o) { o.setAttribute("aria-pressed", String(o === btn)); });
        text.textContent = m.msg;
        var face = btn.querySelector("svg").outerHTML;
        arts.innerHTML = m.articles.map(function (a) {
          return '<a class="mart" href="' + a.u + '" target="_blank" rel="noopener"><span class="mart__img"><img src="' + a.img + '" alt="" loading="lazy"><span class="mart__face">' + face + '</span></span><span class="mart__body"><b>' + esc(a.t) + '</b><small>' + READ + EXT + '</small></span></a>';
        }).join("");
        if (m.extra) { extra.hidden = false; extra.href = m.extra.u; extra.innerHTML = esc(m.extra.t) + ' →'; } else extra.hidden = true;
        ans.classList.add("is-open"); ans.setAttribute("aria-hidden", "false");
      });
    });
  });
  if (bubble) {
    var reply = $(".jd-bubble__reply", bubble);
    $$(".jd-mood", bubble).forEach(function (btn) {
      btn.addEventListener("click", function () {
        var m = moodBy(btn.getAttribute("data-mood")); if (!m) return;
        $$(".jd-mood", bubble).forEach(function (o) { o.setAttribute("aria-pressed", String(o === btn)); });
        bubble.classList.add("has-reply"); clearTimeout(typer.rot);
        typeText($(".jd-bubble__text", bubble), m.msg, function () { bubble.classList.add("is-done"); });
        var a = m.articles[0];
        reply.innerHTML = '<span>' + (LANG === "en" ? "Nong Jaidee recommends:" : "น้องใจดีแนะนำ:") + '</span><a href="' + a.u + '" target="_blank" rel="noopener">' + esc(a.t) + EXT + '</a>' +
          (m.extra ? '<a href="' + m.extra.u + '">' + esc(m.extra.t) + ' →</a>' : '') + '<a href="knowledge.html">' + (LANG === "en" ? "More articles" : "ดูบทความเพิ่มเติม") + ' →</a>';
        reply.hidden = false;
      });
    });
  }

  /* ---------- Site search (header) ---------- */
  var IDX = (window.MANAROM_SEARCH || {})[LANG] || [];
  var hdrEl = $(".hdr"), sBtn = $(".hdr__searchbtn");
  if (sBtn && hdrEl) sBtn.addEventListener("click", function () {
    var open = !hdrEl.classList.contains("search-open");
    hdrEl.classList.toggle("search-open", open); sBtn.setAttribute("aria-expanded", String(open));
    if (open) { var i = $(".search2 input", hdrEl); if (i) i.focus(); }
  });
  function norm(x) { return (x || "").toLowerCase(); }
  $$("[data-site-search]").forEach(function (form) {
    var input = $("input", form), list = $(".search2__results", form), active = -1, hits = [];
    var NONE = LANG === "en" ? "No results. Try another word, or call us." : "ไม่พบผลลัพธ์ ลองคำอื่น หรือโทรสอบถามเรา";
    function close() { list.hidden = true; input.setAttribute("aria-expanded", "false"); active = -1; }
    function mark(t, q) { var i = norm(t).indexOf(q); if (i < 0 || !q) return esc(t); return esc(t.slice(0, i)) + "<mark>" + esc(t.slice(i, i + q.length)) + "</mark>" + esc(t.slice(i + q.length)); }
    function render() {
      var q = norm(input.value.trim());
      if (!q) { close(); return; }
      var words = q.split(/\s+/);
      hits = IDX.map(function (e) {
        var hay = norm(e.t + " " + (e.k || "") + " " + e.c), score = 0;
        for (var w = 0; w < words.length; w++) { if (hay.indexOf(words[w]) < 0) return null; }
        if (norm(e.t).indexOf(q) === 0) score += 3; else if (norm(e.t).indexOf(q) > -1) score += 2;
        if (e.c === (LANG === "en" ? "Service" : "บริการ")) score += 1;
        return { e: e, s: score };
      }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
      list.innerHTML = hits.length ? hits.map(function (h, i) {
        return '<li role="option"><a href="' + h.e.u + '"' + (h.e.x ? ' target="_blank" rel="noopener"' : '') + ' id="' + list.id + '-' + i + '"><span class="cat">' + esc(h.e.c) + '</span><span>' + mark(h.e.t, q) + '</span>' + (h.e.x ? EXT : '') + '</a></li>';
      }).join("") : '<li class="none">' + NONE + '</li>';
      list.hidden = false; input.setAttribute("aria-expanded", "true"); active = -1;
    }
    function move(d) {
      var links = $$("a", list); if (!links.length) return;
      active = (active + d + links.length) % links.length;
      links.forEach(function (l, i) { l.setAttribute("aria-selected", String(i === active)); });
      input.setAttribute("aria-activedescendant", links[active].id);
      links[active].scrollIntoView({ block: "nearest" });
    }
    input.addEventListener("input", render);
    input.addEventListener("focus", function () { if (input.value.trim()) render(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Escape") { close(); }
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var links = $$("a", list); if (!links.length) { render(); links = $$("a", list); }
      var target = links[active > -1 ? active : 0];
      if (target) target.click();
    });
    document.addEventListener("click", function (e) { if (!form.contains(e.target)) close(); });
  });

  /* ---------- Filter + search + load more ---------- */
  $$("[data-collection]").forEach(function (box) {
    var list = document.getElementById(box.getAttribute("data-collection"));
    if (!list) return;
    var items = $$("[data-item]", list), empty = document.getElementById(box.getAttribute("data-collection") + "-empty");
    var search = $("[data-search]", box), btns = $$("[data-filter]", box);
    var more = document.getElementById(box.getAttribute("data-collection") + "-more");
    var pageSize = parseInt(list.getAttribute("data-page-size") || "0", 10), shown = pageSize;
    var cat = "all";
    function apply() {
      var q = (search && search.value || "").trim().toLowerCase(), visible = 0, matched = 0;
      items.forEach(function (it) {
        var okCat = cat === "all" || (it.getAttribute("data-cat") || "").split(" ").indexOf(cat) > -1;
        var okQ = !q || (it.getAttribute("data-text") || it.textContent).toLowerCase().indexOf(q) > -1;
        var ok = okCat && okQ;
        if (ok) matched++;
        var hideByPage = pageSize && ok && matched > shown;
        it.classList.toggle("is-filtered-out", !ok || hideByPage);
        if (ok && !hideByPage) visible++;
      });
      if (empty) empty.hidden = visible > 0;
      if (more) more.hidden = !(pageSize && matched > shown);
    }
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        cat = b.getAttribute("data-filter");
        shown = pageSize;
        btns.forEach(function (o) {
          var on = o === b;
          if (o.getAttribute("role") === "tab") o.setAttribute("aria-selected", String(on)); else o.setAttribute("aria-pressed", String(on));
        });
        apply();
      });
    });
    if (search) search.addEventListener("input", function () { shown = pageSize; apply(); });
    if (more) more.addEventListener("click", function () { shown += pageSize; apply(); });
    apply();
  });

  /* ---------- Accordion ---------- */
  $$(".acc__btn").forEach(function (b) {
    b.addEventListener("click", function () {
      var open = b.getAttribute("aria-expanded") !== "true";
      b.setAttribute("aria-expanded", String(open));
      document.getElementById(b.getAttribute("aria-controls")).classList.toggle("is-open", open);
    });
  });

  /* ---------- Modals (services, doctors) ---------- */
  $$("[data-open-modal]").forEach(function (trigger) {
    trigger.addEventListener("click", function () {
      var dlg = document.getElementById(trigger.getAttribute("data-open-modal"));
      if (!dlg || typeof dlg.showModal !== "function") return;
      $$("[data-slot]", dlg).forEach(function (slot) {
        var key = slot.getAttribute("data-slot"), val = trigger.getAttribute("data-" + key);
        if (val === null) return;
        if (slot.tagName === "IMG") slot.src = val; else slot.textContent = val;
      });
      dlg.showModal();
    });
  });
  $$("dialog.modal").forEach(function (dlg) {
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    $$("[data-close]", dlg).forEach(function (b) { b.addEventListener("click", function () { dlg.close(); }); });
  });

  /* ---------- Copy buttons ---------- */
  function copyText(txt, okMsg) {
    var done = function () { toast(okMsg || T.copied); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(txt).then(done, function () { toast(T.copyFail); });
    } else { toast(T.copyFail); }
  }
  $$("[data-copy]").forEach(function (b) { b.addEventListener("click", function () { copyText(b.getAttribute("data-copy")); }); });
  $$("[data-share]").forEach(function (b) { b.addEventListener("click", function () { copyText(location.href, T.linkCopied); }); });

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* =========================================================
     Forms: validation + submit (demo or live API)
     ========================================================= */
  var Api = {
    submit: function (kind, payload) {
      var c = window.MANAROM_CONFIG || {}, ep = c.ENDPOINTS && c.ENDPOINTS[kind];
      var ref = (kind.slice(0, 3).toUpperCase()) + "-" + Date.now().toString(36).toUpperCase().slice(-6);
      if (!c.API_BASE || !ep) {
        return new Promise(function (res) { setTimeout(function () { res({ ok: true, demo: true, ref: ref }); }, 700); });
      }
      var ctrl = "AbortController" in window ? new AbortController() : null;
      var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, c.TIMEOUT_MS || 15000);
      var headers = Object.assign({ "Content-Type": "application/json", "Accept": "application/json" }, c.HEADERS || {});
      return fetch(c.API_BASE.replace(/\/$/, "") + ep, { method: "POST", headers: headers, body: JSON.stringify(payload), signal: ctrl ? ctrl.signal : undefined })
        .then(function (r) {
          clearTimeout(to);
          return r.json().catch(function () { return {}; }).then(function (body) {
            if (!r.ok) throw new Error(body.message || ("HTTP " + r.status));
            return { ok: true, demo: false, ref: body.reference || body.ref || body.id || ref };
          });
        });
    }
  };
  window.ManaromApi = Api;

  function fieldWrap(el) { return el.closest(".field") || el.parentElement; }
  function setError(el, msg) {
    var w = fieldWrap(el), e = w && $(".err", w);
    if (w) w.classList.toggle("has-error", !!msg);
    if (e) e.textContent = msg || "";
    el.setAttribute("aria-invalid", msg ? "true" : "false");
  }
  function isHidden(el) { return !!el.closest("[hidden]"); }
  function validateField(el) {
    if (isHidden(el) || el.disabled) { setError(el, ""); return true; }
    var v = (el.value || "").trim(), msg = "";
    if (el.type === "checkbox" && el.required && !el.checked) msg = el.name === "consent_pdpa" ? T.consent : T.required;
    else if (el.type === "radio") {
      var group = $$('input[name="' + el.name + '"]', el.form);
      if (el.required && !group.some(function (r) { return r.checked; })) msg = T.choose;
    }
    else if (el.required && !v) msg = T.required;
    else if (v && el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) msg = T.email;
    else if (v && el.type === "tel" && !/^0\d{8,9}$/.test(v.replace(/[\s-]/g, ""))) msg = T.phone;
    else if (v && el.type === "date" && el.hasAttribute("data-future")) {
      var d = new Date(v + "T00:00:00"), today = new Date(); today.setHours(0, 0, 0, 0);
      if (d < today) msg = T.date;
    }
    setError(el, msg);
    return !msg;
  }
  function validateScope(scope) {
    var ok = true, first = null, seen = {};
    $$("input, select, textarea", scope).forEach(function (el) {
      if (el.type === "radio") { if (seen[el.name]) return; seen[el.name] = 1; }
      if (!validateField(el)) { ok = false; if (!first) first = el; }
    });
    if (first) { first.focus({ preventScroll: true }); first.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" }); }
    return ok;
  }
  function collect(form) {
    var data = {};
    $$("input, select, textarea", form).forEach(function (el) {
      if (!el.name || isHidden(el)) return;
      if (el.type === "radio") { if (el.checked) data[el.name] = el.value; return; }
      if (el.type === "checkbox") {
        if (el.hasAttribute("data-multi")) { data[el.name] = data[el.name] || []; if (el.checked) data[el.name].push(el.value); }
        else data[el.name] = el.checked;
        return;
      }
      data[el.name] = el.value.trim();
    });
    return data;
  }
  function labelFor(el) {
    if (el.getAttribute("data-label")) return el.getAttribute("data-label");
    var w = fieldWrap(el), l = w && $("label, legend", w);
    return l ? l.textContent.replace("*", "").trim() : el.name;
  }

  /* Conditional fields: data-show-if="name=value" */
  function syncConditional(form) {
    $$("[data-show-if]", form).forEach(function (box) {
      var parts = box.getAttribute("data-show-if").split("="), sel = $$('[name="' + parts[0] + '"]', form), val = "";
      sel.forEach(function (s) { if ((s.type === "radio" || s.type === "checkbox") ? s.checked : true) val = s.value; });
      box.hidden = parts[1].split("|").indexOf(val) < 0;
    });
  }

  $$("form[data-form]").forEach(function (form) {
    var kind = form.getAttribute("data-form");
    form.setAttribute("novalidate", "");
    syncConditional(form);
    form.addEventListener("change", function (e) { syncConditional(form); if (e.target.matches("input, select, textarea")) validateField(e.target); });
    form.addEventListener("focusout", function (e) { if (e.target.matches("input:not([type=radio]):not([type=checkbox]), select, textarea") && e.target.value) validateField(e.target); });
    $$("input[type=date][data-future]", form).forEach(function (d) { d.min = new Date().toISOString().slice(0, 10); });

    /* Wizard */
    var steps = $$(".wstep", form), marks = $$(".wizard__steps li", form.parentElement), cur = 0;
    function showStep(n) {
      cur = n;
      steps.forEach(function (s, k) { s.classList.toggle("is-active", k === n); });
      marks.forEach(function (m, k) { m.classList.toggle("is-current", k === n); m.classList.toggle("is-done", k < n); if (k === n) m.setAttribute("aria-current", "step"); else m.removeAttribute("aria-current"); });
      if (steps[n] && steps[n].hasAttribute("data-review")) buildReview(steps[n]);
      var top = form.parentElement.getBoundingClientRect().top + window.scrollY - 100;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: reduce ? "auto" : "smooth" });
      var h = steps[n] && $("h2, h3", steps[n]); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
    }
    function buildReview(step) {
      var dl = $(".review", step); if (!dl) return;
      dl.innerHTML = "";
      var seen = {};
      $$("input, select, textarea", form).forEach(function (el) {
        if (!el.name || isHidden(el) || el.type === "checkbox" || seen[el.name] || el.closest("[data-review]")) return;
        var v;
        if (el.type === "radio") { var c = $('input[name="' + el.name + '"]:checked', form); seen[el.name] = 1; v = c ? (c.getAttribute("data-label") || c.value) : ""; }
        else if (el.tagName === "SELECT") v = el.value ? el.options[el.selectedIndex].text : "";
        else v = el.value.trim();
        var dt = document.createElement("dt"), dd = document.createElement("dd");
        dt.textContent = el.type === "radio" ? labelFor($('input[name="' + el.name + '"]', form)) : labelFor(el);
        dd.textContent = v || T.none;
        dl.appendChild(dt); dl.appendChild(dd);
      });
    }
    $$("[data-next-step]", form).forEach(function (b) { b.addEventListener("click", function () { if (validateScope(steps[cur])) showStep(cur + 1); }); });
    $$("[data-prev-step]", form).forEach(function (b) { b.addEventListener("click", function () { showStep(cur - 1); }); });
    if (steps.length) showStep(0);

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validateScope(form)) { toast(T.fix); return; }
      var btn = $("[type=submit]", form), label = btn ? btn.innerHTML : "";
      if (btn) { btn.classList.add("is-loading"); btn.disabled = true; }
      var payload = {
        form: kind,
        lang: LANG,
        submitted_at: new Date().toISOString(),
        page: location.pathname.split("/").pop() || "index.html",
        data: collect(form)
      };
      Api.submit(kind, payload).then(function (res) {
        if (kind === "newsletter") { form.reset(); toast(T.subscribed); return; }
        var ok = document.querySelector('[data-success-for="' + kind + '"]');
        if (ok) {
          var refEl = $("[data-ref]", ok); if (refEl) refEl.textContent = res.ref;
          var pre = $("pre", ok); if (pre) pre.textContent = JSON.stringify(payload, null, 2);
          var demo = $("[data-demo-note]", ok); if (demo) demo.hidden = !res.demo;
          form.hidden = true; ok.hidden = false;
          var wiz = $(".wizard__steps", form.parentElement); if (wiz) wiz.hidden = true;
          var h = $("h3", ok); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); }
        }
      }).catch(function () { toast(T.failed); }).then(function () {
        if (btn) { btn.classList.remove("is-loading"); btn.disabled = false; btn.innerHTML = label; }
      });
    });
  });
  $$("[data-reset-form]").forEach(function (b) {
    b.addEventListener("click", function () {
      var form = $('form[data-form="' + b.getAttribute("data-reset-form") + '"]');
      var ok = b.closest("[data-success-for]");
      if (!form) return;
      form.reset(); form.hidden = false; if (ok) ok.hidden = true;
      var wiz = $(".wizard__steps", form.parentElement); if (wiz) wiz.hidden = false;
      syncConditional(form);
      var first = $(".wstep", form); if (first) { $$(".wstep", form).forEach(function (s, k) { s.classList.toggle("is-active", k === 0); }); $$(".wizard__steps li", form.parentElement).forEach(function (m, k) { m.classList.toggle("is-current", k === 0); m.classList.remove("is-done"); }); }
    });
  });

  /* =========================================================
     Self-assessment quiz
     ========================================================= */
  var quiz = $("#quiz"), qdata = $("#quiz-data");
  if (quiz && qdata) {
    var Q = JSON.parse(qdata.textContent), answers = [], at = 0;
    var cards = $$(".qcard", quiz), fill = $(".quiz__fill", quiz), count = $(".quiz__count", quiz);
    var prevB = $("[data-q-prev]", quiz), nextB = $("[data-q-next]", quiz), nav = $(".quiz__nav", quiz), result = $(".result", quiz);
    function render() {
      cards.forEach(function (c, k) { c.classList.toggle("is-active", k === at); });
      fill.style.width = (answers.filter(function (a) { return a !== undefined; }).length / cards.length * 100) + "%";
      count.textContent = T.count(at + 1, cards.length);
      prevB.disabled = at === 0;
      nextB.textContent = at === cards.length - 1 ? Q.labels.finish : Q.labels.next;
    }
    $$(".qopt", quiz).forEach(function (o) {
      o.addEventListener("click", function () {
        var card = o.closest(".qcard"), k = cards.indexOf(card);
        answers[k] = parseInt(o.getAttribute("data-score"), 10);
        $$(".qopt", card).forEach(function (x) { x.setAttribute("aria-pressed", String(x === o)); });
        render();
        if (k < cards.length - 1) setTimeout(function () { if (at === k) { at++; render(); } }, reduce ? 0 : 380);
      });
    });
    prevB.addEventListener("click", function () { if (at > 0) { at--; render(); } });
    nextB.addEventListener("click", function () {
      if (answers[at] === undefined) { toast(T.answerAll); return; }
      if (at < cards.length - 1) { at++; render(); return; }
      finish();
    });
    function finish() {
      var total = answers.reduce(function (a, b) { return a + b; }, 0), max = Q.max;
      var band = Q.bands.filter(function (b) { return total >= b.min && total <= b.max; })[0] || Q.bands[0];
      cards.forEach(function (c) { c.classList.remove("is-active"); });
      nav.hidden = true; $(".quiz__bar", quiz).hidden = true;
      result.classList.add("is-active");
      $("[data-r-level]", result).textContent = band.label;
      $("[data-r-advice]", result).textContent = band.advice;
      $$(".levels div", result).forEach(function (d, k) { d.classList.toggle("is-on", Q.bands[k] === band); });
      var arc = $("[data-arc]", result), num = $("[data-r-score]", result), len = arc.getTotalLength ? arc.getTotalLength() : 280;
      arc.style.strokeDasharray = len; arc.style.strokeDashoffset = len;
      requestAnimationFrame(function () { arc.style.transition = "stroke-dashoffset 1.4s cubic-bezier(.2,.7,.2,1)"; arc.style.strokeDashoffset = len * (1 - total / max); });
      var s = performance.now();
      (function f(n) { var t = Math.min(1, (n - s) / 1200); num.textContent = Math.round(total * t); if (t < 1) requestAnimationFrame(f); })(s);
      var h = $("h2", result); h.setAttribute("tabindex", "-1"); h.focus();
      var c = window.MANAROM_CONFIG || {};
      if (c.SEND_ASSESSMENT_RESULTS) Api.submit("assessment", { form: "assessment", lang: LANG, submitted_at: new Date().toISOString(), data: { test_id: Q.id, answers: answers, score: total, level: band.key } }).catch(function () {});
    }
    $("[data-q-restart]", quiz).addEventListener("click", function () {
      answers = []; at = 0; result.classList.remove("is-active"); nav.hidden = false; $(".quiz__bar", quiz).hidden = false;
      $$(".qopt", quiz).forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      render();
    });
    render();
  }
})();
