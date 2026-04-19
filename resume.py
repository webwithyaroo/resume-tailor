
from nlp_utils import extract_keywords


def resume_tailor(resume_details) -> dict:
    """
    This block of code filters stopwords from the resume and returns a clean set of keywords.
    Uses spaCy for tokenization and POS tagging to extract meaningful words.
    """
    
    return extract_keywords(resume_details)


if __name__ == "__main__":
    print("hello")
