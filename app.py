from flask import Flask, request, render_template
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """ checks the method based on the req and return the form
    Returns:
        string: the output string
    """
    
    keywords = []
    phrases = []
    phrase_word_list = []
    phrase_list = ["rest api", "machine learning"]
    
    if request.method == "POST":
        
        resume = request.form.get("resume")
        job_desc = request.form.get("job_desc")
        
        # return (f"RESUME: {resume} \n JOB DESCRIPTION: {job_desc}")
        
        print("------ RESUME START ------")
        print(resume)
        print("------ RESUME END ------ \n")
        
       
        
        print("------ JOB DESC START ------")
        
        """ This block of code filters stopwords from the resume and return a clean set of keywords"""
        stop_words = set(stopwords.words("english"))
        normalized_job_desc = job_desc.lower()
        
        # Find the phrase list in the job_desc
        for phrase in phrase_list:
            if phrase in normalized_job_desc:
                phrases.append(phrase)
        
        
        # Split normalized job_desc
        tokens = word_tokenize(normalized_job_desc)
        
        # Remove stop-words
        filter_token = [word for word in tokens if word not in stop_words]
        
        # Remove punctuation
        clean_tokens = [char for char in filter_token if char.isalpha()]
        
        
        for item in phrases:
            phrase_word_list += item.split()
            
            
        # Remove words part of the phrases
        filter_keywords = [words for words in clean_tokens if words not in phrase_word_list]
        
        
        # Filter words > 3 only
        keywords = [ char for char in filter_keywords if len(char) >= 3]
        
        
        
        
        
        print(f"{phrases} \n{keywords}")
        
        print("------ JOB DESC END ------")
        
        
        
    
        
        return f"""
        <h2>Resume received</h2>
        <p>{resume[:50]} .....</p>

        <h2>Job description received</h2>
        <p>{job_desc[:50]} ....</p>
        """
    
    return render_template("form.html")



if __name__ == '__main__':
    app.run(debug=True)