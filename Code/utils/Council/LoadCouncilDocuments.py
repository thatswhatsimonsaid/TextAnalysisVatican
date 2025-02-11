### Packages ###
import os
import pickle
import pandas as pd
import re
from datetime import datetime

### Functions ###
def LoadCouncils(BaseURL):
    DataFrameOutput = []
    
    ## For each council ##
    for council in os.listdir(BaseURL):
        
        ## Council Directory ##
        CouncilDir = os.path.join(BaseURL, council)
        if os.path.isdir(CouncilDir):
            
            ## Set Council Number ##
            CouncilNumber = 1 if council == "Vatican_I" else 2
            
            ## For each document ##
            for document in os.listdir(CouncilDir):
                
                ## Path ##
                document_path = os.path.join(CouncilDir, document)
                
                # Open Content #
                with open(document_path, "rb") as f:
                    DocumentData = pickle.load(f)
                    DocumentText = DocumentData["text"]
                
                # Clean title #
                # Extract the part between the date and language code
                TitleMatch = re.search(r'\d{8}_([^_]+)_[a-z]{2}', document)
                if TitleMatch:
                    CleanTitle = TitleMatch.group(1)
                else:
                    # Fallback: remove file extension
                    CleanTitle = document.replace('.pkl', '')
                
                # Save Content #
                DataFrameOutput.append({
                    "Council": CouncilNumber,
                    "Title": CleanTitle,
                    "DocumentText": DocumentText
                })
    
    ### Reformat ###
    df = pd.DataFrame(DataFrameOutput)
    df = df.sort_values('Title')
    df.index = range(0,len(df))

    ### Return ###
    return df