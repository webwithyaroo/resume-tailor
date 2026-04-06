from flask import Flask, request, render_template
from resume import resume_tailor



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == "POST":
        job_desc = request.form.get("job_desc")
        resume = request.form.get("resume")
        
        
        print("Resume started")
        
        # resume actions
        resume_actions = resume_tailor(resume_text = resume)
        print(resume_actions)
        
        
        print("+" *40)
        print("Job started")
        
        # job actions
        # job_actions = resume_tailor(job_resume_desc = job_desc)
        # print(job_actions)
        
    
        
        return f"""
            <h2>Resume received</h2>
            <p>{resume[:50]} .....</p>
            <h2>Job description received</h2>
            <p>{job_desc[:50]} ....</p>
        """
    
    return render_template("form.html")



if __name__ == '__main__':
    app.run(debug=True)