#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manarom site v2 — Wawa's /WebDevelopment brief (6 Oct 2026).
Reuses page builders from build.py and replaces header, home, services,
corporate, contact, pricing, FAQ, about and knowledge with real content."""
import os, json, html
import build as b
import content as C

E = html.escape
I = b.I
OUT = b.OUT
ph = b.ph

I["bell"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M8 2v4M16 2v4M3 10h18M8 14h3v3H8z"/></svg>'
I["down"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
I["ext"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>'
I["train"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14M9 21l-2-3M15 21l2-3"/><circle cx="9" cy="14" r=".6"/><circle cx="15" cy="14" r=".6"/></svg>'
I["car"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14v-5l-2-5H7l-2 5z"/><circle cx="8" cy="17" r="2"/><circle cx="16" cy="17" r="2"/><path d="M5 12h14"/></svg>'
I["fax"] = I["receipt"]
I["calendar"] = I["bell"]
I["corp"] = I["building"]

def sv(slug):
    return next(s for s in C.SERVICES if s["slug"] == slug)

def svc_href(slug):
    return f"service-{slug}.html"

def img_tag(c, key, alt="", cls="", sizes="(max-width: 860px) 100vw, 50vw", lazy=True):
    kind, name = key.split(":")
    if kind == "photo":
        base = c.p + C.PHOTO[name]
        return (f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="{base}.jpg" srcset="{base}-sm.jpg 800w, {base}.jpg 1600w" sizes="{sizes}" '
                f'alt="{E(alt)}" width="1600" height="1067"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""}>')
    return f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="{c.p}assets/img/{name}.svg" alt="{E(alt)}" width="800" height="600"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""}>'

# ---------------------------------------------------------------- mood + search data
def mood_json(c):
    t = c.t
    out = []
    for k, a, bb, m1, m2, arts in C.MOODS:
        out.append({"key": k, "label": t(a, bb), "msg": t(m1, m2),
                    "articles": [{"t": t(C.ART[x][0], C.ART[x][1]), "u": C.ART[x][2], "img": f"{c.p}{C.PHOTO[C.ART[x][3]]}-sm.jpg"} for x in arts],
                    "extra": {"t": t("เช็กความเครียด 1 นาที", "1-minute stress check"), "u": "test.html"} if k == "tense" else
                             ({"t": t("นัดคุยกับผู้เชี่ยวชาญ", "Talk to a specialist"), "u": "register.html"} if k == "sad" else None)})
    return json.dumps(out, ensure_ascii=False)

def search_entries(lang):
    c = b.Ctx(lang)
    t = c.t
    e = []
    for k, f, a, bb, m in b.PAGES:
        e.append({"t": t(a, bb), "c": t("หน้า", "Page"), "u": f})
    for f, a, bb in [("pricing.html", "อัตราค่าบริการ", "Rates"), ("faq.html", "คำถามที่พบบ่อย", "FAQ"), ("register.html", "ลงทะเบียนผู้ป่วยใหม่ / นัดหมายแพทย์", "New patient registration / book a doctor"),
                     ("test.html", "แบบประเมินความเครียด ST-5", "Stress check ST-5"), ("corporate.html#psychotest", "Psychotest แบบทดสอบจิตวิทยาสำหรับองค์กร", "Psychotest for organisations"),
                     ("corporate.html#training", "Training อบรมพัฒนาบุคลากร", "Staff training"), ("contact.html#jobs", "ร่วมงานกับเรา / สมัครงาน", "Careers"), ("contact.html#map", "แผนที่ การเดินทาง BTS บางนา", "Map and directions, BTS Bang Na")]:
        e.append({"t": t(a, bb), "c": t("หน้า", "Page"), "u": f})
    for s in C.SERVICES:
        kws = " ".join(t(x, y) for h1, h2, items in s["sec"] for x, y in items)
        e.append({"t": t(s["th"], s["en"]), "c": t("บริการ", "Service"), "u": svc_href(s["slug"]), "k": t(s["s_th"], s["s_en"]) + " " + kws})
    for cat, th, en, live in b.TESTS:
        e.append({"t": t(th, en), "c": t("แบบประเมิน", "Assessment"), "u": "test.html" if live else "assessments.html"})
    for k, (th, en, u, img) in C.ART.items():
        e.append({"t": t(th, en), "c": t("บทความ", "Article"), "u": u, "x": 1})
    for typ, a, bb in b.DTYPES:
        e.append({"t": t(a, bb), "c": t("ค้นหาแพทย์", "Doctors"), "u": "doctors.html"})
    for code, en, th, enn in C.PSYCHOTESTS:
        e.append({"t": f"{code} {en}", "c": "Psychotest", "u": "corporate.html#psychotest", "k": t(th, enn)})
    return e

# ---------------------------------------------------------------- layout
NAV = [("home", "index.html", "หน้าหลัก", "Home"), ("about", "about.html", "เกี่ยวกับเรา", "About Us"),
       ("services", "services.html", "การบริการ", "Services"), ("pricing", "pricing.html", "อัตราค่าบริการ", "Rates"),
       ("corporate", "corporate.html", "บริการสำหรับองค์กร", "For Organizations"), ("contact", "contact.html", "ติดต่อเรา", "Contact Us")]

def services_menu(c):
    t = c.t
    cols = []
    for g, a, bb in C.GROUPS:
        items = "".join(f'<li><a href="{svc_href(s["slug"])}"><span class="mi">{I[s["icon"]]}</span>{t(s["th"], s["en"])}</a></li>' for s in C.SERVICES if C.GROUP_OF[s["slug"]] == g)
        cols.append(f'<div><p class="mega__h">{t(a, bb)}</p><ul>{items}</ul></div>')
    return f'<div class="mega" role="group" aria-label="{t("บริการทั้งหมด", "All services")}"><div class="mega__grid">{"".join(cols)}</div><a class="mega__all" href="services.html">{t("ดูบริการทั้งหมด", "See all services")}{I["arrow"]}</a></div>'

def corp_menu(c):
    t = c.t
    return (f'<div class="drop"><ul><li><a href="corporate.html#psychotest"><span class="mi">{I["brain"]}</span>Psychotest<small>{t("แบบทดสอบจิตวิทยาเพื่อคัดเลือกบุคลากร", "Psychological tests for hiring")}</small></a></li>'
            f'<li><a href="corporate.html#training"><span class="mi">{I["chalk"]}</span>Training<small>{t("อบรมพัฒนาบุคลากร", "Staff training & development")}</small></a></li></ul></div>')

def layout(c, key, file, title, desc, body, reading=False):
    t, p = c.t, c.p
    other = ("en/" + file) if c.lang == "th" else ("../" + file)
    th_href, en_href = (file, other) if c.lang == "th" else (other, file)
    navkey = {"assess": "home", "knowledge": "home", "doctors": "home", "register": "home", "faq": "home", "svc": "services"}.get(key, key)
    lis = []
    for k, f, a, bb in NAV:
        cur = ' aria-current="page"' if k == navkey else ""
        if k == "services":
            lis.append(f'<li class="has-drop"><a href="{f}"{cur} aria-haspopup="true">{t(a, bb)}{I["down"]}</a>{services_menu(c)}</li>')
        elif k == "corporate":
            lis.append(f'<li class="has-drop has-drop--sm"><a href="{f}"{cur} aria-haspopup="true">{t(a, bb)}{I["down"]}</a>{corp_menu(c)}</li>')
        else:
            lis.append(f'<li><a href="{f}"{cur}>{t(a, bb)}</a></li>')
    dsub = "".join(f'<a class="dsub" href="{svc_href(s["slug"])}">{t(s["th"], s["en"])}</a>' for s in C.SERVICES)
    dnav = []
    for k, f, a, bb in NAV:
        cur = ' aria-current="page"' if k == navkey else ""
        if k == "services":
            dnav.append(f'<details class="dgroup"><summary>{t(a, bb)}{I["down"]}</summary><a class="dsub dsub--all" href="services.html">{t("ภาพรวมบริการทั้งหมด", "All services overview")}</a>{dsub}</details>')
        elif k == "corporate":
            dnav.append(f'<details class="dgroup"><summary>{t(a, bb)}{I["down"]}</summary><a class="dsub" href="corporate.html#psychotest">Psychotest</a><a class="dsub" href="corporate.html#training">Training</a></details>')
        else:
            dnav.append(f'<a href="{f}"{cur}>{t(a, bb)}{I["right"]}</a>')
    for f, a, bb in [("doctors.html", "ค้นหาแพทย์", "Find a Doctor"), ("assessments.html", "แบบประเมินสุขภาพใจ", "Self-assessments"), ("knowledge.html", "คลังความรู้", "Knowledge"), ("faq.html", "คำถามที่พบบ่อย", "FAQ")]:
        dnav.append(f'<a href="{f}">{t(a, bb)}{I["right"]}</a>')
    lang_sw = (f'<span class="lang2" role="group" aria-label="{t("เลือกภาษา", "Language")}">'
               f'<a href="{th_href}" lang="th" hreflang="th"{" aria-current=\"true\"" if c.lang == "th" else ""}>TH</a><span aria-hidden="true">|</span>'
               f'<a href="{en_href}" lang="en" hreflang="en"{" aria-current=\"true\"" if c.lang == "en" else ""}>EN</a></span>')
    search = (f'<form class="search2" role="search" data-site-search action="#" autocomplete="off">'
              f'<label class="sr-only" for="q-{key}-{file}">{t("ค้นหาในเว็บไซต์", "Search the site")}</label>'
              f'<input id="q-{key}-{file}" type="search" placeholder="{t("ค้นหา บริการ แพทย์ บทความ…", "Search services, doctors, articles…")}" aria-autocomplete="list" aria-controls="sr-{key}" aria-expanded="false">'
              f'<button type="submit" aria-label="{t("ค้นหา", "Search")}">{I["search"]}</button>'
              f'<ul class="search2__results" id="sr-{key}" role="listbox" hidden></ul></form>')
    full_title = (title + " | " if key != "home" else "") + t("โรงพยาบาลมนารมย์", "Manarom Hospital")
    bubble_msgs = json.dumps([t("สวัสดีค่ะ น้องใจดีพร้อมช่วยเหลือนะคะ", "Hi! I'm Nong Jaidee, here to help."),
                              t("อยากนัดพบแพทย์? กดที่น้องใจดีได้เลยค่ะ", "Want to see a doctor? Tap me."),
                              t("หาทางมาโรงพยาบาลไม่เจอ ให้น้องใจดีพาไปค่ะ", "Not sure how to get here? I'll show you."),
                              t("วันนี้ใจเหนื่อยไหมคะ? เลือกอารมณ์ด้านล่างได้เลย", "How's your heart today? Pick a mood below.")], ensure_ascii=False)
    faces = "".join(f'<button class="jd-mood" type="button" data-mood="{k}" aria-label="{t(a, bb)}">{b.FACES[k]}<span>{t(a, bb)}</span></button>' for k, a, bb, *_ in C.MOODS)
    return f"""<!doctype html>
