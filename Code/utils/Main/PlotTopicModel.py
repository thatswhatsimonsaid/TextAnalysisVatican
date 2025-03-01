### Import packages ###
import gc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from nltk.corpus import stopwords
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from utils.Main.CleanText import *

### Context Vector Functions ###
def CalculateContextVectors(words, ConceptTerms1, ConceptTerms2, WindowSize=100):

    ### Build vocabulary and index mapping ###
    Vocabulary = sorted(set(words))
    WordToIndex = {word: i for i, word in enumerate(Vocabulary)}
    
    ### Initialize context vectors ###
    ContextVector1 = np.zeros(len(Vocabulary))
    ContextVector2 = np.zeros(len(Vocabulary))
    
    ### Build context vectors ###
    for i, word in enumerate(words):

        ## Process first concept terms ##
        if word in ConceptTerms1:
            WindowStart = max(0, i - WindowSize)
            WindowEnd = min(len(words), i + WindowSize + 1)
            
            for ContextPos in range(WindowStart, WindowEnd):
                if ContextPos != i:  # Skip the concept term itself
                    ContextWord = words[ContextPos]
                    ContextVector1[WordToIndex[ContextWord]] += 1
        
        ## Process second concept terms ##
        if word in ConceptTerms2:
            WindowStart = max(0, i - WindowSize)
            WindowEnd = min(len(words), i + WindowSize + 1)
            
            for ContextPos in range(WindowStart, WindowEnd):
                if ContextPos != i:  # Skip the concept term itself
                    ContextWord = words[ContextPos]
                    ContextVector2[WordToIndex[ContextWord]] += 1
    
    ### Return ###
    return ContextVector1, ContextVector2

def CalculateCosineSimilarity(words, ConceptTerms1, ConceptTerms2):

    ### Get context vectors ###
    ContextVector1, ContextVector2 = CalculateContextVectors(words, ConceptTerms1, ConceptTerms2)

    ### Calculate cosine similarity ###
    Similarity = cosine_similarity(csr_matrix(ContextVector1.reshape(1, -1)), csr_matrix(ContextVector2.reshape(1, -1)))[0][0]
    
    ### Return ###
    return Similarity

### Data Processing Functions ###
def GenerateTimePeriods(df, IntervalYears):

    ### Year ###
    MinYear = df['Year'].min()
    MaxYear = df['Year'].max()
    
    ### Adjust MinYear to start at a clean interval ###
    StartYear = MinYear - (MinYear % IntervalYears)
    if StartYear < MinYear:
        StartYear += IntervalYears
        
    ### Create list of time periods ###
    TimePeriods = []
    CurrentYear = StartYear
    while CurrentYear < MaxYear:
        EndYear = min(CurrentYear + IntervalYears - 1, MaxYear)
        TimePeriods.append((CurrentYear, EndYear))
        CurrentYear = EndYear + 1

    ### Return ###    
    return TimePeriods

def CalculateSimilarityScores(PeriodDocuments, ConceptTerms1, ConceptTerms2):

    ### Set Up ###
    StopWordsList = set(stopwords.words('english'))
    SimilarityScores = []
    
    ### Loop through documents ###
    for doc in PeriodDocuments['DocumentText']:

        ## Words ##
        words = ProcessText(doc, StopWords=StopWordsList)
        
        ## Calculate similarity and add to scores if positive ##
        Similarity = CalculateCosineSimilarity(words, ConceptTerms1, ConceptTerms2)
        if Similarity > 0:
            SimilarityScores.append(Similarity)
    
    ### Return ###
    return SimilarityScores

def CalculateConfidenceIntervals(SimilarityScores, NumBootstrap=1000):

    ### Mean ###
    MeanSimilarity = np.mean(SimilarityScores)
    
    ### Bootstrap for confidence interval ###
    BootstrapMeans = []
    for _ in range(NumBootstrap):
        BootstrapSample = np.random.choice(SimilarityScores, 
                                           size=len(SimilarityScores), 
                                           replace=True)
        BootstrapMeans.append(np.mean(BootstrapSample))
    
    ### Confidence Interval ###
    CILow = np.percentile(BootstrapMeans, 2.5)
    CIHigh = np.percentile(BootstrapMeans, 97.5)
    
     ### Return ###
    return MeanSimilarity, CILow, CIHigh

