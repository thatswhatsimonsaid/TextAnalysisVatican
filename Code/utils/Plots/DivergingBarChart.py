import matplotlib.pyplot as plt
import numpy as np

### Function ###
def DivergingBarChartFunction(DF_Input, Col1, Col2, NWords=15, figsize=(12, 8)):

    ### Set Up ###
    DF_Filtered = DF_Input[[Col1, Col2]].copy()
    DF_Filtered.loc[:, "Difference"] = DF_Filtered[Col1] - DF_Filtered[Col2] 

    ### Sort by Top Words ###
    TopWords = DF_Filtered.copy()
    TopWords['AbsoluteDifference'] = abs(TopWords['Difference'])
    TopWords = TopWords.nlargest(NWords, 'AbsoluteDifference')
    TopWords = TopWords.sort_values('Difference')
    
    ### Plot ###
    fig, ax = plt.subplots(figsize=figsize)
    y_pos = np.arange(len(TopWords))
    colors = ['blue' if x < 0 else 'orange' for x in TopWords['Difference']]
    bars = ax.barh(y_pos, TopWords['Difference'], color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(TopWords.index)
    ax.axvline(x=0, color='black', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ## Aesthetics ##
    ax.set_xlabel('Difference in Word Frequency Percentage (percentage points)')
    ax.set_title('Word Frequency Comparison \nDifferences shown in percentage points (%)')

    ## Legends ##
    from matplotlib.patches import Patch
    LegendElements = [
        Patch(facecolor='orange', label= f'{Col1} uses more'),
        Patch(facecolor='blue', label= f'{Col2} uses more')
    ]
    ax.legend(handles=LegendElements, loc='upper left')
    
    ## Labels ##
    for i, bar in enumerate(bars):
        width = bar.get_width()
        XLabel = width + (0.01 if width >= 0 else -0.01)
        HaLabel = 'left' if width >= 0 else 'right'
        ax.text(XLabel, bar.get_y() + bar.get_height()/2, 
                f'{width:.3f}', 
                va='center', 
                ha=HaLabel)
    
    plt.tight_layout()
    return fig, ax
