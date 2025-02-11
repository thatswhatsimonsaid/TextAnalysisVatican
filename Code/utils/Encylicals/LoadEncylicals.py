### Packages ###
import os
import pickle
import pandas as pd
from datetime import datetime

### Functions ###
def LoadEncyclicals(BaseURL):
    DataFrameOutput = []
    
    ## For each pope ##
    for pope in os.listdir(BaseURL):
        
        ## Pope Directory ##
        PopeDir = os.path.join(BaseURL, pope)
        if os.path.isdir(PopeDir):
            
            ## For each encyclical ##
            for encyclical in os.listdir(PopeDir):

                ## Path ##
                encyclical_path = os.path.join(PopeDir, encyclical)

                # Open Content #
                with open(encyclical_path, "rb") as f:
                    DocumentData = pickle.load(f)
                    DocumentText = DocumentData["text"]
                    DocumentDate = DocumentData["date"]  # This is already a datetime object in your data
                    file_ext = ".pkl"

                # Ensure DocumentDate is a datetime object
                if not isinstance(DocumentDate, datetime):
                    DocumentDate = datetime.strptime(DocumentDate, "%Y-%m-%d")

                # Compute Indicator #
                PreVaticanII = DocumentDate < datetime(1962, 10, 11)

                # Save Content #
                DataFrameOutput.append({
                    "PopeName": pope,
                    "encyclical": encyclical.replace(file_ext, ""),
                    "DocumentText": DocumentText,
                    "DocumentDate": DocumentDate,
                    "PreVaticanII": PreVaticanII
                })
    
    ### Return ###
    return pd.DataFrame(DataFrameOutput)