### Visualization Functions ###
def CreateProximityPlot(ResultsDF, ConceptName1, ConceptName2):

    ### Initialize ###
    fig, ax = plt.subplots(figsize=(20, 8))

    ### Make Plot ###
    ax.errorbar(
        x=ResultsDF['StartYear'] + (ResultsDF['EndYear'] - ResultsDF['StartYear']) / 2,
        y=ResultsDF['Proximity'],
        yerr=[ResultsDF['Proximity'] - ResultsDF['CI_Low'], 
              ResultsDF['CI_High'] - ResultsDF['Proximity']],
        fmt='o-',
        capsize=5,
        capthick=1.5,
        elinewidth=1.5,
        markersize=8
    )

    ### Add Vatican II Line ###
    ax.axvline(x=1962, color='r', linestyle='--', alpha=0.8, label='Vatican II (1962)')

    ### Aesthetics with bold text ###
    ax.set_ylabel(f'{ConceptName1}-{ConceptName2} Cosine Similarity', fontsize=14, fontweight='bold')
    ax.set_xlabel('Time Period', fontsize=14, fontweight='bold')
    
    # Escape the % symbol in the title with a backslash and make title bold
    ax.set_title(r'Cosine Similarity in Papal Encyclicals' + '\n' + 
                r'Evolution Over Time (with 95\% confidence interval)', 
                fontsize=16, fontweight='bold')
    
    ### Set Regular Decade X-Ticks with rotation and bold text ###
    MinYear = min(ResultsDF['StartYear'])
    MaxYear = 2024
    DecadeStart = (MinYear // 10) * 10  # Round down to nearest decade
    RegularTicks = np.arange(DecadeStart, MaxYear, 10)  # Create ticks every 10 years
    ax.set_xticks(RegularTicks)
    ax.set_xticklabels([str(year) for year in RegularTicks], 
                       rotation=45,  # Rotate x-ticks 45 degrees
                       fontweight='bold')  # Make x-ticks bold
    
    ### Make y-ticks bold ###
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontweight('bold')
    
    ### Set x-axis limits to end with Pope Francis's reign ###
    ax.set_xlim(MinYear, 2024)
    
    ax.grid(True, linestyle='--', alpha=0.7)
    
    ### Bold the legend ###
    legend = ax.legend(loc='best')
    plt.setp(legend.get_title(), fontweight='bold')
    
    ### Adjust layout for rotated x-ticks ###
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    
    ### Output ###
    return fig, ax

def AddPopeReignsToPlot(ax):

    ### Papal Reigns ###
    PopeReigns = [
        ("Leo XIII", 1878, 1903, "tab:red"),
        ("Pius X", 1903, 1914, "tab:green"),
        ("Benedict XV", 1914, 1922, "tab:blue"),
        ("Pius XI", 1922, 1939, "tab:purple"),
        ("Pius XII", 1939, 1958, "tab:orange"),
        ("John XXIII", 1958, 1963, "tab:brown"),
        ("Paul", 1963, 1978, "tab:pink"),
        ("John Paul I", 1978, 1978, "tab:gray"),
        ("John Paul II", 1978, 2005, "tab:cyan"),
        ("Benedict XVI", 2005, 2013, "tab:olive"),
        ("Francis", 2013, 2024, "tab:blue")
    ]
    
    ### Pope Color Bars ###
    BarHeight = 0.01
    YMin, YMax = ax.get_ylim()
    
    ### Plot Papal Color Bars ###
    for Pope, Start, End, Color in PopeReigns:

        ## Draw Pope Color Bar ##
        rect = mpatches.Rectangle(
            (Start, YMin), 
            End - Start, 
            (YMax - YMin) * BarHeight,
            edgecolor='black', 
            facecolor=Color, 
            alpha=0.8,
            transform=ax.transData,
            clip_on=False,
            zorder=100
        )
        ax.add_patch(rect)
        
        ## Add Pope Name with bold text ##
        ax.text(
            Start + (End - Start)/2,
            YMin + (YMax - YMin) * 0.03,
            Pope,
            ha='center', 
            va='bottom', 
            fontsize=9,
            fontweight='bold',
            bbox=dict(facecolor='white', alpha=0.8, pad=0.2, boxstyle='round', edgecolor='gray'),
            transform=ax.transData,
            zorder=101
        )
    
    ### Return ###
    return ax

def AddConceptLabels(fig, ConceptName1, ConceptName2, ConceptTerms1, ConceptTerms2):
    
    ### Spacing ###
    plt.subplots_adjust(bottom=0.20)  # Increase bottom margin for two lines of text
    
    ### Format concept terms ###
    terms1_str = ", ".join(ConceptTerms1)
    terms2_str = ", ".join(ConceptTerms2)
    
    ### Handle line wrapping ###
    max_chars = 80
    
    # Handle line wrapping for concept 1
    if len(terms1_str) > max_chars:
        # Split into chunks of max_chars
        chunks1 = []
        current_chunk = ""
        for term in ConceptTerms1:
            if len(current_chunk + term + ", ") > max_chars and current_chunk:
                chunks1.append(current_chunk.rstrip(", "))
                current_chunk = term + ", "
            else:
                current_chunk += term + ", "
        if current_chunk:
            chunks1.append(current_chunk.rstrip(", "))
        
        concept1_text = f"\\textbf{{{ConceptName1} concept words:}}\n" + "\n".join(chunks1)
    else:
        concept1_text = f"\\textbf{{{ConceptName1} concept words:}} {terms1_str}"
    
    # Handle line wrapping for concept 2
    if len(terms2_str) > max_chars:
        # Split into chunks of max_chars
        chunks2 = []
        current_chunk = ""
        for term in ConceptTerms2:
            if len(current_chunk + term + ", ") > max_chars and current_chunk:
                chunks2.append(current_chunk.rstrip(", "))
                current_chunk = term + ", "
            else:
                current_chunk += term + ", "
        if current_chunk:
            chunks2.append(current_chunk.rstrip(", "))
        
        concept2_text = f"\\textbf{{{ConceptName2} concept words:}}\n" + "\n".join(chunks2)
    else:
        concept2_text = f"\\textbf{{{ConceptName2} concept words:}} {terms2_str}"
    
    ### Add concept texts with bold text ###
    fig.text(0.5, 0.07, concept1_text, ha='center', fontsize=10, fontweight='bold',
           bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5', 
                     edgecolor='gray', linewidth=1))
    
    fig.text(0.5, 0.01, concept2_text, ha='center', fontsize=10, fontweight='bold',
           bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5', 
                     edgecolor='gray', linewidth=1))
    
    ### Return ###
    return fig

