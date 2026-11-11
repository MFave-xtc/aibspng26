from datetime import datetime, date

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

COMPANY_TYPES = ["Government", "Commercial", "Residential"]
DEAL_STAGES = ["Lead", "Contacted", "Quoted", "Negotiation", "Won", "Lost"]
OPEN_DEAL_STAGES = ["Lead", "Contacted", "Quoted", "Negotiation"]
QUOTE_STATUSES = ["Draft", "Sent", "Accepted", "Declined"]
INVOICE_STATUSES = ["Unpaid", "Partial", "Paid"]
TASK_STATUSES = ["Open", "Done"]
USER_ROLES = ["admin", "staff"]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="staff")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), default="Commercial")
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    address = db.Column(db.String(300))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    contacts = db.relationship("Contact", backref="company", lazy=True)
    deals = db.relationship("Deal", backref="company", lazy=True)
    quotes = db.relationship("Quote", backref="company", lazy=True)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    deals = db.relationship("Deal", backref="contact", lazy=True)
    quotes = db.relationship("Quote", backref="contact", lazy=True)
    tasks = db.relationship("Task", backref="contact", lazy=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    stage = db.Column(db.String(30), nullable=False, default="Lead")
    value = db.Column(db.Float, default=0)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assigned_to = db.relationship("User")
    quotes = db.relationship("Quote", backref="deal", lazy=True)
    tasks = db.relationship("Task", backref="deal", lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    sku = db.Column(db.String(100))
    unit_price = db.Column(db.Float, default=0)
    stock_qty = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)

    @property
    def is_low_stock(self):
        return (self.stock_qty or 0) <= (self.low_stock_threshold or 0)


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.String(30), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    deal_id = db.Column(db.Integer, db.ForeignKey("deal.id"))
    status = db.Column(db.String(20), default="Draft")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    line_items = db.relationship(
        "QuoteLineItem", backref="quote", cascade="all, delete-orphan", lazy=True
    )

    @property
    def total(self):
        return sum(li.line_total for li in self.line_items)


class QuoteLineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey("quote.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    description = db.Column(db.String(300), nullable=False)
    qty = db.Column(db.Float, default=1)
    unit_price = db.Column(db.Float, default=0)

    product = db.relationship("Product")

    @property
    def line_total(self):
        return (self.qty or 0) * (self.unit_price or 0)


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(30), unique=True, nullable=False)
    quote_id = db.Column(db.Integer, db.ForeignKey("quote.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    deal_id = db.Column(db.Integer, db.ForeignKey("deal.id"))
    status = db.Column(db.String(20), default="Unpaid")
    issued_date = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date)
    amount_paid = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    quote = db.relationship("Quote")
    company = db.relationship("Company")
    contact = db.relationship("Contact")
    deal = db.relationship("Deal")
    line_items = db.relationship(
        "InvoiceLineItem", backref="invoice", cascade="all, delete-orphan", lazy=True
    )

    @property
    def total(self):
        return sum(li.line_total for li in self.line_items)

    @property
    def balance_due(self):
        return self.total - (self.amount_paid or 0)

    @property
    def is_overdue(self):
        return self.status != "Paid" and self.due_date and self.due_date < date.today()


class InvoiceLineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoice.id"), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    qty = db.Column(db.Float, default=1)
    unit_price = db.Column(db.Float, default=0)

    @property
    def line_total(self):
        return (self.qty or 0) * (self.unit_price or 0)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default="Open")
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    deal_id = db.Column(db.Integer, db.ForeignKey("deal.id"))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assigned_to = db.relationship("User")
    company = db.relationship("Company")

    @property
    def is_overdue(self):
        return self.status == "Open" and self.due_date and self.due_date < date.today()
