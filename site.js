/* ═══════════════════════════════════════════════════
   AIBS Digital Setup Guides — Shared JavaScript
   AI Digital Bridge Solutions PNG
   ═══════════════════════════════════════════════════ */

// ── NAVIGATION ────────────────────────────────────
function initNav() {
  const nav = document.getElementById('main-nav');
  const toggle = document.getElementById('nav-toggle');
  const mobile = document.getElementById('nav-mobile');

  // Scroll effect
  function onScroll() {
    if (nav) {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu toggle
  if (toggle && mobile) {
    toggle.addEventListener('click', () => {
      const isOpen = mobile.classList.toggle('open');
      toggle.classList.toggle('open', isOpen);
      toggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close on link click
    mobile.querySelectorAll('a, button').forEach(el => {
      el.addEventListener('click', () => {
        mobile.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Active nav link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link[href]').forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath !== '/' && currentPath !== '/index.html') {
      if (currentPath.startsWith(href) && href !== '/') {
        link.classList.add('active');
      }
    }
  });
}

// ── GUIDE SEARCH ──────────────────────────────────
function initGuideSearch() {
  const input = document.getElementById('guide-search');
  const cards = document.querySelectorAll('.guide-card[data-search]');
  if (!input || !cards.length) return;

  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();
    cards.forEach(card => {
      const text = (card.dataset.search || '').toLowerCase();
      card.style.display = (!q || text.includes(q)) ? '' : 'none';
    });
  });
}

// ── GUIDE FILTER ──────────────────────────────────
function initGuideFilter() {
  const buttons = document.querySelectorAll('[data-filter]');
  const cards = document.querySelectorAll('.guide-card[data-category]');
  if (!buttons.length || !cards.length) return;

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;
      cards.forEach(card => {
        const cat = (card.dataset.category || '').toLowerCase();
        card.style.display = (filter === 'all' || cat === filter) ? '' : 'none';
      });
    });
  });
}

// ── TABLE OF CONTENTS SCROLL SPY ──────────────────
function initTocSpy() {
  const tocLinks = document.querySelectorAll('.sidebar-toc a[href^="#"]');
  if (!tocLinks.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        tocLinks.forEach(link => {
          link.classList.toggle('active',
            link.getAttribute('href') === '#' + id);
        });
      }
    });
  }, { rootMargin: '-80px 0px -60% 0px', threshold: 0 });

  tocLinks.forEach(link => {
    const id = link.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) observer.observe(el);
  });
}

// ── PRINT CHECKLIST ───────────────────────────────
function initPrint() {
  document.querySelectorAll('[data-print]').forEach(btn => {
    btn.addEventListener('click', () => window.print());
  });
}

// ── CONTACT FORM ──────────────────────────────────
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', e => {
    e.preventDefault();
    const btn = form.querySelector('[type="submit"]');
    const successMsg = document.getElementById('form-success');

    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Sending...';
    }

    // mailto fallback — builds a mailto link from form data
    const name = form.querySelector('#name')?.value || '';
    const org = form.querySelector('#org')?.value || '';
    const province = form.querySelector('#province')?.value || '';
    const contact = form.querySelector('#contact')?.value || '';
    const need = form.querySelector('#need')?.value || '';
    const preferred = form.querySelector('#preferred')?.value || '';

    const body = [
      `Name: ${name}`,
      `Organisation: ${org}`,
      `Province / Location: ${province}`,
      `Phone or Email: ${contact}`,
      `How can we help: ${need}`,
      `Preferred contact: ${preferred}`
    ].join('\n');

    const subject = encodeURIComponent('AIBS Digital Setup Guides — Help Request');
    const bodyEnc = encodeURIComponent(body);
    const email = 'mariosu.fave@gmail.com';

    window.location.href = `mailto:${email}?subject=${subject}&body=${bodyEnc}`;

    setTimeout(() => {
      if (successMsg) successMsg.style.display = 'block';
      form.reset();
      if (btn) {
        btn.disabled = false;
        btn.textContent = 'Send Request';
      }
    }, 500);
  });
}

// ── SMOOTH SCROLL FOR TOC LINKS ───────────────────
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        const offset = 84;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });
}

// ── INIT ON DOM READY ─────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initGuideSearch();
  initGuideFilter();
  initTocSpy();
  initPrint();
  initContactForm();
  initSmoothScroll();
});
