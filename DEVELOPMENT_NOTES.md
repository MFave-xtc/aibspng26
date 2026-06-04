# DEVELOPMENT_NOTES.md

# AIBS Digital Setup Guides — Development Notes

**Version:** v1.0  
**Date:** June 2026  
**Status:** Active

---

## Architecture Decisions

### Static HTML/CSS/JS (No Build System)

**Decision:** Build as a static multi-page website with no framework or build step.

**Rationale:**
- The existing repository uses static HTML/CSS/JS (GitHub Pages deployment)
- A static site loads fast on variable PNG connections
- No Node.js runtime required for hosting
- Easy to maintain and deploy without a CI/CD pipeline
- Owner can edit HTML files directly in a text editor
- GitHub Pages serves static files natively

**Trade-off:** Navigation and footer HTML are duplicated in every page. This is the standard trade-off for static HTML sites. A future migration to Astro or Next.js would resolve this while maintaining static output.

### Navigation Duplication

Currently the navigation and footer HTML are copied into every page. This is intentional for v1.

**Future option:** Move to a JavaScript-injected shared header/footer:

```javascript
// In site.js, inject shared nav
function injectNav() {
  const placeholder = document.getElementById('nav-placeholder');
  if (placeholder) {
    placeholder.innerHTML = NAV_HTML;
  }
}
```

Each page would then have just:
```html
<div id="nav-placeholder"></div>
```

This reduces duplication but adds a JavaScript dependency for navigation rendering. For a public knowledge hub, this is acceptable.

### CSS Design System

The design system is in a single `styles.css` file. All CSS custom properties (variables) are defined in `:root`.

**Color tokens:**
```css
--bg:         #06111C  /* Deep navy background */
--bg-dark:    #02070D  /* Near-black for sections */
--card:       #0B1A2A  /* Card backgrounds */
--gold:       #D6A329  /* Primary gold accent */
--gold-bright:#F5C542  /* Hover/emphasis gold */
--red:        #C91F1F  /* Warning/danger color */
--white:      #F5F7FA  /* Body text */
--muted:      #AAB4C0  /* Secondary text */
--border:     rgba(214, 163, 41, 0.35)  /* Gold border */
```

### Content Source Tags

Every guide uses content tags to mark source status:
- `[CONFIRMED]` — Verified against official/vendor/standards documentation
- `[SUPPORTED]` — Supported by credible public sources
- `[INFERRED]` — Reasoned from validated evidence
- `[ASSUMED]` — Reasonable project assumption, not presented as fact
- `[UNVERIFIED]` — Not yet checked against sources
- `[REQUIRES USER CONFIRMATION]` — Must be confirmed by owner before publication
- `[INSUFFICIENT DATA]` — No reliable evidence found

These are displayed using CSS classes: `.tag-confirmed`, `.tag-assumed`, `.tag-unverified`, `.tag-requires-confirmation`

---

## JavaScript Architecture

`site.js` contains:

| Function | Purpose |
|---|---|
| `initNav()` | Scroll-triggered nav background, mobile toggle, active link detection |
| `initGuideSearch()` | Client-side guide search on guides/index.html |
| `initGuideFilter()` | Category filter buttons on guides/index.html |
| `initTocSpy()` | Table of contents scroll spy on guide pages |
| `initPrint()` | Print button handler for checklists |
| `initContactForm()` | Contact form mailto: fallback |
| `initSmoothScroll()` | Smooth scroll for anchor links |

All functions are called in the `DOMContentLoaded` listener. Functions gracefully handle missing elements (no errors if elements are not present on the page).

---

## SEO Strategy

Each page has:
- Unique `<title>` tag
- Unique `<meta name="description">`
- Open Graph tags (`og:title`, `og:description`, `og:type`)
- Semantic HTML (h1 → h2 → h3 hierarchy)
- Descriptive alt text on images
- Clean URL structure: `/guides/[slug]-png.html`

Guide URL pattern: `/guides/[descriptive-slug]-png.html`
Category URL pattern: `/categories/[category-slug].html`

**PNG suffix on guide URLs** is intentional — it signals PNG-specific content for search indexing and distinguishes from generic guides.

---

## Contact Form

The contact form uses a `mailto:` fallback — it builds a pre-populated email using form data and opens the user's email client.

**To upgrade to a real form backend:**
1. Use Netlify Forms (if deploying to Netlify) — just add `netlify` attribute to form tag
2. Use Formspree.io (free tier available)
3. Use a serverless function (AWS Lambda, Cloudflare Workers)

**Current implementation in site.js:**
```javascript
const mailtoLink = `mailto:${email}?subject=${subject}&body=${body}`;
window.location.href = mailtoLink;
```

---

## Performance Notes

- No external JavaScript dependencies (vanilla JS only)
- Google Fonts not used — system font stack (Inter, Segoe UI, Roboto, Arial)
- SVG assets are inline-embeddable (small file sizes)
- Images: Only SVG assets currently. No raster images.
- CSS: Single file, no network waterfall
- Mobile-optimised: fluid typography, responsive grid, no fixed-width elements

**Target performance:** Should load in under 2 seconds on a 3G connection.

---

## Browser Support

Targets modern browsers only:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Chrome Android 90+
- Safari iOS 14+

CSS Grid and Custom Properties are used throughout. No polyfills.

---

## Future Upgrade Path

### Short term (After owner confirms MVP is ready)
1. Add Google Analytics (or privacy-friendly alternative like Plausible/Fathom)
2. Replace placeholder SVG assets with official AIBS artwork
3. Update CNAME with confirmed domain

### Medium term (After 20-30 guides published)
1. Migrate to Astro.js for:
   - Markdown-based content management (no HTML editing for guides)
   - Shared layout components (no nav/footer duplication)
   - Built-in static generation
   - Better SEO handling
2. Add proper sitemap generation
3. Add PDF checklist downloads

### Long term (After 50 guides)
1. Add interactive tools (router self-assessment, café budget calculator)
2. Add Tok Pisin summaries if confirmed
3. Consider search with Pagefind or Algolia DocSearch

---

## Known Issues

1. The existing repo had an "AIBS Solution Kits" product (different project). Those files have been replaced by this build. The previous project content is no longer in the working tree.
2. The `CNAME` file contains `aibskits.com` which belongs to the previous project. **Must be updated with confirmed domain before deployment.**
3. SVG placeholders (PNG map and Bird of Paradise) are stylised approximations — replace with official artwork before launch.

---

## File Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Guide pages | `[descriptive-slug]-png.html` | `secure-wifi-router-png.html` |
| Category pages | `[category-slug].html` | `home-internet-safety.html` |
| Utility pages | `[page-name].html` | `contact.html`, `about.html` |
| CSS | `styles.css` | — |
| JS | `site.js` | — |
| SVG assets | Descriptive name | `png-map.svg` |
