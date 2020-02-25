# Standard library imports
from flask import Blueprint, render_template, request

# Local app imports
from partyparser.models import CourtCase

home_bp = Blueprint('home_bp', __name__,
                    template_folder='templates')

web_bp = Blueprint('web_bp', __name__,
                   template_folder='templates')


@home_bp.route('/')
@home_bp.route('/index', methods=['GET'])
def index():
    title = 'XML Parser'
    return render_template('index.html', title=title)


@web_bp.route('/web/cases', methods=['GET', 'POST'])
def handle_cases():
    title = 'XML Parser'
    if request.method == 'GET':
        cases = CourtCase.query.all()
        return render_template('index.html', title=title, cases=cases)


@web_bp.route('/web/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    title = 'XML Parser'
    case = CourtCase.query.get(case_id)
    return render_template('index.html', title=title, cases=case)
