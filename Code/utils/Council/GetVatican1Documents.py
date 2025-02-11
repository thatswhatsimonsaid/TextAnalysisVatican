from .ExtractDocumentContent import *

### Get Vatican 1 Documents ###
def GetVatican1Documents(LanguageCode):
    
    ### Set Up ###
    documents = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    ### Base URLs ###
    BaseURLS = [
        f"https://www.vatican.va/archive/hist_councils/i-vatican-council/documents/vat-i_const_18700424_dei-filius_{LanguageCode}.html",
        f"https://www.vatican.va/archive/hist_councils/i-vatican-council/documents/vat-i_const_18700718_pastor-aeternus_{LanguageCode}.html"
    ]
    
    ### Extract document content ###
    for url in BaseURLS:
        doc = ExtractDocumentContentFunction(url, headers)
        if doc:
            documents.append(doc)
            print(f"Successfully processed: {doc['title']}")
    
    return documents