from flask import Flask, render_template, request
from api.google_drive import get_resumes, download_resume, extract_text_from_pdf
from api.nlp_tools import process_resume
from api.matching import match_resumes_to_jd

app = Flask(__name__, template_folder='../templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_description = request.form['jd']
        folder_id = '17Rl-9aGfaXcVcDC4zO6peJVN0-IOX8ge'
        resumes = get_resumes(folder_id)
        resume_data = []
        for resume in resumes:
            file_content = download_resume(resume['id'])  # Gets the in-memory file
            text = extract_text_from_pdf(file_content)  # Directly process the in-memory content
            print(f"Raw Text for {resume['name']}:\n{text}\n")
            parsed_data = process_resume(text)  # Ensure process_resume accepts text directly
            resume_data.append({
                'name': resume['name'],
                'text': text,
                'parsed_data': parsed_data
            })
        
        ranked_resumes = match_resumes_to_jd(job_description, resume_data)
        return render_template('results.html', resumes=ranked_resumes)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