<html lang="{c.lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{p}assets/img/photos/garden-lounge.jpg">
<meta name="color-scheme" content="only light">
<meta name="theme-color" content="#113C80">
<link rel="icon" href="{p}assets/img/favicon.png">
<link rel="alternate" hreflang="th" href="{th_href}">
<link rel="alternate" hreflang="en" href="{en_href}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600&family=Prompt:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{p}assets/css/styles.css">
</head>
<body data-lang="{c.lang}">
<a class="skip" href="#main">{t("ข้ามไปเนื้อหาหลัก", "Skip to main content")}</a>
<div class="progress" aria-hidden="true"></div>
{'<div class="progress reading" aria-hidden="true" style="background:var(--blue-mid)"></div>' if reading else ''}
<header class="hdr">
  <div class="hdr__top">
    <div class="wrap">
      <a class="brand" href="index.html" aria-label="{t("หน้าหลัก โรงพยาบาลมนารมย์", "Manarom Hospital home")}"><img src="{p}assets/img/logo.png" alt="{t("โรงพยาบาลมนารมย์", "Manarom Hospital")}" width="168" height="48"></a>
      {search}
      <span class="hdr__phone">{I["phone"]}<span>{C.PHONE_1}</span><span class="sep" aria-hidden="true">|</span><span>{C.PHONE_2}</span></span>
      <a class="btn btn--primary btn--sm hdr__book" href="register.html">{I["calendar"]}{t("นัดหมายแพทย์", "Book a Doctor")}</a>
      {lang_sw}
      <button class="hdr__icon hdr__searchbtn" type="button" aria-label="{t("ค้นหา", "Search")}" aria-expanded="false">{I["search"]}</button>
      <button class="burger" type="button" aria-label="{t("เปิดเมนู", "Open menu")}" aria-expanded="false" aria-controls="drawer"><span></span></button>
    </div>
  </div>
  <nav class="hdr__nav" aria-label="{t("เมนูหลัก", "Main menu")}"><div class="wrap"><ul>{"".join(lis)}</ul></div></nav>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer__scrim" data-close-drawer></div>
  <div class="drawer__panel" role="dialog" aria-modal="true" aria-label="{t("เมนู", "Menu")}">
    <div class="drawer__top"><img src="{p}assets/img/logo.png" alt="" width="140" height="40"><button class="drawer__close" type="button" data-close-drawer aria-label="{t("ปิดเมนู", "Close menu")}">{I["close"]}</button></div>
    <nav aria-label="{t("เมนูหลัก", "Main menu")}">{"".join(dnav)}</nav>
    <div class="drawer__foot">
      <a class="btn btn--primary btn--block" href="register.html">{t("นัดหมายแพทย์", "Book a Doctor")}{I["arrow"]}</a>
      <span class="lang">{lang_sw}</span>
      <span class="muted" style="font-size:15px">{t("โทร", "Call")} {C.PHONE_1} · {C.PHONE_2}</span>
    </div>
  </div>
</div>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand stack">
        <img src="{p}assets/img/logo-white.png" alt="{t("โรงพยาบาลมนารมย์", "Manarom Hospital")}" width="161" height="46">
        <p>{t("พลังใจดี เริ่มที่...มนารมย์", "A stronger mind starts at Manarom")}</p>
        <span>{t(C.ADDR_TH, C.ADDR_EN)}</span>
        <span>{t("โทร", "Tel")} {C.PHONE_2} · {C.PHONE_1}<br>{t("โทรสาร", "Fax")} {C.FAX} · {C.EMAIL}</span>
        <span>{t(C.HOURS_TH, C.HOURS_EN)}</span>
      </div>
      <div>
        <h4>{t("เมนู", "Menu")}</h4>
        <ul>
          <li><a href="about.html">{t("เกี่ยวกับเรา", "About Us")}</a></li>
          <li><a href="doctors.html">{t("ค้นหาแพทย์", "Find a Doctor")}</a></li>
          <li><a href="pricing.html">{t("อัตราค่าบริการ", "Rates")}</a></li>
          <li><a href="knowledge.html">{t("คลังความรู้", "Knowledge")}</a></li>
          <li><a href="faq.html">{t("คำถามที่พบบ่อย", "FAQ")}</a></li>
          <li><a href="https://www.manarom.com/job_thai.html">{t("ร่วมงานกับเรา", "Careers")}</a></li>
        </ul>
      </div>
      <div>
        <h4>{t("บริการ", "Services")}</h4>
        <ul>
          <li><a href="{svc_href("opd")}">{t("ผู้ป่วยนอก", "Outpatient")}</a></li>
          <li><a href="{svc_href("ipd")}">{t("ผู้ป่วยใน", "Inpatient")}</a></li>
          <li><a href="{svc_href("daycenter")}">{t("ศูนย์กิจกรรมกลางวัน", "Day Activity Center")}</a></li>
          <li><a href="assessments.html">{t("แบบประเมินสุขภาพใจ", "Self-assessments")}</a></li>
          <li><a href="corporate.html">{t("บริการสำหรับองค์กร", "For organizations")}</a></li>
        </ul>
      </div>
      <div class="stack" style="gap:12px">
        <h4 style="margin:0">{t("รับข่าวสารสุขภาพใจ", "Mental health newsletter")}</h4>
        <form class="newsletter" data-form="newsletter">
          <label class="sr-only" for="nl-email-{key}">{t("อีเมล", "Email")}</label>
          <input id="nl-email-{key}" type="email" name="email" required placeholder="{t("อีเมลของคุณ", "Your email")}" autocomplete="email">
          <button class="btn btn--white btn--sm" type="submit">{t("สมัคร", "Join")}</button>
        </form>
        <span class="hotline">{t("สายด่วนสุขภาพจิต", "Mental health hotline")} <b>1323</b></span>
        <ul style="flex-direction:row;flex-wrap:wrap;gap:8px 18px;margin-top:4px">
          <li><a href="https://www.facebook.com/ManaromHospital">Facebook</a></li>
          <li><a href="https://www.youtube.com/user/ManaromCenter">YouTube</a></li>
          <li><a href="https://www.tiktok.com/@manaromhospital">TikTok</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> {t("โรงพยาบาลมนารมย์", "Manarom Hospital")}</span>
      <a href="https://manarom.com/images/Data_Protecti_on_Policy_ManaromHospital.pdf">{t("นโยบายการคุ้มครองข้อมูลส่วนบุคคล", "Data protection policy")}</a>
    </div>
  </div>
</footer>
<div class="fab jd-wrap">
  <div class="jd-bubble" id="jd-bubble" role="dialog" aria-label="{t("น้องใจดี", "Nong Jaidee")}" hidden>
    <button class="jd-bubble__x" type="button" aria-label="{t("ปิดข้อความ", "Close message")}">{I["close"]}</button>
    <p class="jd-bubble__name">{t("น้องใจดี", "Nong Jaidee")}</p>
    <p class="jd-bubble__text" aria-live="polite"></p>
    <div class="jd-bubble__moods" role="group" aria-label="{t("วันนี้ใจเป็นยังไงบ้าง", "How are you feeling?")}">{faces}</div>
    <div class="jd-bubble__reply" hidden></div>
  </div>
  <div class="fab__menu" id="fab-menu">
    <a href="contact.html">{I["chat"]}{t("ส่งข้อความถึงเรา", "Send us a message")}</a>
    <a href="register.html">{I["user_plus"]}{t("ลงทะเบียนผู้ป่วยใหม่", "Register as new patient")}</a>
    <a href="contact.html#map">{I["pin"]}{t("แผนที่และการเดินทาง", "Map and directions")}</a>
  </div>
  <button class="totop" type="button" aria-label="{t("กลับขึ้นด้านบน", "Back to top")}">{I["up"]}</button>
  <button class="fab__main jd" type="button" aria-expanded="false" aria-controls="fab-menu" aria-label="{t("น้องใจดี เปิดเมนูช่วยเหลือ", "Nong Jaidee: open help menu")}"><img src="{p}assets/img/jaidee.png" alt="" width="160" height="218"></button>
