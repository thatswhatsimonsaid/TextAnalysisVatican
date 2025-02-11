### Packages ###
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from collections import defaultdict

### Functions ###
def CalculateDocumentSimilarities(df_Councils, df_Encyclicals):

    ### Set Up ###
    TFIDF_Model = TfidfVectorizer(
        min_df=2,                        # Minimum document frequency
        max_df=0.95,                     # Maximum document frequency
        stop_words='english',            # Remove English stop words
        ngram_range=(1, 2)               # Use both unigrams and bigrams
    )
    
    ### Prepare Council Documents ###
    Vatican1_docs = df_Councils[df_Councils['Council'] == 1]['DocumentText'].tolist()
    Vatican2_docs = df_Councils[df_Councils['Council'] == 2]['DocumentText'].tolist()
    
    # Create combined corpus for TF-IDF
    AllDocs = Vatican1_docs + Vatican2_docs + df_Encyclicals['DocumentText'].tolist() # Combined corpus
    TFIDF_Matrix = TFIDF_Model.fit_transform(AllDocs)                                 # Fit and transform all documents
    
    ### Calculate Average Council Vectors ###
    Vatican1_Length = len(Vatican1_docs)
    Vatican2_Length = Vatican1_Length + len(Vatican2_docs)
    
    # Calculate average vectors - convert to numpy arrays
    Vatican1_Vector = np.asarray(TFIDF_Matrix[:Vatican1_Length].mean(axis=0))
    Vatican2_Vector = np.asarray(TFIDF_Matrix[Vatican1_Length:Vatican2_Length].mean(axis=0))
    
    ### Calculate Similarities for Each Encyclical ###
    SimilarityScores = []
    encyclical_vectors = TFIDF_Matrix[Vatican2_Length:]
    
    for i, row in df_Encyclicals.iterrows():

        CurrentEncylical = np.asarray(encyclical_vectors[i].toarray())
        Vatican1SimilarityScore = cosine_similarity(CurrentEncylical, Vatican1_Vector)[0][0]
        Vatican2SimilarityScore = cosine_similarity(CurrentEncylical, Vatican2_Vector)[0][0]
        
        SimilarityScores.append({
            'PopeName': row['PopeName'],
            'encyclical': row['encyclical'],
            'Vatican1_Similarity': Vatican1SimilarityScore,
            'Vatican2_Similarity': Vatican2SimilarityScore,
            'DocumentDate': row['DocumentDate']
        })
    
    return pd.DataFrame(SimilarityScores)

def CalculatePopeSimilarities(SimilarityScores_ByDocument):
    ### Group by Pope ###
    SimilarityScores_ByPope = SimilarityScores_ByDocument.groupby('PopeName').agg({
        'Vatican1_Similarity': 'mean',
        'Vatican2_Similarity': 'mean'
    }).reset_index()
    
    ### Add standard deviations ###
    std_devs = SimilarityScores_ByDocument.groupby('PopeName').agg({
        'Vatican1_Similarity': 'std',
        'Vatican2_Similarity': 'std'
    }).reset_index()
    
    SimilarityScores_ByPope['Vatican1_StdDev'] = std_devs['Vatican1_Similarity']
    SimilarityScores_ByPope['Vatican2_StdDev'] = std_devs['Vatican2_Similarity']
    
    return SimilarityScores_ByPope

def AnalyzeDocumentSimilarities(df_Councils, df_Encyclicals):
    ### Calculate Document-Level Similarities ###
    SimilarityScores_ByDocument = CalculateDocumentSimilarities(df_Councils, df_Encyclicals)
    
    ### Calculate Pope-Level Similarities ###
    SimilarityScores_ByPope = CalculatePopeSimilarities(SimilarityScores_ByDocument)
    
    return SimilarityScores_ByDocument, SimilarityScores_ByPope