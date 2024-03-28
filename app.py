from dotenv import load_dotenv

load_dotenv() # load all the environment variables

import streamlit as st
import os
import json
import PyPDF2 as pdf
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Gemini Pro Response

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text    
#, software engineering, Data Science, Full Stack Web Development, Big Data Engineering, DEVOPS, and Data Analyst
##Prompt Template
input_prompt= """
Hey Act like a skilled or very experienced ATS (Applicant Tracking System) with a deep 
understanding of computer science and AI field. Your task is to evaluate the resume based on the job 
description. You must consider the job market is very competitive and you should provide the best 
assistance for improving the uploaded resume. Compare the keywords present in both Job Description
and the resume. Assign the percentage Match based on Job Description 
and the missing keywords from the uploaded resume with high accuracy.

resume:{text}
Job Description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%", "MissingKeywords:[]","Profile Summary":""}}
"""

## Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)