</div>
<script type="application/json" id="jd-msgs">{bubble_msgs}</script>
<script type="application/json" id="mood-data">{mood_json(c)}</script>
<script src="{p}assets/js/config.js"></script>
<script src="{p}assets/js/search-index.js"></script>
<script src="{p}assets/js/app.js"></script>
</body>
</html>
"""

def page_hero(c, crumb, title, lead, img, eyebrow="", crumbs_mid=None):
    t = c.t
    mid = "".join(f'<a href="{h}">{E(n)}</a><span aria-hidden="true">/</span>' for h, n in (crumbs_mid or []))
    return f"""<section class="phero">
  <div class="wrap">
    <div class="stack" style="gap:18px">
      <nav class="crumbs" aria-label="{t("ตำแหน่งหน้า", "Breadcrumb")}"><a href="index.html">{t("หน้าหลัก", "Home")}</a><span aria-hidden="true">/</span>{mid}<span>{E(crumb)}</span></nav>
      {f'<span class="eyebrow">{E(eyebrow)}</span>' if eyebrow else ''}
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </div>
    <div class="phero__img reveal">{img_tag(c, img, lazy=False)}</div>
  </div>
</section>"""

def appt_band(c):
    t = c.t
    return f"""<section class="appt">
  <div class="wrap appt__in reveal">
    <div class="appt__icon" aria-hidden="true">{I["phone"]}</div>
    <div class="stack" style="gap:6px;min-width:0">
      <h2 class="h3">{t("สำหรับผู้ป่วยใหม่ กรุณานัดหมายล่วงหน้า", "New patients, please book in advance")}</h2>
      <p>{t("โทร", "Call")} <b class="tel">{C.PHONE_1}</b> {t("หรือ", "or")} <b class="tel">{C.PHONE_2}</b> · {t(C.HOURS_TH, C.HOURS_EN)}</p>
    </div>
    <div class="appt__btns">
      <a class="btn btn--primary" href="register.html">{t("ลงทะเบียนออนไลน์", "Register online")}{I["arrow"]}</a>
      <button class="btn btn--ghost" type="button" data-copy="{C.PHONE_1}">{t("คัดลอกเบอร์โทร", "Copy phone number")}</button>
    </div>
  </div>
</section>"""

def cta_band(c):
    t = c.t
    return f"""<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta reveal">
      <div class="cta__blocks" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="stack" style="gap:10px;max-width:34em">
        <h2 class="h2">{t("ไม่แน่ใจว่าควรเริ่มที่ไหน", "Not sure where to start?")}</h2>
        <p>{t(f"โทรคุยกับเจ้าหน้าที่ {C.PHONE_1} หรือ {C.PHONE_2} หรือส่งข้อความถึงเรา เราจะช่วยแนะนำแพทย์และบริการที่เหมาะกับคุณ", f"Call {C.PHONE_1} or {C.PHONE_2}, or send us a message. We'll help you find the right doctor and service.")}</p>
      </div>
      <div class="cta__btns">
        <a class="btn btn--white" href="register.html">{t("นัดหมายแพทย์", "Book a doctor")}{I["arrow"]}</a>
        <a class="btn btn--line" href="contact.html">{t("ส่งข้อความถึงเรา", "Send us a message")}</a>
      </div>
    </div>
  </div>
</section>"""

def mood_section(c, sid="mood"):
    t = c.t
    opts = "".join(f'<button class="mood__opt" type="button" aria-pressed="false" data-mood="{k}">{b.FACES[k]}{t(a, bb)}</button>' for k, a, bb, *_ in C.MOODS)
    return f"""<section class="mood2" id="{sid}" aria-labelledby="{sid}-h">
  <div class="wrap">
    <div class="mood__card reveal">
      <div class="mood__q">
        <span class="eyebrow">{t("เช็กอินใจกับน้องใจดี", "Check in with Nong Jaidee")}</span>
        <h2 class="h3" id="{sid}-h">{t("วันนี้ใจของคุณเป็นอย่างไรบ้าง", "How are you feeling today?")}</h2>
        <p class="muted" style="font-size:15px">{t("เลือกอารมณ์ แล้วน้องใจดีจะแนะนำบทความที่เหมาะกับคุณ", "Pick a mood and Nong Jaidee will suggest articles for you.")}</p>
      </div>
      <div class="mood__opts">{opts}</div>
      <div class="mood__answer" aria-live="polite" aria-hidden="true"><div><div class="mood__res">
        <div class="mood__say"><img src="{c.p}assets/img/jaidee.png" alt="" width="64" height="87"><p data-mood-text></p></div>
        <div class="mood__arts" data-mood-arts></div>
        <div class="mood__links"><a class="link-arrow" href="{C.ALL_ARTICLES_URL}" target="_blank" rel="noopener">{t("ดูบทความทั้งหมด", "See all articles")}{I["ext"]}</a><a class="link-arrow" data-mood-extra hidden href="#"></a></div>
      </div></div></div>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- home
