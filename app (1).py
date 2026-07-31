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
st.image("https://raw.githubusercontent.com/Madhu29709/Agent-Resume/refs/heads/main/bg.png")

st.sidebar.title("Fill important Details")
st.sidebar.image("https://raw.githubusercontent.com/Madhu29709/Agent-Resume/refs/heads/main/bg.png")


# ====API kEYS========

GOOGLE_API_KEY = st.sidebar.text_input("Gemini-API",type = "password")
GROQ_API_KEY = st.sidebar.text_input("Groq-API",type = "password")
TAVILY_API_KEY = st.sidebar.text_input("Tavily-API",type = "password")

all_API = [GOOGLE_API_KEY,GROQ_API_KEY,TAVILY_API_KEY ]
if not all(all_API):
    st.error("Must given  API keys")
    st.stop()
elif all(all_API):
    st.success("API KEYS LOADED SUCCESSFULLY")
    model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY

)
else:
    st.info("PASS ALL API - KEYS")





# MULTISELECT OPTION
options = ["Delhi","Mumbai",
          "Pune","Banglore",
          "Gurugram/Gurgaon"]
location =  st.sidebar.multiselect("Select Location",
                                  options = options)
profile_op = ["Data Analysts","AI Engineer","Gen AI Developer","Full-Stack Dev",
             "Data Scientist"]
profile = st.sidebar.multiselect("select Job Profile",
                                options = profile_op)


# ====== Get User Info=========
st.markdown("""  GET USER INFO """)
user_info = st.text_area("Write your Resume Description:")


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
  response = client.search(query)
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

  with open('prompt.txt','w') as f:
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

if st.button("Generate Resume"):
    with st.spinner("Agent Running"):
        code = main_agent(agent, user_info)
        st.html(code,width ="stretch",
               unsafe_allow_javascript= True)
        st.divider() # to give horizontal divide
        jobe_code =get_jobs(agent,location,profile)
        st.html(job_code,width ="stretch",
               unsafe_allow_javascript= True)







