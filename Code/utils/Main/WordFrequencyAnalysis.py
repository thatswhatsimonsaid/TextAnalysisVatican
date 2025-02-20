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
        TextedCleaned = [lemmatizer.lemmatize(word) for word in TextedCleaned if not StopWordsSet or word.lower() not in StopWordsSet]
        TokenizedWords.extend(TextedCleaned)

    ### Count word frequencies ###
    WordCounts = Counter(TokenizedWords)
    MostCommonWords = WordCounts.most_common(TopN)
    WordFrequencyDF = pd.DataFrame(MostCommonWords, columns=['Word', 'Frequency'])

    return WordFrequencyDF

### Wrapper Function for each Group ###
def GetWordFrequency(df_input, GroupByVar, StopWordsSet=None, TopNInput=1000, Normalize = False):
    
    ### Set Up ###
    WordCounts = {}

    ### For either PopeName or PreVaticanII ###
    for group in df_input[GroupByVar].unique():
        Content = df_input[df_input[GroupByVar] == group]["DocumentText"]                             # Content
        WordFreqDF = WordFrequencyAnalysis(Content, StopWordsSet=StopWordsSet, TopN=TopNInput)        # Word Frequency
        WordCounts[group] = dict(zip(WordFreqDF["Word"], WordFreqDF["Frequency"]))                    # Reformat

    ### Reformat to DF ###
    WordFreqDF = pd.DataFrame.from_dict(WordCounts, orient="index").T.fillna(0)
    if Normalize:
        WordFreqDF = WordFreqDF.div(WordFreqDF.sum(axis=0), axis=1) * 100                                 # Normalize

    return WordFreqDF

### Statistical Testing ###
### Packages ###
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, chi2

### Compare Word Frequencies ###
def ChiSquaredTestWordFrequency(df, pope1, pope2):

    ### Set Up ###
    results = []
    words = df.index
    freq1 = df[pope1]
    freq2 = df[pope2]
    
    ### Get Chi-Square for each word ###
    for word, count1, count2 in zip(words, freq1, freq2):
        
        # Skip words where both counts are zero
        if count1 == 0 and count2 == 0:
            continue
        
        contingency = np.array([
            [count1, count2],
            [freq1.sum() - count1, freq2.sum() - count2]
        ])
        
        # Perform chi-square test
        chi2_stat, p_value, _, _ = chi2_contingency(contingency)
        
        # Calculate contribution to chi-square
        expected = np.outer(contingency.sum(axis=1), contingency.sum(axis=0)) / contingency.sum()
        contribution = np.sum(((contingency - expected) ** 2) / expected)
        
        results.append({
            "word": word,
            f"{pope1}_freq": count1,
            f"{pope2}_freq": count2,
            "chi2_contribution": contribution,
            "p_value": p_value
        })
    
    ### Create Output DataFrame ###
    results_df = pd.DataFrame(results).sort_values("chi2_contribution", ascending=False)
    
    ### Compute Overall Chi-Square ###
    total_chi2 = results_df["chi2_contribution"].sum()
    total_df = len(results_df) - 1  # Degrees of freedom
    total_p_value = 1 - chi2.cdf(total_chi2, total_df)
    
    ### Create Output ###
    Output = {
        "chi2_statistic": total_chi2,
        "p_value": total_p_value,
        "significant_words": results_df
    }
    
    return Output
