/* index-2570.js — พฤติกรรมเฉพาะหน้า index ใหม่ (ธีม "เว็บ 2570") */
(function(){
  "use strict";

  /* ---------- Header: หดตอนเลื่อนลง ---------- */
  var header = document.querySelector(".h25-header");
  if(header){
    var onScroll = function(){
      header.classList.toggle("is-stuck", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, {passive:true});
  }

  /* ---------- แคปซูลไฮไลต์เมนู เลื่อนตามเมาส์ ---------- */
  var navUl = document.querySelector(".h25-nav > .h25-wrap > ul");
  if(navUl){
    var pill = document.createElement("span");
    pill.className = "h25-nav__pill";
    pill.setAttribute("aria-hidden","true");
    navUl.appendChild(pill);

    var links = Array.prototype.slice.call(navUl.querySelectorAll(":scope > li > a"));
    var currentLink = links.find(function(a){ return a.getAttribute("aria-current") === "page"; });

    function movePillTo(el, isCurrent){
      var navRect = navUl.getBoundingClientRect();
      var r = el.getBoundingClientRect();
      pill.style.left = (r.left - navRect.left) + "px";
      pill.style.width = r.width + "px";
      pill.classList.toggle("is-current", !!isCurrent);
      pill.classList.toggle("is-active", !isCurrent);
    }

    links.forEach(function(a){
      a.addEventListener("mouseenter", function(){ movePillTo(a, a === currentLink); });
    });
    navUl.addEventListener("mouseleave", function(){
      if(currentLink){ movePillTo(currentLink, true); }
    });

    if(currentLink){
      window.addEventListener("load", function(){ movePillTo(currentLink, true); });
      window.addEventListener("resize", function(){ movePillTo(currentLink, true); });
    }
  }

  /* ---------- ค้นหา ---------- */
  var searchForm = document.querySelector("[data-h25-search]");
  if(searchForm && window.MANAROM_SEARCH){
    var input = searchForm.querySelector("input");
    var resultsEl = searchForm.querySelector(".h25-search__results");
    var data = window.MANAROM_SEARCH.th || [];

    function render(list, q){
      resultsEl.innerHTML = "";
      if(!list.length){
        resultsEl.innerHTML = '<p class="h25-search__empty">ไม่พบผลลัพธ์สำหรับ "' + q + '"</p>';
        resultsEl.hidden = false;
        return;
      }
      var ul = document.createElement("ul");
      list.slice(0, 8).forEach(function(item){
        var li = document.createElement("li");
        var a = document.createElement("a");
        var isExternal = item.x === 1 || /^https?:\/\//.test(item.u);
        a.href = item.u;
        if(isExternal){ a.target = "_blank"; a.rel = "noopener"; }
        a.innerHTML = '<span class="h25-sr-title"></span><span class="h25-sr-cat"></span>';
        a.querySelector(".h25-sr-title").textContent = item.t;
        a.querySelector(".h25-sr-cat").textContent = item.c;
        li.appendChild(a);
        ul.appendChild(li);
      });
      resultsEl.appendChild(ul);
      resultsEl.hidden = false;
    }

    function search(q){
      q = q.trim().toLowerCase();
      if(!q){ resultsEl.hidden = true; resultsEl.innerHTML = ""; return; }
      var hits = data.filter(function(item){
        return (item.t && item.t.toLowerCase().indexOf(q) !== -1) ||
               (item.k && item.k.toLowerCase().indexOf(q) !== -1);
      });
      render(hits, q);
    }

    input.addEventListener("input", function(){ search(input.value); });
    searchForm.addEventListener("submit", function(e){
      e.preventDefault();
      var first = resultsEl.querySelector("a");
      if(first){ first.click(); }
    });
    document.addEventListener("click", function(e){
      if(!searchForm.contains(e.target)){ resultsEl.hidden = true; }
    });
  }

  /* ---------- เมนูมือถือ ---------- */
  var burger = document.querySelector(".h25-burger");
  var drawer = document.querySelector(".h25-drawer");
  if(burger && drawer){
    var closeBtn = drawer.querySelector(".h25-drawer__close");
    var scrim = drawer.querySelector(".h25-drawer__scrim");

    function openDrawer(){
      drawer.classList.add("is-open");
      drawer.setAttribute("aria-hidden","false");
      burger.setAttribute("aria-expanded","true");
      document.body.style.overflow = "hidden";
    }
    function closeDrawer(){
      drawer.classList.remove("is-open");
      drawer.setAttribute("aria-hidden","true");
      burger.setAttribute("aria-expanded","false");
      document.body.style.overflow = "";
    }
    burger.addEventListener("click", openDrawer);
    closeBtn && closeBtn.addEventListener("click", closeDrawer);
    scrim && scrim.addEventListener("click", closeDrawer);

    drawer.querySelectorAll("[data-h25-toggle-sub]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var sub = document.getElementById(btn.getAttribute("aria-controls"));
        var open = sub.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });
  }

  /* ---------- ไอคอนค้นหา (มือถือ) ---------- */
  var mobileSearchBtn = document.querySelector(".h25-iconbtn[data-h25-mobile-search]");
  var mobileSearchWrap = document.querySelector("[data-h25-search]");
  if(mobileSearchBtn && mobileSearchWrap){
    mobileSearchBtn.addEventListener("click", function(){
      var opening = !mobileSearchWrap.classList.contains("is-mobile-open");
      mobileSearchWrap.classList.toggle("is-mobile-open", opening);
      if(opening){ mobileSearchWrap.querySelector("input").focus(); }
    });
  }

  /* ---------- น้องใจดี: fade-in ตัวละครพร้อมกล่องตอนโหลดหน้า ---------- */
  var fab = document.querySelector(".fab");
  var bubble = document.getElementById("jd-bubble");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function store(k, v){
    try{
      if(v === undefined) return sessionStorage.getItem(k);
      sessionStorage.setItem(k, v);
    }catch(e){ return null; }
  }
  if(fab){
    requestAnimationFrame(function(){
      requestAnimationFrame(function(){ fab.classList.add("h25-fab-ready"); });
    });
  }
  /* app.js ถูกกันไว้ไม่ให้เด้งเอง (ดูสคริปต์ก่อน app.js ใน index.html) → คืนค่าเดิมทันที */
  if(window.h25JdHold){
    try{ sessionStorage.removeItem("jd-closed"); }catch(e){}
  }
  var fabBtn = fab ? fab.querySelector(".fab__main") : null;
  var mqMobile = window.matchMedia("(max-width: 767px)");
  var mqHover = window.matchMedia("(hover: hover)");

  /* พิมพ์ข้อความทักทายในกล่อง (เหมือนสไตล์ของ app.js) */
  function typeGreeting(){
    var textEl = bubble.querySelector(".jd-bubble__text");
    var msgs = [];
    try{ msgs = JSON.parse((document.getElementById("jd-msgs") || {}).textContent || "[]"); }catch(e){}
    if(!textEl || !msgs.length){ return; }
    var greeting = msgs[0];
    if(reduceMotion){ textEl.textContent = greeting; bubble.classList.add("is-done"); return; }
    var n = 0;
    bubble.classList.remove("is-done");
    (function typeStep(){
      textEl.textContent = greeting.slice(0, ++n);
      if(n < greeting.length){ setTimeout(typeStep, 38); }
      else{ bubble.classList.add("is-done"); }
    })();
  }

  /* คอม: กล่องเต็ม (ข้อความ + 4 อารมณ์) เด้งเองเมื่อเลื่อนผ่าน Hero · ครั้งเดียวต่อ session · ไม่เปิดเมนู 3 ปุ่ม */
  var heroEl = document.querySelector(".h25-hero");
  if(bubble && heroEl && "IntersectionObserver" in window){
    var autoIo = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting || en.boundingClientRect.bottom > 0){ return; } /* ยังไม่ผ่าน Hero */
        if(mqMobile.matches || !mqHover.matches){ return; }
        autoIo.disconnect();
        if(store("h25-jd-auto") || store("jd-closed") || !bubble.hidden || fab.classList.contains("is-open")){ return; }
        store("h25-jd-auto", "1");
        bubble.hidden = false;
        typeGreeting();
      });
    });
    autoIo.observe(heroEl);
  }

  /* มือถือ: ป้ายคำพูดเล็กข้างน้องใจดี · หายเองใน 5 วิ · ครั้งเดียวต่อ session */
  if(fab && fabBtn && mqMobile.matches && !store("h25-jd-tip")){
    var tip = document.createElement("div");
    tip.className = "h25-jd-tip";
    tip.setAttribute("role", "status");
    tip.innerHTML = '<button class="h25-jd-tip__text" type="button">มีอะไรให้ช่วยไหมคะ 💙</button>' +
      '<button class="h25-jd-tip__x" type="button" aria-label="ปิดข้อความ"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>';
    fab.appendChild(tip);
    var hideTip = function(){
      tip.classList.remove("is-show");
      setTimeout(function(){ if(tip.parentNode){ tip.parentNode.removeChild(tip); } }, 400);
    };
    store("h25-jd-tip", "1");
    setTimeout(function(){ tip.classList.add("is-show"); }, 1200);
    var tipTimer = setTimeout(hideTip, 6200); /* แสดง 5 วินาที */
    tip.querySelector(".h25-jd-tip__x").addEventListener("click", function(e){ e.stopPropagation(); clearTimeout(tipTimer); hideTip(); });
    tip.querySelector(".h25-jd-tip__text").addEventListener("click", function(e){ e.stopPropagation(); clearTimeout(tipTimer); hideTip(); fabBtn.click(); });
  }

  /* มือถือ: แตะน้องใจดี → bottom sheet (4 อารมณ์ + 3 ปุ่ม) · พื้นหลังมืด · ล็อกการเลื่อน · Esc/✕/พื้นหลัง ปิด */
  if(fab && fabBtn && bubble){
    var scrim = document.createElement("div");
    scrim.className = "h25-jd-scrim";
    scrim.setAttribute("aria-hidden", "true");
    document.body.appendChild(scrim);
    var sheetOpen = false;

    var openSheet = function(){
      sheetOpen = true;
      bubble.hidden = false;
      bubble.setAttribute("aria-modal", "true");
      document.documentElement.classList.add("h25-sheet-open");
      var x = bubble.querySelector(".jd-bubble__x");
      setTimeout(function(){ if(x){ x.focus({preventScroll:true}); } }, 50);
    };
    var closeSheet = function(returnFocus){
      if(!sheetOpen){ return; }
      sheetOpen = false;
      fab.classList.remove("is-open");
      fabBtn.setAttribute("aria-expanded", "false");
      bubble.hidden = true;
      bubble.removeAttribute("aria-modal");
      document.documentElement.classList.remove("h25-sheet-open");
      if(returnFocus !== false){ fabBtn.focus({preventScroll:true}); }
    };

    /* app.js สลับ .is-open ก่อน (ผูกไว้ก่อน) → อ่านสถานะแล้วเปิด/ปิด sheet ตาม */
    fabBtn.addEventListener("click", function(){
      if(!mqMobile.matches){ return; }
      if(fab.classList.contains("is-open")){ openSheet(); } else { closeSheet(); }
    });
    scrim.addEventListener("click", function(){ closeSheet(); });
    bubble.querySelector(".jd-bubble__x").addEventListener("click", function(){
      if(sheetOpen){ closeSheet(); }
    });
    document.addEventListener("keydown", function(e){
      if(e.key !== "Escape"){ return; }
      if(sheetOpen){ closeSheet(); return; }
      if(!bubble.hidden && !mqMobile.matches){ /* คอม: Esc ปิดกล่องและเมนูด้วย */
        bubble.hidden = true;
        fab.classList.remove("is-open");
        fabBtn.setAttribute("aria-expanded", "false");
        fabBtn.focus({preventScroll:true});
      }
    });
    /* วนโฟกัสอยู่ใน sheet ตอนเปิด */
    bubble.addEventListener("keydown", function(e){
      if(!sheetOpen || e.key !== "Tab"){ return; }
      var f = Array.prototype.filter.call(bubble.querySelectorAll("button, a[href]"), function(el){ return el.offsetParent !== null; });
      if(!f.length){ return; }
      var first = f[0], last = f[f.length - 1];
      if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    });
    /* หมุนจอ/ขยายหน้าต่างจนพ้นมือถือ → ปิด sheet */
    if(mqMobile.addEventListener){ mqMobile.addEventListener("change", function(){ if(!mqMobile.matches){ closeSheet(false); } }); }
  }

  /* ---------- ปุ่มกลับขึ้นด้านบน: แสดงเมื่อเลื่อนเกิน 400px ---------- */
  var totop = document.querySelector(".totop");
  if(totop){
    var onTotopScroll = function(){
      totop.classList.toggle("h25-totop-on", window.scrollY > 400);
    };
    onTotopScroll();
    window.addEventListener("scroll", onTotopScroll, {passive:true});
  }

  /* ---------- Hero: เฟดโผล่ตอนเปิดหน้า (ห่างกันทีละ 80ms) ---------- */
  var hero = document.querySelector(".h25-hero");
  var isTouch = window.matchMedia("(hover: none)").matches;
  var heroCards = Array.prototype.slice.call(document.querySelectorAll(".h25-hero__card"));
  /* จอ ≤767px: ไอคอนอยู่ในกรอบ 96px → จัดชิดซ้ายล่าง · จอใหญ่คืนค่าเดิม (ตรงกลาง) */
  var narrowMq = window.matchMedia("(max-width: 767px)");
  function alignHeroIcons(){
    heroCards.forEach(function(card){
      var svg = card.querySelector(".h25-hero__icon");
      if(!svg){ return; }
      if(narrowMq.matches){ svg.setAttribute("preserveAspectRatio", "xMinYMax meet"); }
      else{ svg.removeAttribute("preserveAspectRatio"); }
    });
  }
  alignHeroIcons();
  if(narrowMq.addEventListener){ narrowMq.addEventListener("change", alignHeroIcons); }
  if(hero && !reduceMotion){
    /* มือถือจริง: การ์ดไม่ร่วมเฟดตอนเปิดหน้า แต่เด้งขึ้นทีละใบตอนเลื่อนเข้าจอ (ด้านล่าง) */
    if(isTouch && "IntersectionObserver" in window){
      heroCards.forEach(function(card){ card.removeAttribute("data-hero-in"); card.classList.add("h25-pop-wait"); });
      var popIo = new IntersectionObserver(function(entries){
        var shown = entries.filter(function(en){ return en.isIntersecting; });
        shown.forEach(function(en, i){
          popIo.unobserve(en.target);
          setTimeout(function(){ en.target.classList.add("is-pop"); }, i * 80);
        });
      }, {threshold:.2});
      heroCards.forEach(function(card){ popIo.observe(card); });
    }
    var heroIn = Array.prototype.slice.call(hero.querySelectorAll("[data-hero-in]"));
    hero.classList.add("js-hero");
    requestAnimationFrame(function(){
      requestAnimationFrame(function(){
        heroIn.forEach(function(el, i){
          setTimeout(function(){ el.classList.add("is-in"); }, i * 80);
        });
      });
    });
  }

  /* ---------- Hero: การ์ดเป็นขาวตอนแตะ (มือถือ — :active ไม่แน่นอนใน Safari) ---------- */
  heroCards.forEach(function(card){
    function release(){ setTimeout(function(){ card.classList.remove("is-pressed"); }, 150); }
    card.addEventListener("pointerdown", function(e){
      if(e.pointerType !== "mouse"){ card.classList.add("is-pressed"); }
    });
    ["pointerup","pointercancel","pointerleave"].forEach(function(t){ card.addEventListener(t, release); });
  });

  /* ---------- Hero: สไลด์ (เลื่อนเองทุก 5 วิ · hover หยุด · จุดกดได้ · ปัดได้) ---------- */
  var slider = document.querySelector(".h25-hero__slider");
  if(slider){
    var slides = Array.prototype.slice.call(slider.querySelectorAll(".h25-hero__slide"));
    var dots = Array.prototype.slice.call(slider.querySelectorAll(".h25-hero__dot"));
    var current = 0, timer = null, paused = false;

    function goTo(n){
      n = (n + slides.length) % slides.length;
      if(n === current){ return; }
      slides.forEach(function(s, i){
        var on = i === n;
        s.classList.toggle("is-active", on);
        s.setAttribute("aria-hidden", on ? "false" : "true");
        s.querySelectorAll("a").forEach(function(a){
          if(on){ a.removeAttribute("tabindex"); } else { a.setAttribute("tabindex", "-1"); }
        });
      });
      dots.forEach(function(d, i){ d.setAttribute("aria-selected", i === n ? "true" : "false"); });
      current = n;
    }
    function stop(){ clearInterval(timer); timer = null; }
    function start(){
      stop();
      if(!paused && !reduceMotion){ timer = setInterval(function(){ goTo(current + 1); }, 5000); }
    }

    dots.forEach(function(d, i){
      d.addEventListener("click", function(){ goTo(i); start(); });
    });
    slider.addEventListener("mouseenter", function(){ paused = true; stop(); });
    slider.addEventListener("mouseleave", function(){ paused = false; start(); });
    slider.addEventListener("focusin", function(){ paused = true; stop(); });
    slider.addEventListener("focusout", function(e){
      if(!slider.contains(e.relatedTarget)){ paused = false; start(); }
    });
    document.addEventListener("visibilitychange", function(){
      if(document.hidden){ stop(); } else { start(); }
    });

    /* ปัดซ้าย–ขวา (มือถือ/ทัชแพด) — ปัดแล้วไม่นับเป็นการกดลิงก์ */
    var startX = 0, startY = 0, swiped = false;
    slider.addEventListener("touchstart", function(e){
      startX = e.touches[0].clientX; startY = e.touches[0].clientY; swiped = false;
    }, {passive:true});
    slider.addEventListener("touchend", function(e){
      var dx = e.changedTouches[0].clientX - startX;
      var dy = e.changedTouches[0].clientY - startY;
      if(Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)){
        swiped = true;
        goTo(current + (dx < 0 ? 1 : -1));
        start();
      }
    }, {passive:true});
    slider.addEventListener("click", function(e){
      if(swiped){ e.preventDefault(); swiped = false; }
    }, true);

    start();
  }

  /* ---------- การบริการ: เลื่อนมาเจอแล้วเฟดโผล่ทีละแถว (ห่างกัน 80ms) ---------- */
  var reveals = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
  if(reveals.length && !reduceMotion && "IntersectionObserver" in window){
    document.documentElement.classList.add("js-reveal");
    var revealIo = new IntersectionObserver(function(entries){
      entries.filter(function(en){ return en.isIntersecting; }).forEach(function(en, i){
        revealIo.unobserve(en.target);
        setTimeout(function(){ en.target.classList.add("is-in"); }, i * 80);
      });
    }, {threshold:.15, rootMargin:"0px 0px -40px 0px"});
    reveals.forEach(function(el){ revealIo.observe(el); });
  }

  /* ---------- การบริการ + นัดหมาย: สถานะแตะบนจอสัมผัส ---------- */
  document.querySelectorAll(".h25-svc__type, .h25-age__card, .h25-pill, .h25-appt__tel").forEach(function(el){
    function release(){ setTimeout(function(){ el.classList.remove("is-pressed"); }, 150); }
    el.addEventListener("pointerdown", function(e){
      if(e.pointerType !== "mouse"){ el.classList.add("is-pressed"); }
    });
    ["pointerup","pointercancel","pointerleave"].forEach(function(t){ el.addEventListener(t, release); });
  });

  /* ---------- นัดหมาย: คอม (มีเมาส์) กดแล้วคัดลอกเบอร์ · มือถือโทรด้วย tel: ตามปกติ ---------- */
  var apptToast = document.querySelector(".h25-appt__toast");
  var canHover = window.matchMedia("(hover: hover)");
  function copyText(text){
    if(navigator.clipboard && window.isSecureContext){ return navigator.clipboard.writeText(text); }
    return new Promise(function(resolve, reject){
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try{ ok = document.execCommand("copy"); }catch(e){}
      document.body.removeChild(ta);
      if(ok){ resolve(); } else { reject(); }
    });
  }
  document.querySelectorAll(".h25-appt__tel[data-copy]").forEach(function(a){
    a.addEventListener("click", function(e){
      if(!canHover.matches){ return; }
      e.preventDefault();
      copyText(a.getAttribute("data-copy")).then(function(){
        if(!apptToast){ return; }
        apptToast.textContent = "คัดลอกแล้ว ✓";
        apptToast.classList.add("is-show");
        clearTimeout(apptToast._t);
        apptToast._t = setTimeout(function(){ apptToast.classList.remove("is-show"); }, 1800);
      }, function(){ window.location.href = a.href; }); /* คัดลอกไม่ได้ → โทรแทน */
    });
  });
  /* ---------- แบบประเมิน + Corporate: สไลด์ ----------
     คอม: เลื่อนเองทุก 6 วิ · ชี้เมาส์/โฟกัสคีย์บอร์ดแล้วหยุด · จุดกดได้ · ลากปัดได้
     มือถือ (≤767px): เลื่อนเองด้วย scroll-snap · ไม่เลื่อนอัตโนมัติ · เส้นบอกตำแหน่งขยับตามการปัด */
  var acMq = window.matchMedia("(max-width: 767px)");
  document.querySelectorAll("[data-ac-carousel]").forEach(function(root){
    var viewport = root.querySelector(".h25-ac__viewport");
    var track = root.querySelector(".h25-ac__track");
    var cards = Array.prototype.slice.call(root.querySelectorAll(".h25-ac__card"));
    var dots = Array.prototype.slice.call(root.querySelectorAll(".h25-ac__dot"));
    var thumb = root.querySelector(".h25-ac__thumb");
    var current = 0, timer = null, hovered = false, kbFocus = false, drag = null, justDragged = false;
    if(thumb){ thumb.style.width = (100 / cards.length) + "%"; }

    function sync(){
      var mobile = acMq.matches;
      cards.forEach(function(card, i){
        var hidden = !mobile && i !== current;
        if(hidden){ card.setAttribute("aria-hidden", "true"); } else { card.removeAttribute("aria-hidden"); }
        card.querySelectorAll("a").forEach(function(a){
          if(hidden){ a.setAttribute("tabindex", "-1"); } else { a.removeAttribute("tabindex"); }
        });
      });
      dots.forEach(function(d, i){ d.setAttribute("aria-current", i === current ? "true" : "false"); });
      track.style.setProperty("--i", current);
    }
    function goTo(n){ current = (n + cards.length) % cards.length; sync(); }
    function stop(){ clearInterval(timer); timer = null; }
    function start(){
      stop();
      if(reduceMotion || acMq.matches || hovered || kbFocus || document.hidden || cards.length < 2){ return; }
      timer = setInterval(function(){ goTo(current + 1); }, 6000);
    }

    dots.forEach(function(d, i){ d.addEventListener("click", function(){ goTo(i); start(); }); });
    root.addEventListener("mouseenter", function(){ hovered = true; stop(); });
    root.addEventListener("mouseleave", function(){ hovered = false; start(); });
    root.addEventListener("focusin", function(e){
      kbFocus = e.target.matches(":focus-visible");
      if(kbFocus){ stop(); }
    });
    root.addEventListener("focusout", function(e){
      if(!root.contains(e.relatedTarget)){ kbFocus = false; start(); }
    });
    document.addEventListener("visibilitychange", start);

    /* ลากปัด (เมาส์/ทัชแพด/แท็บเล็ต) — ลากแล้วไม่นับเป็นการกดลิงก์ */
    viewport.addEventListener("pointerdown", function(e){
      justDragged = false;
      if(acMq.matches || (e.pointerType === "mouse" && e.button !== 0)){ return; }
      drag = {id:e.pointerId, x:e.clientX, y:e.clientY, dx:0, moved:false};
    });
    viewport.addEventListener("pointermove", function(e){
      if(!drag || e.pointerId !== drag.id){ return; }
      var dx = e.clientX - drag.x;
      if(!drag.moved){
        if(Math.abs(dx) < 6){ return; }
        if(Math.abs(e.clientY - drag.y) > Math.abs(dx)){ drag = null; return; } /* เลื่อนหน้าขึ้นลง */
        drag.moved = true;
        track.classList.add("is-dragging");
        try{ viewport.setPointerCapture(e.pointerId); }catch(err){}
        stop();
      }
      drag.dx = dx;
      track.style.setProperty("--dx", dx + "px");
    });
    function endDrag(){
      if(!drag){ return; }
      var d = drag;
      drag = null;
      if(!d.moved){ return; }
      justDragged = true;
      track.classList.remove("is-dragging");
      track.style.setProperty("--dx", "0px");
      if(Math.abs(d.dx) > Math.min(80, viewport.clientWidth * .15)){ goTo(current + (d.dx < 0 ? 1 : -1)); }
      start();
    }
    viewport.addEventListener("pointerup", endDrag);
    viewport.addEventListener("pointercancel", endDrag);
    viewport.addEventListener("click", function(e){
      if(justDragged){ e.preventDefault(); e.stopPropagation(); justDragged = false; }
    }, true);
    viewport.addEventListener("dragstart", function(e){ e.preventDefault(); });

    /* มือถือ: เส้นบอกตำแหน่ง · คอม: กันช่องมองถูกเลื่อนเอง (เช่น ตอนโฟกัสลิงก์) */
    var ticking = false;
    viewport.addEventListener("scroll", function(){
      if(!acMq.matches){ if(viewport.scrollLeft){ viewport.scrollLeft = 0; } return; }
      if(ticking || !thumb){ return; }
      ticking = true;
      requestAnimationFrame(function(){
        ticking = false;
        var max = viewport.scrollWidth - viewport.clientWidth;
        var p = max > 0 ? Math.min(1, viewport.scrollLeft / max) : 0;
        thumb.style.transform = "translateX(" + (p * (cards.length - 1) * 100) + "%)";
      });
    }, {passive:true});

    /* แตะบนจอสัมผัส: ยุบ 0.97 (Safari :active ไม่แน่นอน) */
    cards.concat(root.parentNode.querySelector(".h25-ac__all") || []).forEach(function(el){
      function release(){ setTimeout(function(){ el.classList.remove("is-pressed"); }, 150); }
      el.addEventListener("pointerdown", function(e){
        if(e.pointerType !== "mouse"){ el.classList.add("is-pressed"); }
      });
      ["pointerup","pointercancel","pointerleave"].forEach(function(t){ el.addEventListener(t, release); });
    });

    function onMq(){
      viewport.scrollLeft = 0;
      if(thumb){ thumb.style.transform = ""; }
      sync();
      start();
    }
    if(acMq.addEventListener){ acMq.addEventListener("change", onMq); }
    sync();
    start();
  });

})();
