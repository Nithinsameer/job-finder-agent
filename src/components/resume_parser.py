import openai
from openai import OpenAI
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
import os

def extract_text_from_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_pdf_text(file_path)
    elif file_extension == '.docx':
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
    

def extract_skills_with_llm(resume_text):

    prompt = (
        "Understand the following resume and give me the Comma seperated list of corporate roles that the candidate is most suitable for:\n\n"
        f"{resume_text}\n\n"
        #"Based on the key skills extracted give me the Comma seperated list of roles that the candidate is most suitable for:"
    )


    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    file_path = 'data/Nithin_Sameer_Yerramilli_June.pdf'  
    
    try:
        resume_text = extract_text_from_file(file_path)
        skills = extract_skills_with_llm(resume_text)
        print("Skills:", skills)
    except ValueError as e:
        print(e)