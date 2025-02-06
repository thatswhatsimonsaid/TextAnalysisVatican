import pandas as pd
from .CleanText import *
from gensim import corpora
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel


def TopicModellingFunction(TextInput, NumTopics, StopWordsInput):

    ### Set Up ###
    TokenizedWords = []                                                               # Initialize list for tokenized words
    # Text = TextInput["Text"].copy()                                                 # Get the Text from the data frame

    ### Preprocessing ###
    for text in TextInput["Text"]:
        TextedCleaned = ProcessText(text)
        TokenizedWords.append(TextedCleaned)

    ### Reformat for Topic Modelling with GenSim ###
    CorporaDictionary = corpora.Dictionary(TokenizedWords)                              # Create gensim dictionary
    CorporaMatrix = [CorporaDictionary.doc2bow(word) for word in TokenizedWords]        # Create gensim matrix

    ### Latent Dirichlet Allocation Model #
    LDA_Model = LdaModel(CorporaMatrix, num_topics=NumTopics, id2word=CorporaDictionary, passes=10)

    ### Get Domintant Topic ###
    DocTopicProbability = [LDA_Model.get_document_topics(doc) for doc in CorporaMatrix]      # Probability of being in each topic
    DomintantTopic = [max(topics, key=lambda x: x[1])[0] for topics in DocTopicProbability]  # Get the most probable topic
    TextInput["DomintantTopic"] = DomintantTopic                                             # Append it to df

    ### Get Coherence Score ###
    Coherence_Model = CoherenceModel(model=LDA_Model, texts=TokenizedWords, dictionary=CorporaDictionary, coherence='c_v')
    CoherenceScore = Coherence_Model.get_coherence()

    ### Extract Top Words for Each Topic (Filtering Stopwords Again) ###
    TopWordsPerTopic = []
    for TopicIndex in range(NumTopics):
        words = [word for word, _ in LDA_Model.show_topic(TopicIndex, topn=20)]  # Get more words to account for filtering
        filtered_words = [word for word in words if word.lower() not in StopWordsInput]  # Remove stopwords
        TopWordsPerTopic.append(", ".join(filtered_words[:10]))  # Keep top 10 informative words

    ### Manually Assign Labels (Modify Based on Inspection) ###
    TopicLabels = [f"Topic {i+1} Label" for i in range(NumTopics)]              # Placeholder labels

    ### Extract Top Example Documents for Each Topic ###
    TopDocsPerTopic = {i: [] for i in range(NumTopics)}
    for i, topics in enumerate(DocTopicProbability):
        DominantTopic = max(topics, key=lambda x: x[1])[0]                   # Get the most probable topic
        TopDocsPerTopic[DominantTopic].append(TextInput["Text"][i])      # Store original title
    TopExamples = {i: TopDocsPerTopic[i][:2] if len(TopDocsPerTopic[i]) >= 2 else TopDocsPerTopic[i] + [""] for i in range(NumTopics)}

    ### Create CSV Dataframe ###
    df_output = pd.DataFrame({
        "Topic": range(1, NumTopics + 1),
        "Your label for topic": TopicLabels,
        "TopTerms": TopWordsPerTopic,  
        "Top document example 1": [TopExamples[i][0] if len(TopExamples[i]) > 0 else "" for i in range(NumTopics)],
        "Top document example 2": [TopExamples[i][1] if len(TopExamples[i]) > 1 else "" for i in range(NumTopics)]
    })

    ### Return ###
    Output = {
        "TextInput": TextInput,
        "df_output": df_output,
        "CoherenceScore": CoherenceScore
    }
    return Output
