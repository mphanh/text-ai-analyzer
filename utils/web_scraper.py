import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url}")
    soup = BeautifulSoup(response.content, 'html.parser')
    # Remove scripts and styles
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator='\n')
    # Collapse multiple newlines
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join(line for line in lines if line)
    return text
