from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename
from resume_parser import extract_text_from_resume
from persona_prompt import get_persona_profile

app = Flask(__name__)

USED_KEYS_FILE = 'used_keys.json'

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
    keys = load_keys()

    if access_key in keys and keys[access_key]['status'] == 'unused':
        keys[access_key]['status'] = 'used'
        save_keys(keys)
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



if __name__ == '__main__':
    app.run(debug=True)
