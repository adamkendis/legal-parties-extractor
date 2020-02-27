# import os
# import shutil
# from time import sleep
from bs4 import BeautifulSoup
from collections import deque

# from flask import current_app


def verified_file_type(filename):
    # Return bool indicating if filename is an allowed filetype
    valid_filetypes = set(['xml'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in valid_filetypes


def format_case(case):
    # Structure case for JSON response
    return {
        'type': 'courtcase',
        'id': case['id'],
        'attributes': {
            'plaintiff': case['plaintiff'],
            'defendant': case['defendant']
        }
    }


def extract_party_names(filepath):
    # Receives an xml legal complaint facepage. Extracts plaintiff, defendant names.
    with open(filepath) as file:
        soup = BeautifulSoup(file, 'lxml')
        page_width = int(soup.find('page')['width'])
        # max_left_boundary is set to 40% of total page width.
        # Any tags with a left edge (provided by line tag 'l' attribute) in the
        # left 40% of the page will be caught in line_tags below. This will
        # capture attorney header, court name, case caption, complaint body on
        # facepage, and possibly some other content depending on quality of OCR.
        max_left_boundary = page_width * .4
        defendant = deque()
        plaintiff = deque()
        current_name = None
        defendant_complete = False
        line_tags = soup.find_all(
            lambda tag: tag.name == 'line' and
            'l' in tag.attrs and
            int(tag['l']) < max_left_boundary) 
        lines = list(reversed(line_tags))
        # Iterate through rows of text from bottom up. Defendant will be built first.
        for i, line in enumerate(lines):
            text = line.text.strip()
            first_word = text.split()[0]
            # Courtname header reached, both party names complete.
            if 'county of' in text.lower() and 'superior court' in lines[i + 1].text.lower():
                return({ 'plaintiff': ' '.join(plaintiff), 'defendant': ' '.join(defendant) })
            # Begin building defendant name from the bottom up.
            if 'defendant' in first_word.lower():
                current_name = defendant
                continue
            # Begin building plaintiff name from the bottom up.
            if defendant_complete and 'plaintiff' in first_word.lower():
                current_name = plaintiff
                continue
            # current_name has been initialized and current line is not the party divider.
            if current_name is not None and first_word not in ['v', 'v.', 'vs', 'vs.']:
                # Split on whitespace of 4 characters or greater.
                # 4 characters or greater will (hopefully) not cut off any part of a party name
                # but may help isolate and eliminate unwanted characters resulting from OCR.
                trimmed_text = text.split('   ')[0]
                if not len(current_name) and trimmed_text[-1] in [',', ';', "'"]:
                    # Remove comma, semicolon or apostrophe
                    trimmed_text = trimmed_text[:-1].strip()
                current_name.appendleft(trimmed_text)
                continue
            # Defendant deque has some content and caption divider reached indicating
            # defendant name is complete.
            if len(defendant):
                defendant_complete = True



# def remove_uploads():
#     # Delete uploaded xml files in uploads dir
#     uploads_dir = current_app.config['UPLOAD_FOLDER']
#     if os.path.isdir(uploads_dir):
#         sleep(2)
#         shutil.rmtree(uploads_dir, ignore_errors=True)
#         os.mkdir(uploads_dir)
