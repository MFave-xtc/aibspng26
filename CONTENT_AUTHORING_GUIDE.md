# CONTENT_AUTHORING_GUIDE.md

# AIBS Digital Setup Guides — Content Authoring Guide

**Version:** v1.0  
**For:** Anyone adding or editing guides on the AIBS Digital Setup Guides website  

---

## Adding a New Guide

### Step 1 — Create the Guide File

Copy the closest existing guide as a starting template:

```bash
cp guides/strong-passwords-png.html guides/your-new-guide-png.html
```

### Step 2 — Update the HTML Head

```html
<title>Your Guide Title | AIBS Digital Setup Guides</title>
<meta name="description" content="2-3 sentence description. Include key terms PNG users would search.">
<meta property="og:title" content="Your Guide Title | AIBS Digital Setup Guides">
<meta property="og:description" content="Same as meta description">
```

### Step 3 — Update the Breadcrumb

```html
<nav class="guide-breadcrumb">
  <a href="/">Home</a><span class="guide-breadcrumb-sep">›</span>
  <a href="/guides/index.html">Guides</a><span class="guide-breadcrumb-sep">›</span>
  <a href="/categories/your-category.html">Category Name</a><span class="guide-breadcrumb-sep">›</span>
  <span>Your Guide Title</span>
</nav>
```

### Step 4 — Update the Guide Metadata Strip

```html
<div class="guide-meta-strip">
  <div class="guide-meta-pill"><strong>Audience:</strong> Home users, parents</div>
  <div class="guide-meta-pill"><strong>Difficulty:</strong> <span class="difficulty-beginner">Beginner</span></div>
  <div class="guide-meta-pill"><strong>Time:</strong> 20 minutes</div>
  <div class="guide-meta-pill"><strong>Last reviewed:</strong> Month Year</div>
</div>
```

Difficulty options: `difficulty-beginner`, `difficulty-intermediate`, `difficulty-advanced`

### Step 5 — Update the Sidebar

Update the table of contents with anchor links matching your section IDs:

```html
<ul class="sidebar-toc">
  <li><a href="#quick-summary">Quick Summary</a></li>
  <li><a href="#before-you-start">Before You Start</a></li>
  <li><a href="#png-reality">PNG Reality Check</a></li>
  <li><a href="#safety-warning">Safety Warning</a></li>
  <li><a href="#steps">Step-by-Step Instructions</a></li>
  <li><a href="#settings">Recommended Settings</a></li>
  <li><a href="#what-to-buy">What to Buy</a></li>
  <li><a href="#mistakes">Common Mistakes</a></li>
  <li><a href="#troubleshooting">Troubleshooting</a></li>
  <li><a href="#technician">When to Call a Technician</a></li>
  <li><a href="#checklist">Printable Checklist</a></li>
</ul>
```

### Step 6 — Write Each Section

Use the section pattern:

```html
<div class="guide-section" id="quick-summary">
  <h2><span class="section-number">1</span> Quick Summary</h2>
  <p>3-5 sentences explaining what this guide helps the user do.</p>
</div>
```

### Step 7 — Add the PNG Reality Check

```html
<div class="guide-section" id="png-reality">
  <h2><span class="section-number">3</span> PNG Reality Check</h2>
  <div class="png-reality">
    <div class="png-reality-header">
      <h3>&#9670; Built for PNG conditions</h3>
    </div>
    <p>Explain the specific PNG context that makes this guide relevant or different from generic guides.</p>
    <ul>
      <li>PNG-specific point 1</li>
      <li>PNG-specific point 2</li>
    </ul>
  </div>
</div>
```

### Step 8 — Add Safety Warnings

```html
<div class="warning-box">
  <div class="warning-box-header">
    <h4>&#9888; Security Warning</h4>
  </div>
  <p>Your warning text here.</p>
</div>
```

### Step 9 — Write Steps

```html
<div class="step-block">
  <div class="step-number">Step 1</div>
  <h4>Action Name</h4>
  <p>Explain what to do.</p>
  <div class="step-what-to-look">
    <strong>What to look for:</strong> Simple description of the expected result.
  </div>
</div>
```

### Step 10 — Add Recommended Settings Table

```html
<table class="settings-table">
  <thead>
    <tr>
      <th>Setting</th>
      <th>Recommended Value</th>
      <th>Why</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Setting Name</strong></td>
      <td>Recommended Value</td>
      <td>Explanation</td>
    </tr>
  </tbody>
</table>
```

