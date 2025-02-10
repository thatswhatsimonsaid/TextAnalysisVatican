import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def PlotSentimentScores(df, SentimentScore):

    ### Set Up  ###
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ### Format Date ###
    df['DocumentDate'] = pd.to_datetime(df['DocumentDate'])
    
    ### Get Pope ###
    PopeNameList = df['PopeName'].unique()
    ColorPalette = sns.color_palette('tab10', len(PopeNameList))
    PopeColorPalette = dict(zip(PopeNameList, ColorPalette))
    
    ### Plot Each Pope ###
    for pope in PopeNameList:
        PopeDF = df[df['PopeName'] == pope]
        ax.plot(PopeDF['DocumentDate'], 
                PopeDF[SentimentScore], 'o-', 
                alpha=0.6, 
                markersize=4, 
                label=pope, 
                color=PopeColorPalette[pope])
    
    ### Decades Label ###
    ax.set_xticks(pd.date_range(start=df['DocumentDate'].min(), 
                                end=df['DocumentDate'].max(), 
                                freq='10YS'))
    ax.set_xticklabels(ax.get_xticks(), rotation=45, ha='right')
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    
    ### Aesthetics ###
    ax.set_title(SentimentScore.replace('Score', ' Sentiment'))
    ax.set_xlabel('Decade')
    ax.set_ylabel(SentimentScore)
    ax.grid(alpha=0.3)
    ax.legend(title='Pope', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)
    
    ### Plot ###
    plt.tight_layout()
    plt.show()
