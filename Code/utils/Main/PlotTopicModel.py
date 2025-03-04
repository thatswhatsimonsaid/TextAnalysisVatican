### Import packages ###
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils.Main.CleanText import *

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
    
    # Set global font size for all plots
    plt.rcParams.update({'font.size': 14})  # Increase base font size
    
    ### Create Plot ###
    fig, ax = plt.subplots(figsize=(22, 10))  # Larger figure size
    
    # Create the heatmap with increased font sizes
    sns.heatmap(WordFreq, cmap="YlOrRd", annot=False, linewidths=0.5, ax=ax)
    
    ### Vatican II Line ###
    VaticanIIIndex = AvailablePopes.index('john_xxiii') if 'john_xxiii' in AvailablePopes else -1
    plt.axhline(y=VaticanIIIndex, color='blue', linewidth=3)  # Slightly thicker line
    # You can uncomment this to add the Vatican II label with larger font
    # plt.text(-2, VaticanIIIndex - 0.5, 'Vatican II', fontsize=16, color='blue', fontweight='bold')
    
    ### Aesthetics with bold text and larger fonts ###
    plt.title("Key Words Frequency Across Papal Encyclicals", fontsize=20, fontweight='bold')
    plt.ylabel("Pope", fontsize=18, fontweight='bold')
    plt.xlabel("Words", fontsize=18, fontweight='bold')
    
    # Set xticks rotation and larger font
    plt.xticks(rotation=45, ha='right', fontsize=16)
    plt.yticks(fontsize=16)
    
    # Make xtick labels bold
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')
    
    # Make ytick labels bold
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    
    # Add a color bar label with increased font size
    cbar = ax.collections[0].colorbar
    cbar.ax.set_ylabel("Frequency", fontsize=16, fontweight='bold')
    
    # Apply tighter layout but with more padding
    plt.tight_layout(pad=1.5)
    
    ### Return ###
    return plt

### Topic Model Similarity ###
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

### Topic Evolution Function ###
def CreateTopicEvolution(ProcessedDF):
    ### Categories to categorize topics ###
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
    
    # Set global font size for all plots
    plt.rcParams.update({'font.size': 14})  # Increase base font size
    
    ### Create plot with explicit figsize in inches ###
    fig, ax = plt.subplots(figsize=(22, 10))  # Slightly larger figure size
    
    # Make sure we have the right categories and order
    plot_categories = ['Doctrinal', 'Spiritual', 'Social', 'Moral', 'Other']
    
    # Create the stacked bar plot
    CategoryScore[plot_categories].plot(
        kind='bar', 
        stacked=True,
        colormap='tab10',
        ax=ax
    )
    
    ## Vatican II line ###
    # VaticanIIIndex = AvailablePopes.index('john_xxiii') if 'john_xxiii' in AvailablePopes else -1
    plt.axvline(x=VaticanIIIndex - 0.5, color='red', linestyle='--', linewidth=2)
    # plt.text(VaticanIIIndex - 0.5, 102, 'Vatican II', rotation=90, color='red', fontweight='bold', fontsize=16)
    
    ### Aesthetics with bold text and larger font sizes ###
    plt.title('Topic Category Distribution Across Papal Encyclicals', 
              fontsize=20, fontweight='bold')  # Larger bold title
    plt.ylabel('Percentage (%)', fontsize=18, fontweight='bold')  # Larger bold y-label
    plt.xlabel('', fontsize=18, fontweight='bold')  # Larger bold x-label
    
    # Set xticks rotation and larger font
    plt.xticks(rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    
    # Make xtick and ytick labels bold
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')
    
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    
    # Move legend to the bottom and arrange in one row with LARGER text
    legend = plt.legend(title='Category', loc='upper center', bbox_to_anchor=(0.5, -0.17), 
               ncol=5, fontsize=18, title_fontsize=20)  # Increased fontsize of legend text
    plt.setp(legend.get_title(), fontweight='bold')
    
    # Make the legend markers larger
    for handle in legend.legendHandles:
        handle.set_height(12)  # Increased height
        handle.set_width(24)   # Increased width
    
    # Make legend labels bold
    for text in legend.get_texts():
        text.set_fontweight('bold')
        text.set_fontsize(18)  # Ensure consistent font size
    
    plt.ylim(0, 100)
    
    # Add more space at bottom for the larger legend
    plt.tight_layout(rect=[0, 0.07, 1, 1])  # Added more space at bottom
    
    # Get the current figure
    fig = plt.gcf()
    
    # Return the figure
    return fig

### Topic Model Similarity ###
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
    
    # Create cleaned labels (remove "_Topics" suffix)
    CleanLabels = [pope.replace('_Topics', '') for pope in AvailablePopes]
    
    ### Plot ###
    plt.figure(figsize=(20, 8))
    
    # Create heatmap with bold annotations for values
    sns.heatmap(
        SimilarityDF, 
        annot=True, 
        cmap="YlGnBu", 
        vmin=0, 
        vmax=1,
        fmt=".2f",
        linewidths=0.5,
        annot_kws={"weight": "bold"},  # Bold values in cells
        xticklabels=CleanLabels,  # Use clean labels without "_Topics"
        yticklabels=CleanLabels   # Use clean labels without "_Topics"
    )
    
    ### Add markers for pre/post Vatican II ###
    Vatican2Index = AvailablePopes.index('john_xxiii_Topics') if 'john_xxiii_Topics' in AvailablePopes else -1
    if Vatican2Index > 0:
        plt.axhline(y=Vatican2Index, color='red', linewidth=2)
        plt.axvline(x=Vatican2Index, color='red', linewidth=2)
        
        ### Legend ###
        # red_patch = mpatches.Patch(color='red', label='Vatican II Boundary')
        # plt.legend(handles=[red_patch], loc='upper left')
    
    ### Aesthetics ###
    # Bold title
    plt.title("Similarity Between Papal Topic Distributions", fontsize=16, weight='bold')
    
    # Bold and rotate tick labels
    plt.xticks(rotation=45, ha='right', weight='bold')  # Rotate x-ticks 45 degrees and make bold
    plt.yticks(weight='bold')  # Make y-ticks bold
    
    plt.tight_layout()

    ### Return ###
    return plt
