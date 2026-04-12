from flask import Flask, request, render_template
from resume import resume_tailor
from job import job_description
from matcher import match_resume_to_job
from display import display
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == "POST":

        job = request.form.get('job')
        resume = request.form.get('resume')

        if not job or not resume :
            return "Please provide your resume and job description"

        print("Resume started")

        # resume actions
        resume_processor = resume_tailor(resume_details=resume)
        resume_keywords = resume_processor["keywords"]
        resume_phrases = resume_processor["phrases"]

        print("+" * 40)
        print("Job started")

        # job actions
        job_processor = job_description(job_details=job)
        job_keywords = job_processor["keywords"]
        job_phrases = job_processor["phrases"]

        # resume_job_data = match_resume_to_job(resume_processor, job_processor)
        resume_job_data = match_resume_to_job(job_keywords, resume_keywords, job_phrases, resume_phrases
                                      )
        print("+" * 40)

        # display jobs and resume 
        words_display = display(resume_job_data)


        
        return f"""
            <h2>Resume received</h2>
            <p>{resume[:50]} .....</p>
            <h2>Job description received</h2>
            <p>{job[:50]} ....</p>
            
            {words_display}
            
        """
    return render_template("form.html")


if __name__ == '__main__':
    app.run(debug=True)