### Main Analysis Function ###
def CosineSimilarityFunction(df_Encyclicals, IntervalYears, MinDocs, Concept1, Concept2):

    ### Concept Terms and Keys ###
    ConceptName1 = list(Concept1.keys())[0]
    ConceptName2 = list(Concept2.keys())[0]
    ConceptTerms1 = list(Concept1.values())[0]
    ConceptTerms2 = list(Concept2.values())[0]
    ConceptTerms1 = [c.lower() for c in ConceptTerms1]
    ConceptTerms2 = [c.lower() for c in ConceptTerms2]

    ### Prepare DataFrame ###
    df = df_Encyclicals.copy()
    df['DocumentDate'] = pd.to_datetime(df['DocumentDate'])
    df['Year'] = df['DocumentDate'].dt.year
    
    ### Generate time periods ###
    TimePeriods = GenerateTimePeriods(df, IntervalYears)

    ### Calculate Similarities for Each Period ###
    Results = []
    for StartYear, EndYear in TimePeriods:
        ## Filter documents for the current time period ##
        PeriodDocuments = df[(df['Year'] >= StartYear) & (df['Year'] <= EndYear)]
        
        ## Skip periods with insufficient documents ##
        if len(PeriodDocuments) < MinDocs:
            print(f"Skipping period {StartYear}-{EndYear}: insufficient documents ({len(PeriodDocuments)} found, minimum {MinDocs} required)")
            continue
        
        ## Calculate similarity scores ##
        SimilarityScores = CalculateSimilarityScores(PeriodDocuments, ConceptTerms1, ConceptTerms2)
        
        ## Skip periods with no similarity scores ##
        if not SimilarityScores:
            print(f"Skipping period {StartYear}-{EndYear}: no similarity scores found (tried {len(PeriodDocuments)} documents)")
            continue
        
        ## Calculate statistics with confidence intervals ##
        MeanSimilarity, CILow, CIHigh = CalculateConfidenceIntervals(SimilarityScores)
        
        ## Store period results ##
        Results.append({
            'StartYear': StartYear,
            'EndYear': EndYear,
            'Proximity': MeanSimilarity,
            'CI_Low': CILow,
            'CI_High': CIHigh,
            'NumDocs': len(PeriodDocuments),
            'ScoredDocs': len(SimilarityScores)
        })
        
        ## Clean up ##
        gc.collect()

    ### Format Results ###
    ResultsDF = pd.DataFrame(Results)
    
    ### Create Visualization ###
    fig, ax = CreateProximityPlot(ResultsDF, ConceptName1, ConceptName2)
    ax = AddPopeReignsToPlot(ax)
    fig = AddConceptLabels(fig, ConceptName1, ConceptName2, ConceptTerms1, ConceptTerms2)
        
    ### Print Summary ###
    print("\nSummary of results:")
    print(ResultsDF[['StartYear', 'EndYear', 'Proximity', 'NumDocs', 'ScoredDocs']])
    print(f"\nAnalysis used {IntervalYears}-year intervals with minimum {MinDocs} documents per period")
    print(f"Analysis used cosine similarity for measuring concept proximity")
    
    # Return results and figure
    return ResultsDF, fig, None


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
    
    ### Create plot with explicit figsize in inches ###
    fig, ax = plt.subplots(figsize=(20, 8))  # Force exact figure size
    
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
    VaticanIIIndex = AvailablePopes.index('john_xxiii') if 'john_xxiii' in AvailablePopes else -1
    plt.axvline(x=VaticanIIIndex - 0.5, color='red', linestyle='--', linewidth=2)
    plt.text(VaticanIIIndex - 0.5, 102, 'Vatican II', rotation=90, color='red', fontweight='bold', fontsize=12)
    
    ### Aesthetics with bold text ###
    plt.title('Topic Category Distribution Across Papal Encyclicals', 
              fontsize=16, fontweight='bold')  # Bold title
    plt.ylabel('Percentage (%)', fontsize=14, fontweight='bold')  # Bold y-label
    plt.xlabel('Pope', fontsize=14, fontweight='bold')  # Bold x-label
    
    # Make x-ticks and y-ticks bold
    plt.xticks(rotation=45, fontweight='bold')
    plt.yticks(fontweight='bold')
    
    # Move legend to the bottom and arrange in one row
    legend = plt.legend(title='Category', loc='upper center', bbox_to_anchor=(0.5, -0.15), 
               ncol=5)
    plt.setp(legend.get_title(), fontweight='bold')
    
    plt.ylim(0, 100)
    
    # Adjust layout to make room for legend at the bottom
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    
    # Get the current figure
    fig = plt.gcf()
    
    # Return the figure
    return fig


