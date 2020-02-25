def verify_file_type(filename):
    # Return bool indicating if filename is an allowed filetype
    valid_filetypes = set(['xml'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in valid_filetypes