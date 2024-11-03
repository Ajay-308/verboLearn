
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import io
import pdf2image
import google.generativeai as genai
import base64
from pydantic import BaseModel
from typing import Optional
import re

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
genai.configure(api_key="AIzaSyAV4bjfsvj7R62aQ0cAnRzhc7h-g2eVC2c")

class AnalysisRequest(BaseModel):
    job_description: str
    query_type: str
    custom_query: Optional[str] = None

PROMPT_TEMPLATES = {
    "tell_me_about": """
    You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """,
    "improve_skills": """
    You are a Technical Human Resource Manager with expertise in data science. 
    Your role is to scrutinize the resume in light of the job description provided. 
    Share your insights on the candidate's suitability for the role from an HR perspective. 
    Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
    """,
    "missing_keywords": """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
    Your task is to evaluate the resume against the provided job description as a Human Resource manager,
    assess the compatibility of the resume with the role. Provide the keywords that are missing.
    Also, offer recommendations for enhancing the candidate's skills and identify which areas require further development.
    """,
    "percentage_match": """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
    Your task is to evaluate the resume against the provided job description. Give the percentage of match if the resume matches
    the job description. First, provide the percentage, then list missing keywords, and finally, share final thoughts.
    """
}

def process_pdf(file_bytes: bytes):
    images = pdf2image.convert_from_bytes(file_bytes)
    first_page = images[0]
    
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return [{
        "mime_type": "image/jpeg",
        "data": base64.b64encode(img_byte_arr).decode()
    }]

def get_gemini_response(prompt: str, pdf_content: list, job_description: str):
    try:
        response = genai.generate_text(
            prompt=prompt + f"\nResume Content: {pdf_content[0]['data']}\nJob Description: {job_description}"
        )
        return response.result if response else "No response generated."
    except Exception as e:
        return f"Error generating response: {str(e)}"

def format_response(response_text: str) -> str:
    # Remove all instances of text wrapped in double asterisks and keep the text only
    response_text = re.sub(r"\*\*(.*?)\*\*", r"\1", response_text)

    # Structure the response
    overall_assessment = response_text.split("Overall Assessment:")[1].split("Strengths:")[0].strip()
    strengths = response_text.split("Strengths:")[1].split("Weaknesses:")[0].strip()
    weaknesses = response_text.split("Weaknesses:")[1].strip()

    formatted_response = (
        f"<b>Resume Evaluation for Lead Frontend Developer Role</b><br><br>"
        f"<b>Overall Assessment:</b><br>{overall_assessment}<br><br>"
        f"<b>Strengths:</b><br>{strengths}<br><br>"
        f"<b>Weaknesses:</b><br>{weaknesses}<br>"
    )
    return formatted_response


@app.post("/process")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    query_type: str = Form(...),
    custom_query: Optional[str] = Form(None)
):
    try:
        file_bytes = await file.read()
        pdf_content = process_pdf(file_bytes)
        
        # Determine the prompt to use
        if query_type == "custom" and custom_query:
            prompt = custom_query
        else:
            prompt = PROMPT_TEMPLATES.get(query_type)
            if not prompt:
                return {"error": "Invalid query type"}
        
        # Get response from Gemini AI
        response_text = get_gemini_response(prompt, pdf_content, job_description)
        
        # Format response
        formatted_response = format_response(response_text)
        
        return {"response": formatted_response}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
