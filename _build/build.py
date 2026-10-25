#!/usr/bin/env python3
"""Builds the Manarom static site (Thai at /, English at /en/).
Run:  python3 build.py   -> writes ../site/*.html and ../site/en/*.html
"""
import json, os, html

OUT = os.path.join(os.path.dirname(__file__), "..", "site")
E = html.escape

# ---------------------------------------------------------------- icons
I = {
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "arrow_ur": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>',
 "left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>',
 "right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
 "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
 "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.4A8 8 0 1 1 21 12z"/></svg>',
 "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
 "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
 "alert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>',
 "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>',
 # tile / service icons
 "doctor": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="7" r="4"/><path d="M5 21v-1a7 7 0 0 1 14 0v1"/><path d="M12 14v4M10 16h4"/></svg>',
 "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/></svg>',
 "clipboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9 4V3h6v1M9 10h6M9 14h6M9 18h3"/></svg>',
 "receipt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 3h14v18l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 8h6M9 12h6"/></svg>',
 "user_plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="4"/><path d="M2 21v-1a7 7 0 0 1 11-5.7M19 14v6M16 17h6"/></svg>',
 "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/></svg>',
 "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 21v-4h6v4M8 7h2M14 7h2M8 11h2M14 11h2"/></svg>',
 "bed": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 18V6M3 14h18v4M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="2"/></svg>',
 "child": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="6" r="3"/><path d="M8 21l1-7-3-3 4-2h4l4 2-3 3 1 7"/></svg>',
 "person": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="7" r="4"/><path d="M4 21v-1a8 8 0 0 1 16 0v1"/></svg>',
 "cane": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="10" cy="5" r="2.5"/><path d="M10 8v6l-3 7M10 14l3 7M10 10l4 2M17 10v11M17 10a2 2 0 0 0-2-2"/></svg>',
 "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 11V6a2 2 0 0 0-4 0v5M14 10V4a2 2 0 0 0-4 0v6M10 10.5V6a2 2 0 0 0-4 0v8a8 8 0 0 0 16 0v-3a2 2 0 0 0-4 0"/></svg>',
 "walk": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="13" cy="4" r="2"/><path d="M9 21l2-6 3 3v3M7 12l3-4h4l2 4 3 1M11 15l-1-4"/></svg>',
 "palette": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.3 0-1.1.9-2 2-2h2.3A4.7 4.7 0 0 0 22 10c0-3.9-4.5-7-10-7z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10.5" cy="7" r="1"/><circle cx="15.5" cy="7.5" r="1"/></svg>',
 "dance": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="4" r="2"/><path d="M6 9l6 1 5-3M12 10v5l-4 6M12 15l4 6"/></svg>',
 "music": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/></svg>',
 "moon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
 "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/></svg>',
 "brain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V5a2 2 0 0 0-3-1zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/></svg>',
 "team": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="7" r="3"/><circle cx="17" cy="8" r="2.5"/><path d="M3 20v-1a6 6 0 0 1 12 0v1M15 14a5 5 0 0 1 6 5v1"/></svg>',
 "chalk": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20l4-4 4 4M7 9h6M7 12h10"/></svg>',
}

# mood faces (line drawings, no emoji)
def face(mouth, brow=""):
    return ('<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
            '<circle cx="20" cy="20" r="17" fill="var(--sky)" stroke="var(--blue)"/>'
            '<circle cx="14" cy="17" r="1.6" fill="currentColor" stroke="none"/><circle cx="26" cy="17" r="1.6" fill="currentColor" stroke="none"/>'
            + brow + '<path d="' + mouth + '"/></svg>')
FACES = {
 "good": face("M13 24c2 3.5 12 3.5 14 0"),
 "ok": face("M14 26h12"),
 "sad": face("M13 28c2-3.5 12-3.5 14 0"),
 "tense": face("M13 26c1.5-1 3-1 4.5 0s3 1 4.5 0 3-1 4.5 0", '<path d="M11 12l5 2M29 12l-5 2"/>'),
}

IMG = {k: f"assets/img/{k}.svg" for k in ["building", "consult", "daycenter", "ot", "team", "child", "adult", "elderly", "doctor", "map"]}

PAGES = [  # key, file, th, en, in_main_nav
 ("home", "index.html", "หน้าแรก", "Home", True),
 ("about", "about.html", "เกี่ยวกับเรา", "About Us", True),
 ("services", "services.html", "บริการ", "Services", True),
 ("doctors", "doctors.html", "ค้นหาแพทย์", "Find a Doctor", True),
 ("assess", "assessments.html", "แบบประเมิน", "Self-Assessments", True),
 ("knowledge", "knowledge.html", "คลังความรู้", "Knowledge", True),
 ("corporate", "corporate.html", "บริการองค์กร", "For Organizations", True),
 ("contact", "contact.html", "ติดต่อเรา", "Contact", True),
]

class Ctx:
    def __init__(s, lang):
        s.lang = lang
        s.p = "" if lang == "th" else "../"
    def t(s, th, en):
        return th if s.lang == "th" else en

def ph(x):
    return f'<span class="ph">{E(x)}</span>'

# ---------------------------------------------------------------- layout
def layout(c, key, file, title, desc, body, extra_head="", reading=False):
    t, p = c.t, c.p
    other = ("en/" + file) if c.lang == "th" else ("../" + file)
    th_href, en_href = (file, other) if c.lang == "th" else (other, file)
    nav = "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if k == key else ""}>{t(a, b)}</a>'
        for k, f, a, b, m in PAGES if m)
    dnav = "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if k == key else ""}>{t(a, b)}{I["right"]}</a>'
        for k, f, a, b, m in PAGES)
    lang_sw = (f'<span class="lang" role="group" aria-label="{t("เลือกภาษา", "Language")}">'
               f'<a href="{th_href}" lang="th" hreflang="th"{" aria-current=\"true\"" if c.lang == "th" else ""}>TH</a>'
               f'<a href="{en_href}" lang="en" hreflang="en"{" aria-current=\"true\"" if c.lang == "en" else ""}>EN</a></span>')
    full_title = (title + " | " if key != "home" else "") + t("โรงพยาบาลมนารมย์", "Manarom Hospital")
    return f"""<!doctype html>
<html lang="{c.lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(desc)}">
<meta name="color-scheme" content="only light">
<meta name="theme-color" content="#113C80">
<link rel="icon" href="{p}assets/img/favicon.png">
<link rel="alternate" hreflang="th" href="{th_href}">
<link rel="alternate" hreflang="en" href="{en_href}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600&family=Prompt:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{p}assets/css/styles.css">
{extra_head}</head>
<body>
<a class="skip" href="#main">{t("ข้ามไปเนื้อหาหลัก", "Skip to main content")}</a>
<div class="progress" aria-hidden="true"></div>
{'<div class="progress reading" aria-hidden="true" style="background:var(--blue-mid)"></div>' if reading else ''}
<div class="topbar">
  <div class="wrap">
    <div class="topbar__group">
      <span class="topbar__item">{I["phone"]}{t("โทร", "Call")} {ph(t("[เบอร์โทรศัพท์]", "[Phone number]"))}</span>
      <span class="topbar__item">{I["clock"]}{ph(t("[วัน–เวลาทำการ]", "[Opening hours]"))}</span>
    </div>
    <div class="topbar__group">
      <span class="topbar__group topbar__quick">
        <a href="pricing.html">{t("อัตราค่าบริการ", "Rates")}</a>
        <a href="faq.html">{t("คำถามที่พบบ่อย", "FAQ")}</a>
        <a href="contact.html#jobs">{t("ร่วมงานกับเรา", "Careers")}</a>
      </span>
      {lang_sw}
    </div>
  </div>
</div>
<header class="header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="{t("หน้าแรก โรงพยาบาลมนารมย์", "Manarom Hospital home")}"><img src="{p}assets/img/logo.png" alt="{t("โรงพยาบาลมนารมย์", "Manarom Hospital")}" width="168" height="48"></a>
    <nav class="nav" aria-label="{t("เมนูหลัก", "Main menu")}">{nav}</nav>
    <div class="header__actions">
      <a class="btn btn--primary btn--sm" href="register.html">{t("ลงทะเบียนผู้ป่วยใหม่", "New Patient Registration")}</a>
      <button class="burger" type="button" aria-label="{t("เปิดเมนู", "Open menu")}" aria-expanded="false" aria-controls="drawer"><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer__scrim" data-close-drawer></div>
  <div class="drawer__panel" role="dialog" aria-modal="true" aria-label="{t("เมนู", "Menu")}">
    <div class="drawer__top"><img src="{p}assets/img/logo.png" alt="" width="140" height="40"><button class="drawer__close" type="button" data-close-drawer aria-label="{t("ปิดเมนู", "Close menu")}">{I["close"]}</button></div>
    <nav aria-label="{t("เมนูหลัก", "Main menu")}">{dnav}
      <a href="pricing.html"{' aria-current="page"' if key=="pricing" else ''}>{t("อัตราค่าบริการ", "Rates")}{I["right"]}</a>
      <a href="faq.html"{' aria-current="page"' if key=="faq" else ''}>{t("คำถามที่พบบ่อย", "FAQ")}{I["right"]}</a>
    </nav>
    <div class="drawer__foot">
      <a class="btn btn--primary btn--block" href="register.html">{t("ลงทะเบียนผู้ป่วยใหม่", "New Patient Registration")}{I["arrow"]}</a>
      {lang_sw}
      <span class="muted" style="font-size:15px">{t("โทร", "Call")} {ph(t("[เบอร์โทรศัพท์]", "[Phone number]"))}</span>
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
        <span>{ph(t("[ที่อยู่โรงพยาบาล]", "[Hospital address]"))}</span>
        <span class="hotline">{t("สายด่วนสุขภาพจิต", "Mental health hotline")} <b>1323</b></span>
      </div>
      <div>
        <h4>{t("เมนู", "Menu")}</h4>
        <ul>
          <li><a href="about.html">{t("เกี่ยวกับเรา", "About Us")}</a></li>
          <li><a href="doctors.html">{t("ค้นหาแพทย์", "Find a Doctor")}</a></li>
          <li><a href="pricing.html">{t("อัตราค่าบริการ", "Rates")}</a></li>
          <li><a href="knowledge.html">{t("คลังความรู้", "Knowledge")}</a></li>
          <li><a href="faq.html">{t("คำถามที่พบบ่อย", "FAQ")}</a></li>
        </ul>
      </div>
      <div>
        <h4>{t("บริการ", "Services")}</h4>
        <ul>
          <li><a href="services.html">{t("บริการทั้งหมด", "All services")}</a></li>
          <li><a href="assessments.html">{t("แบบประเมินสุขภาพใจ", "Self-assessments")}</a></li>
          <li><a href="register.html">{t("ลงทะเบียนผู้ป่วยใหม่", "New patient registration")}</a></li>
          <li><a href="corporate.html">{t("บริการสำหรับองค์กร", "For organizations")}</a></li>
          <li><a href="contact.html#jobs">{t("ร่วมงานกับเรา", "Careers")}</a></li>
        </ul>
      </div>
      <div class="stack" style="gap:12px">
        <h4 style="margin:0">{t("รับข่าวสารสุขภาพใจ", "Mental health newsletter")}</h4>
        <form class="newsletter" data-form="newsletter">
          <label class="sr-only" for="nl-email-{key}">{t("อีเมล", "Email")}</label>
          <input id="nl-email-{key}" type="email" name="email" required placeholder="{t("อีเมลของคุณ", "Your email")}" autocomplete="email">
          <button class="btn btn--white btn--sm" type="submit">{t("สมัคร", "Join")}</button>
        </form>
        <ul style="flex-direction:row;flex-wrap:wrap;gap:8px 18px;margin-top:8px">
          <li><a href="https://www.youtube.com/user/ManaromCenter">YouTube</a></li>
          <li><a href="#">Facebook</a></li>
          <li><a href="#">TikTok</a></li>
          <li><a href="#">LINE</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> {t("โรงพยาบาลมนารมย์", "Manarom Hospital")}</span>
      <a href="https://manarom.com/images/Data_Protecti_on_Policy_ManaromHospital.pdf">{t("นโยบายการคุ้มครองข้อมูลส่วนบุคคล", "Data protection policy")}</a>
    </div>
  </div>
</footer>
<div class="fab">
  <div class="fab__menu" id="fab-menu">
    <a href="contact.html">{I["chat"]}{t("ส่งข้อความถึงเรา", "Send us a message")}</a>
    <a href="register.html">{I["user_plus"]}{t("ลงทะเบียนผู้ป่วยใหม่", "Register as new patient")}</a>
    <a href="contact.html#map">{I["pin"]}{t("แผนที่และการเดินทาง", "Map and directions")}</a>
  </div>
  <button class="totop" type="button" aria-label="{t("กลับขึ้นด้านบน", "Back to top")}">{I["up"]}</button>
  <button class="fab__main" type="button" aria-expanded="false" aria-controls="fab-menu" aria-label="{t("ติดต่อเรา", "Contact us")}">{I["plus"]}</button>
</div>
<script src="{p}assets/js/config.js"></script>
<script src="{p}assets/js/app.js"></script>
</body>
</html>
"""

