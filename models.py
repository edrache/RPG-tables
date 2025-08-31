import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('table_id', db.Integer, db.ForeignKey('table.id'), primary_key=True)
)

custom_page_tables = db.Table('custom_page_tables',
    db.Column('custom_page_id', db.Integer, db.ForeignKey('custom_page.id'), primary_key=True),
    db.Column('table_id', db.Integer, db.ForeignKey('table.id'), primary_key=True)
)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    items = db.relationship('Item', backref='table', lazy=True, cascade="all, delete-orphan")
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('tables', lazy=True))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False, default=1)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class CustomPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    tables = db.relationship('Table', secondary=custom_page_tables, lazy='subquery',
        backref=db.backref('custom_pages', lazy=True))
