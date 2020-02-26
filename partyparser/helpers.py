import os
import shutil
from time import sleep

from flask import current_app

def verified_file_type(filename):
    # Return bool indicating if filename is an allowed filetype
    valid_filetypes = set(['xml'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in valid_filetypes


def format_case(case):
    return {
        'type': 'courtcase',
        'id': case['id'],
        'attributes': {
            'plaintiff': case['plaintiff'],
            'defendant': case['defendant']
        }
    }


def remove_uploads():
    # Delete uploaded xml files in uploads dir
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    if os.path.isdir(uploads_dir):
        sleep(2)
        shutil.rmtree(uploads_dir, ignore_errors=True)
        os.mkdir(uploads_dir)