def page_hero(c, crumb, title, lead, img, eyebrow=""):
    t = c.t
    return f"""<section class="phero">
  <div class="wrap">
    <div class="stack" style="gap:18px">
      <nav class="crumbs" aria-label="{t("ตำแหน่งหน้า", "Breadcrumb")}"><a href="index.html">{t("หน้าแรก", "Home")}</a><span aria-hidden="true">/</span><span>{E(crumb)}</span></nav>
      {f'<span class="eyebrow">{E(eyebrow)}</span>' if eyebrow else ''}
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </div>
    <div class="phero__img reveal"><img src="{c.p}{img}" alt="" width="800" height="600"></div>
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
        <p>{t("บอกเราสั้น ๆ ว่ากังวลเรื่องอะไร เจ้าหน้าที่จะช่วยแนะนำแพทย์และบริการที่เหมาะกับคุณ", "Tell us briefly what's on your mind. Our team will suggest the right doctor and service for you.")}</p>
      </div>
      <div class="cta__btns">
        <a class="btn btn--white" href="contact.html">{t("ส่งข้อความถึงเรา", "Send us a message")}{I["arrow"]}</a>
        <a class="btn btn--line" href="register.html">{t("ลงทะเบียนผู้ป่วยใหม่", "Register as new patient")}</a>
      </div>
    </div>
  </div>
</section>"""

def success_box(c, kind, title, text):
    t = c.t
    return f"""<div class="form-success" data-success-for="{kind}" hidden role="status">
  <h3 class="h3">{title}</h3>
  <p>{text}</p>
  <span class="muted" style="font-size:14px">{t("เลขอ้างอิง", "Reference number")}</span>
  <span class="ref" data-ref>—</span>
  <p class="muted" data-demo-note style="font-size:14px">{t("โหมดตัวอย่าง: ข้อมูลยังไม่ถูกส่งจริง จนกว่าทีม IT จะเชื่อมต่อระบบหลังบ้าน (ดู README-IT.md)", "Demo mode: nothing was actually sent until the IT team connects the backend (see README-IT.md).")}</p>
  <details class="payload"><summary>{t("ดูข้อมูลที่จะส่งเข้าระบบ (สำหรับทีม IT)", "See the data that will be sent (for IT)")}</summary><pre></pre></details>
  <button class="btn btn--ghost btn--sm" type="button" data-reset-form="{kind}">{t("กรอกใหม่อีกครั้ง", "Fill in again")}</button>
</div>"""

def field(id_, label, inp, req=True, hint=""):
    return (f'<div class="field"><label for="{id_}">{label}{"<span class=\"req\" aria-hidden=\"true\">*</span>" if req else ""}</label>'
            f'{inp}{f"<span class=\"hint\">{hint}</span>" if hint else ""}<span class="err" aria-live="polite"></span></div>')

# ---------------------------------------------------------------- data
SERVICES = [  # group, icon, th, en, img, desc_th, desc_en
 ("treat", "doctor", "ผู้ป่วยนอก", "Outpatient (OPD)", "consult", "ตรวจรักษากับจิตแพทย์ แบบนัดหมายล่วงหน้า", "See a psychiatrist by appointment"),
 ("treat", "bed", "ผู้ป่วยใน", "Inpatient (IPD)", "building", "ดูแลใกล้ชิดตลอด 24 ชั่วโมงโดยทีมสหวิชาชีพ", "Round-the-clock care by a multidisciplinary team"),
 ("treat", "child", "จิตเวชเด็กและวัยรุ่น", "Child & Adolescent Psychiatry", "child", "พัฒนาการ การเรียนรู้ อารมณ์ และพฤติกรรม", "Development, learning, emotions and behavior"),
 ("treat", "person", "จิตเวชผู้ใหญ่", "Adult Psychiatry", "adult", "ความเครียด ซึมเศร้า วิตกกังวล และปัญหาการนอน", "Stress, depression, anxiety and sleep"),
 ("treat", "cane", "จิตเวชผู้สูงอายุ", "Elderly Psychiatry", "elderly", "ความจำ อารมณ์ และการปรับตัวในวัยเกษียณ", "Memory, mood and adjusting to later life"),
 ("rehab", "sun", "ศูนย์กิจกรรมกลางวัน", "Day Activity Center", "daycenter", "โปรแกรมฟื้นฟูแบบไป–กลับ", "A day rehabilitation program"),
 ("rehab", "hand", "กิจกรรมบำบัด", "Occupational Therapy", "ot", "ฝึกทักษะการใช้ชีวิตประจำวัน", "Building everyday living skills"),
 ("rehab", "walk", "กายภาพบำบัด", "Physical Therapy", "ot", "ฟื้นฟูการเคลื่อนไหวของร่างกาย", "Restoring movement and strength"),
 ("rehab", "palette", "ศิลปะบำบัด", "Art Psychotherapy", "daycenter", "สื่อสารความรู้สึกผ่านงานศิลปะ", "Expressing feelings through art"),
 ("rehab", "dance", "การเต้นบำบัด", "Dance Therapy", "daycenter", "เชื่อมกายและใจผ่านการเคลื่อนไหว", "Connecting body and mind through movement"),
 ("rehab", "music", "ดนตรีบำบัด", "Music Therapy", "daycenter", "ใช้ดนตรีช่วยผ่อนคลายและฟื้นฟู", "Using music to relax and recover"),
 ("special", "moon", "ตรวจรักษาปัญหาการนอน", "Sleep Disorders", "adult", "นอนไม่หลับ นอนมาก หรือหลับไม่สนิท", "Insomnia, oversleeping or restless sleep"),
 ("special", "book", "การศึกษาพิเศษ", "Special Education", "child", "ช่วยเด็กที่มีความต้องการพิเศษในการเรียนรู้", "Support for children with learning needs"),
 ("special", "brain", "การทดสอบทางจิตวิทยา", "Psychological Testing", "consult", "ประเมินด้วยแบบทดสอบมาตรฐานโดยนักจิตวิทยา", "Standardized testing by psychologists"),
]
GROUPS = [("treat", "การรักษา", "Treatment"), ("rehab", "บำบัดและฟื้นฟู", "Therapy & Rehabilitation"), ("special", "บริการเฉพาะทาง", "Specialized Services")]

TESTS = [  # cat, th, en, live
 ("adult", "แบบประเมินความเครียด (ST-5)", "Stress check (ST-5)", True),
 ("adult", "คัดกรองภาวะซึมเศร้าและความเสี่ยงต่อการฆ่าตัวตาย", "Depression and suicide-risk screening", False),
 ("adult", "โรควิตกกังวล", "Anxiety disorder", False),
 ("adult", "โรคแพนิค", "Panic disorder", False),
 ("adult", "โรคเครียดหลังเหตุการณ์ร้ายแรง (PTSD)", "Post-traumatic stress (PTSD)", False),
 ("adult", "สภาพอารมณ์ (Mania)", "Mood (mania)", False),
 ("child", "โรคสมาธิสั้น (ADHD)", "ADHD", False),
 ("child", "ความฉลาดทางอารมณ์ อายุ 12–17 ปี", "Emotional quotient, ages 12–17", False),
 ("adult", "ความฉลาดทางอารมณ์ อายุ 18–60 ปี", "Emotional quotient, ages 18–60", False),
 ("family", "การทำหน้าที่ครอบครัว", "Family functioning", False),
 ("family", "ความสุขของคนไทย", "Thai happiness index", False),
 ("adult", "การติดบุหรี่ของ Fagerstrom", "Fagerstrom nicotine dependence", False),
]

ARTICLES = [  # cat, th, en, img
 ("work", "Burnout สภาวะหมดไฟจากการทำงาน", "Burnout: when work wears you down", "adult"),
 ("work", "Imposter Syndrome ทำไมฉันไม่เคยเก่งพอ", "Imposter syndrome: why I never feel good enough", "consult"),
 ("family", "สังเกตพฤติกรรมลูก เมื่อไหร่ต้องไปพบจิตแพทย์", "When should your child see a psychiatrist?", "child"),
 ("family", "10 วิธี สร้างวินัยให้ลูกรัก", "10 ways to build discipline in your child", "child"),
 ("teen", "5 เทคนิค คุยกับพ่อแม่อย่างไร เมื่อลูกวัยรุ่นอยากพบจิตแพทย์", "5 ways to tell your parents you want to see a psychiatrist", "consult"),
 ("teen", "STOP BULLYING หยุดแกล้งกัน ก่อนซึมเศร้าถามหา", "Stop bullying before depression sets in", "daycenter"),
 ("elder", "กิจกรรมส่งเสริมความจำ สำหรับผู้สูงอายุที่มีภาวะสมองเสื่อม", "Memory activities for older adults with dementia", "elderly"),
 ("elder", "วางแผนจิตใจให้พร้อมก่อนวัยเกษียณ", "Preparing your mind for retirement", "elderly"),
 ("cond", "โรคแพนิก (Panic Disorder) ทุกข์ทรมานแค่ไหน", "Panic disorder: what it really feels like", "adult"),
 ("cond", "เดี๋ยวดี เดี๋ยวร้าย ใช่ไบโพลาร์หรือเปล่านะ?", "Up one day, down the next: is it bipolar?", "consult"),
 ("cond", "CBT-I ปรับความคิด พฤติกรรม บำบัดรักษาโรคนอนไม่หลับ", "CBT-I: treating insomnia by changing thoughts and habits", "adult"),
 ("work", "คลายเครียดง่าย ๆ ที่โต๊ะทำงาน", "Easy stress relief at your desk", "ot"),
]
ACATS = [("work", "วัยทำงาน", "Working life"), ("family", "เด็กและครอบครัว", "Children & family"), ("teen", "วัยรุ่น", "Teens"), ("elder", "ผู้สูงอายุ", "Older adults"), ("cond", "โรคและการรักษา", "Conditions & treatment")]
ACAT = {k: (a, b) for k, a, b in ACATS}

DOCTORS = [  # type, tags_th, tags_en
 ("adult", ["ซึมเศร้า", "วิตกกังวล"], ["Depression", "Anxiety"]),
 ("adult", ["ไบโพลาร์", "การนอน"], ["Bipolar", "Sleep"]),
 ("adult", ["ความเครียด", "วัยทำงาน"], ["Stress", "Working adults"]),
 ("adult", ["ผู้สูงอายุ", "ความจำ"], ["Older adults", "Memory"]),
 ("child", ["สมาธิสั้น", "พัฒนาการ"], ["ADHD", "Development"]),
 ("child", ["ออทิสติก", "การเรียนรู้"], ["Autism", "Learning"]),
 ("child", ["วัยรุ่น", "อารมณ์"], ["Teens", "Emotions"]),
 ("team", ["นักจิตวิทยาคลินิก"], ["Clinical psychologist"]),
 ("team", ["นักกิจกรรมบำบัด"], ["Occupational therapist"]),
 ("team", ["นักดนตรีบำบัด"], ["Music therapist"]),
]
DTYPES = [("adult", "จิตแพทย์ผู้ใหญ่", "Adult psychiatrists"), ("child", "จิตแพทย์เด็กและวัยรุ่น", "Child & adolescent psychiatrists"), ("team", "ทีมสหวิชาชีพ", "Care team")]

