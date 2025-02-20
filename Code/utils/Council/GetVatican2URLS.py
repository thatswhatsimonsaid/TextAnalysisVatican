"""
Extracts the URLS of each document of the Second Vatican Council.

Args:
    BaseURL: The base URL of the Second Vatican Council.
    LanguageCode: The code of the language the doucment is to be extracted from

Return: 
    Returns a list of containing all the links to the documents of the Second Vatican Council.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

### Get Vatican 2 URLS ###
def GetVatican2URLS(BaseURL, LanguageCode):

    # Set Up #
    links = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(BaseURL, headers=headers)

    # Parse HTML #
    soup = BeautifulSoup(response.content, 'html.parser')
        
    # Separators #
    for a in soup.find_all('a', href=True):
        href = a['href'].lower()
        if any(pattern in href for pattern in [
            f'_{LanguageCode}.',
            f'_{LanguageCode}htm',
            'constitutions/',
            'decrees/',
            'declarations/',
            'documents/',
            'sacrosanctum',
            'presbyterorum',
            'apostolicam',
            'perfectae'
        ]):
            if (f'_{LanguageCode}.' in href or f'_{LanguageCode}htm' in href):
                FullURL = urljoin(BaseURL, href)
                if FullURL not in links:
                    links.append(FullURL)
    
    # Output #
    return links
