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
        
        # Split normalized job_desc
        tokens = word_tokenize(normalized_job_desc)
        
        remove_punc = [char for char in tokens if char.isalpha() or char.isspace()]
        
        # Filter token list
        filter_token = [word for word in remove_punc if word not in stop_words]
        
        # Filter words > 3 only
        filter_small_char = [ char for char in filter_token if len(char) >= 3]
        
       

        print(filter_small_char)
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