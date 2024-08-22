import json

def restructure_questions(input_file, output_file):
    # Read the questions.js file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Strip out the JavaScript-specific parts
    json_start = content.find('[')
    json_end = content.rfind(']') + 1

    if json_start == -1 or json_end == -1:
        raise ValueError("The input file does not contain valid JSON data.")

    json_content = content[json_start:json_end]

    # Load the JSON content
    questions_list = json.loads(json_content)

    # Restructure the data
    restructured_data = []
    for paper in questions_list:
        restructured_data.append({
            "name": paper["name"],
            "questions": paper["questions"]
        })

    # Save the restructured data back to a new questions.js file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('const questions = ')
        file.write(json.dumps(restructured_data, ensure_ascii=False, indent=2))
        file.write(';\n\nmodule.exports = { questions };')

    print(f"Restructured data has been saved to {output_file}")

# Specify input and output files
input_file = 'questions.js'
output_file = 'questions_restructured.js'

# Run the restructuring process
restructure_questions(input_file, output_file)
