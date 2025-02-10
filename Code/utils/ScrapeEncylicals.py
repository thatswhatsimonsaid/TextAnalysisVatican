### Packages ###
from .GetEncylicalLinks import *

### Function ###
def ScrapeEncyclicals(Language):
    
    ### All Pope's URLS ###
    PopeURLS = {
        "francesco": "https://www.vatican.va/content/francesco/en/encyclicals.index.html",
        "benedict_xvi": "https://www.vatican.va/content/benedict-xvi/en/encyclicals.index.html",
        "john_paul_ii": "https://www.vatican.va/content/john-paul-ii/en/encyclicals.index.html",
        "paul_vi": "https://www.vatican.va/content/paul-vi/en/encyclicals.index.html",
        "john_xxiii" : "https://www.vatican.va/content/john-xxiii/en/encyclicals.index.html",
        "pius_xii" : "https://www.vatican.va/content/pius-xii/en/encyclicals.index.html", 
        "pius_xi" : "https://www.vatican.va/content/pius-xi/en/encyclicals.index.html",
        "benedict_xv" : "https://www.vatican.va/content/benedict-xv/en/encyclicals.index.html",
        "pius_x" : "https://www.vatican.va/content/pius-x/en/encyclicals.index.html",
        "leo_xiii" : "https://www.vatican.va/content/leo-xiii/en/encyclicals.index.html",
    }
    
    ### Output ###
    Output = {}

    ### Get Output ###
    for pope, url in PopeURLS.items():
        Output[pope] = GetEncylicalLinks(url, Language)
        print(f"Found {len(Output[pope])} encyclicals for {pope}")
    
    return Output