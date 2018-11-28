from project import db


class Company(db.Model):
    NAME_MAX_LENGTH = 128
    IDENTIFIER_MAX_LENGTH = 128

    __tablename__ = 'companies'
    __table_args__ = {'schema': 'companies'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identifier = db.Column(db.String(IDENTIFIER_MAX_LENGTH), nullable=False)
    name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    users = db.relationship("UserCompanies", backref='company')


class UserCompanies(db.Model):
    __tablename__ = 'user_companies'
    __table_args__ = {'schema': 'companies'}

    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(Company.id),
        primary_key=True,
        nullable=False)