# ---------------------------------------------------------------- pages
def home(c):
    t, p = c.t, c.p
    slides = [("building", "อาคารโรงพยาบาล", "Hospital building"), ("consult", "ห้องให้คำปรึกษา", "Consultation room"),
              ("daycenter", "ศูนย์กิจกรรมกลางวัน", "Day Activity Center"), ("ot", "ห้องกิจกรรมบำบัด", "Occupational therapy room"),
              ("team", "ทีมแพทย์และสหวิชาชีพ", "Our care team")]
    sl = "".join(f'<div class="carousel__slide{" is-active" if i == 0 else ""}" role="group" aria-roledescription="slide" aria-label="{i+1} / 5"><img src="{p}{IMG[k]}" alt="{t(a, b)}" width="800" height="600"><span class="carousel__cap">{t(a, b)}</span></div>' for i, (k, a, b) in enumerate(slides))
    dots = "".join(f'<button class="carousel__dot" type="button" aria-label="{t("ภาพที่", "Photo")} {i+1}"></button>' for i in range(5))
    moods = [
        ("good", "สบายดี", "Good", "ดีใจด้วยนะคะ ลองอ่านบทความดูแลใจเพื่อเก็บพลังใจดี ๆ ไว้ใช้ในวันที่เหนื่อย", "Glad to hear it. Our articles can help you keep that energy for harder days.", "knowledge.html", "อ่านบทความดูแลใจ", "Read wellbeing articles"),
        ("ok", "เฉย ๆ", "So-so", "บางวันก็แค่เรื่อย ๆ ลองเช็กความเครียดของตัวเองใน 1 นาที จะได้รู้ทันใจตัวเอง", "Some days are just so-so. A one-minute stress check helps you notice how you're doing.", "test.html", "เช็กความเครียด 1 นาที", "Take the 1-minute stress check"),
        ("sad", "เศร้า", "Low", "ขอบคุณที่บอกกันนะคะ ถ้ารู้สึกแบบนี้ติดต่อกันหลายวัน การได้คุยกับผู้เชี่ยวชาญช่วยได้มาก", "Thank you for sharing. If this lasts several days, talking with a specialist can really help.", "doctors.html", "ค้นหาจิตแพทย์", "Find a psychiatrist"),
        ("tense", "เครียด", "Tense", "ความเครียดสะสมจัดการได้ เริ่มจากทำแบบประเมิน แล้วเราช่วยแนะนำขั้นต่อไปให้", "Built-up stress can be managed. Start with a quick check and we'll suggest what's next.", "test.html", "ทำแบบประเมินความเครียด", "Check your stress"),
    ]
    mo = "".join(f'<button class="mood__opt" type="button" aria-pressed="false" data-msg="{E(t(m1, m2))}" data-href="{h}" data-cta="{E(t(c1, c2))}">{FACES[k]}{t(a, b)}</button>' for k, a, b, m1, m2, h, c1, c2 in moods)
    tiles = [
        ("doctor", "ค้นหาแพทย์", "Find a doctor", "จิตแพทย์ผู้ใหญ่ เด็กและวัยรุ่น และทีมสหวิชาชีพ", "Adult, child and adolescent psychiatrists and our care team", "doctors.html"),
        ("heart", "บริการของเรา", "Our services", "ผู้ป่วยนอก ผู้ป่วยใน และโปรแกรมบำบัดฟื้นฟู", "Outpatient, inpatient and therapy programs", "services.html"),
        ("clipboard", "แบบประเมินสุขภาพใจ", "Self-assessments", "คัดกรองความเครียด ซึมเศร้า วิตกกังวล และอื่น ๆ", "Screen for stress, depression, anxiety and more", "assessments.html"),
        ("receipt", "อัตราค่าบริการ", "Service rates", "ดูค่าบริการก่อนนัดหมาย วางแผนได้สบายใจ", "Check rates before you book", "pricing.html"),
        ("user_plus", "ลงทะเบียนผู้ป่วยใหม่", "New patient registration", "กรอกข้อมูลออนไลน์ล่วงหน้า ลดเวลารอวันมา", "Register online and save time on the day", "register.html"),
        ("map", "ติดต่อและการเดินทาง", "Contact and directions", "ที่อยู่ แผนที่ และช่องทางการติดต่อ", "Address, map and ways to reach us", "contact.html"),
    ]
    tl = "".join(f'<a class="tile reveal" style="--d:{i*70}ms" href="{h}"><span class="tile__icon">{I[ic]}</span><h3>{t(a, b)}</h3><p>{t(d1, d2)}</p><span class="link-arrow">{t("ไปที่หน้านี้", "Go")}{I["arrow"]}</span></a>' for i, (ic, a, b, d1, d2, h) in enumerate(tiles))
    ages = [("child", "เด็กและวัยรุ่น", "Children & teens", "จิตเวชเด็กและวัยรุ่น", "Child & Adolescent Psychiatry", "พัฒนาการ การเรียนรู้ อารมณ์ และพฤติกรรม", "Development, learning, emotions and behavior"),
            ("adult", "วัยทำงาน", "Working age", "จิตเวชผู้ใหญ่", "Adult Psychiatry", "ความเครียด ซึมเศร้า วิตกกังวล และปัญหาการนอน", "Stress, depression, anxiety and sleep"),
            ("elderly", "ผู้สูงอายุ", "Older adults", "จิตเวชผู้สูงอายุ", "Elderly Psychiatry", "ความจำ อารมณ์ และการปรับตัวในวัยเกษียณ", "Memory, mood and adjusting to later life")]
    ag = "".join(f'<a class="age reveal" style="--d:{i*90}ms" href="services.html"><div class="age__img"><img src="{p}{IMG[k]}" alt="" width="800" height="600"><span class="age__tag">{t(g1, g2)}</span></div><h3>{t(a, b)}{I["arrow_ur"]}</h3><p>{t(d1, d2)}</p></a>' for i, (k, g1, g2, a, b, d1, d2) in enumerate(ages))
    therapies = [t(a, b) for a, b in [("ศิลปะบำบัด", "Art therapy"), ("ดนตรีบำบัด", "Music therapy"), ("การเต้นบำบัด", "Dance therapy"), ("กิจกรรมบำบัด", "Occupational therapy"), ("กายภาพบำบัด", "Physical therapy"), ("การศึกษาพิเศษ", "Special education"), ("ตรวจรักษาปัญหาการนอน", "Sleep care"), ("การทดสอบทางจิตวิทยา", "Psychological testing")]]
    mq = "".join(f'<span class="marquee__item">{E(x)}</span>' for x in therapies)
    posts = "".join(art_card(c, a, i) for i, a in enumerate(ARTICLES[:3]))
    return f"""<section class="hero">
  <div class="wrap">
    <div class="hero__text">
      <span class="eyebrow">{t("โรงพยาบาลจิตเวชเฉพาะทาง ดูแลทุกช่วงวัย", "Specialist psychiatric hospital for every age")}</span>
      <h1 class="h1 hero__title">{t('พลังใจดี<br>เริ่มที่...<span class="accent">มนารมย์<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M4 14 C 80 4, 200 4, 296 12"/></svg></span>', 'A stronger mind<br>starts at <span class="accent">Manarom<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M4 14 C 80 4, 200 4, 296 12"/></svg></span>')}</h1>
      <p class="lead">{t("ดูแลสุขภาพใจของเด็ก วัยรุ่น ผู้ใหญ่ และผู้สูงอายุ โดยจิตแพทย์และทีมสหวิชาชีพ ในบรรยากาศที่อบอุ่นและเป็นส่วนตัว", "Mental health care for children, teens, adults and older adults, by psychiatrists and a multidisciplinary team, in a warm and private setting.")}</p>
      <div class="hero__ctas">
        <a class="btn btn--primary" href="register.html">{t("ลงทะเบียนผู้ป่วยใหม่", "Register as a new patient")}{I["arrow"]}</a>
        <a class="btn btn--ghost" href="test.html">{t("เช็กความเครียด 1 นาที", "1-minute stress check")}</a>
      </div>
      <div class="hero__trust">
        <span>{I["shield"]}{t("ข้อมูลการรักษาเป็นความลับ", "Your records stay confidential")}</span>
        <span>{I["check"]}{t("ทีมสหวิชาชีพครบในที่เดียว", "A full care team in one place")}</span>
      </div>
    </div>
    <div class="hero__visual">
      <div class="carousel" aria-roledescription="carousel" aria-label="{t("ภาพบรรยากาศโรงพยาบาล", "Hospital photos")}">
        <div class="carousel__dots">{dots}</div>
        {sl}
        <div class="carousel__nav"><button class="carousel__btn" type="button" data-prev aria-label="{t("ภาพก่อนหน้า", "Previous photo")}">{I["left"]}</button><button class="carousel__btn" type="button" data-next aria-label="{t("ภาพถัดไป", "Next photo")}">{I["right"]}</button></div>
      </div>
      <div class="mosaic" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="hero__float" aria-hidden="true"><span class="dot">{I["chat"]}</span><span><b>{t("คุยกับเราได้", "We're here to listen")}</b><small>{t("ตอบกลับภายในวันทำการ", "Reply within one working day")}</small></span></div>
    </div>
  </div>
</section>

<section class="mood" aria-labelledby="mood-h">
  <div class="wrap">
    <div class="mood__card reveal">
      <div class="mood__q">
        <span class="eyebrow">{t("เช็กอินใจ", "Check in")}</span>
        <h2 class="h3" id="mood-h">{t("วันนี้ใจของคุณเป็นอย่างไรบ้าง", "How are you feeling today?")}</h2>
      </div>
      <div class="mood__opts">{mo}</div>
      <div class="mood__answer" aria-live="polite" aria-hidden="true"><div><div class="mood__answer-inner"><p data-mood-text></p><a class="btn btn--primary btn--sm" href="#" data-mood-link><span data-mood-link-label></span>{I["arrow"]}</a></div></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div class="stack"><span class="eyebrow">{t("เริ่มต้นได้ทันที", "Start here")}</span><h2 class="h2">{t("วันนี้ให้เราช่วยเรื่องอะไรดี", "How can we help you today?")}</h2></div>
    </div>
    <div class="tiles">{tl}</div>
  </div>
</section>

<section class="section section--mist" style="padding-block:clamp(48px,6vw,72px)">
  <div class="wrap">
    <div class="stats reveal">
      <div class="stat"><b><span data-count="14">14</span></b><span>{t("บริการรักษาและบำบัด", "treatment and therapy services")}</span></div>
      <div class="stat"><b><span data-count="12">12</span></b><span>{t("แบบประเมินสุขภาพใจ", "self-assessments")}</span></div>
      <div class="stat"><b><span data-count="210">210</span><sup>+</sup></b><span>{t("บทความความรู้", "health articles")}</span></div>
      <div class="stat"><b><span data-count="3">3</span></b><span>{t("ช่วงวัยที่เราดูแล", "age groups we care for")}</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div class="stack"><span class="eyebrow">{t("ดูแลตามช่วงวัย", "Care for every age")}</span><h2 class="h2">{t("บริการสำหรับทุกคนในครอบครัว", "Services for the whole family")}</h2></div>
      <a class="link-arrow" href="services.html">{t("ดูบริการทั้งหมด", "See all services")}{I["arrow"]}</a>
    </div>
    <div class="ages">{ag}</div>
  </div>
</section>

<div class="marquee" aria-label="{t("โปรแกรมบำบัด", "Therapy programs")}"><div class="marquee__track">{mq}<span aria-hidden="true" style="display:contents">{mq}</span></div></div>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("ขั้นตอนการรับบริการ", "How it works")}</span><h2 class="h2">{t("เริ่มดูแลใจได้ใน 3 ขั้น", "Get started in 3 steps")}</h2></div></div>
    <div class="steps">
      <div class="step" style="--d:0ms"><span class="step__no">{t("ขั้นที่ 1", "STEP 1")}</span><h3>{t("สำรวจใจตัวเอง", "Check in with yourself")}</h3><p>{t("ทำแบบประเมินออนไลน์เพื่อคัดกรองเบื้องต้น ใช้เวลาไม่นานและเป็นส่วนตัว", "Take a short, private online assessment for an initial screening.")}</p><a class="link-arrow" href="assessments.html">{t("ไปที่แบบประเมิน", "Go to assessments")}{I["arrow"]}</a></div>
      <div class="step" style="--d:200ms"><span class="step__no">{t("ขั้นที่ 2", "STEP 2")}</span><h3>{t("เลือกแพทย์และบริการ", "Choose a doctor and service")}</h3><p>{t("ค้นหาจิตแพทย์ตามช่วงวัย ดูตารางออกตรวจ และอัตราค่าบริการ", "Find psychiatrists by age group and check schedules and rates.")}</p><a class="link-arrow" href="doctors.html">{t("ค้นหาแพทย์", "Find a doctor")}{I["arrow"]}</a></div>
      <div class="step" style="--d:400ms"><span class="step__no">{t("ขั้นที่ 3", "STEP 3")}</span><h3>{t("ลงทะเบียนและนัดหมาย", "Register and book")}</h3><p>{t("ลงทะเบียนผู้ป่วยใหม่ออนไลน์ แล้วเจ้าหน้าที่จะติดต่อกลับเพื่อยืนยันนัด", "Register online and our staff will call to confirm your visit.")}</p><a class="link-arrow" href="register.html">{t("ลงทะเบียน", "Register")}{I["arrow"]}</a></div>
    </div>
  </div>
</section>

<section class="section section--sky">
  <div class="wrap split">
    <div class="split__img reveal"><img src="{p}{IMG['daycenter']}" alt="{t("ศูนย์กิจกรรมกลางวัน", "Day Activity Center")}" width="800" height="600"></div>
    <div class="stack reveal" style="--d:120ms;gap:20px">
      <span class="eyebrow">Day Activity Center</span>
      <h2 class="h2">{t("ศูนย์กิจกรรมกลางวัน", "Day Activity Center")}</h2>
      <p class="lead">{t("โปรแกรมฟื้นฟูแบบไป–กลับ สำหรับผู้ที่ต้องการกลับมาใช้ชีวิตประจำวันได้อย่างมั่นใจ ผสานหลายรูปแบบการบำบัดไว้ในวันเดียว", "A day program for people rebuilding confidence in daily life, combining several therapies in one day.")}</p>
      <div class="chips"><span class="chip">{t("กิจกรรมบำบัด", "Occupational")}</span><span class="chip">{t("ศิลปะบำบัด", "Art")}</span><span class="chip">{t("ดนตรีบำบัด", "Music")}</span><span class="chip">{t("การเต้นบำบัด", "Dance")}</span></div>
      <div><a class="btn btn--primary" href="services.html#rehab">{t("ดูรายละเอียดโปรแกรม", "See program details")}{I["arrow"]}</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div class="stack"><span class="eyebrow">{t("คลังความรู้", "Knowledge")}</span><h2 class="h2">{t("บทความสุขภาพใจ", "Mental health articles")}</h2></div>
      <a class="link-arrow" href="knowledge.html">{t("ดูบทความทั้งหมด", "See all articles")}{I["arrow"]}</a>
    </div>
    <div class="cards">{posts}</div>
  </div>
</section>
{cta_band(c)}"""