def home(c):
    t, p = c.t, c.p
    tiles = [("doctors.html", "doctor", "ค้นหาแพทย์", "Find a Doctor", "dark"), ("register.html", "user_plus", "ลงทะเบียนผู้ป่วยใหม่", "New Patient Registration", "mid"),
             ("assessments.html", "clipboard", "ประเมินสุขภาพใจ", "Mental Health Check", "mid"), ("corporate.html", "corp", "บริการองค์กร", "For Organizations", "dark")]
    tl = "".join(f'<a class="qt qt--{tone}" href="{h}"><span class="qt__icon">{I[ic]}</span><span class="qt__label">{t(a, bb)}</span><span class="qt__go">{I["arrow"]}</span></a>' for h, ic, a, bb, tone in tiles)
    slides = [("garden", "มุมพักผ่อนริมสวน", "Garden-side lounge"), ("lounge", "ห้องนั่งเล่นส่วนกลาง", "Shared living room"), ("common", "มุมพักผ่อนแสงธรรมชาติ", "Sunlit lounge"),
              ("dining", "มุมรับประทานอาหารริมหน้าต่าง", "Window dining area"), ("activity", "ห้องกิจกรรม", "Activity room")]
    sl = "".join(f'<div class="carousel__slide{" is-active" if i == 0 else ""}" role="group" aria-roledescription="slide" aria-label="{i+1} / 5">{img_tag(c, "photo:" + k, t(a, bb), sizes="(max-width: 960px) 100vw, 60vw", lazy=i > 0)}<span class="carousel__cap">{t(a, bb)}</span></div>' for i, (k, a, bb) in enumerate(slides))
    dots = "".join(f'<button class="carousel__dot" type="button" aria-label="{t("ภาพที่", "Photo")} {i+1}"></button>' for i in range(5))
    circles = []
    for s in [sv("opd"), sv("ipd"), sv("daycenter")]:
        circles.append(f'<a class="circ reveal" href="{svc_href(s["slug"])}"><span class="circ__ring">{img_tag(c, s["img"], cls="circ__img", sizes="220px")}<span class="circ__icon">{I[s["icon"]]}</span></span><b>{t(s["th"], s["en"])}</b><small>{t(s["s_th"], s["s_en"])}</small></a>')
    circles.append(f'<a class="circ reveal" href="corporate.html"><span class="circ__ring circ__ring--plain"><span class="circ__icon circ__icon--big">{I["corp"]}</span></span><b>{t("บริการองค์กร", "For Organizations")}</b><small>{t("Psychotest และอบรมพัฒนาบุคลากร", "Psychotest and staff training")}</small></a>')
    tints = ["t1", "t2", "t3", "t4"]
    cards = "".join(f'<a class="scard scard--{tints[i % 4]} reveal" style="--d:{(i % 4) * 50}ms" href="{svc_href(s["slug"])}"><span class="scard__icon">{I[s["icon"]]}</span><span class="scard__txt"><b>{t(s["th"], s["en"])}</b><small>{t(s["s_th"], s["s_en"])}</small></span><span class="scard__go">{I["arrow"]}</span></a>'
                    for i, s in enumerate(sv(x) for x in C.CARD_ORDER))
    why = [("shield", "เป็นส่วนตัว ปลอดภัย", "Private and safe", "ข้อมูลการรักษาเป็นความลับตามมาตรฐานจริยธรรมทางการแพทย์", "Your records stay confidential under medical ethics."),
           ("team", "ทีมสหวิชาชีพครบในที่เดียว", "One complete care team", "จิตแพทย์ นักจิตวิทยา พยาบาล นักกิจกรรม กายภาพ ศิลปะ ดนตรี และการเต้นบำบัด", "Psychiatrists, psychologists, nurses and occupational, physical, art, music and dance therapists."),
           ("heart", "ดูแลทุกช่วงวัย", "Care for every age", "ตั้งแต่เด็ก วัยรุ่น วัยทำงาน จนถึงผู้สูงอายุ", "From children and teens to working adults and older adults."),
           ("building", "ก่อตั้งตั้งแต่ปี 2546", "Since 2003", "โรงพยาบาลเอกชนเฉพาะทางจิตเวช บนพื้นที่ร่มรื่นราว 7 ไร่ ย่านสุขุมวิท 70/3", "A private psychiatric hospital on about 7 rai of green space on Sukhumvit 70/3.")]
    wl = "".join(f'<div class="why reveal" style="--d:{i*70}ms"><span class="tile__icon">{I[ic]}</span><h3>{t(a, bb)}</h3><p>{t(d1, d2)}</p></div>' for i, (ic, a, bb, d1, d2) in enumerate(why))
    arts = "".join(art_card(c, k, i) for i, k in enumerate(["burnout", "childsign", "panic"]))
    faq3 = "".join(acc_item(c, q, i, prefix="hf") for i, q in enumerate([C.FAQ[0], C.FAQ[2], C.FAQ[4]]))
    return f"""<section class="hero2">
  <div class="wrap hero2__in">
    <div class="hero2__tiles">
      {tl}
      <a class="qt qt--wide" href="contact.html"><span class="qt__icon">{I["chat"]}</span><span class="qt__label">{t("ติดต่อเรา", "Contact Us")}</span><span class="qt__go">{I["arrow"]}</span></a>
    </div>
    <div class="hero2__stage">
      <div class="carousel carousel--hero" aria-roledescription="carousel" aria-label="{t("ภาพบรรยากาศโรงพยาบาล", "Hospital photos")}">
        <div class="carousel__dots">{dots}</div>
        {sl}
        <div class="hero2__copy">
          <span class="hero2__eyebrow">{t("โรงพยาบาลจิตเวชเฉพาะทาง ดูแลทุกช่วงวัย", "Specialist psychiatric hospital for every age")}</span>
          <h1 class="hero2__title">{t('พลังใจดี<br>เริ่มที่...<span class="accent">มนารมย์</span>', 'A stronger mind<br>starts at <span class="accent">Manarom</span>')}</h1>
          <p class="hero2__lead">{t("ดูแลสุขภาพใจของเด็ก วัยรุ่น ผู้ใหญ่ และผู้สูงอายุ โดยทีมจิตแพทย์และสหวิชาชีพ ในบรรยากาศที่อบอุ่นและเป็นส่วนตัว", "Mental health care for children, teens, adults and older adults, by psychiatrists and a multidisciplinary team, in a warm and private setting.")}</p>
        </div>
        <div class="carousel__nav"><button class="carousel__btn" type="button" data-prev aria-label="{t("ภาพก่อนหน้า", "Previous photo")}">{I["left"]}</button><button class="carousel__btn" type="button" data-next aria-label="{t("ภาพถัดไป", "Next photo")}">{I["right"]}</button></div>
      </div>
    </div>
  </div>
</section>

<section class="svc2" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("เลือกบริการที่ตรงกับคุณ", "Find the right care")}</span><h2 class="h2" id="svc-h">{t("การบริการ", "Our Services")}</h2></div><a class="link-arrow" href="services.html">{t("ภาพรวมบริการทั้งหมด", "All services overview")}{I["arrow"]}</a></div>
    <div class="circs">{"".join(circles)}</div>
    <div class="scards">{cards}</div>
  </div>
</section>

{appt_band(c)}

{mood_section(c)}

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("ขั้นตอนการรับบริการ", "How it works")}</span><h2 class="h2">{t("เริ่มดูแลใจได้ใน 3 ขั้น", "Get started in 3 steps")}</h2></div></div>
    <div class="steps">
      <div class="step" style="--d:0ms"><span class="step__no">{t("ขั้นที่ 1", "STEP 1")}</span><h3>{t("สำรวจใจตัวเอง", "Check in with yourself")}</h3><p>{t("ทำแบบประเมินออนไลน์เพื่อคัดกรองเบื้องต้น ใช้เวลาไม่นานและเป็นส่วนตัว", "Take a short, private online assessment for an initial screening.")}</p><a class="link-arrow" href="assessments.html">{t("ไปที่แบบประเมิน", "Go to assessments")}{I["arrow"]}</a></div>
      <div class="step" style="--d:200ms"><span class="step__no">{t("ขั้นที่ 2", "STEP 2")}</span><h3>{t("เลือกแพทย์และบริการ", "Choose a doctor and service")}</h3><p>{t("ค้นหาจิตแพทย์ตามช่วงวัย ดูบริการ และอัตราค่าบริการ", "Find psychiatrists by age group and check services and rates.")}</p><a class="link-arrow" href="doctors.html">{t("ค้นหาแพทย์", "Find a doctor")}{I["arrow"]}</a></div>
      <div class="step" style="--d:400ms"><span class="step__no">{t("ขั้นที่ 3", "STEP 3")}</span><h3>{t("นัดหมายล่วงหน้า", "Book ahead")}</h3><p>{t(f"ลงทะเบียนออนไลน์ หรือโทร {C.PHONE_REG} มาถึงก่อนเวลานัด 15 นาที พร้อมบัตรประชาชน", f"Register online or call {C.PHONE_REG}. Arrive 15 minutes early with your ID.")}</p><a class="link-arrow" href="register.html">{t("ลงทะเบียน", "Register")}{I["arrow"]}</a></div>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("ทำไมต้องมนารมย์", "Why Manarom")}</span><h2 class="h2">{t("ดูแลใจอย่างอบอุ่น ปลอดภัย และครบถ้วน", "Warm, safe and complete care")}</h2></div><a class="link-arrow" href="about.html">{t("รู้จักเราเพิ่มเติม", "More about us")}{I["arrow"]}</a></div>
    <div class="whys">{wl}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="split__img reveal">{img_tag(c, "photo:activity", t("ห้องกิจกรรม ศูนย์กิจกรรมกลางวัน", "Day Activity Center room"))}</div>
    <div class="stack reveal" style="--d:120ms;gap:20px">
      <span class="eyebrow">Day Activity Center</span>
      <h2 class="h2">{t("ศูนย์กิจกรรมกลางวัน", "Day Activity Center")}</h2>
      <p class="lead">{t("โปรแกรมฟื้นฟูแบบไป–กลับ 1–5 วันต่อสัปดาห์ ช่วยปรับตัวในชีวิตประจำวัน จัดการอารมณ์ ความเครียด และการเข้าสังคม", "A day program, 1–5 days a week, to rebuild daily routines and manage emotions, stress and social life.")}</p>
      <div class="chips"><span class="chip">{t("กิจกรรมบำบัด", "Occupational")}</span><span class="chip">{t("กายภาพบำบัด", "Physical")}</span><span class="chip">{t("ดนตรีบำบัด", "Music")}</span><span class="chip">{t("ทำสวน", "Gardening")}</span></div>
      <div><a class="btn btn--primary" href="{svc_href("daycenter")}">{t("ดูรายละเอียดโปรแกรม", "See program details")}{I["arrow"]}</a></div>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head">
      <div class="stack"><span class="eyebrow">{t("คลังความรู้", "Knowledge")}</span><h2 class="h2">{t("บทความสุขภาพใจ", "Mental health articles")}</h2></div>
      <a class="link-arrow" href="knowledge.html">{t("ดูบทความทั้งหมด", "See all articles")}{I["arrow"]}</a>
    </div>
    <div class="cards">{arts}</div>
    <a class="yt reveal" href="https://www.youtube.com/user/ManaromCenter"><span class="yt__play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></span><span><b>Manarom Channel</b><small>{t("ดูคลิปความรู้สุขภาพใจจากจิตแพทย์บน YouTube", "Watch mental health videos from our psychiatrists on YouTube")}</small></span>{I["ext"]}</a>
  </div>
</section>

<section class="section">
  <div class="wrap" style="max-width:900px">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("คำถามที่พบบ่อย", "FAQ")}</span><h2 class="h2">{t("ก่อนมาโรงพยาบาล", "Before your visit")}</h2></div><a class="link-arrow" href="faq.html">{t("ดูคำถามทั้งหมด", "All questions")}{I["arrow"]}</a></div>
    <div>{faq3}</div>
  </div>
</section>

<section class="section section--sky">
  <div class="wrap grid-2" style="align-items:center">
    <a class="map reveal" href="{C.MAPS}"><img src="{p}assets/img/map.svg" alt="" width="800" height="600" loading="lazy"><span>{I["pin"].replace("<svg", "<svg width=\"18\" height=\"18\"")}{t("เปิดใน Google Maps", "Open in Google Maps")}</span></a>
    <div class="stack reveal" style="gap:18px;--d:120ms">
      <span class="eyebrow">{t("การเดินทาง", "Getting here")}</span>
      <h2 class="h2">{t("มาหาเราได้สะดวก", "Easy to reach")}</h2>
      <p class="lead">{t(C.ADDR_TH, C.ADDR_EN)}</p>
      <div class="info"><span class="info__icon">{I["train"]}</span><span><small>BTS</small><b>{t("สถานีบางนา ทางออก 4 หรือ สถานีแบริ่ง ทางออก 2 (เดินราว 400 ม.)", "Bang Na exit 4 or Bearing exit 2 (about 400 m walk)")}</b></span></div>
      <div class="hero__ctas"><a class="btn btn--primary" href="register.html">{t("นัดหมายแพทย์", "Book a doctor")}{I["arrow"]}</a><a class="btn btn--ghost" href="contact.html#map">{t("วิธีเดินทางทั้งหมด", "All directions")}</a></div>
    </div>
  </div>
</section>"""

def acc_item(c, q, i, prefix="faq", open_=False):
    t = c.t
    qth, qen, ath, aen = q
    return (f'<div class="acc reveal" data-item data-text="{E(t(qth, qen) + " " + t(ath, aen))}"><button class="acc__btn" type="button" aria-expanded="{"true" if open_ else "false"}" aria-controls="{prefix}-{i}">{t(qth, qen)}<span class="acc__icon" aria-hidden="true"></span></button>'
            f'<div class="acc__panel{" is-open" if open_ else ""}" id="{prefix}-{i}"><div><p>{t(ath, aen)}</p></div></div></div>')

def art_card(c, key, i, cat=None):
    t, p = c.t, c.p
    th, en, url, img = C.ART[key]
    catname = t(*b.ACAT[cat]) if cat else ""
    attrs = f' data-item data-cat="{cat}" data-text="{E(t(th, en) + " " + catname)}"' if cat else ""
    return (f'<a class="card reveal" style="--d:{(i % 3) * 80}ms" href="{url}" target="_blank" rel="noopener"{attrs}><div class="card__img">{img_tag(c, "photo:" + img, sizes="(max-width: 600px) 100vw, 33vw")}</div>'
            f'<div class="card__meta">{f"<b>{catname}</b>" if catname else ""}<span>{t("อ่านบน manarom.com", "Read on manarom.com")}</span></div><h3>{E(t(th, en))}</h3></a>')

