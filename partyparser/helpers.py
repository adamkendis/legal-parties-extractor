# import os
# import shutil
# from time import sleep
from bs4 import BeautifulSoup

# from flask import current_app


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


def extract_party_names(filepath):
    with open(filepath) as file:
        soup = BeautifulSoup(file, 'lxml')
        page_width = int(soup.find('page')['width'])
        max_left_boundary = page_width * .4
        defendant = deque()
        plaintiff = deque()
        current_name = defendant
        defendant_complete = False
        line_tags = soup.find_all(
            lambda tag:tag.name == 'line' and
            'l' in tag.attrs and
            int(tag['l']) < max_left_boundary) 
        lines = list(line_tags)
        i = len(lines) - 1
        while i >= 0:
            text = lines[i].text.strip()
            first_word = text.split()[0]
            if 'county of' in text.lower() and 'superior court' in lines[i-1].text.lower():
                plaintiff.pop()
                defendant.pop()
                return({ 'plaintiff': ' '.join(plaintiff), 'defendant': ' '.join(defendant) })
            if 'defendant' in first_word.lower():
                defendant.appendleft(first_word)
                i -= 1
                continue
            if defendant_complete and 'plaintiff' in first_word.lower():
                plaintiff.appendleft(first_word)
                i -=1
                continue
            if len(current_name) and first_word not in ['v', 'v.', 'vs', 'vs.']:
                trimmed_text = text.split('   ')[0]
                current_name.appendleft(trimmed_text)
                i -=1
                continue
            elif len(defendant):
                current_name = plaintiff
                defendant_complete = True
                i -=1
            else:
                i -=1
                continue


# def remove_uploads():
#     # Delete uploaded xml files in uploads dir
#     uploads_dir = current_app.config['UPLOAD_FOLDER']
#     if os.path.isdir(uploads_dir):
#         sleep(2)
#         shutil.rmtree(uploads_dir, ignore_errors=True)
#         os.mkdir(uploads_dir)
