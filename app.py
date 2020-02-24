from partyparser import create_app, db
from partyparser.models import CourtCase

app = create_app()

from partyparser import routes


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'CourtCase': CourtCase}
