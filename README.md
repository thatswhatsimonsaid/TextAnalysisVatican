# Transition of Language in the Catholic Church

## Analysis of Linguistic Shifts in Papal Encyclicals Before and After Vatican II

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains code and data for computational analysis of linguistic shifts in papal encyclicals, examining changes in language and thematic content before and after the Second Vatican Council (1962-1965).

## Main Results

**View the complete results:**
- [Research Poster (PDF)](https://github.com/thatswhatsimonsaid/TextAnalysisVatican/blob/main/CSSS594_Poster.pdf)
- [Full Report (PDF)](https://github.com/thatswhatsimonsaid/TextAnalysisVatican/blob/main/CSSS594_Report.pdf)

## Project Overview

This research applies computational text analysis methods to explore how papal language has evolved from Pope Leo XIII (1878-1903) to Pope Francis (2013-present). Using a combination of word frequency analysis, topic modeling, and cosine similarity measures, the project quantitatively demonstrates a transition from divine-centered to more human-centered theological discourse.

Key findings include:
- Increased frequency of human-centered terminology in post-Vatican II encyclicals
- Evolution of topic distributions showing greater emphasis on social and moral themes
- Growing semantic integration between previously separated concept pairs (faith-reason, divine-human)

## Repository Contents

- `Code/`: Python scripts for data collection, preprocessing, and analysis
  - `utils/Encylicals/`: Utilities for extracting and processing papal documents
  - `utils/Main/`: Core analysis functions 
  - `utils/Plots/`: Visualization scripts
- `Results/`: 
  - `Images/`: Visualizations of analysis results
    - `WordFrequency/`: Diverging bar charts of word frequencies
    - `TopicModelling/`: Topic similarity plots, heatmaps, and evolution charts
    - `CosineSimilarity/`: Plots tracking concept relation changes over time
  - `Data/`: Processed data files
- `CSSS594_Poster.pdf`: Academic poster summarizing research findings
- `CSSS594_Report.pdf`: Comprehensive research report

## Methodology

1. **Data Collection**: Scraped papal encyclicals from the Vatican's official website
2. **Preprocessing**: Cleaned, tokenized, and lemmatized documents using NLTK and spaCy
3. **Analysis**:
   - Word frequency analysis comparing divine vs. human terminology
   - LDA topic modeling to track thematic changes over time
   - Cosine similarity measurements to examine conceptual relationships

## Key Functions

- `ExtractEncylicalContent`: Extracts clean text from Vatican website HTML
- `ProcessText`: Implements text preprocessing pipeline
- `WordFrequencyAnalysis`: Calculates relative term frequencies
- `TopicModellingFunction`: Performs LDA topic modeling
- `CosineSimilarityFunction`: Measures semantic proximity between concept pairs

## Results

The analysis provides quantitative evidence for a shift in papal discourse following Vatican II, characterized by:

1. Significant increases in terms related to human experience and social engagement
2. A notable decrease in doctrinal content with corresponding increases in social/moral topics
3. Progressive integration of previously separated conceptual domains
4. Evolutionary rather than revolutionary linguistic change

## Requirements

- Python 3.8+
- Required packages:
  - BeautifulSoup4
  - NLTK
  - spaCy
  - Gensim
  - NumPy
  - SciPy
  - pandas
  - matplotlib
  - seaborn
