from .GetVatican2URLS import *
from .ExtractDocumentContent import *

### Get Vatican 2 Documents ###
def GetVatican2Documents(LanguageCode):

    # Set Up #
    documents = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    BaseURL = 'https://www.vatican.va/archive/hist_councils/ii_vatican_council/index.htm'
    DocumentURLS = GetVatican2URLS(BaseURL, LanguageCode)
    
    # Extract document content #
    for url in DocumentURLS:
        doc = ExtractDocumentContent(url, headers)
        if "Error" not in doc:
            documents.append(doc)
    
    # Output #
    return documents