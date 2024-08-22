import json

def remove_questions_with_no_options(input_file, output_file):
    # Load the existing questions.js file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract the JSON content from the questions.js file
    json_start = content.find('[')
    json_end = content.rfind(']') + 1
    if json_start == -1 or json_end == -1:
        raise ValueError("The input file does not contain valid JSON data.")

    questions_list = json.loads(content[json_start:json_end])

    # Remove questions that have no options and are not of the 'judge' type
    for paper in questions_list:
        paper['questions'] = [question for question in paper['questions'] if question.get('type') == 'judge' or len(question.get('options', [])) > 0]

    # Save the cleaned data back to a new questions.js file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('const questions = ')
        file.write(json.dumps(questions_list, ensure_ascii=False, indent=2))
        file.write(';\n\nmodule.exports = { questions };')

    print(f"Cleaned data has been saved to {output_file}")

# Specify input and output files
input_file = 'questions_with_type.js'
output_file = 'questions_cleaned.js'

# Run the process to remove questions with no options
remove_questions_with_no_options(input_file, output_file)
