import pdfkit
from flask import Flask, render_template, request, redirect, url_for, make_response
from sheets_helper import load_keys_from_sheet, mark_key_as_used


import json
import os
from werkzeug.utils import secure_filename
from resume_parser import extract_text_from_resume
from persona_prompt import get_persona_profile
from flask import make_response
# from weasyprint import HTML
import tempfile
import base64

app = Flask(__name__)

USED_KEYS_FILE = 'used_keys.json'
# Point to wkhtmltopdf executable
pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')



def load_keys():
    with open(USED_KEYS_FILE, 'r') as f:
        return json.load(f)

def save_keys(keys):
    with open(USED_KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

@app.route('/', methods=['GET'])
def home():
    return render_template('key_input.html')

@app.route('/validate-key', methods=['POST'])
def validate_key():
    access_key = request.form['access_key'].strip()
    # keys = load_keys()
    keys = load_keys_from_sheet()

    if access_key in keys and keys[access_key]['status'].lower() == 'unused':
        mark_key_as_used(access_key)
    # if access_key in keys and keys[access_key]['status'] == 'unused':
    #     keys[access_key]['status'] = 'used'
    #     save_keys(keys)
        return redirect(url_for('upload_resume'))
    else:
        return render_template('key_input.html', error="Invalid or already used key.")

@app.route('/upload', methods=['GET'])
def upload_resume():
    return render_template('upload.html')



@app.route('/process-resume', methods=['POST'])
def process_resume():
    if 'resume_file' not in request.files:
        return render_template('upload.html', error="No file uploaded.")

    file = request.files['resume_file']
    if file.filename == '':
        return render_template('upload.html', error="No selected file.")

    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        resume_text = extract_text_from_resume(filepath)

        # STEP: Get profile from OpenAI
        profile_output = get_persona_profile(resume_text)

        return render_template("result.html", output=profile_output)

    except Exception as e:
        return render_template('upload.html', error=f"Error processing file: {str(e)}")

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    from flask import request

    output_raw = request.form['output']
    # html = render_template("pdf_template.html", output=output_raw)
    from flask import url_for

    logo_path = os.path.join(app.root_path, 'static', 'Final Logo.png')
    html = render_template("pdf_template.html", output=output_raw, logo_path=logo_path)


    pdf = pdfkit.from_string(html, False, configuration=pdfkit_config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=career_report.pdf'
    return response



if __name__ == '__main__':
    app.run(debug=True)
