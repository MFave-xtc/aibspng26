import os
import secrets
from datetime import datetime, date
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from sqlalchemy import inspect, text

from models import (
    db, User, Company, Contact, Deal, Product, Quote, QuoteLineItem, Task,
    Invoice, InvoiceLineItem,
    COMPANY_TYPES, DEAL_STAGES, OPEN_DEAL_STAGES, QUOTE_STATUSES, USER_ROLES,
    INVOICE_STATUSES,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "crm.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

secret_path = os.path.join(BASE_DIR, ".secret_key")
if os.environ.get("CRM_SECRET_KEY"):
    app.secret_key = os.environ["CRM_SECRET_KEY"]
else:
    if not os.path.exists(secret_path):
        with open(secret_path, "w") as f:
            f.write(secrets.token_hex(32))
    with open(secret_path, "r") as f:
        app.secret_key = f.read().strip()

db.init_app(app)


def _ensure_columns():
    """Add any new columns to existing tables (lightweight substitute for a
    full migration tool — new tables are handled by db.create_all())."""
    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())
    added_columns = {
        "product": [
            ("stock_qty", "INTEGER DEFAULT 0"),
            ("low_stock_threshold", "INTEGER DEFAULT 0"),
        ],
    }
    for table, columns in added_columns.items():
        if table not in existing_tables:
            continue
        existing_cols = {c["name"] for c in inspector.get_columns(table)}
        for name, ddl in columns:
            if name not in existing_cols:
                db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))
    db.session.commit()


with app.app_context():
    db.create_all()
    _ensure_columns()


