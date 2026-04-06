import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')


def job_description(job_details)-> tuple[list, list]:
    
    """ This block of code filters stopwords from the job and return a clean set of keywords"""
    
    job_keywords = []
    job_phrases = []
    phrase_word_list = []
    phrase_list = ["rest api", "machine learning"]
    
    
    stop_words = set(stopwords.words("english"))
    
    
    # Words to lowercase
    normalized_job = job_details.lower()
    
    # Find the phrase list in the job
    for phrase in phrase_list:
        if phrase in normalized_job:
            job_phrases.append(phrase)
    
    
    # Split normalized job
    tokens = word_tokenize(normalized_job)
    
    # Remove stop-words
    filter_token = [word for word in tokens if word not in stop_words]
    
    # Remove punctuation
    clean_tokens = [char for char in filter_token if char.isalpha()]
    
    
    for item in job_phrases:
        phrase_word_list += item.split()
        
        
    # Remove words part of the phrases
    filter_keywords = [words for words in clean_tokens if words not in phrase_word_list]
    
    
    # Filter words > 3 only
    job_keywords += [ char for char in filter_keywords if len(char) >= 3]
    
    
    return job_phrases, job_keywords
    
    
if __name__ == "__main__":
    print("hello")