def art_card(c, a, i, item=False):
    t, p = c.t, c.p
    cat, th, en, img = a
    ct = t(*ACAT[cat])
    attrs = f' data-item data-cat="{cat}" data-text="{E(t(th, en) + " " + ct)}"' if item else ""
    return f'<a class="card reveal" style="--d:{(i%3)*80}ms" href="article.html"{attrs}><div class="card__img"><img src="{p}{IMG[img]}" alt="" loading="lazy" width="800" height="600"></div><div class="card__meta"><b>{ct}</b><span>{t("อ่าน 5 นาที", "5 min read")}</span></div><h3>{E(t(th, en))}</h3></a>'

def about(c):
    t, p = c.t, c.p
    team = [("จิตแพทย์", "Psychiatrists"), ("นักจิตวิทยาคลินิก", "Clinical psychologists"), ("พยาบาลจิตเวช", "Psychiatric nurses"),
            ("นักกิจกรรมบำบัด", "Occupational therapists"), ("นักกายภาพบำบัด", "Physical therapists"), ("นักศิลปะ ดนตรี และการเต้นบำบัด", "Creative arts therapists")]
    tm = "".join(f'<div class="reveal" style="--d:{i*60}ms"><b>{t(a, b)}</b><small>{b if c.lang == "th" else ph("[จำนวน]")}</small></div>' for i, (a, b) in enumerate(team))
    tm = "".join(f'<div class="reveal" style="--d:{i*60}ms"><b>{t(a, b)}</b><small>{ph(t("[รายละเอียดหน้าที่]", "[Role description]"))}</small></div>' for i, (a, b) in enumerate(team))
    values = [("shield", "เป็นส่วนตัว", "Private", "ข้อมูลการรักษาเก็บเป็นความลับ", "Your records are kept confidential"),
              ("team", "ทำงานเป็นทีม", "Team-based", "แพทย์และสหวิชาชีพวางแผนร่วมกัน", "Doctors and therapists plan together"),
              ("heart", "อบอุ่นเหมือนบ้าน", "Warm", "บรรยากาศที่ผ่อนคลาย ไม่น่ากลัว", "A calm, welcoming setting")]
    vl = "".join(f'<div class="panel reveal stack" style="--d:{i*80}ms"><span class="tile__icon">{I[ic]}</span><h3 class="h3">{t(a, b)}</h3><p class="muted">{t(d1, d2)}</p></div>' for i, (ic, a, b, d1, d2) in enumerate(values))
    return page_hero(c, t("เกี่ยวกับเรา", "About Us"), t("เกี่ยวกับมนารมย์", "About Manarom"),
                     t("โรงพยาบาลเฉพาะทางด้านจิตเวช ที่ดูแลสุขภาพใจของทุกคนในครอบครัว", "A specialist psychiatric hospital caring for the whole family."), IMG["building"], t("รู้จักเรา", "Who we are")) + f"""
<section class="section">
  <div class="wrap split">
    <div class="stack reveal" style="gap:20px">
      <span class="eyebrow">{t("เรื่องราวของเรา", "Our story")}</span>
      <h2 class="h2">{t("พลังใจดี เริ่มที่...มนารมย์", "A stronger mind starts at Manarom")}</h2>
      <p class="lead">{ph(t("[ประวัติและความเป็นมาของโรงพยาบาล 2–3 ย่อหน้า]", "[Hospital history, 2–3 paragraphs]"))}</p>
    </div>
    <div class="split__img reveal" style="--d:120ms"><img src="{p}{IMG['team']}" alt="{t("ทีมแพทย์และสหวิชาชีพ", "Our care team")}" width="800" height="600"></div>
  </div>
</section>
<section class="section section--mist">
  <div class="wrap">
    <div class="grid-2">
      <div class="panel reveal stack"><span class="eyebrow">Vision</span><h2 class="h3">{t("วิสัยทัศน์", "Vision")}</h2><p class="muted">{ph(t("[ข้อความวิสัยทัศน์]", "[Vision statement]"))}</p></div>
      <div class="panel reveal stack" style="--d:100ms"><span class="eyebrow">Mission</span><h2 class="h3">{t("พันธกิจ", "Mission")}</h2><p class="muted">{ph(t("[ข้อความพันธกิจ]", "[Mission statement]"))}</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("สิ่งที่เรายึดถือ", "What we value")}</span><h2 class="h2">{t("ดูแลใจแบบมนารมย์", "How we care")}</h2></div></div>
    <div class="grid-3">{vl}</div>
  </div>
</section>
<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head"><div class="stack"><span class="eyebrow">{t("ทีมสหวิชาชีพ", "Multidisciplinary team")}</span><h2 class="h2">{t("ผู้เชี่ยวชาญหลายสาขา ในทีมเดียว", "Many specialists, one team")}</h2></div><a class="btn btn--primary" href="doctors.html">{t("ดูรายชื่อแพทย์", "See our doctors")}{I["arrow"]}</a></div>
    <div class="team">{tm}</div>
  </div>
</section>
{cta_band(c)}"""

def services(c):
    t, p = c.t, c.p
    out = []
    for g, a, b in GROUPS:
        cards = "".join(
            f'<button class="svc reveal" style="--d:{(i%3)*70}ms" type="button" data-open-modal="svc-modal" data-title="{E(t(th, en))}" data-sub="{E(t(d1, d2))}" data-img="{p}{IMG[img]}"><span class="svc__icon">{I[ic]}</span><b>{t(th, en)}</b><small>{t(d1, d2)}</small><span class="more">{t("ดูรายละเอียด", "Details")}{I["arrow"].replace("<svg", "<svg width=\"16\" height=\"16\"")}</span></button>'
            for i, (gg, ic, th, en, img, d1, d2) in enumerate([s for s in SERVICES if s[0] == g]))
        out.append(f'<div class="svc-group" id="{g}"><div class="sec-head" style="margin-bottom:24px"><h2 class="h2">{t(a, b)}</h2></div><div class="svc-grid">{cards}</div></div>')
    chips = "".join(f'<a class="chip" href="#{g}" style="text-decoration:none">{t(a, b)}</a>' for g, a, b in GROUPS)
    return page_hero(c, t("บริการ", "Services"), t("บริการของเรา", "Our services"),
                     t("14 บริการ ครอบคลุมการรักษา บำบัด และฟื้นฟู สำหรับทุกช่วงวัย", "14 services covering treatment, therapy and rehabilitation for every age."), IMG["ot"], t("รักษา บำบัด ฟื้นฟู", "Treat, support, recover")) + f"""
<section class="section">
  <div class="wrap">
    <div class="chips" style="margin-bottom:48px">{chips}</div>
    {''.join(out)}
  </div>
</section>
<dialog class="modal" id="svc-modal" aria-labelledby="svc-modal-title">
  <button class="modal__close" type="button" data-close aria-label="{t("ปิด", "Close")}">{I["close"]}</button>
  <div class="modal__img"><img data-slot="img" src="{p}{IMG['consult']}" alt=""></div>
  <div class="modal__body">
    <h2 class="h3" id="svc-modal-title" data-slot="title">—</h2>
    <p class="lead" data-slot="sub" style="font-size:17px"></p>
    <p class="muted">{ph(t("[รายละเอียดบริการ: เหมาะกับใคร ขั้นตอน ระยะเวลา]", "[Service details: who it's for, process, duration]"))}</p>
    <div class="modal__actions"><a class="btn btn--primary" href="register.html">{t("นัดหมายบริการนี้", "Book this service")}{I["arrow"]}</a><a class="btn btn--ghost" href="pricing.html">{t("ดูอัตราค่าบริการ", "See rates")}</a></div>
  </div>
</dialog>
{cta_band(c)}"""

