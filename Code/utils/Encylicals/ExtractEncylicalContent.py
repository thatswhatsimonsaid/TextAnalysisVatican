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
        
        ### Main Content Identification ###
        # Find the main content container
        main_content = None
        content_candidates = [
            soup.find('div', class_='text parbase container vaticanrichtext'),
            soup.find('div', id='content-body'),
            soup.find('div', class_='documento')
        ]
        
        for candidate in content_candidates:
            if candidate and len(candidate.get_text(strip=True)) > 200:
                main_content = candidate
                break
        
        # Fallback to entire document if no specific container is found
        if not main_content:
            main_content = soup
            
        # Get all paragraphs from the content area
        all_elements = main_content.find_all(['p', 'div', 'font', 'h1', 'h2', 'h3'])
        
        ### Document Structure Analysis ###
        # Extract document title/heading
        title_elements = soup.find_all(['h1', 'h2', 'h3'])
        title_text = ""
        for title in title_elements:
            text = title.get_text(strip=True)
            if len(text) > 5:  # Avoid empty or very short titles
                title_text = text
                break
        
        # Clean up elements and extract text
        paragraphs = []
        for elem in all_elements:
            text = elem.get_text(strip=True)
            if text and len(text) > 5:  # Skip empty or very short elements
                paragraphs.append(text)
        
        # Remove exact duplicates that appear consecutively
        filtered_paragraphs = []
        for i, para in enumerate(paragraphs):
            # Skip if this paragraph is identical to the previous one
            if i > 0 and para == paragraphs[i-1]:
                continue
            
            # Skip if this paragraph is identical to one recently seen (within last 5 paragraphs)
            is_recent_duplicate = False
            for j in range(max(0, i-5), i):
                if para == paragraphs[j]:
                    is_recent_duplicate = True
                    break
            
            if not is_recent_duplicate:
                filtered_paragraphs.append(para)
        
        paragraphs = filtered_paragraphs
        
        ### Content Processing ###
        content_parts = []
        content_started = False
        intro_found = False
        blessing_found = False
        seen_paragraphs = set()  # Track seen paragraphs to avoid duplicates
        
        # Special handling for Leo XIII encyclicals
        is_leo_xiii = "leo-xiii" in url.lower()
        
        # First, check if there's a substantial paragraph that doesn't start with a number
        # This is often the first paragraph in many encyclicals
        first_substantial_para = None
        for text in paragraphs:
            if len(text) > 150 and not re.match(r'^\d+\.', text) and "notices which daily come" in text:
                first_substantial_para = text
                break
        
        if first_substantial_para:
            if first_substantial_para not in seen_paragraphs:
                content_parts.append(first_substantial_para)
                seen_paragraphs.add(first_substantial_para)
                content_started = True
        
        # Now process the rest of the paragraphs
        for i, text in enumerate(paragraphs):
            # Skip if we've already added this text (happens with the first paragraph check above)
            if text in seen_paragraphs:
                continue
                
            # Skip document metadata and navigation elements
            if re.search(r'(share|print|pdf|previous|next|copyright|site index)', text, re.IGNORECASE):
                continue
            
            # Leo XIII encyclicals need special handling
            if is_leo_xiii and not content_started and len(text) > 150:
                content_started = True
                content_parts.append(text)
                seen_paragraphs.add(text)
                continue
                
            # Handle numbered paragraphs - especially important for getting paragraph 1
            if re.match(r'^1\.', text):
                content_started = True
                content_parts.append(text)
                seen_paragraphs.add(text)
                continue
                
            # Include other numbered paragraphs
            if re.match(r'^\d+\.\s', text):
                content_started = True
                content_parts.append(text)
                seen_paragraphs.add(text)
                continue
            
            # After finding content, any substantial paragraph that starts with common phrases is likely main content
            if len(text) > 100 and (text.startswith("The ") or text.startswith("We ") or 
                                   text.startswith("It ") or text.startswith("This ")) and not content_started:
                content_started = True
            
            # Include content once we've determined it's started
            if content_started:
                # Check for end of document
                end_patterns = [
                    r'Given (in|at) .+, (on|in) .+\d{1,2},? \d{4}',
                    r'Given in Rome.+(on|in) .+\d{1,2},? \d{4}',
                    r'in the \d+.? year of (my|our) (p|P)ontificate',
                    r'From (the|our) Vatican.+\d{1,2},? \d{4}',
                    r'Given at Rome',
                    r'token of Our love receive'  # Special ending pattern for Quae Ad Nos
                ]
                
                is_ending = False
                for pattern in end_patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        is_ending = True
                        if text not in seen_paragraphs:
                            content_parts.append(text)
                            seen_paragraphs.add(text)
                        break
                
                if is_ending:
                    break
                
                # Skip footnotes
                if re.match(r'^\[\d+\]', text) or re.match(r'^\d+\s+Cf\.', text):
                    continue
                    
                # Skip short fragment-like texts that are likely artifacts
                if len(text) < 15 and not re.search(r'^\d+\.', text):
                    continue
                
                # Final additions check - ensure it's not a duplicate
                if text not in seen_paragraphs:
                    # Check for similar text (to catch near-duplicates with minor differences)
                    is_similar = False
                    for existing in content_parts[-5:] if len(content_parts) > 5 else content_parts:
                        similarity = len(set(text.split()) & set(existing.split())) / len(set(text.split() + existing.split()))
                        if similarity > 0.9:  # 90% similar words
                            is_similar = True
                            break
                    
                    if not is_similar:
                        content_parts.append(text)
                        seen_paragraphs.add(text)
        
        # If we haven't found any content, try a more aggressive approach
        if not content_parts:
            # Get all substantial paragraphs
            substantial_texts = []
            seen_texts = set()
            
            for p in paragraphs:
                if len(p) > 150 and p not in seen_texts:
                    substantial_texts.append(p)
                    seen_texts.add(p)
            
            # Find the start of the document content
            for i, text in enumerate(substantial_texts):
                # Look for common starting patterns
                if (re.search(r'^(The|It is|This|We|I[^a-z])', text) or 
                    re.search(r'(church|christ|god|faith|doctrine|catholic)', text, re.IGNORECASE)):
                    content_parts = substantial_texts[i:]
                    break
            
            # If still no content, just use all substantial paragraphs
            if not content_parts:
                content_parts = substantial_texts
        
        # Remove any remaining duplicates that might have slipped through
        # Sometimes paragraphs are broken differently but contain the same text
        final_content = []
        final_seen = set()
        
        for text in content_parts:
            if text not in final_seen:
                # Also check for substrings - sometimes a paragraph appears both on its own and as part of another
                is_substring = False
                for existing in final_content:
                    if text in existing and text != existing:
                        is_substring = True
                        break
                
                if not is_substring:
                    final_content.append(text)
                    final_seen.add(text)
        
        # If we have content, join it and return
        if final_content:
            return '\n\n'.join(final_content)
        else:
            return "No content extracted. URL may be invalid or document structure not recognized."
        
    except requests.RequestException as e:
        return f"Error fetching {url}: {e}"
    except Exception as e:
        return f"Error processing document: {e}"