# ---------------------------------------------------------------- services list + detail
def services(c):
    t = c.t
    out = []
    for g, a, bb in C.GROUPS:
        items = [s for s in C.SERVICES if C.GROUP_OF[s["slug"]] == g]
        cards = "".join(f'<a class="scard scard--t{(i % 4) + 1} reveal" style="--d:{(i % 3) * 60}ms" href="{svc_href(s["slug"])}"><span class="scard__icon">{I[s["icon"]]}</span><span class="scard__txt"><b>{t(s["th"], s["en"])}</b><small>{t(s["s_th"], s["s_en"])}</small></span><span class="scard__go">{I["arrow"]}</span></a>' for i, s in enumerate(items))
        out.append(f'<div class="svc-group" id="{g}"><div class="sec-head" style="margin-bottom:20px"><h2 class="h2">{t(a, bb)}</h2></div><div class="scards scards--3">{cards}</div></div>')
    out.append(f'<div class="svc-group" id="corp"><div class="sec-head" style="margin-bottom:20px"><h2 class="h2">{t("บริการสำหรับองค์กร", "For organizations")}</h2></div><div class="scards scards--3">'
               f'<a class="scard scard--t2" href="corporate.html#psychotest"><span class="scard__icon">{I["brain"]}</span><span class="scard__txt"><b>Psychotest</b><small>{t("แบบทดสอบจิตวิทยาเพื่อคัดเลือกบุคลากร", "Psychological tests for hiring")}</small></span><span class="scard__go">{I["arrow"]}</span></a>'
               f'<a class="scard scard--t3" href="corporate.html#training"><span class="scard__icon">{I["chalk"]}</span><span class="scard__txt"><b>Training</b><small>{t("อบรมพัฒนาบุคลากร", "Staff training & development")}</small></span><span class="scard__go">{I["arrow"]}</span></a></div></div>')
    chips = "".join(f'<a class="chip" href="#{g}" style="text-decoration:none">{t(a, bb)}</a>' for g, a, bb in C.GROUPS) + f'<a class="chip" href="#corp" style="text-decoration:none">{t("องค์กร", "Organizations")}</a>'
    return page_hero(c, t("การบริการ", "Services"), t("การบริการของเรา", "Our services"),
                     t("14 บริการ ครอบคลุมการรักษา บำบัด และฟื้นฟู สำหรับทุกช่วงวัย กดเลือกบริการเพื่อดูรายละเอียด", "14 services covering treatment, therapy and rehabilitation for every age. Choose one to see the details."), "photo:lounge", t("รักษา บำบัด ฟื้นฟู", "Treat, support, recover")) + f"""
<section class="section">
  <div class="wrap">
    <div class="chips" style="margin-bottom:48px">{chips}</div>
    {''.join(out)}
  </div>
</section>
{appt_band(c)}"""

def service_page(c, s):
    t = c.t
    CHECK = I["check"]
    secs = "".join(f'<div class="panel reveal stack" style="gap:16px"><h2 class="h3">{t(h1, h2)}</h2><ul class="ticks">{"".join(f"<li>{CHECK}<span>{E(t(x, y))}</span></li>" for x, y in items)}</ul></div>' for h1, h2, items in s["sec"])
    extra = ""
    if s.get("extra") == "ipd":
        extra = f"""<div class="panel reveal stack" style="gap:14px"><h2 class="h3">{t("เวลาเยี่ยม", "Visiting hours")}</h2>
<div class="table-wrap" style="border-radius:14px"><table class="table" style="min-width:0"><tbody>
<tr><th scope="row">{t("จันทร์–ศุกร์", "Mon–Fri")}</th><td class="num">16:30–21:00</td></tr>
<tr><th scope="row">{t("เสาร์–อาทิตย์ และวันหยุด", "Weekends & holidays")}</th><td class="num">11:00–13:00 · 16:30–21:30</td></tr></tbody></table></div>
<a class="link-arrow" href="pricing.html#ipd">{t("ดูค่าห้องพักผู้ป่วยใน", "See inpatient room rates")}{I["arrow"]}</a></div>"""
    elif s.get("extra") == "day":
        extra = f"""<div class="panel reveal stack" style="gap:14px"><h2 class="h3">{t("ช่วงเวลากิจกรรม", "Session times")}</h2>
<div class="table-wrap" style="border-radius:14px"><table class="table" style="min-width:0"><tbody>
<tr><th scope="row">{t("ช่วงที่ 1", "Session 1")}</th><td class="num">09:00–12:00</td></tr>
<tr><th scope="row">{t("ช่วงที่ 2", "Session 2")}</th><td class="num">10:30–14:30</td></tr>
<tr><th scope="row">{t("พักกลางวัน", "Lunch")}</th><td class="num">12:00–13:00</td></tr>
<tr><th scope="row">{t("กิจกรรมรายบุคคล", "One-to-one sessions")}</th><td class="num">{t("1 ชม. ตามนัด", "1 hour, by appointment")}</td></tr></tbody></table></div></div>"""
    elif s.get("extra") == "opd":
        extra = f"""<div class="panel reveal stack" style="gap:14px"><h2 class="h3">{t("เวลาให้บริการ", "Opening hours")}</h2><p class="lead" style="font-size:17px">{t("ผู้ป่วยนอก 07:00–20:00 น. ทุกวัน · ฉุกเฉิน 24 ชั่วโมง", "Outpatient 07:00–20:00 daily · Emergency 24 hours")}</p><a class="link-arrow" href="pricing.html">{t("ดูอัตราค่าบริการผู้ป่วยนอก", "See outpatient rates")}{I["arrow"]}</a></div>"""
    others = [x for x in C.SERVICES if C.GROUP_OF[x["slug"]] == C.GROUP_OF[s["slug"]] and x["slug"] != s["slug"]][:3]
    if len(others) < 3:
        others += [x for x in C.SERVICES if x["slug"] not in [o["slug"] for o in others] and x["slug"] != s["slug"]][:3 - len(others)]
    rel = "".join(f'<a class="scard scard--t{(i % 4) + 1}" href="{svc_href(o["slug"])}"><span class="scard__icon">{I[o["icon"]]}</span><span class="scard__txt"><b>{t(o["th"], o["en"])}</b><small>{t(o["s_th"], o["s_en"])}</small></span><span class="scard__go">{I["arrow"]}</span></a>' for i, o in enumerate(others))
    return page_hero(c, t(s["th"], s["en"]), t(s["th"], s["en"]), t(s["s_th"], s["s_en"]), s["img"], t("บริการของเรา", "Our services"),
                     crumbs_mid=[("services.html", t("การบริการ", "Services"))]) + f"""
<section class="section">
  <div class="wrap svc-detail">
    <div class="stack" style="gap:24px;min-width:0">
      <p class="lead svc-intro reveal">{E(t(s["i_th"], s["i_en"]))}</p>
      <div class="svc-secs">{secs}{extra}</div>
    </div>
    <aside class="svc-aside">
      <div class="panel stack" style="gap:14px">
        <span class="tile__icon">{I[s["icon"]]}</span>
        <h2 class="h3">{t("นัดหมายบริการนี้", "Book this service")}</h2>
        <p class="muted" style="font-size:15px">{t("ผู้ป่วยใหม่กรุณานัดหมายล่วงหน้า", "New patients please book ahead")}</p>
        <p><b class="tel">{C.PHONE_1}</b><br><b class="tel">{C.PHONE_2}</b></p>
        <a class="btn btn--primary btn--block" href="register.html">{t("ลงทะเบียนออนไลน์", "Register online")}{I["arrow"]}</a>
        <button class="btn btn--ghost btn--block" type="button" data-copy="{C.PHONE_1}">{t("คัดลอกเบอร์โทร", "Copy phone number")}</button>
        <a class="link-arrow" href="doctors.html" style="font-size:15px">{t("ค้นหาแพทย์", "Find a doctor")}{I["arrow"]}</a>
      </div>
    </aside>
  </div>
</section>
<section class="section section--mist" style="padding-block:56px">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:24px"><h2 class="h3">{t("บริการที่เกี่ยวข้อง", "Related services")}</h2><a class="link-arrow" href="services.html">{t("บริการทั้งหมด", "All services")}{I["arrow"]}</a></div>
    <div class="scards scards--3">{rel}</div>
  </div>
</section>"""

