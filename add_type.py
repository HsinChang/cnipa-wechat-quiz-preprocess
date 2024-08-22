import json
import re

def determine_question_type(correct):
    """
    Determines the question type based on the 'correct' property:
    - If 'correct' contains one capital letter, the type is 'single'.
    - If 'correct' contains multiple capital letters, the type is 'multiple'.
    - If 'correct' contains anything else, the type is 'judge'.
    """
    if isinstance(correct, str):
        # Check for single or multiple capital letters
        capital_letters = re.findall(r'[A-Z]', correct)
        if len(capital_letters) == 1:
            return 'single'
        elif len(capital_letters) > 1:
            return 'multiple'
        else:
            return 'judge'
    else:
        return 'judge'

def add_question_type(input_file, output_file):
    # Load the existing questions.js file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract the JSON content from the questions.js file
    json_start = content.find('[')
    json_end = content.rfind(']') + 1
    if json_start == -1 or json_end == -1:
        raise ValueError("The input file does not contain valid JSON data.")

    questions_list = json.loads(content[json_start:json_end])

    # Add the 'type' property to each question
    for paper in questions_list:
        for question in paper['questions']:
            if 'type' not in question or not question['type']:
                question['type'] = determine_question_type(question['correct'])

    # Save the modified data back to a new questions.js file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('const questions = ')
        file.write(json.dumps(questions_list, ensure_ascii=False, indent=2))
        file.write(';\n\nmodule.exports = { questions };')

    print(f"Modified data has been saved to {output_file}")

# Specify input and output files
input_file = 'questions_restructured.js'
output_file = 'questions_with_type.js'

# Run the process to add 'type' properties
add_question_type(input_file, output_file)
