import datetime

from sqlalchemy.sql import func
from project import db


class Classification(db.Model):
    NAME_MAX_LENGTH = 128

    __tablename__ = 'classification'
    __table_args__ = {'schema': 'companies'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False)
    companies = db.relationship('Company', back_populates='classification')


class Company(db.Model):
    NAME_MAX_LENGTH = 128
    IDENTIFIER_MAX_LENGTH = 128

    __tablename__ = 'companies'
    __table_args__ = {'schema': 'companies'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identifier = db.Column(db.String(IDENTIFIER_MAX_LENGTH), nullable=False)
    name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    classification_id = db.Column(
        db.Integer, db.ForeignKey(Classification.id), nullable=False)
    classification = db.relationship(
        'Classification', back_populates='companies')
    expiration = db.Column(db.DateTime, nullable=True)
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, default=0, nullable=False)
    updated = db.Column(db.DateTime, onupdate=func.now(), nullable=True)
    updated_by = db.Column(db.Integer)
    users = db.relationship("UserCompanies", backref='company')

    @property
    def status(self):
        if self.active is False:
            return False

        if self.expiration is None:
            return self.active

        return datetime.datetime.now() < self.expiration


class UserCompanies(db.Model):
    __tablename__ = 'user_companies'
    __table_args__ = {'schema': 'companies'}

    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(Company.id),
        primary_key=True,
        nullable=False)
