/* ═══════════════════════════════════════════════════
   AIBS Solution Kits — Global Stylesheet
   AI Bridge Solutions PNG
   ═══════════════════════════════════════════════════ */

:root {
  --red: #C41E3A;
  --red-dark: #9A1830;
  --red-light: #E8354F;
  --gold: #D4A843;
  --gold-light: #E8C876;
  --gold-dark: #B08A2E;
  --black: #0D0D0D;
  --dark: #1A1A1A;
  --med-gray: #2D2D2D;
  --text: #1A1A1A;
  --text-muted: #6B6B6B;
  --text-light: #999999;
  --off-white: #FAFAF8;
  --light-gray: #F5F5F5;
  --border: #E5E5E3;
  --card-bg: #FFFFFF;
  --hero-bg: #0D0D0D;
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --max-w: 1200px;
  --max-w-narrow: 900px;
  --radius: 16px;
  --radius-sm: 10px;
  --radius-xs: 8px;
  --shadow: 0 4px 24px rgba(0,0,0,0.06);
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.10);
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

body {
  font-family: var(--font-body);
  color: var(--text);
  background: var(--off-white);
  line-height: 1.6;
  overflow-x: hidden;
}

a { color: inherit; text-decoration: none; }
img { max-width: 100%; height: auto; display: block; }

/* ── ANIMATIONS ────────────────────────────── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes shimmer {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(196,30,58,0.15); }
  50% { box-shadow: 0 0 40px rgba(196,30,58,0.3); }
}
@keyframes grain {
  0%, 100% { transform: translate(0,0); }
  10% { transform: translate(-5%,-10%); }
  30% { transform: translate(3%,-15%); }
  50% { transform: translate(12%,9%); }
  70% { transform: translate(9%,4%); }
  90% { transform: translate(-1%,7%); }
}

.fade-up { animation: fadeUp 0.7s ease forwards; }
.fade-up-d1 { animation: fadeUp 0.7s ease 0.1s forwards; opacity: 0; }
.fade-up-d2 { animation: fadeUp 0.7s ease 0.2s forwards; opacity: 0; }
.fade-up-d3 { animation: fadeUp 0.7s ease 0.3s forwards; opacity: 0; }
.fade-up-d4 { animation: fadeUp 0.7s ease 0.4s forwards; opacity: 0; }

/* ── NAVIGATION ────────────────────────────── */
.nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  padding: 0 24px;
  transition: var(--transition);
}
.nav.scrolled {
  background: rgba(13,13,13,0.97);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--med-gray);
}
.nav-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
}
.nav-logo {
  display: flex; align-items: center; gap: 12;
  cursor: pointer; text-decoration: none;
}
.nav-logo-icon {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, var(--red), var(--gold));
  border-radius: var(--radius-xs);
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 16px; color: #fff;
  transition: transform var(--transition);
}
.nav-logo:hover .nav-logo-icon { transform: rotate(-5deg) scale(1.05); }
.nav-logo-text { color: #fff; font-weight: 700; font-size: 17px; letter-spacing: 1px; }
.nav-logo-sub { color: var(--gold); font-weight: 400; font-size: 13px; margin-left: 6px; }

.nav-links { display: flex; gap: 32; align-items: center; }
.nav-link {
  color: rgba(255,255,255,0.8); font-size: 14px; font-weight: 500;
  letter-spacing: 0.5px; transition: color var(--transition);
  cursor: pointer; background: none; border: none; font-family: inherit;
}
.nav-link:hover, .nav-link.active { color: var(--gold); }
.nav-cta {
  background: linear-gradient(135deg, var(--red), var(--red-dark));
  color: #fff; border: none; padding: 10px 24px;
  border-radius: var(--radius-xs); font-size: 13px; font-weight: 600;
  cursor: pointer; letter-spacing: 0.5px; transition: all var(--transition);
  font-family: inherit;
}
.nav-cta:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(196,30,58,0.3); }

