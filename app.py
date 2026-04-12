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

        if not job or not resume:
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

        # missing = match_resume_to_job(resume_processor, job_processor)
        missing = match_resume_to_job(resume_keywords, resume_phrases, job_keywords, job_phrases
                                      )
        print("+" * 40)


        #################### missing keywords and phrases ##########################################
        print("Missing keywords:")
        print(missing["missing_keywords"])
        print(missing["missing_phrases"])
        
        ################################ matched keywords and phrases ##########################################
        print("Matched keywords:")
        print(missing["matched_keywords"])
        print(missing["matched_phrases"])
        
        ########################################## extracted keywords and phrases ##########################################
        print("Extra keywords:")
        print(missing["extra_keywords"])
        print(missing["extra_phrases"])

        # missing phrases
        phrases_html = ""
        if missing['missing_phrases']:
            phrases_html = f"""
            <h2>Missing phrases:</h2>
            <ul>
                {"".join(f"<li>{phrase}</li>" for phrase in missing['missing_phrases'])}
            </ul>"""

        # missing keywords
        keywords_html = ""
        if missing['missing_keywords']:
            keywords_html = f"""
            <h2>Missing keywords:</h2>
            <ul>
                {"".join(f"<li>{keyword}</li>" for keyword in missing['missing_keywords'])}
            </ul>"""

        return f"""
            <h2>Resume received</h2>
            <p>{resume[:50]} .....</p>
            <h2>Job description received</h2>
            <p>{job[:50]} ....</p>
            
            {keywords_html}
            {phrases_html}
                

        """

    return render_template("form.html")


if __name__ == '__main__':
    app.run(debug=True)
