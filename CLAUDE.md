# CLAUDE.md — กฎการทำงานโปรเจกต์ manarom-website

> อ่านไฟล์นี้ + `DESIGN.md` + `BRIEF-index.md` ก่อนแก้ทุกครั้ง ตอบวาวาเป็นภาษาไทย สั้น ใช้ตาราง ลงท้ายด้วย "ครับ"

## 1. ขอบเขตงานรอบนี้
- ทำใหม่ **เฉพาะ `index.html` (ภาษาไทย)** ตามแบบ `Resources/เว็บ 2570.ai`
- **ห้ามแตะ** หน้าอื่น (`about.html`, `service-*.html`, `en/` ฯลฯ), `assets/css/styles.css`, `assets/js/app.js`
- **`en/index.html` ใช้ดีไซน์ใหม่ (เว็บ 2570) แล้ว** (25 ต.ค. 2569) — ใช้ CSS/JS/รูปชุดเดียวกับหน้าไทย (`../assets/...`) · CSS เฉพาะอังกฤษอยู่ท้าย `index-2570.css` ใต้ `[data-lang="en"]` · แก้หน้าไทยแล้วต้องแก้ `en/index.html` ตาม · หน้าอื่นใน `en/` ยังห้ามแตะ
- **ห้ามแก้ไข ย้าย หรือเซฟทับไฟล์ใน `Resources/` ทุกไฟล์ — อ่านอย่างเดียวเท่านั้น** (เป็นต้นแบบ/ไฟล์อ้างอิง ห้ามเปลี่ยนแปลงเด็ดขาด)
- ไฟล์ใหม่ของหน้า index แยกไว้เป็นของตัวเอง:
  - `assets/css/index-2570.css`
  - `assets/js/index-2570.js`
  - รูป → `assets/img/index/` (ย่อขนาดแล้ว) · บทความ → `assets/img/articles/`
  - ฟอนต์ → `assets/fonts/noto-sans-thai/`
- **ห้ามรัน `_build/build2.py`** (มันจะเขียนทับ index.html ใหม่ทั้งไฟล์)
- ก่อนแก้ index.html ครั้งแรก ให้สำรองเป็น `index-old.html`

## 2. ต้นแบบที่ต้องตาม (ลำดับความสำคัญ)
1. `Resources/เว็บ 2570.ai` (เปิดเป็น PDF ได้) → ขนาด สี ระยะ มุมโค้ง ฟอนต์ **ต้องตรงตามนี้** (artboard กว้าง 1440 px)
2. `Resources/เว็บ 2570.pdf` / `เว็บ 2570.jpg` → ภาพรวมทั้งหน้า
3. `Resources/ตัวอย่างโทรศัพท์.jpg` → สไตล์มือถือ (การ์ดมุมโค้ง สีฟ้าอมเทานุ่ม ปุ่มลูกศร ↗)
4. `BRIEF-index.md` → ลูกเล่นและลิงก์ของแต่ละส่วน
- ถ้าค่าใน `DESIGN.md` ขัดกับไฟล์ .ai → **ยึดไฟล์ .ai** แล้วอัปเดต DESIGN.md
- ห้ามเดา ถ้าไม่แน่ใจให้ถามวาวาก่อน

## 3. วิธีทำงาน
- ทำทีละส่วน (Header → Hero → … → Footer) จบแต่ละส่วนสรุปเป็นตารางสั้น ๆ ให้วาวาดู
- HTML + CSS + JavaScript ธรรมดา ไม่ใช้ framework · ไม่ใช้ jQuery
- ดีไซน์มินิมอล ไม่ดูเหมือน AI ทำ · ลูกเล่นเบา ๆ นุ่ม ๆ (0.25–0.45 วินาที)
- รองรับ `prefers-reduced-motion` (ปิดอนิเมชันให้คนที่ตั้งค่าไว้)
- `<meta name="color-scheme" content="only light">` กันมือถือเปลี่ยนเป็นโหมดมืดเอง

## 4. SEO (บังคับทุกครั้ง)
- `<title>` + `<meta description>` ภาษาไทย มีคำว่า โรงพยาบาลจิตเวช / สุขภาพจิต / บางนา
- H1 มีอันเดียว ("พลังใจดี เริ่มที่...มนารมย์") · หัวข้อส่วนใช้ H2 · การ์ดใช้ H3
- `alt` ภาษาไทยทุกรูป · รูปใต้จอใส่ `loading="lazy"` + กำหนด `width`/`height`
- Canonical, hreflang (th/en/x-default), Open Graph ครบ
- JSON-LD: `Hospital` (ชื่อ ที่อยู่ เบอร์ เวลาเปิด แผนที่ โซเชียล) + `FAQPage` (4 ข้อ)
- **ลิงก์ภายใน**: ทุกปุ่ม/การ์ดลิงก์ไปหน้าจริง · คำสำคัญในคำตอบ FAQ ลิงก์ไปหน้าบริการ/บทความ
- รูปบีบอัด (WebP หรือ JPG คุณภาพ ~80) กว้างไม่เกิน 2 เท่าของขนาดที่แสดง

## 5. ข้อมูลจริง (ห้ามแต่งเอง)
| เรื่อง | ค่า |
|---|---|
| เบอร์ | 02-725-9595 · 02-032-9595 (นัดหมาย/เวชระเบียน 02-725-9592) |
| อีเมล | contact@manarom.com |
| ที่อยู่ | 9 ซอยสุขุมวิท 70/3 แขวงบางนาใต้ เขตบางนา กรุงเทพฯ 10260 |
| เวลา | ผู้ป่วยนอก 07:00–20:00 น. ทุกวัน · ฉุกเฉิน 24 ชม. |
| Facebook | https://www.facebook.com/ManaromHospital |
| YouTube | https://www.youtube.com/user/ManaromCenter |
| Instagram | https://www.instagram.com/manaromhospital |
| TikTok | https://www.tiktok.com/@manaromhospital |
| คลิปหน้าแรก | https://www.youtube.com/watch?v=FADtQRRRccY |
| บทความทั้งหมด | https://www.manarom.com/blog/article_thai.html |
| สมัครงาน | https://www.manarom.com/job_thai.html |
| นโยบายข้อมูลส่วนบุคคล | https://manarom.com/images/Data_Protecti_on_Policy_ManaromHospital.pdf |

## 6. เช็กก่อนส่งงาน (ทุกครั้ง)
- [ ] เปิดดูจริงที่จอคอม 1440 px และมือถือ 390 px · ไม่มีอะไรล้นจอแนวนอน
- [ ] เทียบกับไฟล์ .ai ทีละส่วน (ขนาด สี ระยะ)
- [ ] ทุกลิงก์กดได้ ไม่มีลิงก์เสีย · ไม่มี error ใน Console
- [ ] หน้าอื่นไม่ถูกแก้ (`git status` / เทียบวันที่ไฟล์)
- [ ] สรุปสิ่งที่เปลี่ยนเป็นตารางสั้น ๆ ให้วาวา