/* Mobile nav */
.nav-toggle { display: none; background: none; border: none; cursor: pointer; padding: 8px; }
.nav-toggle span {
  display: block; width: 24px; height: 2px; background: #fff;
  margin: 5px 0; transition: var(--transition);
}
.nav-toggle.open span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.nav-toggle.open span:nth-child(2) { opacity: 0; }
.nav-toggle.open span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

.nav-mobile {
  display: none; position: fixed; top: 72px; left: 0; right: 0; bottom: 0;
  background: rgba(13,13,13,0.98); backdrop-filter: blur(20px);
  flex-direction: column; align-items: center; justify-content: center; gap: 32;
  z-index: 999;
}
.nav-mobile.open { display: flex; }
.nav-mobile .nav-link { font-size: 22px; }
.nav-mobile .nav-cta { font-size: 18px; padding: 14px 40px; }

/* ── HERO ──────────────────────────────────── */
.hero {
  background: var(--hero-bg);
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
  padding: 120px 24px 80px;
}
.hero::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.015'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  z-index: 0;
}
.hero-orb {
  position: absolute; border-radius: 50%; z-index: 0; pointer-events: none;
}
.hero-orb-1 {
  top: 8%; right: -5%; width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(196,30,58,0.08), transparent 70%);
}
.hero-orb-2 {
  bottom: 5%; left: -10%; width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(212,168,67,0.06), transparent 70%);
}
.hero-orb-3 {
  top: 40%; left: 30%; width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(196,30,58,0.04), transparent 70%);
}
.hero-content {
  max-width: 920px; text-align: center; position: relative; z-index: 1;
}
.hero-badge {
  display: inline-block; padding: 6px 20px; border-radius: 24px;
  border: 1px solid rgba(212,168,67,0.3); background: rgba(212,168,67,0.08);
  margin-bottom: 36px; font-size: 12px; color: var(--gold);
  font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
}
.hero h1 {
  font-family: var(--font-display);
  font-size: clamp(40px, 6.5vw, 76px);
  font-weight: 700; color: #fff;
  line-height: 1.05; margin: 0 0 28px; letter-spacing: -1px;
}
.hero h1 .gradient {
  background: linear-gradient(135deg, var(--red), var(--gold));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  font-size: 19px; color: var(--text-light); line-height: 1.7;
  max-width: 660px; margin: 0 auto 52px; font-weight: 400;
}
.hero-actions { display: flex; gap: 16; justify-content: center; flex-wrap: wrap; }

.btn-primary {
  background: linear-gradient(135deg, var(--red), var(--red-dark));
  color: #fff; border: none; padding: 16px 40px; border-radius: var(--radius-sm);
  font-size: 16px; font-weight: 600; cursor: pointer; letter-spacing: 0.3px;
  transition: all var(--transition); font-family: inherit; display: inline-block;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 32px rgba(196,30,58,0.35); }

.btn-outline {
  background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.25);
  padding: 16px 40px; border-radius: var(--radius-sm);
  font-size: 16px; font-weight: 500; cursor: pointer;
  transition: all var(--transition); font-family: inherit; display: inline-block;
}
.btn-outline:hover { border-color: var(--gold); color: var(--gold); }

