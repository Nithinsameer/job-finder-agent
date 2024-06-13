from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from typing import Any
import ast
import openai
from openai import OpenAI
from langchain_core.tools import Tool
import re
import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from resume_parser import extract_text_from_file, extract_skills_with_llm
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.utilities import GoogleSerperAPIWrapper
import json
import tabulate
import pandas as pd

load_dotenv()
tool = TavilySearchResults()
client = OpenAI()
search = SerpAPIWrapper()

def prompt_generator(skills):
    prompt = (
        "Following are the roles the person is suitable for based on their resume:\n\n"
        f"{skills}\n\n"
        "Entry level positions for the above roles in USA posted in the last 24 hours exclusively from linkedin"
        #"Understand the Roles that the person is eligible for and use that knowledge to generate a prompt for another LLM to crawl the web and find the 20 latest entry level job listings and positions opened in the last 24 hours on https://www.linkedin.com/jobs/ for these roles"
        #"Find Joblistings on https://www.linkedin.com/jobs/ only for these roles, are entry level and have been posted in the last 24 hours"
        #"The prompt should include the Job Titles relevant to the skills and technologies but not the list of skills"
    )
    print(prompt)

    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    return prompt

skills = "Data Analyst, Data Scientist, Data Engineer, Business Analyst, Programmer Analyst, Machine Learning Engineer"

# generated_prompt = prompt_generator(skills)
# print("Generated Prompt:", generated_prompt)


def print_list(lst):
    for i, item in enumerate(lst):
        print(f"{i}: {item}")

def joblistings(query: str):
    result = search.results(query)
    print("Type of result:", type(result))
    #print("Content of result:", result)
    return result


def title_link(postings: dict) -> list[tuple[str, str]]:
    pattern = r"'title': '(.*?)', 'link': '(.*?)'"
    matches = re.findall(pattern, postings)
    return matches



search = GoogleSerperAPIWrapper()
llm = ChatOpenAI(temperature=0, model_name ="gpt-3.5-turbo")
tools = [
    Tool(
        name="Get 20 Job Listings",
        func= joblistings,
        description="Searches google for jobs using the users exact input.",
    ),
    Tool(
        name="Get Job Links",
        func= title_link,
        description="Extracts the linkedin.com/jobs/ link from the results.",
    )
]
#tools=load_tools(tool_names,llm)
agent=initialize_agent(tools,llm,agent='zero-shot-react-description', verbose=True)

links = agent.run(prompt_generator(skills))
print(links)

# print(type(links))

# if isinstance(links, str):
#     try:
#         links = ast.literal_eval(links)
#     except (ValueError, SyntaxError) as e:
#         print("Error converting links to list of tuples:", e)
#         links = []

# print(type(links))

# postings = pd.DataFrame(links, columns=['Job Title', 'URL'])
# print(postings['URL'])