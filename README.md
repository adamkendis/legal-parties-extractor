# Legal Parties Parser

A simple REST API written in Python/Flask with an (extremely basic) web interface and JSON endpoints. Ingests xml legal documents and outputs extracted plaintiff and defendant names.

#### Quick navigation

- [Setup](#setup)
- [Running the app](#running-the-app)
- [Using the app](#using-the-app)
- [Web Interface](#web-interface)
- [JSON API](#json-api)
- [Troubleshooting](#troubleshooting)

### Requirements

- Python3

### Setup

    # Clone the code repository.
      git clone https://github.com/adamkendis/legal-parties-extractor.git
      cd legal-parties-extractor

    # Run setup.sh (macOS) or setup.bat (Windows) to create a 
    # virtual environment and install dependencies.
      setup.sh
    or for Windows:
      setup.bat 

    # Initialize the database. Creates a sqlite court_cases.db file 
    # in the project's root directory.
      flask db migrate

  Setup complete!

### Running the app

    # Start the Flask server:
      flask run

    # To stop the server:
      CTRL + C

### Using the app

The app has: 
  - Browser-accessible web interface endpoints serving up html.
  - JSON endpoints with no web interface if you prefer using curl or Postman.

#### JSON API

See the [wiki](https://github.com/adamkendis/legal-parties-extractor/wiki/API-Reference) for API specification.

#### Web Interface

Point your browser to http://localhost:5000/

You can select and upload an .xml file. If the .xml file is valid and the server is able to extract the necessary text, the resulting plaintiff/defendant names will be appear at the top of the page.

Available web endpoints:

    # Home page
    /
    OR
    /index

    # View all saved cases
    /web/cases
  
    # View single case
    /web/cases/:id


### Troubleshooting

The server can be restarted by:
    
    # Stop server
      CTRL + C

    # Restart server
      flask run









