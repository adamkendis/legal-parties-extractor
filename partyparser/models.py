from partyparser import db


class CourtCase(db.Model):
    __tablename__ = 'courtcase'
    id = db.Column(db.Integer, primary_key=True)
    plaintiff = db.Column(db.Text, nullable=False)
    defendant = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<{} Plaintiff(s): {}, Defendant(s): {}>'.format(
            self.__tablename__, self.plaintiff, self.defendant)


# class BaseParty(db.Model):
#     __abstract__ = True
#     courtcase_id = db.Column(db.Integer, db.ForeignKey('courtcase.id'))
#     name = db.Column(db.Text, nullable=False)

#     def __repr__(self, tablename):
        # return '<{} {}, id: {}>'.format(
        #     self.__tablename__, self.name, self.id)


# class Plaintiff(BaseParty):
#     __tablename__ = 'plaintiff'
#     id = db.Column(db.Integer, primary_key=True)


# class Defendant(BaseParty):
#     __tablename__ = 'defendant'
#     id = db.Column(db.Integer, primary_key=True)
