# Import Libraries 
import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
from dotenv import load_dotenv
load_dotenv()

# API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Model
def get_gemini_response(input):
  model = genai.GenerativeModel('gemini-1.5-flash')
  response=model.generate_content(input)
  return response.text

# Streamlit using Costum Css styles
st.set_page_config(page_title="Resume ATS", layout="wide")

with open("Style.css") as f:
  st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<h1 class="main-title"> Resume Application Tracking System</h1>', unsafe_allow_html=True)
st.markdown('<div class="centered">', unsafe_allow_html=True)
Job_Desc = st.text_area("Enter your Job Description text here", key="input")
uploaded_file = st.file_uploader("Upload your Resume", type="pdf", key="file")
st.markdown('</div>', unsafe_allow_html=True)

sub1 = st.button("Keywords Missing in my Resume")
sub2 = st.button("Percentage Match ")

# PDF to Text Model 
def input_pdf_text(uploaded_file):
  Read_PDF=pdf.PdfReader(uploaded_file)
  text=""
  for page in range(len(Read_PDF.pages)):
    page=Read_PDF.pages[page]
    text+=str(page.extract_text())
  return text

# Prompts
input_prompt1 = """
You are an advanced AI Resume Optimization Specialist designed to perform a strategic keyword gap analysis between a candidate's resume and a specific job description and you will use the information in the uploaded resume. 
Your objective is to provide a nuanced, actionable assessment that bridges the communication gap between a candidate's professional profile and employer expectations.
Candidate Name: 
Resume: {text}
Job Description: {jd}
Primary Responsibilities:
1. Conduct a comprehensive semantic keyword comparison
2. Identify critical skill and experience keywords missing from the resume
3. Provide strategic recommendations for resume enhancement

Detailed Analysis Requirements:
- Perform a deep linguistic and contextual mapping between the job description and resume
- Categorize missing keywords into:
  a) Hard Skills (technical abilities, specific tools, programming languages)
  b) Soft Skills (leadership, communication, problem-solving)
  c) Industry-Specific Terminology
  d) Quantifiable Achievements and Metrics

Deliverable Expectations:
- Generate a prioritized list of recommended keywords
- Offer specific, concise suggestions for integrating identified keywords
- Highlight the potential impact on Applicant Tracking System (ATS) scoring
- Maintain a professional, data-driven tone focused on strategic career optimization

Guiding Principles:
- Ensure authenticity: Recommend only keywords genuinely reflective of the candidate's experience
- Prioritize relevance over keyword density
- Focus on meaningful keyword integration that enhances the resume's narrative
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one field of data analysis, data science, machine learning engineering, AI engineering, DevOps, cloud computing, or cybersecurity, and deep ATS functionality. 
Your job is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. 
Resume: {text}
Job Description: {jd}
So your tasks are:
First, provide the output as a percentage, 
Then list the missing keywords, 
And finally, give your final thoughts.
"""


if sub1:
    if uploaded_file is not None and Job_Desc:
        text = input_pdf_text(uploaded_file)
        input = input_prompt1.format(text=text, jd=Job_Desc)
        response = get_gemini_response(input)
        st.markdown('<h2 class="sub-header"> Missing Keywords</h2>', unsafe_allow_html=True)
        st.write(response)
    else:
        st.warning("Please check your resume or job description")

elif sub2:
    if uploaded_file is not None and Job_Desc:
        text = input_pdf_text(uploaded_file)
        input = input_prompt2.format(text=text, jd=Job_Desc)
        response = get_gemini_response(input)
        st.markdown('<h2 class="sub-header"> Percentage Match</h2>', unsafe_allow_html=True)
        st.write(response)
    else:
        st.warning("Please check your resume or job description")