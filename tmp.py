import os
import win32com.client as win32
from pywps import Wps

def convert_wps_to_docx(wps_file, output_folder):
    # Open the WPS file
    with open(wps_file, 'rb') as file:
        doc = Wps(file)

    # Get the content and save it as .docx
    docx_file = os.path.join(output_folder, os.path.splitext(os.path.basename(wps_file))[0] + '.docx')
    doc.save(docx_file)
    print(f"Converted {wps_file} to {docx_file}")

def convert_doc_to_docx(doc_file):
    word = win32.Dispatch('Word.Application')
    doc = word.Documents.Open(doc_file)
    docx_file = os.path.splitext(doc_file)[0] + '.docx'
    doc.SaveAs(docx_file, FileFormat=16)  # 16 corresponds to wdFormatDocumentDefault
    doc.Close()
    word.Quit()
    print(f"Converted {doc_file} to {docx_file}")

def main():
    current_folder = os.getcwd()

    # Convert .wps files
    for file_name in os.listdir(current_folder):
        if file_name.endswith('.wps'):
            convert_wps_to_docx(os.path.join(current_folder, file_name), current_folder)

    # Convert .doc files
    for file_name in os.listdir(current_folder):
        if file_name.endswith('.doc') and not file_name.endswith('.docx'):
            convert_doc_to_docx(os.path.join(current_folder, file_name))

if __name__ == "__main__":
    main()
