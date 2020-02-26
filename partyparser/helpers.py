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
