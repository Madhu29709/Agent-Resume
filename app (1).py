# ===loaded all the modules======
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent

from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np



# to show the web-app:complete page layout
st.set_page_config(layout = 'wide')

# TO give title
st.title("AI RESUME GENERATOR")

st.write("""This app helps user to build customized professional Resume with latest Job Apply Link""")
st.image("bg.png")
# ====API kEYS========

GOOGLE_API_KEY ="AQ.Ab8RN6IZ7tWDZnFe3AH6xnSM-rMV1NoO5eUasIm8SxZ_HnS0Dg"
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

# ======MODELS==========
model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY

)
#response = model.invoke("Hello Buddy!")
#response.content[-1]['text']


# =====TOOLS========
def search_lastest_news_jobs(query):
  """TThis function helps to fect latest
  news or jobs  related article using
  tavily"""
  client = TavilyClient(
      api_key = TAVILY_API_KEY)
  responsev = client.search(query)
  return response



# ==========Agent========
# Agent creation
agent = create_agent(
    model = model,
    tools = [search_lastest_news_jobs])

#agent


# =====models======
def  main_agent(agent, query):
  """This is main agent or leader agent
  orchestrate sub agents"""

  # Giving prompt to create detailed  prompt for code generation
  prompt = """ you are AI assistant and below
  given is a prompt , your task is to give detailed prompt for
  this.
  you are a professional Resume Generator
  where user will give their personal info,
  for students or professional one
  it must be with dynamic UI and UX and,
  with advanced CSS Professional Designing
  Make sure to give output in HTML format only
  no markdowns allowed
  """

  response = agent.invoke({'messages':[{'role':'user','content':prompt}]})

  detailed_prompt =  response['messages'][-1].content[-1]['text']

  # SAVE PROMPT using File Handling

  with open('prompt.text','w') as f:
    f.write(detailed_prompt)
  user_details = f"""Below given is a user details
  generate resume based on that , if not
  given Keep:Default Resume:Pyhton Developer
  user details:{query}"""


  final_prompt = prompt + detailed_prompt + user_details

  # CODE GENERATION
  response = agent.invoke({'messages':[{'role':'user','content':final_prompt}]})
  code =  response['messages'][-1].content[-1]['text']


  return code




# ======= agent======
# code = main_agent(agent,"MADHU, DATA SCIENTIST")
# from IPython import display  as DISPLAY
# DISPLAY.HTML(code)



# ====== tools====
#Fetch latest domain related jobs using Tvaily
def get_jobs(agent,
             Location ="Noida,Delhi",
             Profile="Data Analysts,AI Engineer"):
  Location ="Noida,Delhi"
  Profile ="Data Analysts,AI Engineer"


  prompt = f"""Based or user  given job  profile,
  fetch latest jobs or job apply article
  using Naukri,Linkedin, Indeed, or all popular
  Job apply platform, show Results with
  JOB PROFILE NAME, LOCATION, SALARY,COMPANY NAME,
  SHOW JOBS only related to given
  {Location} and {Profile}.output must be in
  Professional HTML Naukri Theme cards with Dynamic Design,
  show atleast Top 10-20 results with direct apply link"""

  response = agent.invoke({'messages':[{'role':'user','content':prompt}]})
  code =  response['messages'][-1].content[-1]['text']

  return code


# =======
# code = get_jobs(agent)
# DISPLAY.HTML(code)