### Combined Similarity Plot Functions ###
def CreateCombinedProximityPlot(ResultsDF1, ResultsDF2, ConceptName1A, ConceptName1B, ConceptName2A, ConceptName2B):
    """
    Create a combined plot showing both sets of concept relationships,
    without the concept word labels at the bottom.
    
    Parameters:
    ResultsDF1 - DataFrame with Faith-Reason results
    ResultsDF2 - DataFrame with Divine-Human results
    ConceptNameXY - The concept names for labeling
    """
    
    # Initialize with exact figsize of 20x8 inches
    fig, ax = plt.subplots(figsize=(20, 8))
    
    # Plot Faith-Reason data
    line1 = ax.errorbar(
        x=ResultsDF1['StartYear'] + (ResultsDF1['EndYear'] - ResultsDF1['StartYear']) / 2,
        y=ResultsDF1['Proximity'],
        yerr=[ResultsDF1['Proximity'] - ResultsDF1['CI_Low'], 
              ResultsDF1['CI_High'] - ResultsDF1['Proximity']],
        fmt='o-',
        capsize=5,
        capthick=1.5,
        elinewidth=1.5,
        markersize=8,
        color='blue',
        label=f'{ConceptName1A}-{ConceptName1B}'
    )
    
    # Plot Divine-Human data
    line2 = ax.errorbar(
        x=ResultsDF2['StartYear'] + (ResultsDF2['EndYear'] - ResultsDF2['StartYear']) / 2,
        y=ResultsDF2['Proximity'],
        yerr=[ResultsDF2['Proximity'] - ResultsDF2['CI_Low'], 
              ResultsDF2['CI_High'] - ResultsDF2['Proximity']],
        fmt='s-',  # Square markers to differentiate
        capsize=5,
        capthick=1.5,
        elinewidth=1.5,
        markersize=8,
        color='green',  # Different color
        label=f'{ConceptName2A}-{ConceptName2B}'
    )
    
    # Add Vatican II Line
    ax.axvline(x=1962, color='r', linestyle='--', alpha=0.8, label='Vatican II (1962)')
    
    # Aesthetics with bold text
    ax.set_ylabel('Cosine Similarity', fontsize=14, fontweight='bold')
    ax.set_xlabel('Time Period', fontsize=14, fontweight='bold')
    
    # Escape the % symbol in the title with a backslash and make title bold
    ax.set_title(r'Cosine Similarity in Papal Encyclicals' + '\n' + 
                r'Evolution Over Time (with 95\% confidence interval)', 
                fontsize=16, fontweight='bold')
    
    # Set Regular Decade X-Ticks with rotation and bold text
    MinYear = min(min(ResultsDF1['StartYear']), min(ResultsDF2['StartYear']))
    MaxYear = 2024
    DecadeStart = (MinYear // 10) * 10  # Round down to nearest decade
    RegularTicks = np.arange(DecadeStart, MaxYear, 10)  # Create ticks every 10 years
    ax.set_xticks(RegularTicks)
    ax.set_xticklabels([str(year) for year in RegularTicks], 
                       rotation=45,  # Rotate x-ticks 45 degrees
                       fontweight='bold')  # Make x-ticks bold
    
    # Make y-ticks bold
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontweight('bold')
    
    # Set x-axis limits
    ax.set_xlim(MinYear, 2024)
    
    # Add grid and legend
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Move legend to the right side outside the plot with bold title
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), 
                     fontsize=12)
    plt.setp(legend.get_title(), fontweight='bold')
    
    # Adjust layout to make room for legend and rotated x-ticks
    plt.tight_layout(rect=[0, 0.05, 0.85, 1])
    
    # Return the figure and axis
    return fig, ax

