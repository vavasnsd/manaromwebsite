/* =========================================================
   Manarom website — backend settings (for the IT team)
   ---------------------------------------------------------
   While API_BASE is empty the site runs in DEMO MODE:
   forms validate and show a success screen with the JSON
   that WOULD be sent, but nothing leaves the browser.

   To go live: set API_BASE (and adjust ENDPOINTS if your
   routes differ). Every form POSTs JSON — see README-IT.md.
   ========================================================= */
window.MANAROM_CONFIG = {
  API_BASE: "",                         // e.g. "https://api.manarom.com"
  ENDPOINTS: {
    register:   "/api/v1/patients/pre-register",
    contact:    "/api/v1/contact-messages",
    corporate:  "/api/v1/corporate-inquiries",
    assessment: "/api/v1/assessment-results",
    newsletter: "/api/v1/newsletter-subscribers"
  },
  HEADERS: {},                          // e.g. { "X-Api-Key": "..." }
  TIMEOUT_MS: 15000,
  SEND_ASSESSMENT_RESULTS: false        // keep false unless PDPA consent flow is approved
};
