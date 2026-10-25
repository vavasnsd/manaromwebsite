# Manarom Hospital website — notes for the IT team

Static site: plain HTML + CSS + JavaScript. No build step, no framework, no database.
Thai pages live at `/`, English pages at `/en/` (same file names).

```
index.html  about.html  services.html  doctors.html  assessments.html  test.html
knowledge.html  article.html  corporate.html  contact.html  faq.html  pricing.html  register.html
service-*.html            14 service detail pages (opd, ipd, daycenter, child, adult, elderly, ot, pt,
                          art, dance, music, sleep, special-ed, psych-test)
en/…                      same 27 pages in English
assets/css/styles.css     all styles (brand tokens at the top)
assets/js/app.js          all interactions + form handling
assets/js/config.js       ← the only file you need to edit to connect the backend
assets/js/search-index.js header search index (generated; TH + EN entries {t,c,u,k,x})
assets/img/               illustrations, logo, favicon, jaidee.png (mascot)
assets/img/photos/        hero/service photos (1600px + 800px -sm), resized from pic/
pic/                      original photos from the hospital (not loaded by the site)
```

## 1. Hosting

Upload the whole folder to any static host (Nginx/Apache, Netlify, Vercel, S3 + CloudFront, GitHub Pages).
Nothing has to run on the server. Serve with HTTPS.

## 2. Connecting forms to the backend

Open `assets/js/config.js` and set `API_BASE`:

```js
window.MANAROM_CONFIG = {
  API_BASE: "https://api.manarom.com",
  ENDPOINTS: {
    register:   "/api/v1/patients/pre-register",
    contact:    "/api/v1/contact-messages",
    corporate:  "/api/v1/corporate-inquiries",
    assessment: "/api/v1/assessment-results",
    newsletter: "/api/v1/newsletter-subscribers"
  },
  HEADERS: {},          // e.g. { "X-Api-Key": "..." } — don't put secrets here; it's public
  TIMEOUT_MS: 15000,
  SEND_ASSESSMENT_RESULTS: false
};
```

While `API_BASE` is empty the site is in **demo mode**: forms validate and show a success screen
with a generated reference number and the JSON that would be sent. Nothing leaves the browser.

### Request

Every form sends `POST {API_BASE}{endpoint}` with `Content-Type: application/json`:

```json
{
  "form": "register",
  "lang": "th",
  "submitted_at": "2026-10-06T03:15:22.481Z",
  "page": "register.html",
  "data": { "...fields below..." }
}
```

### Expected response

- Success: HTTP 2xx, JSON body with `reference` (or `ref` / `id`) → shown to the user as the reference number.
- Error: HTTP 4xx/5xx, optional `{ "message": "..." }` → the user sees a generic "couldn't send, please try again or call us".
- CORS: allow the website origin, method `POST`, header `Content-Type` (+ any custom header you add).

### Fields per form (`data`)

**register** (`register.html`, 3-step wizard)

| field | type | required | notes |
|---|---|---|---|
| patient_for | `self` \| `child` \| `family` | yes | |
| first_name, last_name | string | yes | patient |
| date_of_birth | `YYYY-MM-DD` | yes | |
| gender | `female` \| `male` \| `other` | no | |
| guardian_name, guardian_relationship | string | when patient_for ≠ self | |
| phone | string | yes | validated `0` + 8–9 digits |
| email | string | no | |
| service | string | yes | English service name or `not_sure` |
| preferred_date | `YYYY-MM-DD` | yes | today or later |
| preferred_time | `morning` \| `afternoon` \| `evening` | no | |
| preferred_doctor | string | no | |
| concern | string ≤1000 | no | sensitive — store encrypted |
| contact_channel | `phone` \| `line` \| `email` | yes | |
| line_id | string | when contact_channel = line | |
| consent_pdpa | boolean | yes (must be true) | |
| consent_marketing | boolean | no | |

**contact** — `name`*, `phone`*, `email`, `topic`* (`general|booking|billing|feedback`), `message`*, `consent_pdpa`*

**corporate** — `organization`*, `company_size`* (`1–50|51–200|201–1000|1000+`), `contact_name`*, `phone`*, `email`*, `interests` (array of `psychotest|training|workshop|eap`), `message`, `consent_pdpa`*

**newsletter** (footer, every page) — `email`*

**assessment** (only if `SEND_ASSESSMENT_RESULTS: true`) — `test_id`, `answers` (array of 0–3), `score`, `level` (`low|medium|high|severe`).
Keep this off until the clinical and PDPA teams approve storing screening results.

Validation runs in the browser for user experience only — **validate again on the server.**

## 3. Content still to fill

Phone, address, hours, prices, services, corporate (Psychotest/Training), history, FAQ and
travel info now come from the current manarom.com. Remaining placeholders (striped `[brackets]`):
doctor names and schedules in `doctors.html`. Search the HTML for `class="ph"` to find them.
Articles link out to the existing blog at https://www.manarom.com/blog/ .

The ST-5 stress test (`test.html`) uses the Department of Mental Health ST-5 items and score bands.
Ask the clinical team to confirm the wording before launch.

Images in `assets/img/*.svg` are illustrations; replace them with real hospital photos
(keep the same file names, or update the `src`).

## 4. Fonts

Prompt (headings) and IBM Plex Sans Thai (body) from Google Fonts.
To use the brand font PSL Kittithada on the web (licence allows websites), add `@font-face`
rules at the top of `styles.css` and put it first in `--f-display`.