# ---------------------------------------------------------------- about / pricing / faq / contact / corporate / knowledge
def about(c):
    t = c.t
    team = [("จิตแพทย์", "Psychiatrists"), ("นักจิตวิทยาคลินิก", "Clinical psychologists"), ("พยาบาลจิตเวช", "Psychiatric nurses"),
            ("นักกิจกรรมบำบัด", "Occupational therapists"), ("นักกายภาพบำบัด", "Physical therapists"), ("นักศิลปะ ดนตรี และการเต้นบำบัด", "Creative arts therapists"), ("ครูการศึกษาพิเศษ", "Special educators")]
    tm = "".join(f'<div class="reveal" style="--d:{i*50}ms"><b>{t(a, bb)}</b></div>' for i, (a, bb) in enumerate(team))
    gal = "".join(f'<div class="gal__item reveal" style="--d:{i*60}ms">{img_tag(c, "photo:" + k, sizes="(max-width: 860px) 50vw, 25vw")}</div>' for i, k in enumerate(["garden", "lounge", "dining", "activity"]))
    return page_hero(c, t("เกี่ยวกับเรา", "About Us"), t("เกี่ยวกับมนารมย์", "About Manarom"),
                     t("โรงพยาบาลเอกชนเฉพาะทางด้านสุขภาพจิตและจิตเวช ดูแลทุกคนในครอบครัวตั้งแต่ปี 2546", "A private psychiatric and mental health hospital caring for families since 2003."), "photo:common", t("รู้จักเรา", "Who we are")) + f"""
<section class="section">
  <div class="wrap split">
    <div class="stack reveal" style="gap:20px">
      <span class="eyebrow">{t("ความเป็นมา", "Our story")}</span>
      <h2 class="h2">{t("พลังใจดี เริ่มที่...มนารมย์", "A stronger mind starts at Manarom")}</h2>
      <p class="lead">{t("โรงพยาบาลมนารมย์ก่อตั้งเมื่อวันที่ 15 ตุลาคม 2546 โดยคณะจิตแพทย์ที่เห็นความต้องการบริการสุขภาพจิตที่เพิ่มขึ้นในสังคม ตั้งอยู่บนที่ดินราว 7 ไร่ ถนนสุขุมวิท ซอย 70/3 และเปิดให้บริการเต็มรูปแบบในเดือนมิถุนายน 2549", "Manarom Hospital was founded on 15 October 2003 by a group of psychiatrists who saw a growing need for mental health care. It sits on about 7 rai of land on Sukhumvit Soi 70/3 and opened fully in June 2006.")}</p>
      <p class="muted">{t("บุคลากรของเรามีประสบการณ์จากหลายสถาบันการแพทย์ในประเทศไทย ให้บริการทั้งผู้ป่วยนอก ผู้ป่วยใน และศูนย์กิจกรรมกลางวัน", "Our staff come from leading medical institutions across Thailand, providing outpatient, inpatient and day-program care.")}</p>
    </div>
    <div class="split__img reveal" style="--d:120ms">{img_tag(c, "photo:garden", t("มุมพักผ่อนริมสวน", "Garden-side lounge"))}</div>
  </div>
</section>
<section class="section section--mist">
  <div class="wrap">
    <div class="grid-3">
      <div class="panel reveal stack"><span class="eyebrow">Vision</span><h2 class="h3">{t("วิสัยทัศน์", "Vision")}</h2><p class="muted">{t("เป็นผู้นำในการให้บริการด้านสุขภาพจิตและจิตเวชที่ครบสมบูรณ์ มีประสิทธิภาพและคุณภาพตามมาตรฐานสากล", "To lead in complete, effective mental health and psychiatric care that meets international standards.")}</p></div>
      <div class="panel reveal stack" style="--d:100ms"><span class="eyebrow">Mission</span><h2 class="h3">{t("พันธกิจ", "Mission")}</h2><p class="muted">{t("ให้บริการสุขภาพจิตตามมาตรฐานสากล โดยบุคลากรสหวิชาชีพ และมุ่งพัฒนาคุณภาพการบริการอย่างต่อเนื่อง", "To provide mental health care to international standards through a multidisciplinary team, and keep improving it.")}</p></div>
      <div class="panel reveal stack" style="--d:200ms"><span class="eyebrow">Value</span><h2 class="h3">{t("ค่านิยม", "Our belief")}</h2><p class="muted">{t("สุขภาพจิตที่ดี คือรากฐานที่สำคัญของคุณภาพชีวิต ครอบครัว และสังคม", "Good mental health is the foundation of a good life, family and society.")}</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("บรรยากาศ", "Our spaces")}</span><h2 class="h2">{t("พื้นที่ที่ออกแบบมาให้ใจได้พัก", "Spaces designed for rest")}</h2></div></div>
    <div class="gal">{gal}</div>
  </div>
</section>
<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("ทีมสหวิชาชีพ", "Multidisciplinary team")}</span><h2 class="h2">{t("ผู้เชี่ยวชาญหลายสาขา ในทีมเดียว", "Many specialists, one team")}</h2></div><a class="btn btn--primary" href="doctors.html">{t("ค้นหาแพทย์", "Find a doctor")}{I["arrow"]}</a></div>
    <div class="team">{tm}</div>
  </div>
</section>
{cta_band(c)}"""

def pricing(c):
    t = c.t
    opd = "".join(f'<tr><td>{t(a, bb)}</td><td class="num">{v}</td></tr>' for a, bb, v in C.OPD_PRICES)
    ipd = "".join(f'<tr><td>{t(a, bb)}</td><td class="num">{r}</td><td class="num">{n}</td><td class="num">{th}</td><td class="num">{s}</td><td class="num"><b>{tot}</b></td></tr>' for a, bb, r, n, th, s, tot in C.IPD_PRICES)
    return page_hero(c, t("อัตราค่าบริการ", "Rates"), t("อัตราค่าบริการ", "Service rates"),
                     t("ข้อมูลค่าบริการเบื้องต้น เพื่อช่วยวางแผนก่อนนัดหมาย (หน่วย: บาท)", "Indicative rates to help you plan before booking (in Thai baht)."), "photo:dining") + f"""
<section class="section">
  <div class="wrap" style="max-width:1000px">
    <h2 class="h3" style="margin-bottom:16px">{t("ผู้ป่วยนอก", "Outpatient")}</h2>
    <div class="table-wrap reveal"><table class="table"><thead><tr><th scope="col">{t("รายการ", "Service")}</th><th scope="col" class="num">{t("ค่าบริการ (บาท)", "Rate (THB)")}</th></tr></thead><tbody>{opd}</tbody></table></div>
    <h2 class="h3" style="margin:48px 0 16px" id="ipd">{t("ผู้ป่วยใน (ต่อวัน)", "Inpatient (per day)")}</h2>
    <div class="table-wrap reveal"><table class="table" style="min-width:760px"><thead><tr><th scope="col">{t("ประเภทห้อง", "Room")}</th><th scope="col" class="num">{t("ค่าห้อง", "Room")}</th><th scope="col" class="num">{t("ค่าการพยาบาล", "Nursing")}</th><th scope="col" class="num">{t("ค่าบำบัดสหวิชาชีพ", "Therapy team")}</th><th scope="col" class="num">{t("ค่าบริการ รพ.", "Hospital service")}</th><th scope="col" class="num">{t("รวม", "Total")}</th></tr></thead><tbody>{ipd}</tbody></table></div>
    <div class="notice" style="margin-top:24px">{I["alert"]}<p>{t("ราคาผู้ป่วยในไม่รวมค่าอาหาร ค่ายา และค่าแพทย์ · โรงพยาบาลไม่รับสิทธิประกันสังคม สิทธิข้าราชการ และไม่วางบิลกับบริษัทประกัน · ราคาอาจเปลี่ยนแปลง กรุณาสอบถามก่อนเข้ารับบริการ", "Inpatient rates exclude food, medication and doctor's fees · The hospital does not accept social security or civil-servant schemes, or bill insurers directly · Prices may change; please ask before your visit.")}</p></div>
    <div class="hero__ctas" style="margin-top:28px"><button class="btn btn--primary" type="button" data-copy="{C.PHONE_2}">{t(f"สอบถามค่าใช้จ่าย {C.PHONE_2}", f"Ask about costs {C.PHONE_2}")}</button><a class="btn btn--ghost" href="faq.html">{t("คำถามที่พบบ่อย", "FAQ")}</a></div>
  </div>
</section>"""

def faq(c):
    t = c.t
    acc = "".join(acc_item(c, q, i, open_=(i == 0)) for i, q in enumerate(C.FAQ))
    return page_hero(c, t("คำถามที่พบบ่อย", "FAQ"), t("คำถามที่พบบ่อย", "Frequently asked questions"),
                     t("รวมคำตอบเรื่องที่ผู้รับบริการถามบ่อย ก่อนมาโรงพยาบาล", "Answers to what people often ask before a visit."), "photo:lounge") + f"""
<section class="section">
  <div class="wrap" style="max-width:880px" data-collection="faq-list">
    <div class="toolbar"><label class="search" style="max-width:none"><span class="sr-only">{t("ค้นหาคำถาม", "Search questions")}</span>{I["search"]}<input type="search" data-search placeholder="{t("พิมพ์คำถาม เช่น ประกัน", "Type a question, e.g. insurance")}"></label></div>
    <div id="faq-list">{acc}</div>
    <p class="empty" id="faq-list-empty" hidden>{t("ไม่พบคำถามนี้ ส่งคำถามถึงเราได้เลย", "Not found. Send us your question.")}</p>
    <div class="hero__ctas" style="margin-top:40px;align-items:center"><span class="muted">{t("ไม่พบคำตอบที่ต้องการ?", "Can't find your answer?")}</span><a class="btn btn--primary btn--sm" href="contact.html">{t("ถามเจ้าหน้าที่", "Ask our staff")}{I["arrow"]}</a></div>
  </div>
</section>"""

