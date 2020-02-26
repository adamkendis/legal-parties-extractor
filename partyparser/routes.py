# Standard library imports
import os

# Third party imports
from flask import Blueprint, current_app, render_template, \
    request, jsonify
from werkzeug.utils import secure_filename

# Local app imports
from partyparser.models import CourtCase
from partyparser.helpers import verified_file_type, format_case

home_bp = Blueprint('home_bp', __name__,
                    template_folder='templates')

web_bp = Blueprint('web_bp', __name__,
                   template_folder='templates')

api_bp = Blueprint('api_bp', __name__)


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
    if request.method == 'POST':
        if 'file' not in request.files:
            res = jsonify({'message': 'No file part in request.'})
            res.status_code = 400
            return res
        file = request.files['file']
        if file.filename == '':
            res = jsonify({'message': 'No file uploaded.'})
            res.status_code = 400
            return res
        if file and verified_file_type(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))
            # PLACE XML PARSING LOGIC HERE, UPDATE RESPONSE AFTER
            res = jsonify({'message': 'File uploaded.'})
            res.status_code = 201
            return res
        else:
            res = jsonify({'message': 'Allowed file type is xml'})
            res.status_code = 400
            return res


@web_bp.route('/web/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    title = 'XML Parser'
    case = CourtCase.query.get(case_id)
    if case is not None:
        return render_template('index.html', title=title, cases=case)
    else:
        res = jsonify({'message': 'Case does not exist.'})
        res.status_code = 404
        return res

@api_bp.route('/api/cases', methods=['GET', 'POST'])
def handle_api_cases():
    title = 'XML Parser'
    if request.method == 'GET':
        cases = CourtCase.query.all()
        formatted_cases = [format_case(case) for case in cases]
        res = jsonify(formatted_cases)
        res.status_code = 200
        return res
    if request.method == 'POST':
        if 'file' not in request.files:
            res = jsonify({'message': 'No file part in request.'})
            res.status_code = 400
            return res
        file = request.files['file']
        if file.filename == '':
            res = jsonify({'message': 'No file uploaded.'})
            res.status_code = 400
            return res
        if file and verified_file_type(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))
            # PLACE XML PARSING LOGIC HERE, UPDATE RESPONSE AFTER
            res = jsonify({'message': 'File uploaded.'})
            res.status_code = 201
            return res
        else:
            res = jsonify({'message': 'Allowed file type is xml'})
            res.status_code = 400
            return res

@api_bp.route('/api/cases/<int:case_id>', methods=['GET'])
def get_api_case(case_id):
    title = 'XML Parser'
    case = CourtCase.query.get(case_id)
    if case is not None:
        formatted_case = format_case(case)
        res = jsonify(formatted_case)
        res.status_code = 200
        return res
    else:
        res = jsonify({'message': 'Case not found.'})
        res.status_code = 404
        return res
