from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import io
import pdf2image
import google.generativeai as genai
import base64
from pydantic import BaseModel
from typing import Optional

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
genai.configure(api_key="AIzaSyA971jVdDQ9qpAB8ORjXIPnZIbC64Gzu40")

class AnalysisRequest(BaseModel):
    job_description: str
    query_type: str
    custom_query: Optional[str] = None

PROMPT_TEMPLATES = {
    "tell_me_about": """
    You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. 
    Ensure your response does not include any of these **/##/*, symbols, or asterisks.
    """,
    "improve_skills": """
    You are a Technical Human Resource Manager with expertise in data science. 
    Your role is to scrutinize the resume in light of the job description provided. 
    Share your insights on the candidate's suitability for the role from an HR perspective. 
    Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed. 
    Please do not use  any of these **/##/*, or symbols in your response.
    """,
    "missing_keywords": """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
    Your task is to evaluate the resume against the provided job description as a Human Resource manager,
    assess the compatibility of the resume with the role. Provide the keywords that are missing.
    Also, offer recommendations for enhancing the candidate's skills and identify which areas require further development. 
    Avoid using any of these **/##/*, or symbols in your response.
    """,
    "percentage_match": """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
    Your task is to evaluate the resume against the provided job description. Give the percentage of match if the resume matches
    the job description. First, provide the percentage, then list missing keywords, and finally, share final thoughts.
    Do not include  any of these **/##/*, symbols, or asterisks in your response.
    """
}

def process_pdf(file_bytes: bytes) -> list:
    images = pdf2image.convert_from_bytes(file_bytes)
    first_page = images[0]
    
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return [{
        "mime_type": "image/jpeg",
        "data": base64.b64encode(img_byte_arr).decode()
    }]

def get_gemini_response(prompt: str, pdf_content: list, job_description: str) -> str:
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content([prompt, pdf_content[0], job_description])
    return response.text

def format_response(response_text: str) -> str:
    # Remove any stray asterisks that might still appear
    response_text = response_text.replace("**", "")

    # Initialize variables for sections
    overall_assessment = ""
    strengths = ""
    weaknesses = ""

    # Split the response text only if the keywords are present
    if "Overall Assessment:" in response_text:
        parts = response_text.split("Overall Assessment:")
        overall_assessment = parts[1].split("Strengths:")[0].strip() if len(parts) > 1 else ""

    if "Strengths:" in response_text:
        parts = response_text.split("Strengths:")
        strengths = parts[1].split("Weaknesses:")[0].strip() if len(parts) > 1 else ""

    if "Weaknesses:" in response_text:
        parts = response_text.split("Weaknesses:")
        weaknesses = parts[1].strip() if len(parts) > 1 else ""

    # Structure the response
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
) -> dict:
    try:
        file_bytes = await file.read()
        pdf_content = process_pdf(file_bytes)
        
        if query_type == "custom" and custom_query:
            prompt = custom_query
        else:
            prompt = PROMPT_TEMPLATES.get(query_type)
            if not prompt:
                return {"error": "Invalid query type"}
        
        response = get_gemini_response(prompt, pdf_content, job_description)
        formatted_response = format_response(response)
        return {"response": formatted_response}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
