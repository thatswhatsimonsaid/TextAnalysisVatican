"""
Extracts the contents of the First Vatican Council. This function is used as the official Vatican link only contains Latin links, with this function used for a link with an English translation.

Args:
    url: URL to the First or Second Vatican Council

Return: 
    Returns a dictionary containing the two documents of the First Vatican Council.
"""

### Packages ###
import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict

### Extract Vatican I Documents ###
def ExtractVatican1DocumentFromAnotherWebsite(url):
    
    ### Set Up ###
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return None
    
    ### Parse HTML ###
    soup = BeautifulSoup(response.content, "html.parser")
    
    ### Find All Rows ###
    rows = soup.find_all("tr")
    
    ### Initialize Variables ###
    dei_filius_paragraphs = []
    pastor_aeternus_paragraphs = []
    current_document = "dei_filius"  # Start with Dei Filius
    
    ### Extract Text ###
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2:  # We need at least 2 cells (Latin and English)
            text = cells[1].get_text(strip=True)  # Second cell contains English
            
            # Only include valid paragraphs
            if text and len(text.split()) > 3:
                # Clean text
                text = re.sub(r'\s+', ' ', text)
                text = re.sub(r'[\r\n]+', ' ', text)
                text = re.sub(r'[^\w\s.,;?!\'"-]', '', text)
                
                # Check for document transition
                if "First Dogmatic Constitution on the Church of Christ" in text:
                    current_document = "pastor_aeternus"
                    continue
                
                # Skip headers and other non-content text
                if any(marker in text.lower() for marker in [
                    "session", "published in", "sacred council", "servants of god",
                    "approval of the", "everlasting remembrance"
                ]):
                    continue
                
                # Add to appropriate document
                if current_document == "dei_filius":
                    dei_filius_paragraphs.append(text.strip())
                else:
                    pastor_aeternus_paragraphs.append(text.strip())
    
    ### Create Output ###
    Documents = [
        {"title": "Dei Filius", "text": "\n\n".join(dei_filius_paragraphs)},
        {"title": "Pastor Aeternus", "text": "\n\n".join(pastor_aeternus_paragraphs)}
    ]
    
    return Documents
