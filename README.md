# Citation Extractor

## Description
This Python program extracts citations from a paginated API response and presents them in a user-friendly HTML table format.

## Features
- Fetches data from a paginated API endpoint
- Identifies citations for each response-sources pair
- Presents the citations in an HTML table
- Uses NLTK for text processing and Rich library for table formatting
- Provides a simple Flask web server to display the HTML table in a browser

## Requirements
- Python 3.x
- requests
- NLTK
- rich
- Flask

## Installation
1. Clone this repository
2. Insatall all the requirements, {pip install requests ...}

 ## Usage
1. Run the Python script:
 ```
  python3 main.py
 ```
for running python script and getting the result inside console

```
   python3 mainBrowser.py
   ```
   for getting the result on browser, 
2. Access the HTML table in your web browser by visiting http://localhost:5000

## Sample Output
Upon running the program, it will fetch data from the specified API endpoint, extract citations, and generate an HTML table. You can then access this table via the provided Flask web server.






