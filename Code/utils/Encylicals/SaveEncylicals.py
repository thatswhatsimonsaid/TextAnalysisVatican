### Packages ###
import os
import re
import pickle
from utils.Encylicals.ScrapeEncylicals import *
from utils.Encylicals.ExtractEncylicalContent import *
from utils.Encylicals.GetEncyclicalDates import *


### Function ###
def SaveEnclylicals():
    
    ### Set Up ###
    print("Getting encylical links:")
    PopeEncylicalLinks = ScrapeEncyclicals("English") 
    print("Found all encylical links!")
    print(" ")
    BaseURL = "/Users/simondn/Documents/CSSS594/TextAnalysisVatican/Data/Encylicals" 
    
    ### For each pope ###
    for PopeName in PopeEncylicalLinks.keys():
        print("Pope Name: " + PopeName)
        
        ### For each document ###
        for DocumentLink in PopeEncylicalLinks[PopeName]:
            
            ### Match ###
            match = re.search(r"(?:enc_)?\d+_?(.*)\.html", DocumentLink)
            if match:
                
                ## Document Link ##
                DocumentTitle = match.group(1)
                DocumentTitle = re.sub(r"^(enciclica|epistula|constitutio|bulla)-", "", DocumentTitle)
                
                ## Content to save ##
                DocumentContent = ExtractEncylicalContent(DocumentLink)
                DocumentDate = ExtractDateFromURL(DocumentLink)
                
                ## Create document dictionary ##
                DocumentData = {
                    "text": DocumentContent,
                    "date": DocumentDate
                }
                
                ## Directory path ##
                PopeDirectory = os.path.join(BaseURL, PopeName)
                SaveLocation = os.path.join(PopeDirectory, DocumentTitle + ".pkl")
                os.makedirs(PopeDirectory, exist_ok=True)
                
                ## SAVE ##   
                with open(SaveLocation, 'wb') as output:
                    pickle.dump(DocumentData, output)
                
                ## Print saved document ##
                print(f"Saved: {DocumentTitle} | {DocumentDate}")
                # print(f"Save Location: {SaveLocation}")
                # print(f"Document Date: {DocumentDate}")
                print(" ")
    
    print("All documents saved successfully")