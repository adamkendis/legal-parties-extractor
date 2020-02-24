from partyparser import db


class CourtCase(db.Model):
    __tablename__ = 'courtcase'
    id = db.Column(db.Integer, primary_key=True)


class BaseParty(db.Model):
    __abstract__ = True
    courtcase_id = db.Column(
        db.Integer,
        db.ForeignKey('courtcase.id'),
        nullable=False
    )
    name = db.Column(db.Text, nullable=False)


class Plaintiff(BaseParty):
    __tablename__ = 'plaintiff'
    id = db.Column(db.Integer, primary_key=True)


class Defendant(BaseParty):
    __tablename__ = 'defendant'
    id = db.Column(db.Integer, primary_key=True)
