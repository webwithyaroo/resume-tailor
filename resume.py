
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def _ensure_nltk_resources() -> None:
    resources = (
        ('corpora/stopwords', 'stopwords'),
        ('tokenizers/punkt', 'punkt'),
    )
    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


def resume_tailor(resume_details)-> dict:
        
    """ This block of code filters stopwords from the resume and return a clean set of keywords"""
    
    _ensure_nltk_resources()

    resume_keywords = []
    resume_phrases = []
    phrase_word_list = []
    phrase_list = ["rest api", "machine learning"]
    
    
    stop_words = set(stopwords.words("english"))
    
    
    # Words to lowercase
    normalized_resume = resume_details.lower()
    
    # Find the phrase list in the resume
    for phrase in phrase_list:
        if phrase in normalized_resume:
            resume_phrases.append(phrase)
    
    
    # Split normalized resume
    tokens = word_tokenize(normalized_resume)
    
    # Remove stop-words
    filter_token = [word for word in tokens if word not in stop_words]
    
    # Remove punctuation
    clean_tokens = [char for char in filter_token if char.isalpha()]
    
    
    for item in resume_phrases:
        phrase_word_list += item.split()
        
        
    # Remove words part of the phrases
    filter_keywords = [words for words in clean_tokens if words not in phrase_word_list]
    
    
    # Filter words > 3 only
    resume_keywords += [ char for char in filter_keywords if len(char) >= 3]
    
    result = {"keywords": resume_keywords, "phrases": resume_phrases}
    return result


if __name__ == "__main__":
    print("hello")