# ───────────────────────── auth helpers ─────────────────────────

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.path))
        if not g.user.is_admin:
            flash("Admin access required.", "error")
            return redirect(url_for("dashboard"))
        return view(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_globals():
    return {
        "current_user": g.get("user"),
        "COMPANY_TYPES": COMPANY_TYPES,
        "DEAL_STAGES": DEAL_STAGES,
        "QUOTE_STATUSES": QUOTE_STATUSES,
        "USER_ROLES": USER_ROLES,
        "INVOICE_STATUSES": INVOICE_STATUSES,
    }


def next_quote_number():
    year = datetime.utcnow().year
    count = Quote.query.filter(Quote.quote_number.like(f"Q{year}-%")).count() + 1
    return f"Q{year}-{count:04d}"


def next_invoice_number():
    year = datetime.utcnow().year
    count = Invoice.query.filter(Invoice.invoice_number.like(f"INV{year}-%")).count() + 1
    return f"INV{year}-{count:04d}"


# ───────────────────────── setup / auth routes ─────────────────────────

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if User.query.count() > 0:
        return redirect(url_for("login"))
    if request.method == "POST":
        username = request.form["username"].strip()
        full_name = request.form["full_name"].strip()
        password = request.form["password"]
        confirm = request.form["confirm"]
        if not username or not full_name or not password:
            flash("All fields are required.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
        else:
            user = User(username=username, full_name=full_name, role="admin")
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            flash("Admin account created.", "success")
            return redirect(url_for("dashboard"))
    return render_template("setup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if User.query.count() == 0:
        return redirect(url_for("setup"))
    if g.user:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.is_active and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            flash(f"Welcome back, {user.full_name}.", "success")
            return redirect(request.args.get("next") or url_for("dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/account/password", methods=["GET", "POST"])
@login_required
def account_password():
    if request.method == "POST":
        current = request.form["current_password"]
        new = request.form["new_password"]
        confirm = request.form["confirm"]
        if not g.user.check_password(current):
            flash("Current password is incorrect.", "error")
        elif new != confirm:
            flash("New passwords do not match.", "error")
        elif len(new) < 6:
            flash("Password must be at least 6 characters.", "error")
        else:
            g.user.set_password(new)
            db.session.commit()
            flash("Password updated.", "success")
            return redirect(url_for("dashboard"))
    return render_template("account_password.html")


# ───────────────────────── dashboard ─────────────────────────

@app.route("/")
@login_required
def root():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    stage_counts = {s: 0 for s in DEAL_STAGES}
    stage_values = {s: 0 for s in DEAL_STAGES}
    for d in Deal.query.all():
        stage_counts[d.stage] = stage_counts.get(d.stage, 0) + 1
        stage_values[d.stage] = stage_values.get(d.stage, 0) + (d.value or 0)
    open_value = sum(stage_values.get(s, 0) for s in OPEN_DEAL_STAGES)
    open_tasks = (
        Task.query.filter_by(status="Open")
        .order_by(Task.due_date.is_(None), Task.due_date.asc())
        .limit(8)
        .all()
    )
    recent_quotes = Quote.query.order_by(Quote.created_at.desc()).limit(6).all()
    recent_companies = Company.query.order_by(Company.created_at.desc()).limit(5).all()
    low_stock_products = [p for p in Product.query.all() if p.is_low_stock]
    outstanding_total = sum(
        inv.balance_due for inv in Invoice.query.filter(Invoice.status != "Paid").all()
    )
    return render_template(
        "dashboard.html",
        stage_counts=stage_counts,
        stage_values=stage_values,
        open_value=open_value,
        open_tasks=open_tasks,
        recent_quotes=recent_quotes,
        recent_companies=recent_companies,
        today=date.today(),
        total_companies=Company.query.count(),
        total_contacts=Contact.query.count(),
        low_stock_products=low_stock_products,
        outstanding_total=outstanding_total,
    )


# ───────────────────────── companies ─────────────────────────

@app.route("/companies")
@login_required
def companies_list():
    q = request.args.get("q", "").strip()
    query = Company.query
    if q:
        query = query.filter(Company.name.ilike(f"%{q}%"))
    companies = query.order_by(Company.name.asc()).all()
    return render_template("companies_list.html", companies=companies, q=q)


@app.route("/companies/new", methods=["GET", "POST"])
@login_required
def company_new():
    if request.method == "POST":
        c = Company(
            name=request.form["name"].strip(),
            type=request.form.get("type", "Commercial"),
            phone=request.form.get("phone", "").strip(),
            email=request.form.get("email", "").strip(),
            address=request.form.get("address", "").strip(),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(c)
        db.session.commit()
        flash("Company added.", "success")
        return redirect(url_for("company_view", company_id=c.id))
    return render_template("company_form.html", company=None)


@app.route("/companies/<int:company_id>")
@login_required
def company_view(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template("company_view.html", company=company)


@app.route("/companies/<int:company_id>/edit", methods=["GET", "POST"])
@login_required
def company_edit(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == "POST":
        company.name = request.form["name"].strip()
        company.type = request.form.get("type", "Commercial")
        company.phone = request.form.get("phone", "").strip()
        company.email = request.form.get("email", "").strip()
        company.address = request.form.get("address", "").strip()
        company.notes = request.form.get("notes", "").strip()
        db.session.commit()
        flash("Company updated.", "success")
        return redirect(url_for("company_view", company_id=company.id))
    return render_template("company_form.html", company=company)


@app.route("/companies/<int:company_id>/delete", methods=["POST"])
@login_required
def company_delete(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash("Company deleted.", "success")
    return redirect(url_for("companies_list"))


# ───────────────────────── contacts ─────────────────────────

@app.route("/contacts")
@login_required
def contacts_list():
    q = request.args.get("q", "").strip()
    query = Contact.query
    if q:
        query = query.filter(
            (Contact.first_name.ilike(f"%{q}%")) | (Contact.last_name.ilike(f"%{q}%"))
        )
    contacts = query.order_by(Contact.first_name.asc()).all()
    return render_template("contacts_list.html", contacts=contacts, q=q)


@app.route("/contacts/new", methods=["GET", "POST"])
@login_required
def contact_new():
    companies = Company.query.order_by(Company.name.asc()).all()
    if request.method == "POST":
        contact = Contact(
            first_name=request.form["first_name"].strip(),
            last_name=request.form.get("last_name", "").strip(),
            title=request.form.get("title", "").strip(),
            phone=request.form.get("phone", "").strip(),
            email=request.form.get("email", "").strip(),
            company_id=request.form.get("company_id") or None,
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(contact)
        db.session.commit()
        flash("Contact added.", "success")
        return redirect(url_for("contact_view", contact_id=contact.id))
    return render_template("contact_form.html", contact=None, companies=companies)


@app.route("/contacts/<int:contact_id>")
@login_required
def contact_view(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template("contact_view.html", contact=contact)


@app.route("/contacts/<int:contact_id>/edit", methods=["GET", "POST"])
@login_required
def contact_edit(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    companies = Company.query.order_by(Company.name.asc()).all()
    if request.method == "POST":
        contact.first_name = request.form["first_name"].strip()
        contact.last_name = request.form.get("last_name", "").strip()
        contact.title = request.form.get("title", "").strip()
        contact.phone = request.form.get("phone", "").strip()
        contact.email = request.form.get("email", "").strip()
        contact.company_id = request.form.get("company_id") or None
        contact.notes = request.form.get("notes", "").strip()
        db.session.commit()
        flash("Contact updated.", "success")
        return redirect(url_for("contact_view", contact_id=contact.id))
    return render_template("contact_form.html", contact=contact, companies=companies)


@app.route("/contacts/<int:contact_id>/delete", methods=["POST"])
@login_required
def contact_delete(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted.", "success")
    return redirect(url_for("contacts_list"))


# ───────────────────────── deals ─────────────────────────

@app.route("/deals")
@login_required
def deals_board():
    deals_by_stage = {s: [] for s in DEAL_STAGES}
    for d in Deal.query.order_by(Deal.updated_at.desc()).all():
        deals_by_stage.setdefault(d.stage, []).append(d)
    return render_template("deals_board.html", deals_by_stage=deals_by_stage)


@app.route("/deals/new", methods=["GET", "POST"])
@login_required
def deal_new():
    companies = Company.query.order_by(Company.name.asc()).all()
    contacts = Contact.query.order_by(Contact.first_name.asc()).all()
    users = User.query.filter_by(is_active=True).order_by(User.full_name.asc()).all()
    if request.method == "POST":
        deal = Deal(
            title=request.form["title"].strip(),
            company_id=request.form.get("company_id") or None,
            contact_id=request.form.get("contact_id") or None,
            stage=request.form.get("stage", "Lead"),
            value=float(request.form.get("value") or 0),
            assigned_to_id=request.form.get("assigned_to_id") or None,
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(deal)
        db.session.commit()
        flash("Deal added.", "success")
        return redirect(url_for("deal_view", deal_id=deal.id))
    return render_template(
        "deal_form.html", deal=None, companies=companies, contacts=contacts, users=users
    )


@app.route("/deals/<int:deal_id>")
@login_required
def deal_view(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    return render_template("deal_view.html", deal=deal)


@app.route("/deals/<int:deal_id>/edit", methods=["GET", "POST"])
@login_required
def deal_edit(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    companies = Company.query.order_by(Company.name.asc()).all()
    contacts = Contact.query.order_by(Contact.first_name.asc()).all()
    users = User.query.filter_by(is_active=True).order_by(User.full_name.asc()).all()
    if request.method == "POST":
        deal.title = request.form["title"].strip()
        deal.company_id = request.form.get("company_id") or None
        deal.contact_id = request.form.get("contact_id") or None
        deal.stage = request.form.get("stage", "Lead")
        deal.value = float(request.form.get("value") or 0)
        deal.assigned_to_id = request.form.get("assigned_to_id") or None
        deal.notes = request.form.get("notes", "").strip()
        db.session.commit()
        flash("Deal updated.", "success")
        return redirect(url_for("deal_view", deal_id=deal.id))
    return render_template(
        "deal_form.html", deal=deal, companies=companies, contacts=contacts, users=users
    )


@app.route("/deals/<int:deal_id>/stage", methods=["POST"])
@login_required
def deal_stage_update(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    stage = request.form.get("stage")
    if stage in DEAL_STAGES:
        deal.stage = stage
        db.session.commit()
        flash("Stage updated.", "success")
    return redirect(request.referrer or url_for("deals_board"))


@app.route("/deals/<int:deal_id>/delete", methods=["POST"])
@login_required
def deal_delete(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    db.session.delete(deal)
    db.session.commit()
    flash("Deal deleted.", "success")
    return redirect(url_for("deals_board"))


# ───────────────────────── quotes ─────────────────────────

@app.route("/quotes")
@login_required
def quotes_list():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return render_template("quotes_list.html", quotes=quotes)


@app.route("/quotes/new", methods=["GET", "POST"])
@login_required
def quote_new():
    companies = Company.query.order_by(Company.name.asc()).all()
    contacts = Contact.query.order_by(Contact.first_name.asc()).all()
    deals = Deal.query.order_by(Deal.title.asc()).all()
    products = Product.query.order_by(Product.name.asc()).all()
    if request.method == "POST":
        quote = Quote(
            quote_number=next_quote_number(),
            company_id=request.form.get("company_id") or None,
            contact_id=request.form.get("contact_id") or None,
            deal_id=request.form.get("deal_id") or None,
            status="Draft",
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(quote)
        _apply_line_items(quote, request.form)
        db.session.commit()
        flash(f"Quote {quote.quote_number} created.", "success")
        return redirect(url_for("quote_view", quote_id=quote.id))
    return render_template(
        "quote_form.html", quote=None, companies=companies, contacts=contacts,
        deals=deals, products=products,
    )


def _apply_line_items(quote, form):
    quote.line_items.clear()
    descriptions = form.getlist("line_description[]")
    product_ids = form.getlist("line_product_id[]")
    qtys = form.getlist("line_qty[]")
    prices = form.getlist("line_price[]")
    for desc, pid, qty, price in zip(descriptions, product_ids, qtys, prices):
        if not desc.strip():
            continue
        quote.line_items.append(
            QuoteLineItem(
                description=desc.strip(),
                product_id=pid or None,
                qty=float(qty or 0),
                unit_price=float(price or 0),
            )
        )


@app.route("/quotes/<int:quote_id>")
@login_required
def quote_view(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return render_template("quote_view.html", quote=quote)


@app.route("/quotes/<int:quote_id>/edit", methods=["GET", "POST"])
@login_required
def quote_edit(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    companies = Company.query.order_by(Company.name.asc()).all()
    contacts = Contact.query.order_by(Contact.first_name.asc()).all()
    deals = Deal.query.order_by(Deal.title.asc()).all()
    products = Product.query.order_by(Product.name.asc()).all()
    if request.method == "POST":
        quote.company_id = request.form.get("company_id") or None
        quote.contact_id = request.form.get("contact_id") or None
        quote.deal_id = request.form.get("deal_id") or None
        quote.notes = request.form.get("notes", "").strip()
        _apply_line_items(quote, request.form)
        db.session.commit()
        flash("Quote updated.", "success")
        return redirect(url_for("quote_view", quote_id=quote.id))
    return render_template(
        "quote_form.html", quote=quote, companies=companies, contacts=contacts,
        deals=deals, products=products,
    )


@app.route("/quotes/<int:quote_id>/status", methods=["POST"])
@login_required
def quote_status_update(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    status = request.form.get("status")
    if status in QUOTE_STATUSES:
        quote.status = status
        db.session.commit()
        flash("Quote status updated.", "success")
    return redirect(url_for("quote_view", quote_id=quote.id))


@app.route("/quotes/<int:quote_id>/delete", methods=["POST"])
@login_required
def quote_delete(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    flash("Quote deleted.", "success")
    return redirect(url_for("quotes_list"))


@app.route("/quotes/<int:quote_id>/convert", methods=["POST"])
@login_required
def quote_to_invoice(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    invoice = Invoice(
        invoice_number=next_invoice_number(),
        quote_id=quote.id,
        company_id=quote.company_id,
        contact_id=quote.contact_id,
        deal_id=quote.deal_id,
        status="Unpaid",
    )
    for li in quote.line_items:
        invoice.line_items.append(
            InvoiceLineItem(description=li.description, qty=li.qty, unit_price=li.unit_price)
        )
    db.session.add(invoice)
    db.session.commit()
    flash(f"Invoice {invoice.invoice_number} created from this quote.", "success")
    return redirect(url_for("invoice_edit", invoice_id=invoice.id))


# ───────────────────────── invoices ─────────────────────────

@app.route("/invoices")
@login_required
def invoices_list():
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return render_template("invoices_list.html", invoices=invoices)


@app.route("/invoices/<int:invoice_id>")
@login_required
def invoice_view(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template("invoice_view.html", invoice=invoice)


@app.route("/invoices/<int:invoice_id>/edit", methods=["GET", "POST"])
@login_required
def invoice_edit(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    if request.method == "POST":
        due = request.form.get("due_date") or None
        invoice.due_date = date.fromisoformat(due) if due else None
        invoice.amount_paid = float(request.form.get("amount_paid") or 0)
        invoice.notes = request.form.get("notes", "").strip()
        db.session.commit()
        flash("Invoice updated.", "success")
        return redirect(url_for("invoice_view", invoice_id=invoice.id))
    return render_template("invoice_form.html", invoice=invoice)


@app.route("/invoices/<int:invoice_id>/status", methods=["POST"])
@login_required
def invoice_status_update(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    status = request.form.get("status")
    if status in INVOICE_STATUSES:
        invoice.status = status
        db.session.commit()
        flash("Invoice status updated.", "success")
    return redirect(url_for("invoice_view", invoice_id=invoice.id))


@app.route("/invoices/<int:invoice_id>/delete", methods=["POST"])
@login_required
def invoice_delete(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    flash("Invoice deleted.", "success")
    return redirect(url_for("invoices_list"))


# ───────────────────────── tasks ─────────────────────────

@app.route("/tasks")
@login_required
def tasks_list():
    show = request.args.get("show", "open")
    query = Task.query
    if show == "open":
        query = query.filter_by(status="Open")
    elif show == "mine":
        query = query.filter_by(assigned_to_id=g.user.id, status="Open")
    tasks = query.order_by(Task.due_date.is_(None), Task.due_date.asc()).all()
    return render_template("tasks_list.html", tasks=tasks, show=show, today=date.today())


@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def task_new():
    companies = Company.query.order_by(Company.name.asc()).all()
    contacts = Contact.query.order_by(Contact.first_name.asc()).all()
    deals = Deal.query.order_by(Deal.title.asc()).all()
    users = User.query.filter_by(is_active=True).order_by(User.full_name.asc()).all()
    if request.method == "POST":
        due = request.form.get("due_date") or None
        task = Task(
            title=request.form["title"].strip(),
            due_date=date.fromisoformat(due) if due else None,
            assigned_to_id=request.form.get("assigned_to_id") or g.user.id,
            company_id=request.form.get("company_id") or None,
            contact_id=request.form.get("contact_id") or None,
            deal_id=request.form.get("deal_id") or None,
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(task)
        db.session.commit()
        flash("Task added.", "success")
        return redirect(url_for("tasks_list"))
    return render_template(
        "task_form.html", task=None, companies=companies, contacts=contacts,
        deals=deals, users=users,
    )


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
@login_required
def task_toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = "Done" if task.status == "Open" else "Open"
    db.session.commit()
    return redirect(request.referrer or url_for("tasks_list"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def task_delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("tasks_list"))


# ───────────────────────── products ─────────────────────────

@app.route("/products")
@login_required
def products_list():
    products = Product.query.order_by(Product.name.asc()).all()
    return render_template("products_list.html", products=products)


@app.route("/products/new", methods=["GET", "POST"])
@login_required
def product_new():
    if request.method == "POST":
        p = Product(
            name=request.form["name"].strip(),
            brand=request.form.get("brand", "").strip(),
            sku=request.form.get("sku", "").strip(),
            unit_price=float(request.form.get("unit_price") or 0),
            stock_qty=int(request.form.get("stock_qty") or 0),
            low_stock_threshold=int(request.form.get("low_stock_threshold") or 0),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(p)
        db.session.commit()
        flash("Product added.", "success")
        return redirect(url_for("products_list"))
    return render_template("product_form.html", product=None)


@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        product.name = request.form["name"].strip()
        product.brand = request.form.get("brand", "").strip()
        product.sku = request.form.get("sku", "").strip()
        product.unit_price = float(request.form.get("unit_price") or 0)
        product.stock_qty = int(request.form.get("stock_qty") or 0)
        product.low_stock_threshold = int(request.form.get("low_stock_threshold") or 0)
        product.notes = request.form.get("notes", "").strip()
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("products_list"))
    return render_template("product_form.html", product=product)


@app.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("products_list"))


# ───────────────────────── users (admin) ─────────────────────────

@app.route("/users")
@admin_required
def users_list():
    users = User.query.order_by(User.full_name.asc()).all()
    return render_template("users_list.html", users=users)


@app.route("/users/new", methods=["GET", "POST"])
@admin_required
def user_new():
    if request.method == "POST":
        username = request.form["username"].strip()
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "error")
            return render_template("user_form.html")
        user = User(
            username=username,
            full_name=request.form["full_name"].strip(),
            role=request.form.get("role", "staff"),
        )
        user.set_password(request.form["password"])
        db.session.add(user)
        db.session.commit()
        flash("Staff account created.", "success")
        return redirect(url_for("users_list"))
    return render_template("user_form.html")


@app.route("/users/<int:user_id>/toggle", methods=["POST"])
@admin_required
def user_toggle(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == g.user.id:
        flash("You cannot deactivate your own account.", "error")
    else:
        user.is_active = not user.is_active
        db.session.commit()
        flash("Account updated.", "success")
    return redirect(url_for("users_list"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
