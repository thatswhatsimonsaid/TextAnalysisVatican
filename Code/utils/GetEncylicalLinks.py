### Packages ###
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

### Function ###
def GetEncylicalLinks(IndexURL, language="English"):

    ### Set Up ###
    EncylicalLinks = []
    PageNum = 1
    
    # While there are still pages left #
    while True:
        ### Page Number ###
        if PageNum == 1:
            EnylicalURL = IndexURL
        else:
            EnylicalURL = IndexURL.replace('.html', f'.{PageNum}.html')
        
        ### Try Page Number ###
        try:
            response = requests.get(EnylicalURL) # Get page number
            if response.status_code != 200:      # Exit if page number does not exist
                break
                
            ### Parse HTML ###
            soup = BeautifulSoup(response.text, 'html.parser')
            
            ### Track number of links ###
            FoundLinks = 0
            
            ### Get Encylicals ###
            for li in soup.find_all("li"):
                for a_tag in li.find_all("a"):

                    ## Language ##
                    language_match = (
                        (language.lower() in a_tag.text.lower()) or
                        (a_tag.find("span", string=lambda x: x and language.lower() in x.lower())) or
                        (any(span.text.lower() == language.lower() for span in li.find_all("span")))
                    )
                    
                    ## Construct URL ##
                    if language_match and a_tag.get("href"):
                        if a_tag["href"].startswith("/"):
                            encyclical_link = urljoin("https://www.vatican.va", a_tag["href"])
                        elif a_tag["href"].startswith("http"):
                            encyclical_link = a_tag["href"]
                        else:
                            continue
                         
                        ## Append URL and add 1 to FoundLinks ##
                        EncylicalLinks.append(encyclical_link)
                        FoundLinks += 1
            
            ## Break Loop if no Encyclical ##
            if FoundLinks == 0:
                break
                
            ### Next Page ###
            PageNum += 1
            
        except requests.RequestException as e:
            print(f"Error fetching {EnylicalURL}: {e}")
            break
    
    return EncylicalLinks