def doctors(c):
    t, p = c.t, c.p
    tabs = f'<button class="tab" type="button" role="tab" aria-selected="true" data-filter="all">{t("ทั้งหมด", "All")}</button>' + "".join(
        f'<button class="tab" type="button" role="tab" aria-selected="false" data-filter="{k}">{t(a, b)}</button>' for k, a, b in DTYPES)
    tname = {k: t(a, b) for k, a, b in DTYPES}
    cards = []
    for i, (typ, tt, te) in enumerate(DOCTORS):
        tags = tt if c.lang == "th" else te
        name = t(f"[ชื่อ–นามสกุล {i+1}]", f"[Full name {i+1}]")
        img = IMG["doctor"] if typ != "team" else IMG["team"]
        cards.append(f'<button class="doc reveal" style="--d:{(i%4)*60}ms" type="button" data-item data-cat="{typ}" data-text="{E(name + " " + " ".join(tags) + " " + tname[typ])}" data-open-modal="doc-modal" data-title="{E(name)}" data-sub="{E(tname[typ] + " · " + ", ".join(tags))}" data-img="{p}{img}">'
                     f'<div class="doc__img"><img src="{p}{img}" alt="" loading="lazy" width="800" height="600"><span class="badge">{tname[typ]}</span></div>'
                     f'<b>{name}</b><div class="tags">{"".join(f"<span class=tag>{E(x)}</span>" for x in tags)}</div></button>')
    days = [t(a, b) for a, b in [("จันทร์", "Mon"), ("อังคาร", "Tue"), ("พุธ", "Wed"), ("พฤหัสบดี", "Thu"), ("ศุกร์", "Fri")]]
    sched = "".join(f'<tr><td>{d}</td><td>{ph(t("[เวลา]", "[Time]"))}</td></tr>' for d in days)
    return page_hero(c, t("ค้นหาแพทย์", "Find a Doctor"), t("ค้นหาแพทย์และทีมสหวิชาชีพ", "Find a doctor or care team member"),
                     t("ค้นหาจากชื่อ ความเชี่ยวชาญ หรือช่วงวัยที่ต้องการ แล้วกดดูตารางออกตรวจได้ทันที", "Search by name, specialty or age group, then open a profile to see the schedule."), IMG["team"]) + f"""
<section class="section">
  <div class="wrap" data-collection="doc-list">
    <div class="toolbar">
      <label class="search"><span class="sr-only">{t("ค้นหาแพทย์", "Search doctors")}</span>{I["search"]}<input type="search" data-search placeholder="{t("ค้นหา เช่น ซึมเศร้า, สมาธิสั้น", "Search, e.g. depression, ADHD")}"></label>
    </div>
    <div class="tabs" role="tablist" aria-label="{t("ประเภทแพทย์", "Doctor type")}">{tabs}</div>
    <div class="docs" id="doc-list">{''.join(cards)}</div>
    <p class="empty" id="doc-list-empty" hidden>{t("ไม่พบแพทย์ที่ตรงกับคำค้น ลองคำอื่น หรือโทรสอบถามเราได้", "No matches. Try another word or call us.")}</p>
  </div>
</section>
<dialog class="modal" id="doc-modal" aria-labelledby="doc-modal-title">
  <button class="modal__close" type="button" data-close aria-label="{t("ปิด", "Close")}">{I["close"]}</button>
  <div class="modal__img"><img data-slot="img" src="{p}{IMG['doctor']}" alt=""></div>
  <div class="modal__body">
    <h2 class="h3" id="doc-modal-title" data-slot="title">—</h2>
    <p class="muted" data-slot="sub"></p>
    <h3 style="font-size:17px;margin-top:6px">{t("ตารางออกตรวจ", "Clinic schedule")}</h3>
    <table class="sched"><thead><tr><th>{t("วัน", "Day")}</th><th>{t("เวลา", "Time")}</th></tr></thead><tbody>{sched}</tbody></table>
    <div class="modal__actions"><a class="btn btn--primary" href="register.html">{t("นัดพบแพทย์", "Book an appointment")}{I["arrow"]}</a></div>
  </div>
</dialog>
{cta_band(c)}"""

def assessments(c):
    t = c.t
    cats = [("adult", "ผู้ใหญ่", "Adults"), ("child", "เด็กและวัยรุ่น", "Children & teens"), ("family", "ครอบครัว", "Family")]
    cn = {k: t(a, b) for k, a, b in cats}
    filt = f'<button class="filter" type="button" aria-pressed="true" data-filter="all">{t("ทั้งหมด", "All")}</button>' + "".join(f'<button class="filter" type="button" aria-pressed="false" data-filter="{k}">{t(a, b)}</button>' for k, a, b in cats)
    cards = "".join(
        f'<a class="test-card reveal{" is-live" if live else ""}" style="--d:{(i%3)*60}ms" href="test.html" data-item data-cat="{cat}" data-text="{E(t(th, en))}"><span class="test-card__top"><span>{cn[cat]}</span>{"<span class=\"pill pill--live\">" + t("ทำได้เลย", "Ready") + "</span>" if live else "<span class=\"pill\">" + t("ตัวอย่าง", "Sample") + "</span>"}</span><b>{E(t(th, en))}</b><span class="link-arrow">{t("เริ่มทำแบบประเมิน", "Start")}{I["arrow"]}</span></a>'
        for i, (cat, th, en, live) in enumerate(TESTS))
    pdfs = ["PHQ-9", "MDQ", t("แบบประเมินความเครียด", "Stress questionnaire"), "Adult ADHD Self-Report Scale", "Generalized Anxiety"]
    pl = "".join(f'<a class="chip" style="text-decoration:none" href="https://manarom.com/download/index_eng.html">{E(x)} · PDF</a>' for x in pdfs)
    return page_hero(c, t("แบบประเมิน", "Self-Assessments"), t("แบบประเมินสุขภาพใจ", "Mental health self-assessments"),
                     t("ใช้เวลาไม่กี่นาที เพื่อสำรวจใจตัวเองเบื้องต้น ผลเป็นการคัดกรอง ไม่ใช่การวินิจฉัย", "A few minutes to check in with yourself. Results are a screening, not a diagnosis."), IMG["consult"]) + f"""
<section class="section">
  <div class="wrap" data-collection="test-list">
    <div class="toolbar">
      <div class="filters" role="group" aria-label="{t("กลุ่มผู้ใช้", "Audience")}">{filt}</div>
      <label class="search"><span class="sr-only">{t("ค้นหาแบบประเมิน", "Search assessments")}</span>{I["search"]}<input type="search" data-search placeholder="{t("ค้นหาแบบประเมิน", "Search assessments")}"></label>
    </div>
    <div class="tests" id="test-list">{cards}</div>
    <p class="empty" id="test-list-empty" hidden>{t("ไม่พบแบบประเมินที่ค้นหา", "No assessments match your search")}</p>
    <div class="notice reveal" style="margin-top:40px">{I["alert"]}<p>{t("หากมีความคิดทำร้ายตนเอง หรือต้องการความช่วยเหลือเร่งด่วน โทร <b>สายด่วนสุขภาพจิต 1323</b> ได้ตลอด 24 ชั่วโมง", "If you are thinking of harming yourself or need urgent help, call the <b>Mental Health Hotline 1323</b>, open 24 hours.")}</p></div>
  </div>
</section>
<section class="section section--mist" style="padding-block:56px">
  <div class="wrap stack" style="gap:20px">
    <h2 class="h3">{t("ดาวน์โหลดแบบประเมิน (PDF)", "Download questionnaires (PDF)")}</h2>
    <div class="chips">{pl}</div>
  </div>
</section>"""

def test(c):
    t = c.t
    # ST-5 stress test, Department of Mental Health, Thailand — verify wording with the clinical team before launch
    qs_th = ["มีปัญหาการนอน นอนไม่หลับหรือนอนมาก", "มีสมาธิน้อยลง", "หงุดหงิด / กระวนกระวาย / ว้าวุ่นใจ", "รู้สึกเบื่อ เซ็ง", "ไม่อยากพบปะผู้คน"]
    qs_en = ["Trouble sleeping, or sleeping too much", "Finding it harder to concentrate", "Feeling irritable, restless or unsettled", "Feeling bored or fed up", "Not wanting to see other people"]
    opts = [t(a, b) for a, b in [("แทบไม่มี", "Hardly ever"), ("เป็นบางครั้ง", "Sometimes"), ("บ่อยครั้ง", "Often"), ("เป็นประจำ", "Almost always")]]
    qs = qs_th if c.lang == "th" else qs_en
    cards = "".join(
        f'<div class="qcard{" is-active" if i == 0 else ""}" role="group" aria-labelledby="q{i}"><span class="eyebrow">{t("ในช่วง 2–4 สัปดาห์ที่ผ่านมา", "Over the past 2–4 weeks")}</span><h2 id="q{i}">{E(q)}</h2><div class="qopts">'
        + "".join(f'<button class="qopt" type="button" aria-pressed="false" data-score="{s}"><span class="qopt__key">{s}</span>{E(o)}</button>' for s, o in enumerate(opts))
        + '</div></div>' for i, q in enumerate(qs))
    bands = [
        {"key": "low", "min": 0, "max": 4, "label": t("เครียดน้อย", "Low stress"), "advice": t("ดูแลตัวเองต่อไปแบบนี้ พักผ่อนให้พอ และหากิจกรรมที่ชอบทำ", "Keep it up: rest well and make time for things you enjoy.")},
        {"key": "medium", "min": 5, "max": 7, "label": t("เครียดปานกลาง", "Moderate stress"), "advice": t("ลองหาเวลาผ่อนคลาย ออกกำลังกาย หรือพูดคุยกับคนที่ไว้ใจ ถ้ายังไม่ดีขึ้นใน 2 สัปดาห์ ปรึกษาผู้เชี่ยวชาญได้", "Try to relax, move your body or talk to someone you trust. If it doesn't ease in 2 weeks, talk to a specialist.")},
        {"key": "high", "min": 8, "max": 9, "label": t("เครียดมาก", "High stress"), "advice": t("ความเครียดระดับนี้ส่งผลต่อชีวิตประจำวัน แนะนำให้ปรึกษาจิตแพทย์หรือนักจิตวิทยา", "Stress at this level affects daily life. We recommend talking with a psychiatrist or psychologist.")},
        {"key": "severe", "min": 10, "max": 15, "label": t("เครียดมากที่สุด", "Very high stress"), "advice": t("ควรพบผู้เชี่ยวชาญโดยเร็ว หากมีความคิดทำร้ายตนเอง โทร 1323 ได้ตลอด 24 ชั่วโมง", "Please see a specialist soon. If you're thinking of harming yourself, call 1323 any time.")},
    ]
    data = {"id": "st5", "max": 15, "bands": bands, "labels": {"next": t("ถัดไป", "Next"), "finish": t("ดูผลลัพธ์", "See my result")}}
    levels = "".join(f'<div>{b["label"]}<br>{b["min"]}–{b["max"]}</div>' for b in bands)
    return f"""<section class="phero" style="padding-block:40px">
  <div class="wrap" style="grid-template-columns:1fr">
    <div class="stack" style="gap:14px">
      <nav class="crumbs" aria-label="{t("ตำแหน่งหน้า", "Breadcrumb")}"><a href="index.html">{t("หน้าแรก", "Home")}</a><span aria-hidden="true">/</span><a href="assessments.html">{t("แบบประเมิน", "Self-Assessments")}</a><span aria-hidden="true">/</span><span>ST-5</span></nav>
      <h1>{t("แบบประเมินความเครียด (ST-5)", "Stress check (ST-5)")}</h1>
      <p class="lead">{t("5 คำถาม ใช้เวลาประมาณ 1 นาที ผลเป็นการคัดกรองเบื้องต้น ไม่ใช่การวินิจฉัย", "5 questions, about 1 minute. Results are a screening, not a diagnosis.")}</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:48px">
  <div class="wrap">
    <div class="quiz panel" id="quiz">
      <div class="quiz__bar"><div class="quiz__track"><div class="quiz__fill"></div></div><span class="quiz__count" aria-live="polite">{t("ข้อ 1 จาก 5", "Question 1 of 5")}</span></div>
      {cards}
      <div class="quiz__nav"><button class="btn btn--ghost btn--sm" type="button" data-q-prev>{t("ย้อนกลับ", "Back")}</button><button class="btn btn--primary btn--sm" type="button" data-q-next>{t("ถัดไป", "Next")}</button></div>
      <div class="result" aria-live="polite">
        <div class="gauge"><svg viewBox="0 0 200 110" aria-hidden="true"><path d="M15 100 A85 85 0 0 1 185 100" fill="none" stroke="var(--line)" stroke-width="16" stroke-linecap="round"/><path data-arc d="M15 100 A85 85 0 0 1 185 100" fill="none" stroke="var(--blue-deep)" stroke-width="16" stroke-linecap="round"/></svg><div class="gauge__num"><b data-r-score>0</b><span>{t("คะแนนจาก 15", "out of 15")}</span></div></div>
        <h2 class="h2" style="text-align:center" data-r-level>—</h2>
        <p class="lead" style="text-align:center;margin-inline:auto" data-r-advice></p>
        <div class="levels" aria-hidden="true">{levels}</div>
        <div class="hero__ctas" style="justify-content:center"><a class="btn btn--primary" href="register.html">{t("นัดพบผู้เชี่ยวชาญ", "Book a specialist")}{I["arrow"]}</a><button class="btn btn--ghost" type="button" data-q-restart>{t("ทำใหม่อีกครั้ง", "Take it again")}</button></div>
        <p class="muted" style="font-size:14px;text-align:center">{t("ที่มา: แบบประเมินความเครียด ST-5 กรมสุขภาพจิต · ผลไม่ถูกเก็บหรือส่งไปที่ใด", "Source: ST-5 stress test, Department of Mental Health, Thailand · Your answers are not stored or sent anywhere.")}</p>
      </div>
    </div>
    <div class="notice" style="max-width:760px;margin:32px auto 0">{I["alert"]}<p>{t("หากมีความคิดทำร้ายตนเอง หรือต้องการความช่วยเหลือเร่งด่วน โทร <b>สายด่วนสุขภาพจิต 1323</b> ได้ตลอด 24 ชั่วโมง", "If you are thinking of harming yourself or need urgent help, call the <b>Mental Health Hotline 1323</b>, open 24 hours.")}</p></div>
  </div>
</section>
<script type="application/json" id="quiz-data">{json.dumps(data, ensure_ascii=False)}</script>"""

