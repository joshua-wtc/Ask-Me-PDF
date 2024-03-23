import streamlit as st
import PyPDF2
from openai import OpenAI

# Set up OpenAI Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfFileReader(uploaded_file)
    num_pages = reader.numPages
    for page_number in range(num_pages):
        page = reader.getPage(page_number)
        text += page.extractText()
    return text

st.title("Ask Me PDF")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:

    # Extract text if file is uploaded
    text = extract_text_from_pdf(uploaded_file)

    # Answer questions using OpenAI API
    question = st.text_input("Ask a question about the PDF:")
    if question:
        st.info(f"**Question:** {question}")

        with st.spinner("Thinking..."):
	        response = client.chat.completions.create(
	        	model="gpt-3.5-turbo",
	        	messages=[{"role": "system", "content": f"You are a friendly chatbot answering questions about this resume. Here is the resume: {text}"},
	        	{"role": "user", "content": question}],
	        	temperature=0,
	        	seed=0
	        	)

	       	answer = response.choices[0].message.content
        st.info(f"**Answer:** {answer}")
else:
    st.warning("Please upload a PDF file.", icon="🥺")