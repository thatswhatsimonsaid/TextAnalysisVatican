### Packages ###
import requests
from bs4 import BeautifulSoup
import re
from .CleanText import ProcessText  # Import ProcessText function

## Extract Document Content #
def ExtractDocumentContent(url, headers, stopwords_set=None):

    # Set Up #
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"Error": f"Failed to retrieve the webpage. Status code: {response.status_code}"}
    
    # Parse HTML #
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Initialize #
    title = ""
    date = "" 
    paragraphs = []
   
    # Title #
    TitleElement = soup.find("div", class_="titolo")
    if TitleElement:
        title = TitleElement.get_text(strip=True)
    
    # Date #
    DateMatch = re.search(r'(\d{8})', url)
    if DateMatch:
        DateString = DateMatch.group(1)
        date = f"{DateString[:4]}-{DateString[4:6]}-{DateString[6:8]}"
    
    # Text Extraction #
    ContentElements = soup.find_all(['td', 'p'])

    for element in ContentElements:
        if element.get('class') and any(cls in ['clearfix', 'title', 'docdate'] for cls in element.get('class')):
            continue
        
        text = element.get_text(strip=True)
        
        if text and len(text.split()) > 3:
            if not any(marker in text.lower() for marker in [
                "vatican.va", "copyright", "jump to", "contents",
                "previous", "next", "[1]", "[2]", "[3]", "chapter"
            ]):
                paragraphs.append(text)

    # Process full text at once (after combining paragraphs)
    DocumentText = " ".join(paragraphs) if paragraphs else ""
    
    if DocumentText:
        DocumentText = " ".join(ProcessText(DocumentText, stopwords_set))  # Process and rejoin cleaned words

    # Output
    Output = {
        "Title": title,
        "Date": date,
        "Text": DocumentText,
        "URL": url
    }
    
    return Output
