### Packages ###
import requests
from bs4 import BeautifulSoup
import re

### Function ###
def ExtractEncylicalContent(url):
    try:

        ### Parse HTML ###
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        ContentParts = []
        
        ### All Paragraphs ###
        paragraphs = soup.find_all(['p', 'div'])
        ContentStarted = False
        
        ### End Patterns (ChatGPT helped me get these patterns yay) ###
        EndPatterns = [
            # Standard location/date patterns
            r'Given (in|at) .+, (on|in) .+',
            
            # Anniversary patterns
            r'(the|my) \d+.+(year|anniversary) of (my Pontificate|my priesthood|the Rosary)',
            
            # Modern Pope signature patterns
            r'BENEDICT(US)? PP\. XVI',
            r'IOANNES PAULUS( PP\.)? II',
            r'FRANCISCUS( PP\.)?',
            r'PAULUS( PP\.)? VI',
            r'PIUS( PP\.)? (IX|X|XI|XII)',
            r'LEO( PP\.)? XIII',
            
            # Latin variations of signatures
            r'FRANCISCUS EPISCOPUS',
            r'Servus Servorum Dei',
            r'In Chr?isto Iesu',
            
            # Document section markers
            r'^NOTES$',
            r'^\[\d+\]',
            r'^\d+\s+Cf\.',
            
            # Additional document end markers
            r'Given at Saint Peter\'s in Rome',
            r'Given at Saint Peter\'s, Rome',
            r'From the Vatican',
            r'Ex Aedibus Vaticanis',
            
            # Year of pontificate patterns
            r'in the \d+.? year of (my|our) (p|P)ontificate',
            r'anno \d+.? Pontificatus (mei|nostri)',
            
            # Feast day references
            r'on the (Solemnity|Feast|Memorial) of .+',
            r'in festo .+',
            
            # Traditional Latin closings
            r'Datum Romae, apud Sanctum Petrum',
            r'sub anulo Piscatoris',
            
            # Document type endings
            r'Apostolic (Letter|Constitution|Exhortation)',
            r'Post-Synodal Exhortation',
            r'Motu Proprio'
        ]
        
        ### Combine all Patterns ###
        end_pattern = '|'.join(f'({pattern})' for pattern in EndPatterns)
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if not text:
                continue
            if re.match(r'^\d+\.', text): # If a text starts with a number followed by a period (REALLY BAD CONTENT STARTING SEPARATOR)
                ContentStarted = True
                
            # Include paragraphs who start with number followed by period (again, bad separator lol) #
            if ContentStarted:
                if re.search(end_pattern, text, re.IGNORECASE):                       # Check if we've reached any ending pattern
                    given_match = re.search(r'Given (in|at) .+', text, re.IGNORECASE) # Only include the "Given in Rome" part if it exists
                    if given_match:
                        ContentParts.append(given_match.group(0))
                    break
                    
                # Skip footnotes #
                if re.match(r'^\[\d+\]$', text):
                    continue
                    
                # Skip references #
                if re.match(r'^\d+\s+Cf\.', text):
                    continue

                # Append paragraph #    
                ContentParts.append(text)
        
        return '\n\n'.join(ContentParts)
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""