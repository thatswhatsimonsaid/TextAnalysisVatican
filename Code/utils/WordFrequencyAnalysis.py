### Packages ###
import pandas as pd
from .CleanText import *
from collections import Counter
from nltk.stem import WordNetLemmatizer


### Word Frequency ###
def WordFrequencyAnalysis(TextInput, StopWordsSet, TopN=20):

    ### Set Up ###
    TokenizedWords = []
    if isinstance(TextInput, str):
        TextInput = [TextInput]  
    else:
        TextInput = TextInput  

    ### Initialize Lemmatizer ###
    lemmatizer = WordNetLemmatizer()

    ### Preprocessing ###
    for text in TextInput:
        TextedCleaned = ProcessText(text)
        TokenizedWords.extend(TextedCleaned)
        # TextedCleaned = [lemmatizer.lemmatize(word) for word in TextedCleaned if word.lower() not in StopWordsSet]
        TextedCleaned = [lemmatizer.lemmatize(word) for word in TextedCleaned if not StopWordsSet or word not in StopWordsSet]


    ### Count word frequencies ###
    WordCounts = Counter(TokenizedWords)
    MostCommonWords = WordCounts.most_common(TopN)
    WordFrequencyDF = pd.DataFrame(MostCommonWords, columns=['Word', 'Frequency'])

    return WordFrequencyDF

def GetEncylicalWordFrequency(df_input, GroupByVar="PopeName", stop_words=None, TopNInput=1000):
    
    ### Set Up ###
    WordCounts = {}

    ### For either PopeName or PreVaticanII ###
    for group in df_input[GroupByVar].unique():
        Content = df_input[df_input[GroupByVar] == group]["DocumentText"]                                # Content
        WordFreqDF = WordFrequencyAnalysis(Content, StopWordsSet=stop_words, TopN=TopNInput)   # Word Frequency
        WordCounts[group] = dict(zip(WordFreqDF["Word"], WordFreqDF["Frequency"]))         # Reformat

    ### Reformat to DF ###
    WordFreqDF = pd.DataFrame.from_dict(WordCounts, orient="index").T.fillna(0)
    WordFreqDF = WordFreqDF.div(WordFreqDF.sum(axis=0), axis=1) * 100  # Normalize

    return WordFreqDF
