# Standard library imports
from collections import deque

# Third party imports
from bs4 import BeautifulSoup


def verified_file_type(filename):
    # Return bool indicating if filename is an allowed filetype.
    valid_filetypes = set(['xml'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in valid_filetypes


def format_case(case):
    # Structure case for JSON response.
    return {
        'type': 'courtcase',
        'id': case['id'],
        'attributes': {
            'plaintiff': case['plaintiff'],
            'defendant': case['defendant']
        }
    }


def extract_party_names(filepath):
    """Receives an xml file representation of a legal complaint facepage.
        Returns:
            { plaintiff: String, defendant: String }"""
    with open(filepath) as file:
        soup = BeautifulSoup(file, 'lxml')
        page = soup.find('page')
        if not page:
            return None
        page_width = int(page['width'])
        max_left_boundary = page_width * .4
        defendant = deque()
        plaintiff = deque()
        current_name = None
        defendant_complete = False
        # max_left_boundary is set to 40% of total page width.
        # Any tags with a left edge (provided by line tag 'l' attribute) in the
        # left 40% of the page will be caught in line_tags below. This will
        # capture left margin line numbers, attorney header, courtname,
        # case caption, complaint body on facepage, and possibly some other
        # content depending on OCR quality.
        line_tags = soup.find_all(
            lambda tag: tag.name == 'line'
            and 'l' in tag.attrs  # noqa: W503
            and int(tag['l']) < max_left_boundary)  # noqa: W503
        lines = list(reversed(line_tags))
        # Iterate through rows of text from bottom up.
        # Defendant will be built first.
        for i, line in enumerate(lines):
            text = line.text.strip()
            first_word = text.split()[0]
            # Courtname header reached, both party names complete.
            if 'county of' in text.lower() and 'superior court' in \
                    lines[i + 1].text.lower():
                return({'plaintiff': ' '.join(plaintiff),
                        'defendant': ' '.join(defendant)})
            # Begin building defendant name from the bottom up.
            if 'defendant' in first_word.lower():
                current_name = defendant
                continue
            # Begin building plaintiff name from the bottom up.
            if defendant_complete and 'plaintiff' in first_word.lower():
                current_name = plaintiff
                continue
            # current_name initialized and current line is not party divider.
            if current_name is not None and \
                    first_word not in ['v', 'v.', 'vs', 'vs.']:
                # Splitting on 4 characters of whitespace or greater will
                # (hopefully) not cut off any part of a party name and may
                # isolate unwanted characters resulting from OCR.
                trimmed_text = text.split('   ')[0]
                if not len(current_name) and trimmed_text[-1] in [',', ';', "'"]:
                    # Remove trailing comma, semicolon or apostrophe.
                    trimmed_text = trimmed_text[:-1].strip()
                current_name.appendleft(trimmed_text)
                continue
            # Defendant deque has some content and caption divider reached
            # indicating defendant name is complete.
            if len(defendant):
                defendant_complete = True
