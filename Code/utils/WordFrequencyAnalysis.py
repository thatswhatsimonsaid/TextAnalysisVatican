### Packages ###
import pandas as pd
from .CleanText import *
from collections import Counter

### Word Frequency ###
def WordFrequencyAnalysis(TextInput, stopwords_set, TopN=20):

    ### Set Up ###
    TokenizedWords = []
    if isinstance(TextInput, str):
        TextInput = [TextInput]  
    else:
        TextInput = TextInput  

    ### Preprocessing ###
    for text in TextInput["Text"]:
        TextedCleaned = ProcessText(text)
        TokenizedWords.extend(TextedCleaned)

    ### Count word frequencies ###
    WordCounts = Counter(TokenizedWords)
    MostCommonWords = WordCounts.most_common(TopN)
    WordFrequencyDF = pd.DataFrame(MostCommonWords, columns=['Word', 'Frequency'])

    return WordFrequencyDF