def knowledge(c):
    t = c.t
    filt = f'<button class="filter" type="button" aria-pressed="true" data-filter="all">{t("ทั้งหมด", "All")}</button>' + "".join(f'<button class="filter" type="button" aria-pressed="false" data-filter="{k}">{t(a, b)}</button>' for k, a, b in ACATS)
    cards = "".join(art_card(c, a, i, item=True) for i, a in enumerate(ARTICLES))
    return page_hero(c, t("คลังความรู้", "Knowledge"), t("คลังความรู้สุขภาพใจ", "Mental health knowledge"),
                     t("บทความจากจิตแพทย์และทีมสหวิชาชีพ อ่านง่าย ใช้ได้จริงในชีวิตประจำวัน", "Articles by our psychiatrists and care team: easy to read, useful every day."), IMG["daycenter"]) + f"""
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
    <a class="panel stack reveal" style="text-decoration:none;color:inherit" href="https://www.youtube.com/user/ManaromCenter"><span class="eyebrow">Video</span><h2 class="h3">Manarom Channel</h2><p class="muted">{t("คลิปความรู้สุขภาพใจบน YouTube", "Mental health videos on YouTube")}</p><span class="link-arrow">{t("ไปที่ YouTube", "Open YouTube")}{I["arrow_ur"]}</span></a>
    <a class="panel stack reveal" style="--d:100ms;text-decoration:none;color:inherit" href="article.html"><span class="eyebrow">{t("วารสาร", "Journal")}</span><h2 class="h3">{t("วารสารพลังใจดี", "Palang Jai Dee journal")}</h2><p class="muted">{t("อ่านและดาวน์โหลดฉบับย้อนหลัง (PDF)", "Read and download past issues (PDF)")}</p><span class="link-arrow">{t("ดูฉบับย้อนหลัง", "Browse issues")}{I["arrow"]}</span></a>
  </div>
</section>"""

def article(c):
    t, p = c.t, c.p
    rel = "".join(art_card(c, a, i) for i, a in enumerate([ARTICLES[1], ARTICLES[11], ARTICLES[10]]))
    return f"""<section class="section" style="padding-top:48px">
  <article class="wrap article">
    <nav class="crumbs" aria-label="{t("ตำแหน่งหน้า", "Breadcrumb")}"><a href="index.html">{t("หน้าแรก", "Home")}</a><span aria-hidden="true">/</span><a href="knowledge.html">{t("คลังความรู้", "Knowledge")}</a><span aria-hidden="true">/</span><span>{t("วัยทำงาน", "Working life")}</span></nav>
    <span class="eyebrow">{t("วัยทำงาน", "Working life")}</span>
    <h1>{t("Burnout สภาวะหมดไฟจากการทำงาน", "Burnout: when work wears you down")}</h1>
    <div class="byline"><span>{ph(t("[ชื่อผู้เขียน]", "[Author]"))}</span><span>{ph(t("[วันที่เผยแพร่]", "[Publish date]"))}</span><span>{t("อ่าน 5 นาที", "5 min read")}</span>
      <span class="share"><button type="button" data-share aria-label="{t("คัดลอกลิงก์บทความ", "Copy article link")}">{I["link"]}</button></span></div>
    <div class="split__img"><img src="{p}{IMG['adult']}" alt="" width="800" height="600"></div>
    <p>{ph(t("[ย่อหน้าเปิดบทความ]", "[Opening paragraph]"))}</p>
    <h2>{ph(t("[หัวข้อย่อยที่ 1]", "[Subheading 1]"))}</h2>
    <p>{ph(t("[เนื้อหาบทความ]", "[Article content]"))}</p>
    <blockquote>{ph(t("[ข้อความเน้นจากจิตแพทย์]", "[Pull quote from the psychiatrist]"))}</blockquote>
    <h2>{ph(t("[หัวข้อย่อยที่ 2]", "[Subheading 2]"))}</h2>
    <p>{ph(t("[เนื้อหาบทความ]", "[Article content]"))}</p>
    <div class="cta" style="margin-top:20px;padding:32px">
      <div class="cta__blocks" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="stack" style="gap:8px"><h2 class="h3" style="color:#fff">{t("รู้สึกเหนื่อยล้าต่อเนื่อง?", "Feeling worn out for a while?")}</h2><p>{t("เช็กความเครียดใน 1 นาที หรือนัดคุยกับผู้เชี่ยวชาญ", "Check your stress in 1 minute or book a specialist.")}</p></div>
      <div class="cta__btns"><a class="btn btn--white btn--sm" href="test.html">{t("เช็กความเครียด", "Stress check")}</a><a class="btn btn--line btn--sm" href="register.html">{t("นัดพบจิตแพทย์", "See a psychiatrist")}</a></div>
    </div>
  </article>
</section>
<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head"><h2 class="h2">{t("บทความที่เกี่ยวข้อง", "Related articles")}</h2><a class="link-arrow" href="knowledge.html">{t("กลับไปคลังความรู้", "Back to Knowledge")}{I["arrow"]}</a></div>
    <div class="cards">{rel}</div>
  </div>
</section>"""

def pricing(c):
    t = c.t
    rows = [("ค่าตรวจรักษาผู้ป่วยนอก (จิตแพทย์)", "Outpatient consultation (psychiatrist)"), ("ค่าห้องพักผู้ป่วยใน (ต่อวัน)", "Inpatient room (per day)"),
            ("การทดสอบทางจิตวิทยา", "Psychological testing"), ("ศูนย์กิจกรรมกลางวัน (ต่อวัน)", "Day Activity Center (per day)"),
            ("กิจกรรมบำบัด / กายภาพบำบัด (ต่อครั้ง)", "Occupational / physical therapy (per session)"), ("ศิลปะ ดนตรี และการเต้นบำบัด (ต่อครั้ง)", "Art, music or dance therapy (per session)")]
    tr = "".join(f'<tr><td>{t(a, b)}</td><td class="num">{ph(t("[ราคา]", "[Price]"))}</td></tr>' for a, b in rows)
    return page_hero(c, t("อัตราค่าบริการ", "Rates"), t("อัตราค่าบริการ", "Service rates"),
                     t("ข้อมูลค่าบริการเบื้องต้น เพื่อช่วยวางแผนก่อนนัดหมาย", "Indicative rates to help you plan before booking."), IMG["adult"]) + f"""
<section class="section">
  <div class="wrap" style="max-width:920px">
    <div class="table-wrap reveal"><table class="table"><thead><tr><th scope="col">{t("รายการ", "Service")}</th><th scope="col" class="num">{t("ค่าบริการ (บาท)", "Rate (THB)")}</th></tr></thead><tbody>{tr}</tbody></table></div>
    <p class="muted" style="margin-top:20px;font-size:15px">{ph(t("[หมายเหตุ: ราคาไม่รวมค่ายา / สิทธิประกันสุขภาพที่รับ]", "[Notes: excludes medication / accepted insurance]"))}</p>
    <div class="hero__ctas" style="margin-top:28px"><a class="btn btn--primary" href="contact.html">{t("สอบถามค่าบริการเพิ่มเติม", "Ask about rates")}{I["arrow"]}</a><a class="btn btn--ghost" href="faq.html">{t("คำถามที่พบบ่อย", "FAQ")}</a></div>
  </div>
</section>"""

def faq(c):
    t = c.t
    qs = [("ต้องเตรียมตัวอย่างไร เมื่อมาพบจิตแพทย์ครั้งแรก", "How should I prepare for my first visit?"),
          ("ต้องนัดหมายล่วงหน้าหรือไม่", "Do I need to book in advance?"),
          ("พาบุตรหลานมาพบแพทย์ ต้องเตรียมเอกสารอะไรบ้าง", "What documents do I need for my child?"),
          ("ข้อมูลการรักษาจะถูกเก็บเป็นความลับหรือไม่", "Is my treatment information confidential?"),
          ("ใช้สิทธิประกันสุขภาพได้หรือไม่", "Can I use my health insurance?"),
          ("มีบริการปรึกษาออนไลน์หรือไม่", "Do you offer online consultations?")]
    acc = "".join(f'<div class="acc reveal" data-item data-text="{E(t(a, b))}"><button class="acc__btn" type="button" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="faq-{i}">{t(a, b)}<span class="acc__icon" aria-hidden="true"></span></button><div class="acc__panel{" is-open" if i == 0 else ""}" id="faq-{i}"><div><p>{ph(t("[คำตอบจากทีมโรงพยาบาล]", "[Answer from the hospital team]"))}</p></div></div></div>' for i, (a, b) in enumerate(qs))
    return page_hero(c, t("คำถามที่พบบ่อย", "FAQ"), t("คำถามที่พบบ่อย", "Frequently asked questions"),
                     t("รวมคำตอบเรื่องที่ผู้รับบริการถามบ่อย ก่อนมาโรงพยาบาล", "Answers to what people often ask before their first visit."), IMG["elderly"]) + f"""
<section class="section">
  <div class="wrap" style="max-width:880px" data-collection="faq-list">
    <div class="toolbar"><label class="search" style="max-width:none"><span class="sr-only">{t("ค้นหาคำถาม", "Search questions")}</span>{I["search"]}<input type="search" data-search placeholder="{t("พิมพ์คำถาม เช่น ประกัน", "Type a question, e.g. insurance")}"></label></div>
    <div id="faq-list">{acc}</div>
    <p class="empty" id="faq-list-empty" hidden>{t("ไม่พบคำถามนี้ ส่งคำถามถึงเราได้เลย", "Not found. Send us your question.")}</p>
    <div class="hero__ctas" style="margin-top:40px;align-items:center"><span class="muted">{t("ไม่พบคำตอบที่ต้องการ?", "Can't find your answer?")}</span><a class="btn btn--primary btn--sm" href="contact.html">{t("ถามเจ้าหน้าที่", "Ask our staff")}{I["arrow"]}</a></div>
  </div>
</section>"""

