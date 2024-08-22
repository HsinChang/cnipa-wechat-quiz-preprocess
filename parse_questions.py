import os
import json
from docx import Document
import re

def parse_docx_improved(file_path):
    doc = Document(file_path)
    questions = []
    current_question = None
    collecting_options = False
    previous_line_was_question = False

    for para in doc.paragraphs:
        text = para.text.strip()

        # Detect question numbers (e.g., 1., 2.), and support variations
        question_match = re.match(r'^\d+\.\s*(.+)', text)
        option_match = re.match(r'^([A-D])\.\s*(.+)', text)

        if question_match:
            # Save the previous question if present
            if current_question:
                questions.append(current_question)
            # Start a new question
            current_question = {
                'question': question_match.group(1),
                'options': [],
                'correct': '',
                'explanation': '',
                'difficulty': ''
            }
            collecting_options = True
            previous_line_was_question = True

        elif option_match and collecting_options:
            key = option_match.group(1)
            option_text = option_match.group(2)
            current_question['options'].append({"key": key, "text": option_text})
            previous_line_was_question = False

        elif text.startswith('【答案】'):
            if current_question:
                current_question['correct'] = text.replace('【答案】', '').strip()

        elif text.startswith('【解析】'):
            if current_question:
                current_question['explanation'] = text.replace('【解析】', '').strip()

        elif text.startswith('【难度等级】'):
            if current_question:
                current_question['difficulty'] = text.replace('【难度等级】', '').strip()

        # Handle cases where the question continues on the next line
        elif previous_line_was_question:
            current_question['question'] += " " + text

    # Add the last question if present
    if current_question:
        questions.append(current_question)

    return questions

def convert_to_js_improved(folder_path):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.docx')]
    all_papers = []

    for file_name in all_files:
        file_path = os.path.join(folder_path, file_name)
        questions = parse_docx_improved(file_path)
        paper = {
            'name': file_name.replace('.docx', ''),
            'questions': questions
        }
        all_papers.append(paper)
    
    output_data = {
        'questions': all_papers
    }

    with open('questions.js', 'w', encoding='utf-8') as js_file:
        js_file.write('const questions = ')
        js_file.write(json.dumps(output_data, ensure_ascii=False, indent=2))
        js_file.write(';\n\nmodule.exports = { questions };')

if __name__ == '__main__':
    current_folder = os.getcwd()
    convert_to_js_improved(current_folder)
    print("Conversion complete. 'questions.js' file has been created.")