### Step 11 — Add Printable Checklist

```html
<div class="guide-section" id="checklist">
  <h2><span class="section-number">12</span> Printable Checklist</h2>
  <div class="checklist-block">
    <h3>&#10003; [Guide Title] Checklist</h3>
    <ul class="checklist-items">
      <li>Step 1 completed</li>
      <li>Step 2 completed</li>
      <li>Security setting checked</li>
      <li>Password recorded safely</li>
      <li>Final test completed</li>
    </ul>
  </div>
  <p style="margin-top:12px; font-size:13px; color:var(--muted);">
    <button data-print style="background:none; border:1px solid var(--border); color:var(--gold); padding:8px 16px; border-radius:6px; cursor:pointer; font-size:13px;">Print this checklist</button>
  </p>
</div>
```

### Step 12 — Add Source Register

```html
<div class="guide-section" id="sources">
  <h2><span class="section-number">13</span> Source Register</h2>
  <table class="register-table">
    <thead>
      <tr><th>ID</th><th>Source</th><th>Claim</th><th>Status</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>SRC-01</td>
        <td>Vendor documentation</td>
        <td>Specific claim</td>
        <td><span class="tag tag-confirmed">CONFIRMED</span></td>
      </tr>
      <tr>
        <td>SRC-02</td>
        <td>Field observation</td>
        <td>PNG-specific claim</td>
        <td><span class="tag tag-assumed">ASSUMED</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

### Step 13 — Add to Guides Listing

In `guides/index.html`, add a guide card:

```html
<a class="guide-card" href="/guides/your-guide-png.html"
   data-category="your-category"
   data-search="keywords for search">
  <div class="guide-card-top">
    <span class="guide-category-badge">Category Name</span>
  </div>
  <h3>Your Guide Title</h3>
  <p>One-sentence benefit description.</p>
  <div class="guide-card-meta">
    <span class="guide-meta-item difficulty-beginner">&#9679; Beginner</span>
    <span class="guide-meta-item">&#9200; 20 min</span>
    <span class="checklist-badge">&#10003; Checklist</span>
  </div>
</a>
```

### Step 14 — Add to Category Page

Open the relevant category page and add the same guide card to the guide grid.

### Step 15 — Run QA Checklist

Before considering the guide complete, check every item in `docs/QA_CHECKLIST.md`.

---

## Source Tagging Reference

Use these CSS classes in the source register:

| Class | Display | When to Use |
|---|---|---|
| `tag tag-confirmed` | CONFIRMED | Checked against official/vendor/standards source |
| `tag tag-supported` | SUPPORTED | Credible established public source |
| `tag tag-assumed` | ASSUMED | Reasonable assumption not presented as fact |
| `tag tag-unverified` | UNVERIFIED | Not yet checked |
| `tag tag-requires-confirmation` | REQUIRES CONFIRMATION | Must be confirmed by owner before publishing |

---

## Writing Style Guide

### Do Write Like This

> Before you change your router settings, take a photo of the current setup and write down the Wi-Fi name and password. This helps you recover quickly if something goes wrong.

### Do NOT Write Like This

> Leverage best-in-class cyber hygiene practices to optimise household digital resilience.

**Rules:**
- Write for someone who is not technical
- Use short sentences
- Use numbered lists for steps
- Start each step with a verb (Do this, Check this, Click this)
- Explain why, not just what
- Always include the PNG context (what is different or relevant in PNG)
- Never claim a specific product is "best" without evidence
- Never give prices without confirming they are current
- Always tag uncertain claims

---

## Publishing Checklist

Before a guide is published:

- [ ] Target user clearly stated
- [ ] Difficulty and time estimate included
- [ ] PNG reality check included
- [ ] Step-by-step instructions written
- [ ] Safety warning included (if relevant)
- [ ] Recommended settings table included (if relevant)
- [ ] What to buy/not buy included (if relevant)
- [ ] Troubleshooting section included
- [ ] When to call a technician section included
- [ ] Printable checklist included
- [ ] Source register completed
- [ ] Assumptions register completed
- [ ] No unsupported factual claims
- [ ] No placeholder text remaining
- [ ] Status badge updated (DRAFT → PUBLISHED)
- [ ] Last reviewed date updated
- [ ] Owner approval confirmed
- [ ] Tested on mobile

---

## Content Roadmap

See `docs/CONTENT_ROADMAP.md` for the full 50-guide publishing schedule.

Launch pack (12 guides) was published in Week 1.  
Target: 2 new guides per week after launch.
