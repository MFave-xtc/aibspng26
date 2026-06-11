# AIBS Digital Setup Guides

**Website:** AIBS Digital Setup Guides — PNG Digital Setup Knowledge Hub  
**Owner:** Mariosu Fave / AI Digital Bridge Solutions PNG (AIBS)  
**Version:** v1.0  
**Status:** MVP Build — Owner Review Required Before Publication  

Free step-by-step ICT, internet safety, cybersecurity, small office, internet café, and gaming zone setup guides built for Papua New Guinea homes, SMEs, parents, schools, churches, and community users.

---

## Quick Start

This is a **static HTML/CSS/JS website** — no build system required.

```bash
# Serve locally (Python 3)
python3 -m http.server 8080

# Or with Node.js
npx serve .

# Open in browser
open http://localhost:8080
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Pages | Static HTML5 |
| Styling | Vanilla CSS (`styles.css`) |
| Interactivity | Vanilla JS (`site.js`) |
| Deployment | GitHub Pages (static) |

No build step. No framework. No npm dependencies. Open any HTML file in a browser.

---

## File Structure

```
/
├── index.html                    Homepage
├── start-here.html               Start Here guide selector
├── about.html                    About AIBS
├── contact.html                  Contact / Request Help
├── checklists.html               Free checklists listing
├── disclaimer.html               Public disclaimer
├── privacy.html                  Privacy statement
├── 404.html                      404 Not Found page
│
├── guides/
│   ├── index.html                All guides with search/filter
│   ├── secure-wifi-router-png.html
│   ├── strong-passwords-png.html
│   ├── two-factor-authentication-png.html
│   ├── identify-online-scams-png.html
│   ├── protect-personal-information-png.html
│   ├── internet-safety-children-png.html
│   ├── content-filtering-home-png.html
│   ├── content-filtering-office-png.html
│   ├── secure-smartphone-png.html
│   ├── public-wifi-safety-png.html
│   ├── start-internet-cafe-png.html
│   └── internet-cafe-hardware-png.html
│
├── categories/
│   ├── home-internet-safety.html
│   ├── small-office-setup.html
│   ├── internet-cafe-setup.html
│   ├── gaming-zone-setup.html
│   ├── children-family-safety.html
│   ├── cybersecurity-basics.html
│   ├── buying-guides.html
│   └── templates-checklists.html
│
├── docs/                         Project documentation
├── assets/svg/                   SVG brand assets (placeholders)
├── styles.css                    Design system CSS
├── site.js                       Shared JavaScript
├── sitemap.xml
└── robots.txt
```

---

## How to Add a New Guide

1. Copy an existing guide: `cp guides/strong-passwords-png.html guides/your-guide-png.html`
2. Update `<title>` and `<meta description>`
3. Update breadcrumb category link
4. Update guide metadata strip (audience, difficulty, time)
5. Update sidebar table of contents anchor links
6. Write content following `CONTENT_AUTHORING_GUIDE.md`
7. Add guide card to `guides/index.html`
8. Add guide card to the relevant `categories/[category].html`
9. Run QA checklist from `docs/QA_CHECKLIST.md`
10. Get owner approval before changing status from DRAFT to PUBLISHED

**Guide URL pattern:** `/guides/[descriptive-slug]-png.html`

---

## Deployment

### GitHub Pages

Push to the configured branch. GitHub Pages serves the repo root.

```bash
git add .
git commit -m "Add new guides"
git push origin main
```

Configure: Repository Settings → Pages → Source: Deploy from branch → main / root

**Important:** Update `CNAME` with the confirmed domain before deployment.  
Current CNAME contains a previous project domain and must be replaced.  
**[REQUIRES USER CONFIRMATION: Final domain name]**

### Alternative Hosts

- **Netlify:** Connect GitHub repo, no build command, publish directory: `.`
- **Cloudflare Pages:** Connect GitHub repo, no build command, output: `.`
- **Vercel:** Framework: Other, output directory: `.`

---

## Items Requiring Owner Confirmation

| Item | Status |
|---|---|
| Final domain name | REQUIRES CONFIRMATION |
| Contact email address | REQUIRES CONFIRMATION |
| Analytics platform | REQUIRES CONFIRMATION |
| Tok Pisin summaries | REQUIRES CONFIRMATION |
| Official PNG map SVG | REQUIRES CONFIRMATION |
| Official Bird of Paradise SVG | REQUIRES CONFIRMATION |

---

## Known Limitations

1. Nav/footer HTML is duplicated in every page — update all files when nav changes
2. Contact form uses mailto: fallback — no server-side processing
3. SVG assets are placeholder approximations — replace with official artwork
4. CNAME needs updating with confirmed domain
5. Analytics not yet installed

---

## Next Steps

1. Owner review all 12 guide pages for accuracy and PNG context
2. Replace placeholder contact email
3. Update CNAME with confirmed domain
4. Install analytics
5. Replace placeholder SVG assets with official AIBS artwork
6. Complete QA checklist for all 12 guides
7. Test on mobile devices
8. Continue content roadmap (Guides 13-20)

See `DEVELOPMENT_NOTES.md` and `CONTENT_AUTHORING_GUIDE.md` for technical details.
