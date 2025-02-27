### Packages ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
from sklearn.metrics.pairwise import cosine_similarity

### Preprocess Data ###
def PreprocessTopicData(df):

    ### Set Up ###
    ProcessedData = []
    
    ### Looop through popes ###
    for pope in df.index:

        ## Remove Topics ##
        pope_name = pope.replace('_Topics', '')
        
        ## Loop through all topics ##
        for col in df.columns:

            # Split words and clean #
            words = [word.strip() for word in df.loc[pope, col].split(',')]
            
            # Add each word with its position #
            for pos, word in enumerate(words):
                ProcessedData.append({
                    'pope': pope_name,
                    'word': word,
                    'position': pos
                })
    
    ### Return ###
    return pd.DataFrame(ProcessedData)

### Heat Map ###
def CreateTopicHeatmap(ProcessedDF):

    ### Top Words ###
    TopWords = ProcessedDF['word'].value_counts().head(30).index.tolist()
    
    ### Pivot Table with weighted frequencies ###
    ProcessedDF['Weight'] = 1 / (ProcessedDF['position'] + 1)
    WordFreq = ProcessedDF.pivot_table(
        index='pope', 
        columns='word', 
        values='Weight', 
        aggfunc='sum',
        fill_value=0
    )
    
    ### Cleaning ###
    WordFreq = WordFreq[[w for w in TopWords if w in WordFreq.columns]]
    WordFreq = WordFreq.div(WordFreq.sum(axis=1), axis=0)
    ChronologicalOrder = ['leo_xiii',  'benedict_xv',  'pius_x',  'pius_xi',  'pius_xii', 'john_xxiii', 'paul_vi', 'john_paul_ii', 'benedict_xvi', 'francesco']
    AvailablePopes = [pope for pope in ChronologicalOrder if pope in WordFreq.index]
    WordFreq = WordFreq.loc[AvailablePopes]
    
    ### Create Plot ###
    plt.figure(figsize=(20, 8))
    sns.heatmap(WordFreq, cmap="YlOrRd", annot=False, linewidths=0.5)

    ### Vaican II Line ###
    VaticanIIIndex = AvailablePopes.index('john_xxiii') if 'john_xxiii' in AvailablePopes else -1
    plt.axhline(y=VaticanIIIndex, color='blue', linewidth=2)
    plt.text(-2, VaticanIIIndex - 0.5, 'Vatican II', fontsize=12, color='blue')
    
    ### Aesthetics ###
    plt.title("Key Words Frequency Across Papal Encyclicals", fontsize=16)
    plt.ylabel("Pope", fontsize=14)
    plt.xlabel("Words", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    ### Return ###
    return plt

### Topic Evolution ###
def CreateTopicEvolution(ProcessedDF):

    ### Categories to categorize topics (kinda like manual labelling in COVID Topic Modelling HW) ### TODO: Add more to this category
    Categories = {
        'Doctrinal': [
            # Core theological concepts
            'church', 'faith', 'catholic', 'truth', 'divine', 'doctrine', 'scripture', 'bishop', 
            'theology', 'magisterium', 'dogma', 'gospel', 'tradition', 'salvation', 'revelation', 
            'ministry', 'apostolic', 'teaching', 'ecclesial', 'creed', 'sacrament', 'hermeneutic', 
            'canonical', 'pontifical', 'encyclical', 'papal', 'theological', 'interpretation'
        ],
        'Spiritual': [
            # Spiritual and contemplative terms
            'christ', 'prayer', 'soul', 'spirit', 'holy', 'sacred', 'heart', 'jesus', 
            'mystical', 'contemplation', 'meditation', 'salvation', 'grace', 'redemption', 
            'worship', 'devotion', 'sacred', 'divine', 'transcendent', 'spiritual', 'prayer', 
            'contemplative', 'blessed', 'holy', 'sanctity', 'resurrection', 'salvation', 
            'transfiguration', 'eternal', 'heavenly'
        ],
        'Social': [
            # Social and global concepts
            'human', 'world', 'social', 'right', 'people', 'state', 'nation', 'peace', 
            'development', 'economic', 'environment', 'community', 'justice', 'solidarity', 
            'progress', 'global', 'society', 'politics', 'culture', 'humanitarian', 'welfare', 
            'policy', 'international', 'sustainability', 'democracy', 'equality', 'citizenship', 
            'common', 'public', 'global', 'universal', 'solidarity'
        ],
        'Moral': [
            # Ethical and moral concepts
            'moral', 'charity', 'freedom', 'dignity', 'education', 'family', 'love', 'justice', 
            'ethics', 'virtue', 'goodness', 'compassion', 'mercy', 'values', 'principles', 
            'human', 'rights', 'conscience', 'integrity', 'respect', 'responsibility', 'care', 
            'kindness', 'equality', 'fairness', 'truth', 'wisdom', 'character', 'moral', 
            'ethical', 'virtuous', 'compassionate'
        ]
    }
    
    ### Categorize words function ###
    def CategorizeWord(word):
        for category, words in Categories.items():
            if word in words:
                return category
        return 'Other'
    ProcessedDF['category'] = ProcessedDF['word'].apply(CategorizeWord)
    
    ### Calculate category emphasis ###
    CategoryScore = ProcessedDF.groupby(['pope', 'category']).size().unstack(fill_value=0)
    CategoryScore = CategoryScore.div(CategoryScore.sum(axis=1), axis=0) * 100
    
    ### Ensure all categories are present ###
    for cat in Categories.keys():
        if cat not in CategoryScore.columns:
            CategoryScore[cat] = 0
    
    ### Sort chronologically ###
    ChronologicalOrder = ['leo_xiii', 'benedict_xv', 'pius_x', 'pius_xi', 'pius_xii','john_xxiii', 'paul_vi', 'john_paul_ii', 'benedict_xvi', 'francesco']
    AvailablePopes = [pope for pope in ChronologicalOrder if pope in CategoryScore.index]
    CategoryScore = CategoryScore.loc[AvailablePopes]
    
    ### Create plot ###
    plt.figure(figsize=(20, 8))
    CategoryScore[['Doctrinal', 'Spiritual', 'Social', 'Moral', 'Other']].plot(
        kind='bar', 
        stacked=True,
        colormap='tab10'
    )
    
    ## Vatican II line ###
    VaticanIIIndex = AvailablePopes.index('john_xxiii') if 'john_xxiii' in AvailablePopes else -1
    plt.axvline(x=VaticanIIIndex - 0.5, color='black', linestyle='--', linewidth=2)
    plt.text(VaticanIIIndex - 0.5, 105, 'Vatican II', rotation=90)
    
    ### Aesthetics ###
    plt.title('Topic Category Distribution Across Papal Encyclicals', fontsize=16)
    plt.ylabel('Percentage (%)', fontsize=14)
    plt.xlabel('Pope', fontsize=14)
    plt.legend(title='Category')
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    plt.tight_layout()
    
    ### Output ###
    return plt

def CreateTopicSimilarity(df):

    ### Extract all unique topics ##
    AllWords = set()
    for col in df.columns:
        for TopicText in df[col]:
            words = [w.strip() for w in TopicText.split(',')]
            AllWords.update(words)
    
    ### Pope word matrix ###
    PopeWordMatrix = {}
    for pope in df.index:
        WordCounts = {word: 0 for word in AllWords}
        for col in df.columns:
            TopicText = df.loc[pope, col]
            words = [w.strip() for w in TopicText.split(',')]
            for pos, word in enumerate(words):

                # Weight by position (earlier words are more important)
                WordCounts[word] += 1 / (pos + 1)
        PopeWordMatrix[pope] = WordCounts
    
    ### Cleaning ###
    PopeWordDF = pd.DataFrame(PopeWordMatrix).T
    RowSums = PopeWordDF.sum(axis=1)
    PopeWordDF = PopeWordDF.div(RowSums, axis=0)
    
    ### Cosine Similarity ###
    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity(PopeWordDF)
    SimilarityDF = pd.DataFrame(similarity, index=PopeWordDF.index, columns=PopeWordDF.index)
    
    # Get chronological order of popes
    OrderedPope = ['leo_xiii_Topics', 'benedict_xv_Topics', 'pius_x_Topics', 'pius_xi_Topics', 'pius_xii_Topics','john_xxiii_Topics', 'paul_vi_Topics', 'john_paul_ii_Topics', 'benedict_xvi_Topics', 'francesco_Topics']
    AvailablePopes = [pope for pope in OrderedPope if pope in SimilarityDF.index]
    SimilarityDF = SimilarityDF.loc[AvailablePopes, AvailablePopes]
    
    ### Plot ###
    plt.figure(figsize=(20, 8))
    sns.heatmap(
        SimilarityDF, 
        annot=True, 
        cmap="YlGnBu", 
        vmin=0, 
        vmax=1,
        fmt=".2f",
        linewidths=0.5
    )
    
    ### Add markers for pre/post Vatican II ###
    Vatican2Index = AvailablePopes.index('john_xxiii_Topics') if 'john_xxiii_Topics' in AvailablePopes else -1
    if Vatican2Index > 0:
        plt.axhline(y=Vatican2Index, color='red', linewidth=2)
        plt.axvline(x=Vatican2Index, color='red', linewidth=2)
        
        ### Legend ###
        red_patch = mpatches.Patch(color='red', label='Vatican II Boundary')
        plt.legend(handles=[red_patch], loc='upper left')
    
    ### Aesthetics ###
    plt.title("Similarity Between Papal Topic Distributions", fontsize=16)
    plt.tight_layout()

    ### Return ###
    return plt