def CombinedAnalysisFunction(df_Encyclicals, IntervalYears, MinDocs, 
                            Concept1A, Concept1B, Concept2A, Concept2B):
    """
    Run analysis for both concept pairs and create a combined visualization.
    
    Parameters:
    df_Encyclicals - DataFrame with the encyclical documents
    IntervalYears - Size of time intervals to analyze
    MinDocs - Minimum number of documents needed per period
    ConceptXY - Dictionaries containing concept names and terms
    """
    
    # Run the first analysis (Faith-Reason)
    ResultsDF1, _, _ = CosineSimilarityFunction(
        df_Encyclicals, IntervalYears, MinDocs, Concept1A, Concept1B
    )
    
    # Run the second analysis (Divine-Human)
    ResultsDF2, _, _ = CosineSimilarityFunction(
        df_Encyclicals, IntervalYears, MinDocs, Concept2A, Concept2B
    )
    
    # Get concept information
    ConceptName1A = list(Concept1A.keys())[0]
    ConceptName1B = list(Concept1B.keys())[0]
    ConceptName2A = list(Concept2A.keys())[0]
    ConceptName2B = list(Concept2B.keys())[0]
    
    # Create the combined visualization
    fig, ax = CreateCombinedProximityPlot(
        ResultsDF1, ResultsDF2, 
        ConceptName1A, ConceptName1B, 
        ConceptName2A, ConceptName2B
    )
    
    # Add pope reigns to the plot
    ax = AddPopeReignsToPlot(ax)
    
    # Print summary
    print("\nSummary of combined analysis:")
    print(f"Analysis used {IntervalYears}-year intervals with minimum {MinDocs} documents per period")
    print(f"Analysis used cosine similarity for measuring concept proximity")
    
    # Return results and figure
    return ResultsDF1, ResultsDF2, fig
