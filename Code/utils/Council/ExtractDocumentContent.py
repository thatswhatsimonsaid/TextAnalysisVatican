"""
Extracts the contents of the First and Second Vatican Council.

Args:
    url: URL to the First or Second Vatican Council
    headers: Header of the documents

Return: 
    Returns a dictionary containing the title, texts, date, and url of the council document.
"""

### Packages ###
import requests
from bs4 import BeautifulSoup
import re
from utils.Main.CleanText import *

### Extract Document Content ###
def ExtractDocumentContentFunction(url, headers):
    
    ### Set Up ###
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return None
    
    ### Parse HTML ###
    soup = BeautifulSoup(response.content, "html.parser")
    
    ### Get Title ###
    title = ""
    TitleElement = soup.find("div", class_="titolo")
    if TitleElement:
        title = TitleElement.get_text(strip=True)
    if not title:
        match = re.search(r'[^/]+(?=\.html)', url)
        title = match.group(0).replace('-', ' ').title() if match else "Untitled Document"
    
    ### Get Date ###
    date = ""
    DateMatch = re.search(r'(\d{8})', url)
    if DateMatch:
        DateString = DateMatch.group(1)
        date = f"{DateString[:4]}-{DateString[4:6]}-{DateString[6:8]}"
    
    ### Get Text ###
    paragraphs = []
    ContentElements = soup.find_all(['td', 'p'])
    
    for element in ContentElements:
        if element.get('class') and any(cls in ['clearfix', 'title', 'docdate'] for cls in element.get('class')):
            continue
        text = element.get_text(strip=True)
        
        # Only include valid paragraphs
        if text and len(text.split()) > 3:
            if not any(marker in text.lower() for marker in [
                "vatican.va", "copyright", "jump to", "contents",
                "previous", "next", "[1]", "[2]", "[3]", "chapter"
            ]):
                # Clean text
                text = re.sub(r'\s+', ' ', text)
                text = re.sub(r'[^\w\s.,;?!\'"-]', '', text)
                paragraphs.append(text.strip())
    
    ### Create Output ###
    DocumentText = "\n\n".join(paragraphs) if paragraphs else ""
    
    Output = {
        "title": title,
        "text": DocumentText,
        "date": date,
        "url": url
    }
    
    return Output