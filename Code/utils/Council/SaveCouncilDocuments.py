### Packages ###
import os
import re
import pickle
from utils.Council.GetVatican1Documents import *
from utils.Council.GetVatican2Documents import *

### Save Vatican Documents ###
def SaveVaticanDocuments(LanguageCode="en"):
    
    ### Set Up ###
    print("Getting Vatican Council documents:")
    BaseURL = "/Users/simondn/Documents/CSSS594/TextAnalysisVatican/Data/Councils"
    
    ### Get Vatican I Documents ###
    print("\nProcessing Vatican I documents:")
    Vatican1Docs = GetVatican1Documents(LanguageCode)
    SaveCouncilDocuments(Vatican1Docs, BaseURL, "Vatican_I")
    print("")
    
    ### Get Vatican II Documents ###
    print("\nProcessing Vatican II documents:")
    Vatican2Docs = GetVatican2Documents(LanguageCode)
    SaveCouncilDocuments(Vatican2Docs, BaseURL, "Vatican_II")
    
    print("\nAll council documents saved successfully")

### Save Council Documents ###
def SaveCouncilDocuments(documents, BasePath, CouncilName):
    
    ### Create directory ###
    CouncilDirectory = os.path.join(BasePath, CouncilName)
    os.makedirs(CouncilDirectory, exist_ok=True)
    
    ### Save each document ###
    for doc in documents:
        # Create safe filename from title
        SafeTitle = re.sub(r'[^\w\s-]', '', doc['title']).strip().lower()
        SafeTitle = re.sub(r'[-\s]+', '-', SafeTitle)
        
        SaveLocation = os.path.join(CouncilDirectory, f"{SafeTitle}.pkl")
        # print(SaveLocation)
        with open(SaveLocation, 'wb') as output:
            pickle.dump(doc, output)
        
        print(f"Saved: {doc['title']}")
        # print(f"Date: {doc['date']}")
        # print()