### Packages ###
from datetime import datetime
import re

### Function ###
def ExtractDateFromURL(url):
    try:

        ## Extract PopeName name from URL ##
        PopeMatch = re.search(r'content/([^/]+)/en', url)
        PopeName = PopeMatch.group(1)
        
        ### Pope Francis Special Pattern ####
        if PopeName == 'francesco':
            DateMatch = re.search(r'/(\d{8})-', url)                       # Try (YYYYMMDD) format
            if not DateMatch:
                DateMatch = re.search(r'francesco_(\d{8})_', url)          # Try (YYYYMMDD) format 
            if DateMatch:
                DateString = DateMatch.group(1)
                return datetime.strptime(DateString, '%Y%m%d')
        
        ### Other Pope ###
        DateMatch = re.search(r'_enc_(\d{8})_', url)      
        DateString = DateMatch.group(1)
        
        ### List of Execption URLs that use DDMMYYYY format (ChatGPT helped me here) ###
        DDMMYYY_URLS_urls = ["hf_p-xi_enc_31121929_divini-illius-magistri"]
        
        ### Exception List ###
        if any(pattern in url for pattern in DDMMYYY_URLS_urls):
            return datetime.strptime(DateString, '%d%m%Y')
        
        ### Special Pattern for Benedict XVI and John Paul II (YYYYMMDD) ###
        if PopeName == 'benedict-xvi' or (PopeName == 'john-paul-ii' and DateString.startswith('200')):
            return datetime.strptime(DateString, '%Y%m%d')
        
        ### Other Pope (YYYYMMDD) ####
        try:
            return datetime.strptime(DateString, '%Y%m%d')
        except ValueError:
            return datetime.strptime(DateString, '%d%m%Y')    # If YYYYMMDD fails, try DDMMYYYY
            
    ### Errors 
    except Exception as e:
        print(f"Error extracting date from URL {url}: {e}")
        return None