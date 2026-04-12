from flask import Flask, request, render_template
from resume import resume_tailor
from job import job_description
from matcher import match_resume_to_job

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == "POST":
        
        job = request.form.get('job') 
        resume = request.form.get('resume') 
        
        
        if not job or not resume or resume is None or job is None:
            return "Please provide your resume and job description"
        
        print("Resume started")
        
        
        # resume actions
        resume_processor = resume_tailor(resume_details = resume)
        resume_keywords = resume_processor[1]
        resume_phrases = resume_processor[0]
        
        
        
        print("+" *40)
        print("Job started")
        
        # job actions
        job_processor = job_description(job_details = job)
        job_keywords = job_processor[1]
        job_phrases = job_processor[0]
        
        
        # missing = match_resume_to_job(resume_processor, job_processor)
        missing = match_resume_to_job(resume_keywords, resume_phrases, job_keywords,job_phrases
)
        print("+" *40)
        
        
        print("Missing keywords:")
        print(missing["keywords"])
        
        print("Missing phrases:")
        print(missing["phrases"])
        

        # missing phrases
        phrases_html = ""
        if missing['phrases']:
            phrases_html = f"""
            <h2>Missing phrases:</h2>
            <ul>
                {"".join(f"<li>{phrase}</li>" for phrase in missing['phrases'])}
            </ul>"""
        
        
        # missing keywords 
        keywords_html = ""
        if missing['keywords']:
            keywords_html = f"""
            <h2>Missing keywords:</h2>
            <ul>
                {"".join(f"<li>{keyword}</li>" for keyword in missing['keywords'])}
            </ul>"""
        
        
        
        
        return f"""
            <h2>Resume received</h2>
            <p>{resume[:50]} .....</p>
            <h2>Job description received</h2>
            <p>{job[:50]} ....</p>
            
            {keywords_html}
            {phrases_html}
                

        """
    
    return  render_template("form.html")



if __name__ == '__main__':
    app.run(debug=True)