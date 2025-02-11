### Packages ###
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

### Function ###
def PlotCouncilEncyclicalSimilarityScore(PopeSimilarity):

    ### Plot ###
    YPosition = np.arange(len(PopeSimilarity))
    fig, ax = plt.subplots(figsize=(10, 6))

    ### For each pope ###
    for i, row in PopeSimilarity.iterrows():

        ## Plot connecting line ##
        ax.plot([row["Vatican1_Similarity"], 
                 row["Vatican2_Similarity"]], 
                 [YPosition[i] + 0.15, YPosition[i] - 0.15], 
                 color='gray', linestyle='dashed', alpha=0.7)
        
        ## Vatican 1 ##
        ax.errorbar(row["Vatican1_Similarity"], 
                    YPosition[i] + 0.15, 
                    xerr=row["Vatican1_StdDev"], 
                    fmt='o', 
                    color='blue', 
                    label='Vatican I Similarity' if i == 0 else "")
        
        ## Vatican 2 ##
        ax.errorbar(row["Vatican2_Similarity"], 
                    YPosition[i] - 0.15, 
                    xerr=row["Vatican2_StdDev"], 
                    fmt='o', 
                    color='orange',
                    label='Vatican II Similarity' if i == 0 else "")

    ### Aesthetics ###
    ax.set_yticks(YPosition)
    ax.set_yticklabels(PopeSimilarity["PopeName"])
    ax.set_xlabel("Similarity Score")
    ax.set_title("Similarity of Popes' Encylicals to the Documents of Vatican I and II")
    ax.legend()
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()
