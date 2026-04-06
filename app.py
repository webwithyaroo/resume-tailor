from flask import Flask, request, render_template
from resume import resume_tailor
from job import job_description



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == "POST":
        
        job = request.form.get('job') 
        resume = request.form.get('resume') 
        
        
        # validate inputs

        if not job or resume or resume is None or job is None:
            return "Please provide your resume and job description", 400
            
        
        
        print("Resume started")
        
        
        # resume actions
        resume_processor = resume_tailor(resume_details = resume)
        print(resume_processor)
        
        
        print("+" *40)
        print("Job started")
        
        # job actions
        job_processor = job_description(job_details = job)
        print(job_processor)
        
    
        
        return f"""
            <h2>Resume received</h2>
            <p>{resume[:50]} .....</p>
            <h2>Job description received</h2>
            <p>{job[:50]} ....</p>
        """
    
    return  render_template("form.html")



if __name__ == '__main__':
    app.run(debug=True)