def contact(c):
    t, p = c.t, c.p
    COPY = t("คัดลอก", "Copy")
    topics = [("general", "สอบถามทั่วไป", "General question"), ("booking", "การนัดหมาย", "Appointments"), ("billing", "ค่าบริการ", "Rates and billing"), ("feedback", "ข้อเสนอแนะ", "Feedback")]
    tp = "".join(f'<option value="{k}">{t(a, bb)}</option>' for k, a, bb in topics)
    info = [("pin", t("ที่อยู่", "Address"), t(C.ADDR_TH, C.ADDR_EN), ""),
            ("phone", t("โทรศัพท์", "Phone"), f"{C.PHONE_2} · {C.PHONE_1}", C.PHONE_2),
            ("user_plus", t("นัดหมาย / เวชระเบียน", "Appointments / medical records"), C.PHONE_REG, C.PHONE_REG),
            ("receipt", t("โทรสาร", "Fax"), C.FAX, ""),
            ("mail", t("อีเมล", "Email"), C.EMAIL, C.EMAIL),
            ("clock", t("เวลาทำการ", "Opening hours"), t(C.HOURS_TH, C.HOURS_EN), "")]
    il = "".join(f'<div class="info"><span class="info__icon">{I[ic]}</span><span><small>{a}</small><b>{E(v)}</b>{f"<br><button class=copy-btn type=button data-copy={chr(34)}{cp}{chr(34)}>{COPY}</button>" if cp else ""}</span></div>' for ic, a, v, cp in info)
    form_html = f"""<form class="form" data-form="contact">
        <h2 class="h3">{t("ส่งข้อความถึงเรา", "Send us a message")}</h2>
        <div class="row">
          {b.field("c-name", t("ชื่อ", "Name"), '<input id="c-name" name="name" required autocomplete="name">')}
          {b.field("c-phone", t("เบอร์โทรศัพท์", "Phone"), '<input id="c-phone" type="tel" name="phone" required inputmode="tel" autocomplete="tel" placeholder="0812345678">')}
        </div>
        {b.field("c-email", t("อีเมล", "Email"), '<input id="c-email" type="email" name="email" autocomplete="email">', req=False)}
        {b.field("c-topic", t("เรื่องที่ติดต่อ", "Topic"), f'<select id="c-topic" name="topic" required><option value="">{t("เลือกเรื่อง", "Choose a topic")}</option>{tp}</select>')}
        {b.field("c-msg", t("ข้อความ", "Message"), '<textarea id="c-msg" name="message" required maxlength="2000"></textarea>')}
        <div class="field"><label class="check"><input type="checkbox" name="consent_pdpa" required> <span>{t("ยินยอมให้ติดต่อกลับตามนโยบายการคุ้มครองข้อมูลส่วนบุคคล", "I agree to be contacted under the data protection policy")}</span></label><span class="err" aria-live="polite"></span></div>
        <div><button class="btn btn--primary" type="submit">{t("ส่งข้อความ", "Send message")}{I["arrow"]}</button></div>
      </form>
      {b.success_box(c, "contact", t("ส่งข้อความแล้ว", "Message sent"), t("ขอบคุณที่ติดต่อเรา เจ้าหน้าที่จะตอบกลับภายใน 1 วันทำการ", "Thank you. Our team will reply within one working day."))}"""
    bus = "2, 23, 25, 102, 129, 142, 507, 511, 536"
    return page_hero(c, t("ติดต่อเรา", "Contact Us"), t("ติดต่อเรา", "Contact us"),
                     t("โทร ส่งข้อความ หรือแวะมาพบเรา ย่านสุขุมวิท 70/3 ใกล้ BTS บางนาและแบริ่ง", "Call, message or visit us on Sukhumvit 70/3, near BTS Bang Na and Bearing."), "photo:garden") + f"""
<section class="section">
  <div class="wrap grid-2" style="align-items:start">
    <div class="stack" style="gap:28px">
      <div class="info-list">{il}</div>
    </div>
    <div class="panel">{form_html}</div>
  </div>
</section>
<section class="section section--mist" id="map">
  <div class="wrap grid-2" style="align-items:start">
    <a class="map reveal" href="{C.MAPS}" style="min-height:380px"><img src="{p}assets/img/map.svg" alt="" width="800" height="600" loading="lazy"><span>{I["pin"].replace("<svg", "<svg width=\"18\" height=\"18\"")}{t("เปิดใน Google Maps", "Open in Google Maps")}</span></a>
    <div class="stack" style="gap:20px">
      <span class="eyebrow">{t("การเดินทาง", "Getting here")}</span>
      <h2 class="h2">{t("วิธีเดินทางมาโรงพยาบาล", "How to get here")}</h2>
      <div class="info"><span class="info__icon">{I["train"]}</span><span><small>BTS</small><b>{t("สถานีบางนา ทางออก 4 หรือ สถานีแบริ่ง ทางออก 2 เดินประมาณ 400 เมตร", "Bang Na exit 4 or Bearing exit 2, about a 400 m walk")}</b></span></div>
      <div class="info"><span class="info__icon">{I["car"]}</span><span><small>{t("รถโดยสารประจำทาง", "Bus")}</small><b>{t("สาย", "Lines")} {bus}</b></span></div>
      <div class="info"><span class="info__icon">{I["map"]}</span><span><small>{t("รถยนต์", "By car")}</small><b>{t("เข้าทางถนนสุขุมวิท ซอย 70/3 เดินทางสะดวกจากทางด่วน ถนนบางนา–ตราด และสนามบินสุวรรณภูมิ", "Enter from Sukhumvit Soi 70/3, easy from the expressway, Bang Na–Trat Road and Suvarnabhumi Airport")}</b></span></div>
    </div>
  </div>
</section>
<section class="section" id="jobs">
  <div class="wrap split">
    <div class="split__img reveal">{img_tag(c, "photo:activity")}</div>
    <div class="stack reveal" style="--d:120ms;gap:18px">
      <span class="eyebrow">{t("ร่วมงานกับเรา", "Careers")}</span>
      <h2 class="h2">{t("มาเป็นส่วนหนึ่งของทีมดูแลใจ", "Join our care team")}</h2>
      <p class="lead">{t("ดูตำแหน่งงานที่เปิดรับและวิธีสมัครได้ที่หน้าสมัครงาน", "See open positions and how to apply on our careers page.")}</p>
      <div><a class="btn btn--primary" href="https://www.manarom.com/job_thai.html">{t("ดูตำแหน่งงานทั้งหมด", "See all openings")}{I["ext"]}</a></div>
    </div>
  </div>
</section>"""

def corporate(c):
    t = c.t
    tests = "".join(f'<div class="pt reveal" style="--d:{i*70}ms"><span class="pt__code">{code}</span><b>{full}</b><p>{t(th, en)}</p></div>' for i, (code, full, th, en) in enumerate(C.PSYCHOTESTS))
    bens = "".join(f'<li>{I["check"]}<span>{t(a, bb)}</span></li>' for a, bb in C.PSYCHO_BENEFITS)
    trs = "".join(f'<div class="tr reveal" style="--d:{(i%4)*60}ms"><span class="tr__no">{i+1:02d}</span><b>{t(a, bb)}</b></div>' for i, (a, bb) in enumerate(C.TRAININGS))
    interests = [("psychotest", "Psychotest"), ("training", t("อบรม / เวิร์กช็อป", "Training / workshop")), ("coaching", "Executive Coaching"), ("custom", t("หลักสูตรเฉพาะองค์กร", "Custom program"))]
    it = "".join(f'<label class="choice"><input type="checkbox" name="interests" value="{k}" data-multi><span>{E(v)}</span></label>' for k, v in interests)
    so = "".join(f'<option value="{s}">{s} {t("คน", "people")}</option>' for s in ["1–50", "51–200", "201–1000", "1000+"])
    return page_hero(c, t("บริการสำหรับองค์กร", "For Organizations"), "Manarom Corporate Service",
                     t("ดูแลสุขภาพใจของคนในองค์กร สถาบัน และโรงเรียน โดยทีมจิตแพทย์และนักจิตวิทยาของโรงพยาบาลมนารมย์", "Mental health support for companies, institutions and schools, by Manarom's psychiatrists and psychologists."), "photo:dining", t("บริการสำหรับองค์กร", "For organizations")) + f"""
<section class="corp-switch">
  <div class="wrap"><nav class="corp-tabs" aria-label="{t("บริการองค์กร", "Corporate services")}"><a href="#psychotest">{I["brain"]}<span><b>Psychotest</b><small>{t("คัดเลือกบุคลากร", "Hiring")}</small></span></a><a href="#training">{I["chalk"]}<span><b>Training</b><small>{t("พัฒนาบุคลากร", "Development")}</small></span></a><a href="#quote">{I["mail"]}<span><b>{t("ขอใบเสนอราคา", "Get a quote")}</b><small>{t("ติดต่อทีมงาน", "Contact us")}</small></span></a></nav></div>
</section>
<section class="section" id="psychotest">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">HR Psychotest</span><h2 class="h2">{t("แบบทดสอบจิตวิทยาเพื่อการบริหาร", "Psychological testing for HR")}</h2><p class="lead">{t("ช่วยองค์กรคัดเลือกบุคลากรที่เหมาะสม แปลผลโดยทีมจิตแพทย์และนักจิตวิทยาผู้เชี่ยวชาญ พร้อมให้คำปรึกษาตลอดการใช้บริการ", "Helps organisations choose the right people. Results are interpreted by our psychiatrists and psychologists, with advice throughout.")}</p></div></div>
    <div class="pts">{tests}</div>
    <div class="panel reveal" style="margin-top:32px"><h3 class="h3" style="margin-bottom:14px">{t("ประโยชน์ต่อองค์กร", "What your organisation gains")}</h3><ul class="ticks ticks--2">{bens}</ul></div>
  </div>
</section>
<section class="section section--mist" id="training">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">Training &amp; Development</span><h2 class="h2">{t("อบรมพัฒนาบุคลากร", "Staff training & development")}</h2><p class="lead">{t("หลักสูตรบรรยายและอบรมเชิงปฏิบัติการ (Workshop) ใช้หลักจิตวิทยาช่วยให้พนักงานเข้าใจตนเอง องค์กร และเพื่อนร่วมงาน", "Talks and hands-on workshops that use psychology to help employees understand themselves, their organisation and their colleagues.")}</p></div></div>
    <div class="trs">{trs}</div>
  </div>
</section>
<section class="section" id="quote">
  <div class="wrap grid-2" style="align-items:start">
    <div class="stack reveal" style="gap:18px">
      <span class="eyebrow">{t("ขอใบเสนอราคา", "Request a quote")}</span>
      <h2 class="h2">{t("บอกความต้องการขององค์กร เราจะออกแบบโปรแกรมให้", "Tell us what your organisation needs")}</h2>
      <p class="lead">{t("หรือโทรหา Manarom Corporate Service", "Or call Manarom Corporate Service")}</p>
      <p><b class="tel">{C.PHONE_2}</b> {t("ต่อ", "ext.")} 1260, 1245<br><b class="tel">{C.PHONE_1}</b></p>
    </div>
    <div class="panel">
      <form class="form" data-form="corporate">
        <div class="row">
          {b.field("o-org", t("ชื่อองค์กร", "Organisation"), '<input id="o-org" name="organization" required autocomplete="organization">')}
          {b.field("o-size", t("จำนวนพนักงาน", "Company size"), f'<select id="o-size" name="company_size" required><option value="">{t("เลือก", "Choose")}</option>{so}</select>')}
        </div>
        <div class="row">
          {b.field("o-name", t("ชื่อผู้ติดต่อ", "Contact name"), '<input id="o-name" name="contact_name" required autocomplete="name">')}
          {b.field("o-phone", t("เบอร์โทรศัพท์", "Phone"), '<input id="o-phone" type="tel" name="phone" required inputmode="tel" placeholder="0812345678">')}
        </div>
        {b.field("o-email", t("อีเมล", "Email"), '<input id="o-email" type="email" name="email" required autocomplete="email">')}
        <fieldset class="field"><legend>{t("บริการที่สนใจ", "Interested in")}</legend><div class="choices">{it}</div></fieldset>
        {b.field("o-msg", t("รายละเอียดเพิ่มเติม", "Details"), '<textarea id="o-msg" name="message" maxlength="2000"></textarea>', req=False)}
        <div class="field"><label class="check"><input type="checkbox" name="consent_pdpa" required> <span>{t("ยินยอมให้ติดต่อกลับตามนโยบายการคุ้มครองข้อมูลส่วนบุคคล", "I agree to be contacted under the data protection policy")}</span></label><span class="err" aria-live="polite"></span></div>
        <div><button class="btn btn--primary" type="submit">{t("ขอใบเสนอราคา", "Request a quote")}{I["arrow"]}</button></div>
      </form>
      {b.success_box(c, "corporate", t("ได้รับคำขอแล้ว", "Request received"), t("ทีมงานจะติดต่อกลับพร้อมข้อเสนอภายใน 3 วันทำการ", "Our team will send you a proposal within 3 working days."))}
    </div>
  </div>
</section>"""

