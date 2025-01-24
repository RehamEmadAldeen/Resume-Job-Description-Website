import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
import pathlib
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
  model = genai.GenerativeModel('gemini-1.5-flash')
  response=model.generate_content(input)
  return response.text


def input_pdf_text(uploaded_file):
  reader=pdf.PdfReader(uploaded_file)
  text=""
  for page in range(len(reader.pages)):
    page=reader.pages[page]
    text+=str(page.extract_text())
  return text


# streamlit app
st.set_page_config(page_title="Resume ATS", layout="wide")
def load_css(file_path):
    with open(file_path)as f:
        st.html(f"<style>{f.read()}</style>")

css_path= pathlib.Path("Style.css")
load_css(css_path)


st.markdown('<h1 class="main-title"> Resume Application Tracking System</h1>', unsafe_allow_html=True)
st.markdown('<div class="centered">', unsafe_allow_html=True)
Job_Desc = st.text_area("Enter your Job Description text here", key="input")
uploaded_file = st.file_uploader("Upload your Resume", type="pdf", key="file", help="Please upload the pdf")
st.markdown('</div>', unsafe_allow_html=True)




submit = st.button("Submit")
if submit:
    # Check if both uploaded_file and Job_Desc are empty or None
    if not uploaded_file and not Job_Desc:
        st.warning("Warning: Please upload a PDF file and put the job description")
    elif not uploaded_file:
        st.warning("Please upload a PDF file")
    elif not Job_Desc:
        st.warning("Please put the job description")
    else:
        st.write("Successfully.")



sub1 = st.button(" What Keywords are Missing in my Resume")
sub2 = st.button("Percentage Match ")

# Prompits

input_prompt1 = """
You are an experienced ATS (Applicant Tracking System) specialist with deep knowledge of keyword optimization in resumes. 
Your task is to review the provided resume and job description, and identify which important keywords are missing from the resume.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one field of data analysis, data science, machine learning engineering, AI engineering, DevOps, cloud computing, or cybersecurity, and deep ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. 
First, provide the output as a percentage, then list the missing keywords, and finally, give your final thoughts.
"""




if sub1:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input=input_prompt1.format(text=text,jd=Job_Desc)
        response = get_gemini_response(input)
        st.markdown('<h2 class="sub-header"> Missing Keywords</h2>', unsafe_allow_html=True)
        st.write(response)


elif sub2:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input=input_prompt2.format(text=text,jd=Job_Desc)
        response = get_gemini_response(input)
        st.markdown('<h2 class="sub-header"> Percentage Match</h2>', unsafe_allow_html=True)
        st.write(response)

