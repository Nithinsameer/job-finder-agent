from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from resume_parser import extract_text_from_file, extract_skills_with_llm
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()
tool = TavilySearchResults()
client = OpenAI()
search = SerpAPIWrapper()

def prompt_generator(skills):
    prompt = (
        "Following are the key skills and technologies of the person based on their resume:\n\n"
        f"{skills}\n\n"
        "Understand the Skills and use that knowledge to generate a prompt for another LLM for it to crawl the web and find the 20 latest entry level job listings and positions opened in the last 24 hours that require these skills and technologies"
        "The prompt should include the Job Titles relevant to the skills and technologies but not the list of skills"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

skills = "Python, R, MySQL, Exploratory.io, Tableau, HTML/CSS/JavaScript, Latex, Databricks, Selenium, Scikit-learn, TensorFlow, PyTorch, Seaborn, Scipy, Statsmodel, Keras, NLTK, Langchain, TF-IDF vectorization, OpenAI's GPT-3.5-turbo model, Streamlit, Databricks/Python/Keras, Logistic Regression, K-Means, Decision Trees, Prophet, Flask, MongoDB, OCR, Sentence Embedding"

# generated_prompt = prompt_generator(skills)
# print("Generated Prompt:", generated_prompt)

# try:
#     result = tool.invoke({"query": generated_prompt})
#     print(result)
# except Exception as e:
#     print("Error:", e)

####-------- web search agent --------------####
file_path = "data/Nithin_Sameer_Yerramilli_June.pdf"
resume_text = extract_text_from_file(file_path)
skills = extract_skills_with_llm(resume_text)


# instructions = """You are an assistant."""
# base_prompt = hub.pull("langchain-ai/openai-functions-template")
# prompt = base_prompt.partial(instructions=instructions)
# llm = ChatOpenAI(temperature=0)
# tavily_tool = TavilySearchResults()
# search_tool = SerpAPIWrapper()  
# tools = [search_tool]

# def wrapper_function(*args, **kwargs):
#     return search_tool(*args, **kwargs)

# search_engine_function = convert_to_openai_function(wrapper_function)

# agent = create_openai_functions_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=tools,
#     verbose=True,
# )

# agent_executor.invoke({"input": prompt_generator(skills)})

llm = ChatOpenAI(temperature=0, model_name ="gpt-3.5-turbo")
tool_names =['serpapi']
tools=load_tools(tool_names,llm)
agent=initialize_agent(tools,llm,agent='zero-shot-react-description', verbose=True)

agent.run(f"20 Entry Level Data Scientist jobs listed in the last 24 hours in the United States")