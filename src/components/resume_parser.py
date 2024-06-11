import openai
from openai import OpenAI

def extract_skills_with_llm(resume_text):

    prompt = (
        "Extract key skills and technologies from the following resume:\n\n"
        f"{resume_text}\n\n"
        "Comma seperated list of skills and technologies:"
    )


    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    api_key = 'sk-proj-4nA8mk64m2ZDzjRGcedpT3BlbkFJCHZ7ukA9SLIkw3SANJkS'
    resume_text = """
    John Doe
    Software Engineer with 5 years of experience in developing web applications. Proficient in Python, JavaScript, React, and Django. Experience with machine learning and data analysis. Worked on various projects involving natural language processing and computer vision.

    Work Experience:
    - Developed a web application using React and Django that increased user engagement by 30%.
    - Implemented machine learning models to predict customer behavior using Python and scikit-learn.

    Projects:
    - Built a chatbot using natural language processing techniques with Python and NLTK.
    - Created a computer vision system for image classification using TensorFlow and Keras.
    """
    skills = extract_skills_with_llm(resume_text)
    print("Skills:", skills)