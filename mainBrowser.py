import requests
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
from rich.table import Table
from rich.console import Console
from flask import Flask

# Download NLTK data files
download('punkt')
download('stopwords')


API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"

app = Flask(__name__)

def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()["data"]["data"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []

def tokenize_and_clean(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    return [word for word in tokens if word.isalnum() and word not in stop_words]

def find_citations(response_text, sources):
    response_tokens = tokenize_and_clean(response_text)
    citations = []
    
    for source in sources:
        source_tokens = tokenize_and_clean(source['context'])
        if any(token in response_tokens for token in source_tokens):
            citation = {"id": source["id"]}
            if "link" in source and source["link"]:
                citation["link"] = source["link"]
            citations.append(citation)
    
    return citations

def generate_html_table(all_citations):
    console = Console()
    html = "<table border='1'><tr><th>Response Index</th><th>Citations</th></tr>"
    
    for i, citations in enumerate(all_citations):
        citation_str = json.dumps(citations, indent=2)
        html += f"<tr><td>{i}</td><td>{citation_str}</td></tr>"
    
    html += "</table>"
    return html

def main():
    print("Fetching data from API...")
    data = fetch_data(API_URL)
    
    all_citations = []
    for item in data:
        response_text = item["response"]
        sources = item["source"]
        citations = find_citations(response_text, sources)
        all_citations.append(citations)
    
    html_table = generate_html_table(all_citations)
    with open("citations_table.html", "w") as html_file:
        html_file.write(html_table)

@app.route('/')
def display_table():
    with open("citations_table.html", "r") as html_file:
        table_html = html_file.read()
    return table_html

if __name__ == '__main__':
    main()
    app.run(debug=True)
