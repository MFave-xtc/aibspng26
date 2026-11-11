# PISC CRM

An internal CRM for PNG IT & Security Consults Limited — contacts/companies,
sales pipeline, quotes, and tasks. Hosted locally on your office network;
not deployed publicly.

## What's included (v1)

- **Companies & Contacts** — customer/lead records
- **Deals pipeline** — Lead → Contacted → Quoted → Negotiation → Won/Lost
- **Quotes** — line-item quotes against a product catalog, with status tracking
- **Tasks** — follow-ups linked to companies/contacts/deals
- **Staff accounts** — multiple logins for your team, admin-managed

## Requirements

- Python 3.9+ (you already have this — it's what ran the website's local server)
- pip

## First-time setup

Open a terminal in this folder (`crm/`) and run:

```
pip install -r requirements.txt
python app.py
```

The first time it starts, visit `http://localhost:5050/` — you'll be asked to
create the first admin account. After that, everyone logs in with their own
username/password.

## Running it for your team (same network, like the website demo)

1. Find your computer's local IP (same as before): `ipconfig` on Windows,
   look for the IPv4 address (e.g. `10.20.31.80`).
2. Start the server: `python app.py`
3. Share the link: `http://<your-ip>:5050/` — your staff open that on their
   own device while on the same office network.
4. Leave the terminal window open; closing it stops the server.

Windows Firewall may ask to allow the connection the first time — allow it
on **Private networks**.

## Data

Everything is stored in a local file, `crm.db` (SQLite), created automatically
in this folder the first time you run the app. It is not committed to git
(see `.gitignore`) — it's your live data, specific to your machine.

**Back this file up** (copy `crm.db` somewhere safe) since it's the only copy
of your CRM data. There's no cloud backup built in — this is a local tool.

## Adding staff accounts

Log in as an admin, go to **Staff** in the sidebar, and create an account for
each team member with a temporary password. They should change it under
their account menu (top of the sidebar → their name → *Change password*)
after first login.

## Limitations (by design, for v1)

- Single SQLite file — fine for a small office team, not built for heavy
  concurrent write load.
- No email notifications, no file attachments on records yet.
- Deals board stage changes are click-based (no drag-and-drop yet).
- Runs on Flask's built-in dev server — fine for internal LAN use; not
  intended to be exposed to the public internet as-is.