def register(c):
    t = c.t
    svc_opts = "".join(f'<option value="{E(en)}">{E(t(th, en))}</option>' for g, ic, th, en, img, d1, d2 in SERVICES[:6]) + f'<option value="not_sure">{t("ยังไม่แน่ใจ ให้เจ้าหน้าที่แนะนำ", "Not sure, please advise")}</option>'
    who = [("self", "ตนเอง", "Myself"), ("child", "บุตรหลาน (ต่ำกว่า 18 ปี)", "My child (under 18)"), ("family", "สมาชิกในครอบครัว", "A family member")]
    who_html = "".join(f'<label class="choice"><input type="radio" name="patient_for" value="{k}" data-label="{E(t(a, b))}" required{" checked" if k == "self" else ""}><span>{t(a, b)}</span></label>' for k, a, b in who)
    gender = [("female", "หญิง", "Female"), ("male", "ชาย", "Male"), ("other", "ไม่ระบุ", "Prefer not to say")]
    g_html = "".join(f'<label class="choice"><input type="radio" name="gender" value="{k}" data-label="{E(t(a, b))}"><span>{t(a, b)}</span></label>' for k, a, b in gender)
    times = [("morning", "ช่วงเช้า", "Morning"), ("afternoon", "ช่วงบ่าย", "Afternoon"), ("evening", "ช่วงเย็น", "Evening")]
    t_html = "".join(f'<label class="choice"><input type="radio" name="preferred_time" value="{k}" data-label="{E(t(a, b))}"><span>{t(a, b)}</span></label>' for k, a, b in times)
    contact = [("phone", "โทรศัพท์", "Phone"), ("line", "LINE", "LINE"), ("email", "อีเมล", "Email")]
    c_html = "".join(f'<label class="choice"><input type="radio" name="contact_channel" value="{k}" data-label="{E(t(a, b))}" required{" checked" if k == "phone" else ""}><span>{t(a, b)}</span></label>' for k, a, b in contact)
    docs = [("แบบข้อมูลเด็กและครอบครัว", "Child & family background form"), ("แบบฟอร์มผู้ป่วยเด็ก 0–4 ปี", "Child patient form, ages 0–4"), ("แบบฟอร์มผู้ป่วยเด็ก 5–17 ปี", "Child patient form, ages 5–17")]
    d_html = "".join(f'<a class="info" style="text-decoration:none;padding:16px;border:1px solid var(--line);border-radius:14px;background:#fff" href="https://manarom.com/download/index_eng.html"><span class="info__icon">{I["clipboard"]}</span><span><b>{t(a, b)}</b><small>PDF · {t("ดาวน์โหลด", "Download")}</small></span></a>' for a, b in docs)
    return page_hero(c, t("ลงทะเบียนผู้ป่วยใหม่", "New Patient Registration"), t("ลงทะเบียนผู้ป่วยใหม่", "New patient registration"),
                     t("กรอกข้อมูลล่วงหน้า 3 ขั้นตอน ใช้เวลาประมาณ 3 นาที เจ้าหน้าที่จะติดต่อกลับเพื่อยืนยันนัด", "Three short steps, about 3 minutes. Our staff will contact you to confirm."), IMG["building"]) + f"""
<section class="section">
  <div class="wrap" style="display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:40px;align-items:start" id="book">
    <div class="panel">
      <ol class="wizard__steps"><li>{t("ข้อมูลผู้รับบริการ", "Patient details")}</li><li>{t("บริการและวันที่", "Service and date")}</li><li>{t("ตรวจสอบและยืนยัน", "Review and confirm")}</li></ol>
      <form class="form" data-form="register">
        <div class="wstep">
          <h2 class="h3">{t("ข้อมูลผู้รับบริการ", "Patient details")}</h2>
          <fieldset class="field"><legend>{t("ลงทะเบียนให้", "Registering for")}<span class="req" aria-hidden="true">*</span></legend><div class="choices">{who_html}</div><span class="err" aria-live="polite"></span></fieldset>
          <div class="row">
            {field("r-first", t("ชื่อ (ผู้รับบริการ)", "First name (patient)"), '<input id="r-first" name="first_name" required autocomplete="given-name">')}
            {field("r-last", t("นามสกุล", "Last name"), '<input id="r-last" name="last_name" required autocomplete="family-name">')}
          </div>
          <div class="row">
            {field("r-dob", t("วันเกิด", "Date of birth"), '<input id="r-dob" type="date" name="date_of_birth" required>')}
            <fieldset class="field"><legend>{t("เพศ", "Gender")}</legend><div class="choices">{g_html}</div><span class="err" aria-live="polite"></span></fieldset>
          </div>
          <div class="stack" data-show-if="patient_for=child|family" style="gap:18px;padding:20px;border-radius:16px;background:var(--mist)">
            <b style="color:var(--navy)">{t("ข้อมูลผู้ติดต่อ / ผู้ปกครอง", "Contact person / guardian")}</b>
            <div class="row">
              {field("r-gname", t("ชื่อ–นามสกุล ผู้ติดต่อ", "Contact person's full name"), '<input id="r-gname" name="guardian_name" required autocomplete="name">')}
              {field("r-grel", t("ความสัมพันธ์กับผู้รับบริการ", "Relationship to patient"), '<input id="r-grel" name="guardian_relationship" required>')}
            </div>
          </div>
          <div class="row">
            {field("r-phone", t("เบอร์โทรศัพท์", "Phone number"), '<input id="r-phone" type="tel" name="phone" required inputmode="tel" autocomplete="tel" placeholder="0812345678">')}
            {field("r-email", t("อีเมล", "Email"), '<input id="r-email" type="email" name="email" autocomplete="email" placeholder="name@email.com">', req=False)}
          </div>
          <div class="wizard__nav"><span></span><button class="btn btn--primary" type="button" data-next-step>{t("ถัดไป", "Next")}{I["arrow"]}</button></div>
        </div>
        <div class="wstep">
          <h2 class="h3">{t("บริการและวันที่สะดวก", "Service and preferred date")}</h2>
          {field("r-svc", t("บริการที่สนใจ", "Service of interest"), f'<select id="r-svc" name="service" required><option value="">{t("เลือกบริการ", "Choose a service")}</option>{svc_opts}</select>')}
          <div class="row">
            {field("r-date", t("วันที่สะดวก", "Preferred date"), '<input id="r-date" type="date" name="preferred_date" required data-future>')}
            <fieldset class="field"><legend>{t("ช่วงเวลาที่สะดวก", "Preferred time")}</legend><div class="choices">{t_html}</div><span class="err" aria-live="polite"></span></fieldset>
          </div>
          {field("r-doc", t("แพทย์ที่ต้องการ (ถ้ามี)", "Preferred doctor (optional)"), '<input id="r-doc" name="preferred_doctor">', req=False)}
          {field("r-note", t("อาการหรือเรื่องที่อยากปรึกษา (เล่าสั้น ๆ)", "What would you like help with? (briefly)"), '<textarea id="r-note" name="concern" maxlength="1000"></textarea>', req=False, hint=t("ไม่บังคับ เขียนเท่าที่สะดวกใจ", "Optional. Share only what you're comfortable with."))}
          <fieldset class="field"><legend>{t("ช่องทางที่สะดวกให้ติดต่อกลับ", "How should we contact you?")}<span class="req" aria-hidden="true">*</span></legend><div class="choices">{c_html}</div><span class="err" aria-live="polite"></span></fieldset>
          <div data-show-if="contact_channel=line">{field("r-line", "LINE ID", '<input id="r-line" name="line_id" required>')}</div>
          <div class="wizard__nav"><button class="btn btn--ghost" type="button" data-prev-step>{t("ย้อนกลับ", "Back")}</button><button class="btn btn--primary" type="button" data-next-step>{t("ตรวจสอบข้อมูล", "Review")}{I["arrow"]}</button></div>
        </div>
        <div class="wstep" data-review>
          <h2 class="h3">{t("ตรวจสอบข้อมูลก่อนส่ง", "Review before sending")}</h2>
          <dl class="review"></dl>
          <div class="field"><label class="check"><input type="checkbox" name="consent_pdpa" required> <span>{t('ข้าพเจ้ายินยอมให้โรงพยาบาลเก็บและใช้ข้อมูลนี้เพื่อการนัดหมาย ตาม<a href="https://manarom.com/images/Data_Protecti_on_Policy_ManaromHospital.pdf">นโยบายการคุ้มครองข้อมูลส่วนบุคคล</a>', 'I agree that the hospital may collect and use this information to arrange my visit, under the <a href="https://manarom.com/images/Data_Protecti_on_Policy_ManaromHospital.pdf">data protection policy</a>.')}</span></label><span class="err" aria-live="polite"></span></div>
          <div class="field"><label class="check"><input type="checkbox" name="consent_marketing"> <span>{t("รับข่าวสารและบทความสุขภาพใจทางอีเมล (ไม่บังคับ)", "Send me mental health news and articles by email (optional)")}</span></label></div>
          <div class="wizard__nav"><button class="btn btn--ghost" type="button" data-prev-step>{t("แก้ไขข้อมูล", "Edit")}</button><button class="btn btn--primary" type="submit">{t("ส่งข้อมูลลงทะเบียน", "Send registration")}{I["arrow"]}</button></div>
        </div>
      </form>
      {success_box(c, "register", t("ลงทะเบียนเรียบร้อย", "Registration received"), t("เจ้าหน้าที่จะติดต่อกลับภายใน 1 วันทำการ เพื่อยืนยันวันและเวลานัด", "Our staff will contact you within one working day to confirm your appointment."))}
    </div>
    <aside class="stack" style="gap:14px">
      <h2 class="h3">{t("เอกสารลงทะเบียน (ผู้ป่วยเด็ก)", "Registration forms (children)")}</h2>
      {d_html}
      <div class="notice" style="margin-top:12px;background:var(--sky);border-color:var(--blue-soft);color:var(--navy)">{I["shield"].replace('stroke="currentColor"','stroke="var(--blue-deep)"')}<p>{t("ข้อมูลของคุณเข้ารหัสระหว่างส่ง และใช้เพื่อการนัดหมายเท่านั้น", "Your data is encrypted in transit and used only to arrange your visit.")}</p></div>
    </aside>
  </div>
</section>
<style>@media (max-width: 960px) {{ #book {{ grid-template-columns: 1fr !important; }} }}</style>"""