def knowledge(c):
    t = c.t
    filt = f'<button class="filter" type="button" aria-pressed="true" data-filter="all">{t("ทั้งหมด", "All")}</button>' + "".join(f'<button class="filter" type="button" aria-pressed="false" data-filter="{k}">{t(a, bb)}</button>' for k, a, bb in b.ACATS)
    cards = "".join(art_card(c, k, i, cat=cat) for i, (cat, k) in enumerate(C.KNOW))
    return page_hero(c, t("คลังความรู้", "Knowledge"), t("คลังความรู้สุขภาพใจ", "Mental health knowledge"),
                     t("บทความจากจิตแพทย์และทีมสหวิชาชีพ อ่านง่าย ใช้ได้จริงในชีวิตประจำวัน", "Articles by our psychiatrists and care team: easy to read and useful every day."), "photo:lounge") + mood_section(c, "mood-k") + f"""
<section class="section">
  <div class="wrap" data-collection="art-list">
    <div class="toolbar">
      <div class="filters" role="group" aria-label="{t("หมวดบทความ", "Categories")}">{filt}</div>
      <label class="search"><span class="sr-only">{t("ค้นหาบทความ", "Search articles")}</span>{I["search"]}<input type="search" data-search placeholder="{t("ค้นหาบทความ เช่น นอนไม่หลับ", "Search, e.g. sleep")}"></label>
    </div>
    <div class="cards" id="art-list" data-page-size="6">{cards}</div>
    <p class="empty" id="art-list-empty" hidden>{t("ไม่พบบทความที่ค้นหา", "No articles match your search")}</p>
    <div class="more-wrap"><button class="btn btn--ghost" type="button" id="art-list-more">{t("โหลดบทความเพิ่ม", "Load more articles")}</button></div>
  </div>
</section>
<section class="section section--mist">
  <div class="wrap grid-2">
    <a class="panel stack reveal" style="text-decoration:none;color:inherit" href="https://www.youtube.com/user/ManaromCenter"><span class="eyebrow">Video</span><h2 class="h3">Manarom Channel</h2><p class="muted">{t("คลิปความรู้สุขภาพใจบน YouTube", "Mental health videos on YouTube")}</p><span class="link-arrow">{t("ไปที่ YouTube", "Open YouTube")}{I["ext"]}</span></a>
    <a class="panel stack reveal" style="--d:100ms;text-decoration:none;color:inherit" href="https://www.manarom.com/magazine/index.html"><span class="eyebrow">{t("วารสาร", "Journal")}</span><h2 class="h3">{t("วารสารพลังใจดี", "Palang Jai Dee journal")}</h2><p class="muted">{t("อ่านและดาวน์โหลดฉบับย้อนหลัง (PDF)", "Read and download past issues (PDF)")}</p><span class="link-arrow">{t("ดูฉบับย้อนหลัง", "Browse issues")}{I["ext"]}</span></a>
  </div>
</section>"""

# ---------------------------------------------------------------- build
def main():
    b.page_hero = lambda c, crumb, title, lead, img, eyebrow="": page_hero(c, crumb, title, lead, "ill:" + img.split("/")[-1].replace(".svg", ""), eyebrow)
    b.cta_band = cta_band
    pages = [
        ("home", "index.html", home, ("หน้าหลัก", "Home"), ("โรงพยาบาลจิตเวชเฉพาะทาง ดูแลสุขภาพใจทุกช่วงวัย ย่านสุขุมวิท 70/3 บางนา", "Specialist psychiatric hospital for every age, Sukhumvit 70/3, Bang Na"), False),
        ("about", "about.html", about, ("เกี่ยวกับเรา", "About Us"), ("ประวัติ วิสัยทัศน์ และทีมสหวิชาชีพของโรงพยาบาลมนารมย์", "History, vision and team of Manarom Hospital"), False),
        ("services", "services.html", services, ("การบริการ", "Services"), ("บริการรักษา บำบัด และฟื้นฟู 14 บริการ", "14 treatment, therapy and rehabilitation services"), False),
        ("doctors", "doctors.html", b.doctors, ("ค้นหาแพทย์", "Find a Doctor"), ("ค้นหาจิตแพทย์และทีมสหวิชาชีพ", "Find psychiatrists and care team"), False),
        ("assess", "assessments.html", b.assessments, ("แบบประเมิน", "Self-Assessments"), ("แบบประเมินสุขภาพใจออนไลน์", "Online self-assessments"), False),
        ("assess", "test.html", b.test, ("แบบประเมินความเครียด ST-5", "Stress check ST-5"), ("เช็กความเครียดใน 1 นาที", "Check your stress in 1 minute"), False),
        ("knowledge", "knowledge.html", knowledge, ("คลังความรู้", "Knowledge"), ("บทความสุขภาพใจจากจิตแพทย์", "Mental health articles"), False),
        ("knowledge", "article.html", b.article, ("บทความ", "Article"), ("ตัวอย่างหน้าบทความ", "Sample article page"), True),
        ("corporate", "corporate.html", corporate, ("บริการสำหรับองค์กร", "For Organizations"), ("Psychotest และอบรมพัฒนาบุคลากร โดยโรงพยาบาลมนารมย์", "Psychotest and staff training by Manarom Hospital"), False),
        ("contact", "contact.html", contact, ("ติดต่อเรา", "Contact Us"), ("ที่อยู่ เบอร์โทร แผนที่ และการเดินทาง", "Address, phone, map and directions"), False),
        ("faq", "faq.html", faq, ("คำถามที่พบบ่อย", "FAQ"), ("คำถามที่พบบ่อยก่อนมาโรงพยาบาล", "Frequently asked questions"), False),
        ("pricing", "pricing.html", pricing, ("อัตราค่าบริการ", "Rates"), ("อัตราค่าบริการผู้ป่วยนอกและผู้ป่วยใน", "Outpatient and inpatient rates"), False),
        ("register", "register.html", b.register, ("ลงทะเบียนผู้ป่วยใหม่", "New Patient Registration"), ("ลงทะเบียนผู้ป่วยใหม่ออนไลน์", "Register online"), False),
    ]
    n = 0
    for lang in ("th", "en"):
        c = b.Ctx(lang)
        d = OUT if lang == "th" else os.path.join(OUT, "en")
        os.makedirs(d, exist_ok=True)
        for key, file, fn, title, desc, reading in pages:
            with open(os.path.join(d, file), "w", encoding="utf-8") as f:
                f.write(layout(c, key, file, c.t(*title), c.t(*desc), fn(c), reading=reading)); n += 1
        for s in C.SERVICES:
            file = svc_href(s["slug"])
            with open(os.path.join(d, file), "w", encoding="utf-8") as f:
                f.write(layout(c, "svc", file, c.t(s["th"], s["en"]), c.t(s["s_th"], s["s_en"]), service_page(c, s))); n += 1
    with open(os.path.join(OUT, "assets", "js", "search-index.js"), "w", encoding="utf-8") as f:
        f.write("/* Site search index — generated by build2.py */\nwindow.MANAROM_SEARCH = " + json.dumps({"th": search_entries("th"), "en": search_entries("en")}, ensure_ascii=False) + ";\n")
    print("built", n, "pages")

if __name__ == "__main__":
    main()
