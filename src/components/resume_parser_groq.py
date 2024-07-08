import os
import json
import re
from typing import List
from dotenv import load_dotenv
from groq import Groq
from pdfminer.high_level import extract_text as extract_pdf_text

# Load environment variables
load_dotenv()

class GroqResumeAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def extract_text_from_file(self, file_path: str) -> str:
        if not file_path.lower().endswith('.pdf'):
            raise ValueError("The resume file must be in PDF format.")
        return extract_pdf_text(file_path)

    def generate_search_terms(self, resume_text: str) -> List[str]:
        prompt = f"""
        Analyze the following resume and generate 5 effective professional job search terms.
        Focus on industry-relevant job titles in data science, data analytics, and machine learning fields.
        The terms should match the candidate's skills and experience level.
        Avoid using academic titles or any software testing roles.
        Consider the candidate's background in data analysis, Python programming, and machine learning.

        Resume:
        {resume_text}

        Provide ONLY a JSON array of 5 search terms, nothing else. For example:
        ["Data Scientist", "Machine Learning Engineer", "Data Analyst", "Business Intelligence Analyst", "Python Developer for Data Science"]
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="mixtral-8x7b-32768",
                temperature=0.2,
                max_tokens=200,
            )

            content = chat_completion.choices[0].message.content
            print("Raw API response:", content)  # Debug print

            # Extract JSON array from the response
            json_array = re.search(r'\[.*\]', content, re.DOTALL)
            if json_array:
                return json.loads(json_array.group())
            else:
                print("No JSON array found in the response")
                return []

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {str(e)}")
            return []
        except Exception as e:
            print(f"Error in API call: {str(e)}")
            return []

# Usage
if __name__ == "__main__":
    analyzer = GroqResumeAnalyzer()
    resume_path = 'output/Nithin_Sameer_Yerramilli_June.pdf'
    resume_text = analyzer.extract_text_from_file(resume_path)
    search_terms = analyzer.generate_search_terms(resume_text)
    print("\nGenerated professional job search terms:", search_terms)

    # Optional: Save search terms to a JSON file
    with open('search_terms.json', 'w') as f:
        json.dump({"search_terms": search_terms}, f, indent=2)
    print("Search terms saved to search_terms.json")