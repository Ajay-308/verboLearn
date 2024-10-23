import io
import os
import base64
import fitz  # PyMuPDF
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

gemini_api_key = "AIzaSyAV4bjfsvj7R62aQ0cAnRzhc7h-g2eVC2c"
if not gemini_api_key:
    raise ValueError("Gemini_Api key is not set in the environment variables.")

genai.configure(api_key=gemini_api_key)

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    
    if not response or not hasattr(response, 'text'):
        raise ValueError("Invalid response from the Gemini API.")
    
    return response.text

async def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        contents = await uploaded_file.read()  # Await the read call
        
        # Extract text from the PDF using PyMuPDF
        pdf_document = fitz.open(stream=contents, filetype="pdf")
        text_content = ""
        
        for page in pdf_document:
            text_content += page.get_text()
        
        pdf_document.close()
        
        if not text_content:
            raise ValueError("No text found in the PDF.")
        
        return [text_content]  # Return the extracted text as a list
    else:
        raise FileNotFoundError("No file uploaded")

@app.post("/process")
async def evaluate_resume(
    file: UploadFile = File(...),
    job_description: str = "",
    task: str = "evaluation"
):
    # Check if the file type is PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File type not allowed. Please upload a PDF file.")

    try:
        pdf_content = await input_pdf_setup(file)  # Await the async function

        # Define the prompts based on the task
        prompts = {
            "evaluation": """You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.""",
            "improvement": """You are a Technical Human Resource Manager with expertise in data science, 
your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective. 
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.""",
            "keywords": """You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. As a Human Resource manager,
 assess the compatibility of the resume with the role. Give me what are the keywords that are missing
 Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development.""",
            "percentage_match": """You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts."""
        }

        if task not in prompts:
            raise HTTPException(status_code=400, detail="Invalid task specified.")

        response_text = await get_gemini_response(prompts[task], pdf_content, job_description)  # Await the async function

        return JSONResponse(content={"response": response_text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in processing: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the ATS Resume Expert API!"}
