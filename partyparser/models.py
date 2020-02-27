from partyparser import db


class CourtCase(db.Model):
    __tablename__ = 'courtcase'

    def __getitem__(self, field):
        return self.__dict__[field]

    id = db.Column(db.Integer, primary_key=True)
    plaintiff = db.Column(db.Text, nullable=False)
    defendant = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<{} id: {} Plaintiffs: {}, Defendants: {}>'.format(
            self.__tablename__, self.id, self.plaintiff, self.defendant)