.btn-red-outline {
  background: transparent; color: var(--red); border: 2px solid var(--red);
  padding: 14px 40px; border-radius: var(--radius-sm);
  font-size: 15px; font-weight: 600; cursor: pointer;
  transition: all var(--transition); font-family: inherit; display: inline-block;
}
.btn-red-outline:hover { background: var(--red); color: #fff; }

.btn-gold {
  background: linear-gradient(135deg, var(--gold), var(--gold-dark));
  color: #fff; border: none; padding: 14px 32px; border-radius: var(--radius-sm);
  font-size: 15px; font-weight: 600; cursor: pointer; font-family: inherit;
  transition: all var(--transition);
}
.btn-gold:hover { transform: translateY(-2px); box-shadow: 0 12px 32px rgba(212,168,67,0.3); }

.btn-dark {
  background: var(--light-gray); color: var(--text); border: none;
  padding: 14px 32px; border-radius: var(--radius-sm);
  font-size: 15px; font-weight: 600; cursor: pointer; font-family: inherit;
  width: 100%; transition: all var(--transition);
}
.btn-dark:hover { background: #eaeae8; }

.hero-stats {
  display: flex; gap: 56px; justify-content: center; margin-top: 72px; flex-wrap: wrap;
}
.hero-stat-num {
  font-family: var(--font-display);
  font-size: 38px; font-weight: 700; color: var(--gold);
}
.hero-stat-label {
  font-size: 13px; color: var(--text-light); margin-top: 4px;
  letter-spacing: 0.5px; text-transform: uppercase;
}

/* ── SECTIONS ──────────────────────────────── */
.section { padding: 100px 24px; }
.section-white { background: var(--card-bg); }
.section-off { background: var(--off-white); }
.section-dark { background: var(--hero-bg); }
.container { max-width: var(--max-w); margin: 0 auto; }
.container-narrow { max-width: var(--max-w-narrow); margin: 0 auto; }

.section-title {
  font-family: var(--font-display);
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 700; color: var(--text);
  margin: 0 0 16px; letter-spacing: -0.5px;
}
.section-title-light { color: #fff; }
.section-sub {
  font-size: 17px; color: var(--text-muted); max-width: 620px;
  margin: 0 auto 56px; line-height: 1.7;
}
.text-center { text-align: center; }

/* ── KIT CARDS ─────────────────────────────── */
.kit-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}
.kit-card {
  background: var(--card-bg); border-radius: var(--radius);
  padding: 36px; border: 1px solid var(--border);
  transition: all var(--transition); position: relative; overflow: hidden;
  cursor: pointer; text-decoration: none; display: block;
}
.kit-card::after {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0;
  height: 3px; background: linear-gradient(90deg, var(--red), var(--gold));
  transform: scaleX(0); transform-origin: left;
  transition: transform var(--transition);
}
.kit-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
  border-color: var(--red);
}
.kit-card:hover::after { transform: scaleX(1); }
.kit-card-header { display: flex; align-items: center; gap: 16; margin-bottom: 18; }
.kit-card-icon { font-size: 38px; line-height: 1; }
.kit-card-num { font-size: 11px; font-weight: 700; color: var(--red); letter-spacing: 2px; text-transform: uppercase; }
.kit-card h3 { font-size: 20px; font-weight: 700; color: var(--text); margin: 0 0 8px; line-height: 1.3; }
.kit-card p { font-size: 14px; color: var(--text-muted); line-height: 1.6; margin: 0 0 20px; }
.kit-card-link { font-size: 13px; color: var(--red); font-weight: 600; display: flex; align-items: center; gap: 6; }
.kit-card-link span { transition: transform var(--transition); }
.kit-card:hover .kit-card-link span { transform: translateX(4px); }

/* ── KIT DETAIL ────────────────────────────── */
.kit-detail-hero {
  display: flex; align-items: center; gap: 24;
  margin-bottom: 20;
}
.kit-detail-icon { font-size: 56px; line-height: 1; }
.kit-detail-num { font-size: 12px; font-weight: 700; color: var(--red); letter-spacing: 2px; }
.kit-detail-title {
  font-family: var(--font-display);
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 700; color: var(--text); margin: 6px 0 0;
}
.kit-detail-desc {
  font-size: 17px; color: var(--text-muted); line-height: 1.8;
  margin-bottom: 48;
}
.back-link {
  display: inline-flex; align-items: center; gap: 8;
  color: var(--red); font-size: 14px; font-weight: 600;
  margin-bottom: 36; cursor: pointer;
  background: none; border: none; font-family: inherit;
  transition: gap var(--transition);
}
.back-link:hover { gap: 12; }

/* ── TIER CARDS ────────────────────────────── */
.tier-card {
  background: var(--card-bg); border-radius: var(--radius);
  padding: 36px; border: 1px solid var(--border);
  margin-bottom: 24;
}
.tier-header {
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 16; margin-bottom: 24;
}
.tier-name { font-size: 12px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
.tier-name-starter { color: var(--text-muted); }
.tier-name-pro { color: var(--gold); }
.tier-name-gov { color: var(--red); }
.tier-price { font-family: var(--font-display); font-size: 32px; font-weight: 700; color: var(--text); margin-top: 4px; }
.tier-usd { font-size: 13px; color: var(--text-muted); }
.tier-includes { font-size: 13px; color: var(--text-muted); font-style: italic; margin-bottom: 16px; }
.tier-items {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 8px;
}
.tier-item {
  display: flex; gap: 10px; align-items: flex-start; padding: 8px 0;
}
.tier-item-check { color: var(--red); font-size: 14px; margin-top: 2px; flex-shrink: 0; }
.tier-item-text { font-size: 14px; color: var(--text); line-height: 1.5; }

/* ── PRICING PAGE ──────────────────────────── */
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px; margin-bottom: 48px;
}
.pricing-card {
  background: var(--card-bg); border-radius: 20px;
  padding: 44px; position: relative;
  border: 1px solid var(--border);
  transition: all var(--transition);
}
.pricing-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
.pricing-card.popular {
  border: 2px solid var(--gold);
  box-shadow: 0 20px 60px rgba(212,168,67,0.12);
}
.pricing-popular-badge {
  position: absolute; top: -13px; left: 50%; transform: translateX(-50%);
  background: linear-gradient(135deg, var(--gold), var(--gold-dark));
  color: #fff; padding: 5px 22px; border-radius: 20px;
  font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
}
.pricing-tier-name { font-size: 13px; font-weight: 700; letter-spacing: 2px; margin-bottom: 10px; text-transform: uppercase; }
.pricing-amount { font-family: var(--font-display); font-size: 46px; font-weight: 700; color: var(--text); margin-bottom: 4px; }
.pricing-usd { font-size: 14px; color: var(--text-muted); margin-bottom: 20px; }
.pricing-desc { font-size: 14px; color: var(--text-muted); line-height: 1.6; margin-bottom: 28px; }
.pricing-features { margin-bottom: 36px; }
.pricing-feature {
  display: flex; gap: 10px; padding: 7px 0; align-items: center;
}
.pricing-feature-check { color: var(--red); font-size: 13px; }
.pricing-feature-text { font-size: 14px; color: var(--text); }

/* Bundle */
.bundle-card {
  background: linear-gradient(135deg, var(--black), var(--med-gray));
  border-radius: 20px; padding: 56px;
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 32;
}
.bundle-label { font-size: 13px; font-weight: 700; color: var(--gold); letter-spacing: 2px; margin-bottom: 8px; }
.bundle-title { font-family: var(--font-display); font-size: 34px; font-weight: 700; color: #fff; margin: 0 0 10px; }
.bundle-desc { font-size: 16px; color: var(--text-light); }
.bundle-price { font-family: var(--font-display); font-size: 52px; font-weight: 700; color: var(--gold); text-align: center; }
.bundle-usd { font-size: 14px; color: var(--text-light); margin-bottom: 20px; text-align: center; }

/* Subscription */
.sub-card {
  background: var(--card-bg); border-radius: 20px; padding: 52px;
  margin-top: 24px; border: 1px solid var(--border); text-align: center;
}
.sub-title { font-family: var(--font-display); font-size: 26px; font-weight: 700; color: var(--text); margin: 0 0 12px; }
.sub-desc { font-size: 15px; color: var(--text-muted); max-width: 600px; margin: 0 auto 28px; }
.sub-prices { display: flex; justify-content: center; gap: 56px; flex-wrap: wrap; }
.sub-amount { font-family: var(--font-display); font-size: 30px; font-weight: 700; }
.sub-amount-label { font-size: 14px; font-weight: 400; color: var(--text-muted); }

/* ── BUYERS GRID ───────────────────────────── */
.buyers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}
.buyer-card {
  background: var(--light-gray); border-radius: var(--radius);
  padding: 32px; transition: all var(--transition);
}
.buyer-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.buyer-card-icon { font-size: 32px; margin-bottom: 14px; }
.buyer-card h4 { font-size: 16px; font-weight: 700; color: var(--text); margin: 0 0 6px; }
.buyer-card p { font-size: 13px; color: var(--text-muted); margin: 0; line-height: 1.5; }

/* ── ABOUT ─────────────────────────────────── */
.about-diff {
  background: linear-gradient(135deg, var(--black), var(--med-gray));
  border-radius: 20px; padding: 48px; margin-bottom: 36px;
}
.about-diff h3 { font-family: var(--font-display); font-size: 22px; font-weight: 700; color: var(--gold); margin: 0 0 24px; }
.about-diff-item { display: flex; gap: 14px; margin-bottom: 14px; align-items: flex-start; }
.about-diff-marker { color: var(--gold); font-size: 16px; margin-top: 3px; flex-shrink: 0; }
.about-diff-text { color: #fff; font-size: 15px; line-height: 1.6; }

.contact-card {
  background: var(--card-bg); border-radius: var(--radius);
  padding: 32px; border: 1px solid var(--border);
}
.contact-row { display: flex; gap: 14px; margin-bottom: 12px; }
.contact-label { font-size: 14px; font-weight: 600; color: var(--text); min-width: 80px; }
.contact-value { font-size: 14px; color: var(--text-muted); }

/* ── CONTACT PAGE ──────────────────────────── */
.contact-grid { display: grid; gap: 20px; }
.contact-method {
  background: var(--card-bg); border-radius: var(--radius); padding: 32px;
  border: 1px solid var(--border); display: flex; gap: 22px; align-items: flex-start;
  transition: all var(--transition);
}
.contact-method:hover { border-color: var(--red); box-shadow: var(--shadow); }
.contact-method-icon { font-size: 36px; flex-shrink: 0; }
.contact-method h3 { font-size: 17px; font-weight: 700; color: var(--text); margin: 0 0 4px; }
.contact-method-value { font-size: 15px; color: var(--red); font-weight: 600; margin-bottom: 4px; }
.contact-method-sub { font-size: 13px; color: var(--text-muted); }

/* ── FOOTER ────────────────────────────────── */
.footer {
  background: var(--black); padding: 72px 24px 36px;
  border-top: 1px solid var(--med-gray);
}
.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 48px; margin-bottom: 52px;
}
.footer-brand p { font-size: 13px; color: var(--text-light); line-height: 1.7; }
.footer-heading {
  color: var(--gold); font-size: 11px; font-weight: 700;
  letter-spacing: 2px; margin-bottom: 18px; text-transform: uppercase;
}
.footer-link {
  display: block; font-size: 13px; color: var(--text-light);
  margin-bottom: 10px; transition: color var(--transition);
  cursor: pointer;
}
.footer-link:hover { color: var(--gold); }
.footer-bottom {
  border-top: 1px solid var(--med-gray); padding-top: 28px;
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px;
}
.footer-copy { font-size: 12px; color: var(--text-light); }

/* ── RESPONSIVE ────────────────────────────── */
@media (max-width: 768px) {
  .nav-links { display: none; }
  .nav-toggle { display: block; }
  .hero-stats { gap: 32px; }
  .kit-grid { grid-template-columns: 1fr; }
  .pricing-grid { grid-template-columns: 1fr; }
  .bundle-card { padding: 36px; flex-direction: column; text-align: center; }
  .bundle-card > div:first-child { text-align: center; }
  .tier-header { flex-direction: column; align-items: flex-start; }
  .tier-items { grid-template-columns: 1fr; }
  .buyers-grid { grid-template-columns: 1fr; }
  .sub-prices { flex-direction: column; gap: 24px; }
  .hero h1 { font-size: clamp(32px, 8vw, 52px); }
  .footer-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 480px) {
  .footer-grid { grid-template-columns: 1fr; }
  .hero-actions { flex-direction: column; align-items: center; }
  .btn-primary, .btn-outline { width: 100%; text-align: center; }
}
