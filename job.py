import spacy

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def job_description(job_details) -> dict:
    """
    This block of code filters stopwords from the job and returns a clean set of keywords.
    Uses spaCy for tokenization and POS tagging to extract meaningful words.
    """
    
    job_keywords = []
    job_phrases = []
    phrase_list = ["rest api", "machine learning"]
    
    # Words to lowercase
    normalized_job = job_details.lower()
    
    # Find the phrase list in the job
    for phrase in phrase_list:
        if phrase in normalized_job:
            job_phrases.append(phrase)
    
    # Process with spaCy
    doc = nlp(normalized_job)
    
    # Extract phrase words to filter them out later
    phrase_word_list = []
    for item in job_phrases:
        phrase_word_list += item.split()
    
    # Extract keywords: filter stop words, punctuation, and words part of phrases
    for token in doc:
        # Skip if it's a stop word, punctuation, or part of a phrase
        if token.is_stop or token.is_punct or token.text in phrase_word_list:
            continue
        
        # Only keep words with length >= 3
        if len(token.text) >= 3 and token.text.isalpha():
            job_keywords.append(token.text)
    
    result = {"keywords": job_keywords, "phrases": job_phrases}
    
    return result
    
if __name__ == "__main__":
    print("hello")
