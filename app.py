
# # Updated app.py

from flask import Flask, request, jsonify, render_template
import pandas as pd
import time
import os
import gc
import json
import pickle
import secrets
import pandas as pd
from flask import Flask, request, render_template, session
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Load and process data from Excel
data_df = pd.read_excel('C:\\Users\\G01921\\Downloads\\sir_suggested_file3.xlsx')
# Update the 'data' dictionary to include dynamically loaded subjects
data = {
    'Select Subject': list(data_df['Subject'].drop_duplicates()),

    'Select Module': data_df.groupby('Subject')['Module'].apply(lambda x: list(set(x))).to_dict(),
    'Select Area': data_df.groupby(['Subject', 'Module'])['Area'].apply(lambda x: list(set(x))).to_dict(),
    'Questions Based On Module And Area': data_df.groupby(['Subject', 'Module', 'Area'])['Question'].apply(lambda x: list(set(x))).to_dict(),
    'Answer Of Question Based On Area And Module': data_df.groupby(['Subject', 'Module', 'Area', 'Question'])['Answer'].first().to_dict()
}

@app.route('/')
def chatbot_greeting():
    session.clear()  # Clear session on restart
    subjects = data['Select Subject']
    session['step'] = 0  # Initial step
    return render_template('index.html', subjects=subjects, step=0)

@app.route('/select-module', methods=['POST'])
def select_subject():
    selected_subject = request.form.get('selected_subject')
    session['selected_subject'] = selected_subject
    session['step'] = 1
    modules = data['Select Module'].get(selected_subject, [])
    return render_template('index.html', selected_subject=selected_subject, modules=modules, step=1)

@app.route('/select-area', methods=['POST'])
def select_area():
    selected_subject = session.get('selected_subject')  # Get subject from session
    module = request.form.get('module')
    session['module'] = module
    session['step'] = 2  # Update to step 2
    areas = data['Select Area'].get((selected_subject, module), [])
    return render_template('index.html', selected_subject=selected_subject, module=module, areas=areas, step=2)

@app.route('/get-questions', methods=['POST'])
def get_questions():
    selected_subject = session.get('selected_subject')
    module = request.form.get('module')
    area = request.form.get('area')
    session['area'] = area
    session['step'] = 3  # Update to step 3
    questions = data['Questions Based On Module And Area'].get((selected_subject, module, area), [])
    return render_template('index.html', selected_subject=selected_subject, module=module, area=area, questions=questions, step=3)

@app.route('/get-answer', methods=['POST'])
def get_answer():
    selected_subject = session.get('selected_subject')
    module = request.form.get('module')
    area = request.form.get('area')
    question = request.form.get('question')
    session['question'] = question
    session['step'] = 4  # Update to step 4
    drive_link = "https://docs.google.com/spreadsheets/d/1x4sExhhTBdiNHKYtrPQ3KV8EEQAO0ye6/edit?gid=1221427571#gid=1221427571"
    answer = data['Answer Of Question Based On Area And Module'].get((selected_subject, module, area, question), 'No answer available')
    link_html = f'<a href="{drive_link}" target="_blank">Document Link</a>'
    final_answer = Markup(f"{answer}<br><br>For more details, refer to this {link_html}.")
    return render_template('index.html', selected_subject=selected_subject, module=module, area=area, question=question, answer=final_answer, step=4)


@app.route('/go-back', methods=['POST'])
def go_back():
    # Step back one level if not at step 0
    step = session.get('step', 0)
    if step > 0:
        session['step'] = step - 1

    # Handle each step and render the appropriate template
    if session['step'] == 0:
        session.clear()  # Clear session for a fresh start
        subjects = data['Select Subject']
        return render_template('index.html', subjects=subjects, step=0)

    selected_subject = session.get('selected_subject', '')
    module = session.get('module', '')
    area = session.get('area', '')
    question = session.get('question', '')

    if session['step'] == 1:
        modules = data['Select Module'].get(selected_subject, [])
        return render_template('index.html', selected_subject=selected_subject, modules=modules, step=1)
    elif session['step'] == 2:
        areas = data['Select Area'].get((selected_subject, module), [])
        return render_template('index.html', module=module, areas=areas, step=2)
    elif session['step'] == 3:
        questions = data['Questions Based On Module And Area'].get((selected_subject, module, area), [])
        return render_template('index.html', module=module, area=area, questions=questions, step=3)
    elif session['step'] == 4:
        drive_link = "https://docs.google.com/spreadsheets/d/1x4sExhhTBdiNHKYtrPQ3KV8EEQAO0ye6/edit?gid=1221427571#gid=1221427571"
        answer = data['Answer Of Question Based On Area And Module'].get((selected_subject, module, area, question), 'No answer available')
        link_html = f'<a href="{drive_link}" target="_blank">Document Link</a>'
        final_answer = Markup(f"{answer}<br><br>For more details, refer to this {link_html}.")
        return render_template('index.html', module=module, area=area, question=question, answer=final_answer, step=4)

    # Fallback for invalid cases
    return redirect('/')


if __name__ == '__main__':
    app.run()
