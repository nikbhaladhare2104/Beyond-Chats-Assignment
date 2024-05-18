import requests
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
from rich.console import Console
from rich.table import Table

# Download NLTK data files
download('punkt')
download('stopwords')

API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"

console = Console()

def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()["data"]["data"]
    except requests.exceptions.RequestException as e:
        console.print(f"Error fetching data from API: {e}", style="bold red")
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

def main():
    # console.print("Fetching data from API...", style="bold green")
    data = fetch_data(API_URL)
    
    all_citations = []
    for item in data:
        response_text = item["response"]
        sources = item["source"]
        citations = find_citations(response_text, sources)
        all_citations.append(citations)
    
    # Displaying the  citations in a user-friendly manner
    table = Table(title="Citations")
    table.add_column("Response ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Citations", style="magenta")
    
    for i, citations in enumerate(all_citations):
        citation_str = json.dumps(citations, indent=2)
        table.add_row(str(i+1), citation_str)
    
    console.print(table)

if __name__ == "__main__":
    main()
