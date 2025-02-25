### Packages ###
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

### Function ###
def ProcessText(text, StopWords=None):

    ### Initialize Lemmatizer ###
    lemmatizer = WordNetLemmatizer()
    
    ### Clean Text ###
    text = text.lower()                                                       # Lower case words
    text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/{}<>\\^`~]', ' ', text)       # Remove special characters
    text = re.sub(r'\b\d+\b|\b\w{1,4}\b', '', text)                           # Remove numbers & short words (≤4 chars)
    text = re.sub(r'\s+', ' ', text).strip()                                  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)                                   # Keep only letters and spaces
    text = re.sub(r'\s+', ' ', text).strip()                                  # Remove extra spaces  
    
    ### Tokenize ###
    words = word_tokenize(text)

    ### Lemmatize if not in stop words###
    Output = [lemmatizer.lemmatize(word) for word in words if not StopWords or word not in StopWords]
    
    return Output