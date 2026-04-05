from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """ checks the method based on the req and return the form
    Returns:
        string: the output string
    """
    if request.method == "POST":
        
        resume = request.form["resume"]
        job_desc = request.form["job_desc"]
        
        # return (f"RESUME: {resume} \n JOB DESCRIPTION: {job_desc}")
        
        print("------ RESUME START ------")
        print(resume)
        print("------ RESUME END ------ \n")
        
       
        
        print("------ JOB DESC START ------")
        print(job_desc)
        print("------ JOB DESC END ------")
        
        return f"""
        <h2>Resume received</h2>
        <p>{resume[:200]}</p>

        <h2>Job description received</h2>
        <p>{job_desc[:200]}</p>
        """
    
    return render_template("form.html")



if __name__ == '__main__':
    app.run(debug=True)