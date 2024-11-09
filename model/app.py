from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import io
import pdf2image
import google.generativeai as genai
import base64
from pydantic import BaseModel
from typing import Optional, List
import os
import re
from dotenv import load_dotenv

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
genai.configure(api_key=os.getenv("Gemini_Api"))

# Define response models for better structure
class AnalysisResponse(BaseModel):
    summary: str
    strengths: List[dict]
    weaknesses: List[dict]
    suggestions: List[dict]

PROMPT_TEMPLATES = {
    "tell_me_about": """
    You are an experienced Technical Human Resource Manager. Analyze the provided resume against the job description and provide a structured evaluation following exactly this format:

    Summary of Analysis:
    [Provide a brief overview]

    Strengths:
    1. [Title]: [Detailed explanation]
    2. [Title]: [Detailed explanation]
    3. [Title]: [Detailed explanation]
    4. [Title]: [Detailed explanation]
    5. [Title]: [Detailed explanation]

    Weaknesses:
    1. [Title]: [Detailed explanation]
    2. [Title]: [Detailed explanation]
    3. [Title]: [Detailed explanation]

    Suggestions for Improvement:
    1. [Title]: [Detailed explanation]
    2. [Title]: [Detailed explanation]
    3. [Title]: [Detailed explanation]
    4. [Title]: [Detailed explanation]

    Note: Each point must have a clear title followed by a colon and explanation.
    """,

    "improve_skills": """
    You are a Technical Human Resource Manager with expertise in data science. 
    Your role is to scrutinize the resume in light of the job description provided. 
    Share your insights on the candidate's suitability for the role from an HR perspective. 
    Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed. 
    Please do not use  any of these **/##/*, or symbols in your response.

    Strengths:
    1. [Title]: [Detailed explanation]
    2. [Title]: [Detailed explanation]
    3. [Title]: [Detailed explanation]

    Areas for Improvement:
    1. [Title]: [Detailed explanation]
    2. [Title]: [Detailed explanation]
    3. [Title]: [Detailed explanation]

    Skill Enhancement Suggestions:
    1. [Title]: [Detailed explanation]
    2. [Title]: [Detailed explanation]
    3. [Title]: [Detailed explanation]
    Note: Each point must have a clear title followed by a colon and explanation.
    """,

    "missing_keywords": """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
    Your task is to evaluate the resume against the provided job description as a Human Resource manager,
    assess the compatibility of the resume with the role. Provide the keywords that are missing.
    Also, offer recommendations for enhancing the candidate's skills and identify which areas require further development. 
    Avoid using any of these **/##/*, or symbols in your response.

    Compatibility Evaluation:
    [Provide a brief overview of the compatibility]

    Missing Keywords:
    1. [Keyword 1]
    2. [Keyword 2]
    3. [Keyword 3]

    Areas for Skill Improvement:
    1. [Title]: [Detailed explanation]
    2. [Title]: [Detailed explanation]

    Note: Each point must have a clear title followed by a colon and explanation.
    """,

    "percentage_match": """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
    Your task is to evaluate the resume against the provided job description. Give the percentage of match if the resume matches
    the job description. First, provide the percentage, then list missing keywords, and finally, share final thoughts.
    Do not include  any of these **/##/*, symbols, or asterisks in your response.

    percentage_match:
    [Provide the percentage match]

    Missing Keywords:
    1. [Keyword 1]
    2. [Keyword 2]
    3. [Keyword 3]

    Final Thoughts:
    [Provide a summary on the candidate’s fit]

    Note: Each point must have a clear title followed by a colon and explanation.
    """,

    "custom_query": """
    You are an experienced Technical Human Resource Manager tasked with reviewing a resume against a job description. Based on the provided custom query, analyze the candidate’s profile, and provide structured feedback.

    Custom Analysis:
    [Provide detailed feedback based on the custom query]

    Note: Each point must have a clear title followed by a colon and explanation.
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

def format_response(response_text: str, query_type: str) -> dict:
    if query_type == "percentage_match":
        sections = {
            "summary": "",
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }
        
        current_section = None
        missing_keywords = []
        percentage = ""
        final_thoughts = ""
        
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Extract percentage match using regex
            if "Percentage Match:" in line:
                current_section = None
                # Use regex to find the percentage value
                match = re.search(r"(\d+(\.\d+)?)\s?%", line)
                if match:
                    percentage = match.group(0).strip()
                if not percentage:
                    percentage = "N/A"
            
            # Extract missing keywords
            elif "Missing Keywords:" in line:
                current_section = "missing_keywords"
                continue
            
            # Extract final thoughts
            elif "Final Thoughts:" in line:
                current_section = "final_thoughts"
                final_thoughts = line.split(":", 1)[-1].strip()
                if final_thoughts:  # Only add if there are actual thoughts
                    sections["suggestions"].append({
                        "title": "Recommendations",
                        "description": final_thoughts
                    })
                continue
            
            # Process missing keywords
            elif current_section == "missing_keywords" and line[0].isdigit():
                keyword = line.split(".", 1)[-1].strip()
                if keyword:  # Only add if there's an actual keyword
                    sections["weaknesses"].append({
                        "title": "Missing Keyword",
                        "description": keyword
                    })
            
            # Add any additional points under final thoughts
            elif current_section == "final_thoughts" and line:
                final_thoughts += " " + line
                sections["suggestions"] = [{
                    "title": "Recommendations",
                    "description": final_thoughts.strip()
                }]

        return sections
    
    elif query_type == "missing_keywords":
        sections = {
            "summary": "",
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }
        
        current_section = None
        
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "Compatibility Evaluation:" in line:
                current_section = "summary"
                sections["summary"] = line.split(":", 1)[-1].strip()
            elif "Missing Keywords:" in line:
                current_section = "missing_keywords"
            elif "Areas for Skill Improvement:" in line:
                current_section = "improvements"
            elif current_section == "missing_keywords" and line[0].isdigit():
                keyword = line.split(".", 1)[-1].strip()
                if keyword:
                    sections["weaknesses"].append({
                        "title": "Missing Keyword",
                        "description": keyword
                    })
            elif current_section == "improvements" and line[0].isdigit():
                title, desc = line.split(":", 1) if ":" in line else (line, "")
                if desc.strip():
                    sections["suggestions"].append({
                        "title": title.split(".", 1)[-1].strip(),
                        "description": desc.strip()
                    })
        
        return sections
    
    else:
        # Original format_response logic for other query types
        sections = {
            "summary": "",
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }
        
        current_section = None
        
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "Summary of Analysis" in line:
                current_section = "summary"
                continue
            elif "Strengths" in line:
                current_section = "strengths"
                continue
            elif "Weaknesses" in line or "Areas for Improvement" in line:
                current_section = "weaknesses"
                continue
            elif "Suggestions for Improvement" in line or "Skill Enhancement Suggestions" in line:
                current_section = "suggestions"
                continue
                
            if current_section == "summary":
                sections["summary"] += line + " "
            elif current_section in ["strengths", "weaknesses", "suggestions"]:
                if line[0].isdigit():  # Check if line starts with a number
                    point = parse_point(line)
                    sections[current_section].append(point)
        
        return sections

def parse_point(point: str) -> dict:
    """Parse a point into title and description"""
    try:
        # Remove the number and dot at the start
        point = point.split('.', 1)[-1].strip()
        if ':' in point:
            title, description = point.split(':', 1)
            return {
                "title": title.strip(),
                "description": description.strip()
            }
        else:
            return {
                "title": "Point",
                "description": point.strip()
            }
    except:
        return {
            "title": "Point",
            "description": point.strip()
        }

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
        structured_response = format_response(response, query_type)
        print(structured_response)
        return structured_response
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)