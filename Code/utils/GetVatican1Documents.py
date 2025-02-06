from .ExtractDocumentContent import *

### Get Vatican 1 Documents ###
def GetVatican1Documents(LanguageCode):

    # Set Up #
    documents = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    # Only two URLS yay #
    BaseURLS = [
        f"https://www.vatican.va/archive/hist_councils/i-vatican-council/documents/vat-i_const_18700424_dei-filius_{LanguageCode}.html",
        f"https://www.vatican.va/archive/hist_councils/i-vatican-council/documents/vat-i_const_18700718_pastor-aeternus_{LanguageCode}.html"
    ]
    
    # Extract document content #
    for url in BaseURLS:
        doc = ExtractDocumentContent(url, headers)
        if "Error" not in doc:
            documents.append(doc)
    
    # Output #
    return documents