def contact(c):
    t, p = c.t, c.p
    topics = [("general", "สอบถามทั่วไป", "General question"), ("booking", "การนัดหมาย", "Appointments"), ("billing", "ค่าบริการและประกัน", "Rates and insurance"), ("feedback", "ข้อเสนอแนะ", "Feedback")]
    tp = "".join(f'<option value="{k}">{t(a, b)}</option>' for k, a, b in topics)
    return page_hero(c, t("ติดต่อเรา", "Contact"), t("ติดต่อเรา", "Contact us"),
                     t("ส่งข้อความ โทร หรือแวะมาพบเรา เจ้าหน้าที่ยินดีช่วยเหลือ", "Message us, call or visit. Our team is happy to help."), IMG["map"]) + f"""
<section class="section">
  <div class="wrap grid-2" style="align-items:start">
    <div class="stack" style="gap:28px">
      <div class="info-list">
        <div class="info"><span class="info__icon">{I["pin"]}</span><span><small>{t("ที่อยู่", "Address")}</small><b>{ph(t("[ที่อยู่โรงพยาบาล]", "[Hospital address]"))}</b></span></div>
        <div class="info"><span class="info__icon">{I["phone"]}</span><span><small>{t("โทรศัพท์", "Phone")}</small><b>{ph(t("[เบอร์โทรศัพท์]", "[Phone number]"))}</b></span></div>
        <div class="info"><span class="info__icon">{I["mail"]}</span><span><small>{t("อีเมล", "Email")}</small><b>{ph(t("[อีเมล]", "[Email]"))}</b></span></div>
        <div class="info"><span class="info__icon">{I["clock"]}</span><span><small>{t("เวลาทำการ", "Opening hours")}</small><b>{ph(t("[วัน–เวลาทำการ]", "[Opening hours]"))}</b></span></div>
      </div>
      <a class="map reveal" id="map" href="https://www.google.com/maps/search/{t("โรงพยาบาลมนารมย์", "Manarom+Hospital")}"><img src="{p}{IMG['map']}" alt="" width="800" height="600"><span>{I["pin"].replace("<svg", "<svg width=\"18\" height=\"18\"")}{t("เปิดใน Google Maps", "Open in Google Maps")}</span></a>
    </div>
    <div class="panel">
      <form class="form" data-form="contact">
        <h2 class="h3">{t("ส่งข้อความถึงเรา", "Send us a message")}</h2>
        <div class="row">
          {field("c-name", t("ชื่อ", "Name"), '<input id="c-name" name="name" required autocomplete="name">')}
          {field("c-phone", t("เบอร์โทรศัพท์", "Phone"), '<input id="c-phone" type="tel" name="phone" required inputmode="tel" autocomplete="tel" placeholder="0812345678">')}
        </div>
        {field("c-email", t("อีเมล", "Email"), '<input id="c-email" type="email" name="email" autocomplete="email">', req=False)}
        {field("c-topic", t("เรื่องที่ติดต่อ", "Topic"), f'<select id="c-topic" name="topic" required><option value="">{t("เลือกเรื่อง", "Choose a topic")}</option>{tp}</select>')}
        {field("c-msg", t("ข้อความ", "Message"), '<textarea id="c-msg" name="message" required maxlength="2000"></textarea>')}
        <div class="field"><label class="check"><input type="checkbox" name="consent_pdpa" required> <span>{t("ยินยอมให้ติดต่อกลับตามนโยบายการคุ้มครองข้อมูลส่วนบุคคล", "I agree to be contacted under the data protection policy")}</span></label><span class="err" aria-live="polite"></span></div>
        <div><button class="btn btn--primary" type="submit">{t("ส่งข้อความ", "Send message")}{I["arrow"]}</button></div>
      </form>
      {success_box(c, "contact", t("ส่งข้อความแล้ว", "Message sent"), t("ขอบคุณที่ติดต่อเรา เจ้าหน้าที่จะตอบกลับภายใน 1 วันทำการ", "Thank you. Our team will reply within one working day."))}
    </div>
  </div>
</section>
<section class="section section--mist" id="jobs">
  <div class="wrap split">
    <div class="split__img reveal"><img src="{p}{IMG['team']}" alt="" width="800" height="600"></div>
    <div class="stack reveal" style="--d:120ms;gap:18px">
      <span class="eyebrow">{t("ร่วมงานกับเรา", "Careers")}</span>
      <h2 class="h2">{t("มาเป็นส่วนหนึ่งของทีมดูแลใจ", "Join our care team")}</h2>
      <p class="lead">{ph(t("[ตำแหน่งที่เปิดรับ]", "[Open positions]"))}</p>
      <div><a class="btn btn--primary" href="https://manarom.com/job_thai.html">{t("ดูตำแหน่งงานทั้งหมด", "See all openings")}{I["arrow_ur"]}</a></div>
    </div>
  </div>
</section>"""

def corporate(c):
    t = c.t
    svcs = [("brain", "Psychotest", "แบบทดสอบจิตวิทยาสำหรับองค์กร", "Psychological testing for hiring", "ช่วยคัดเลือกบุคลากรด้วยแบบทดสอบบุคลิกภาพมาตรฐาน", "Standardized personality testing to support hiring decisions"),
            ("chalk", "Training", "อบรมพัฒนาบุคลากร", "Staff training", "หลักสูตรดูแลใจในที่ทำงาน การจัดการความเครียด และการสื่อสาร", "Courses on workplace wellbeing, stress and communication"),
            ("team", "Seminar / Workshop", "สัมมนาและเวิร์กช็อป", "Seminars and workshops", "กิจกรรมเชิงปฏิบัติสำหรับทีม จัดได้ทั้งที่องค์กรและที่โรงพยาบาล", "Hands-on sessions for teams, on site or at the hospital")]
    cards = "".join(f'<div class="panel stack reveal" style="--d:{i*80}ms"><span class="tile__icon">{I[ic]}</span><span class="eyebrow">{e}</span><h2 class="h3">{t(a, b)}</h2><p class="muted">{t(d1, d2)}</p></div>' for i, (ic, e, a, b, d1, d2) in enumerate(svcs))
    interests = [("psychotest", "Psychotest"), ("training", t("อบรม", "Training")), ("workshop", t("สัมมนา / เวิร์กช็อป", "Seminar / workshop")), ("eap", t("ดูแลสุขภาพใจพนักงาน", "Employee wellbeing"))]
    it = "".join(f'<label class="choice"><input type="checkbox" name="interests" value="{k}" data-multi><span>{E(v)}</span></label>' for k, v in interests)
    sizes = ["1–50", "51–200", "201–1000", "1000+"]
    so = "".join(f'<option value="{s}">{s} {t("คน", "people")}</option>' for s in sizes)
    return page_hero(c, t("บริการองค์กร", "For Organizations"), t("บริการสำหรับองค์กร", "Services for organizations"),
                     t("ดูแลสุขภาพใจของคนในองค์กร ตั้งแต่การคัดเลือกบุคลากรถึงการพัฒนาทีม", "Supporting your people's mental health, from hiring to team development."), IMG["team"]) + f"""
<section class="section">
  <div class="wrap"><div class="grid-3">{cards}</div></div>
</section>
<section class="section section--mist">
  <div class="wrap grid-2" style="align-items:start">
    <div class="stack reveal" style="gap:18px">
      <span class="eyebrow">{t("ขอใบเสนอราคา", "Request a quote")}</span>
      <h2 class="h2">{t("บอกความต้องการขององค์กร เราจะออกแบบโปรแกรมให้", "Tell us what your organization needs")}</h2>
      <p class="lead">{t("ทีมงานจะติดต่อกลับพร้อมข้อเสนอที่เหมาะกับขนาดและเป้าหมายขององค์กร", "Our team will reply with a proposal that fits your size and goals.")}</p>
    </div>
    <div class="panel">
      <form class="form" data-form="corporate">
        <div class="row">
          {field("o-org", t("ชื่อองค์กร", "Organization"), '<input id="o-org" name="organization" required autocomplete="organization">')}
          {field("o-size", t("จำนวนพนักงาน", "Company size"), f'<select id="o-size" name="company_size" required><option value="">{t("เลือก", "Choose")}</option>{so}</select>')}
        </div>
        <div class="row">
          {field("o-name", t("ชื่อผู้ติดต่อ", "Contact name"), '<input id="o-name" name="contact_name" required autocomplete="name">')}
          {field("o-phone", t("เบอร์โทรศัพท์", "Phone"), '<input id="o-phone" type="tel" name="phone" required inputmode="tel" placeholder="0812345678">')}
        </div>
        {field("o-email", t("อีเมล", "Email"), '<input id="o-email" type="email" name="email" required autocomplete="email">')}
        <fieldset class="field"><legend>{t("บริการที่สนใจ", "Interested in")}</legend><div class="choices">{it}</div></fieldset>
        {field("o-msg", t("รายละเอียดเพิ่มเติม", "Details"), '<textarea id="o-msg" name="message" maxlength="2000"></textarea>', req=False)}
        <div class="field"><label class="check"><input type="checkbox" name="consent_pdpa" required> <span>{t("ยินยอมให้ติดต่อกลับตามนโยบายการคุ้มครองข้อมูลส่วนบุคคล", "I agree to be contacted under the data protection policy")}</span></label><span class="err" aria-live="polite"></span></div>
        <div><button class="btn btn--primary" type="submit">{t("ขอใบเสนอราคา", "Request a quote")}{I["arrow"]}</button></div>
      </form>
      {success_box(c, "corporate", t("ได้รับคำขอแล้ว", "Request received"), t("ทีมงานจะติดต่อกลับพร้อมข้อเสนอภายใน 3 วันทำการ", "Our team will send you a proposal within 3 working days."))}
    </div>
  </div>
</section>"""

BUILD = [
 ("home", "index.html", home, ("หน้าแรก", "Home"), ("โรงพยาบาลจิตเวชเฉพาะทาง ดูแลสุขภาพใจทุกช่วงวัย", "Specialist psychiatric hospital caring for every age"), False),
 ("about", "about.html", about, ("เกี่ยวกับเรา", "About Us"), ("ประวัติ วิสัยทัศน์ และทีมสหวิชาชีพของโรงพยาบาลมนารมย์", "History, vision and care team of Manarom Hospital"), False),
 ("services", "services.html", services, ("บริการ", "Services"), ("บริการรักษา บำบัด และฟื้นฟู 14 บริการ", "14 treatment, therapy and rehabilitation services"), False),
 ("doctors", "doctors.html", doctors, ("ค้นหาแพทย์", "Find a Doctor"), ("ค้นหาจิตแพทย์และทีมสหวิชาชีพ พร้อมตารางออกตรวจ", "Find psychiatrists and care team members with schedules"), False),
 ("assess", "assessments.html", assessments, ("แบบประเมิน", "Self-Assessments"), ("แบบประเมินสุขภาพใจออนไลน์ 12 แบบ", "12 online mental health self-assessments"), False),
 ("assess", "test.html", test, ("แบบประเมินความเครียด ST-5", "Stress check ST-5"), ("เช็กความเครียดใน 1 นาที", "Check your stress in 1 minute"), False),
 ("knowledge", "knowledge.html", knowledge, ("คลังความรู้", "Knowledge"), ("บทความสุขภาพใจจากจิตแพทย์", "Mental health articles by psychiatrists"), False),
 ("knowledge", "article.html", article, ("Burnout สภาวะหมดไฟ", "Burnout"), ("บทความ Burnout สภาวะหมดไฟจากการทำงาน", "Article: Burnout"), True),
 ("corporate", "corporate.html", corporate, ("บริการองค์กร", "For Organizations"), ("บริการด้านสุขภาพใจสำหรับองค์กร", "Mental health services for organizations"), False),
 ("contact", "contact.html", contact, ("ติดต่อเรา", "Contact"), ("ที่อยู่ แผนที่ และช่องทางติดต่อโรงพยาบาลมนารมย์", "Address, map and contact"), False),
 ("faq", "faq.html", faq, ("คำถามที่พบบ่อย", "FAQ"), ("คำถามที่พบบ่อยก่อนมาโรงพยาบาล", "Frequently asked questions"), False),
 ("pricing", "pricing.html", pricing, ("อัตราค่าบริการ", "Rates"), ("อัตราค่าบริการเบื้องต้น", "Indicative service rates"), False),
 ("register", "register.html", register, ("ลงทะเบียนผู้ป่วยใหม่", "New Patient Registration"), ("ลงทะเบียนผู้ป่วยใหม่ออนไลน์", "Register online as a new patient"), False),
]

def main():
    for lang in ("th", "en"):
        c = Ctx(lang)
        d = OUT if lang == "th" else os.path.join(OUT, "en")
        os.makedirs(d, exist_ok=True)
        for key, file, fn, title, desc, reading in BUILD:
            html_ = layout(c, key, file, c.t(*title), c.t(*desc), fn(c), reading=reading)
            with open(os.path.join(d, file), "w", encoding="utf-8") as f:
                f.write(html_)
    print("built", len(BUILD) * 2, "pages")

if __name__ == "__main__":
    main()
