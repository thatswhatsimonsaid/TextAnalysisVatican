### Packages ###
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

### Function ###
def GetEncylicalSentiments(df):

    ### Set Up 
    Output = []
    SIA = SentimentIntensityAnalyzer() # Initalize Sentiment Analysis

    ### Get SIA for each document ###
    for _, row in df.iterrows():

        # Scores #
        SIA_Scores = SIA.polarity_scores(row['DocumentText'])
        
        # Data #
        SIA_Scores['encyclical'] = row['encyclical']
        SIA_Scores['DocumentDate'] = pd.to_datetime(row['DocumentDate'])  # Convert to datetime
        SIA_Scores['PopeName'] = row['PopeName']
        SIA_Scores['PreVaticanII'] = row['PreVaticanII']
        
        # Append #
        Output.append(SIA_Scores)

    ### Output ###
    Output = pd.DataFrame(Output)
    Output = Output.sort_values('DocumentDate')
    Output.columns = [
                    "NegativeScore", 
                    "NeutralScore", 
                    "PositiveScore", 
                    "CompoundScore", 
                    "DocumentTitle", 
                    "DocumentDate", 
                    "PopeName", 
                    "PreVaticanII"]
    Output = Output[
        ["DocumentTitle", 
        "DocumentDate", 
        "PopeName", 
        "PreVaticanII",         
        "NegativeScore", 
        "NeutralScore", 
        "PositiveScore", 
        "CompoundScore"]
        ]
    
    ### Return ###
    return Output