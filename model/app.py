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
    Your task is to evaluate the resume against the provided job description. 
    Follow this exact format in your response:

    percentage_match: [number]%

    Missing Keywords:
    1. [Keyword 1]
    2. [Keyword 2]
    3. [Keyword 3]

    Final Thoughts:
    [Provide a brief summary of the candidate's fit]

    Note: The percentage must be a number between 0 and 100, followed by the % symbol.
    """,
        "custom_query": """
    You are an experienced Technical Human Resource Manager. Based on the provided resume and job description, 
    analyze and respond to this specific query:

    {query}

    Please structure your response in this format:

    Summary of Analysis:
    [Provide a comprehensive overview]

    Key Points:
    1. [Title]: [Detailed explanation]
    2. [Title]: [Detailed explanation]
    3. [Title]: [Detailed explanation]

    Additional Insights:
    - [Important point 1]
    - [Important point 2]
    - [Important point 3]

    Note: Each point should have a clear title followed by a detailed explanation.
    """,

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
    if query_type == "missing_keywords":
        sections = {
            "summary": "",
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }
        
        current_section = None
        lines = response_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Handle Compatibility Evaluation section
            if "Compatibility Evaluation:" in line:
                current_section = "compatibility"
                continue
            elif "Missing Keywords:" in line:
                current_section = "missing_keywords"
                continue
            elif "Areas for Skill Improvement:" in line:
                current_section = "improvements"
                continue
            
            # Process sections
            if current_section == "compatibility":
                if not line.startswith("Missing") and not line.startswith("Areas"):
                    sections["summary"] += line + " "
            
            elif current_section == "missing_keywords" and line[0].isdigit():
                keyword = line.split(".", 1)[-1].strip()
                if keyword:
                    sections["weaknesses"].append({
                        "title": "Missing Keyword",
                        "description": keyword
                    })
            
            elif current_section == "improvements" and line[0].isdigit():
                point = parse_point(line)
                sections["suggestions"].append(point)
        
        return sections
        
    elif query_type == "percentage_match":
        sections = {
            "summary": "",
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "percentage": "0"
        }
        
        current_section = None
        lines = response_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            if "percentage" in line.lower() or "match" in line.lower():
                match = re.search(r"(\d+(\.\d+)?)\s*%?", line)
                if match:
                    sections["percentage"] = match.group(1)
                    sections["summary"] = f"Resume matches {sections['percentage']}% with the job description"
                continue
            elif "Missing Keywords:" in line:
                current_section = "missing_keywords"
                continue
            elif "final thoughts:" in line.lower():
                current_section = "final_thoughts"
                thoughts = []
                for next_line in lines[i+1:]:
                    if next_line.strip() and not any(section in next_line.lower() for section in ["missing keywords:", "percentage match:"]):
                        thoughts.append(next_line.strip())
                    else:
                        break
                if thoughts:
                    sections["suggestions"].append({
                        "title": "Final Thoughts",
                        "description": " ".join(thoughts)
                    })
                continue
            
            if current_section == "missing_keywords" and line[0].isdigit():
                keyword = line.split(".", 1)[-1].strip()
                if keyword:
                    sections["weaknesses"].append({
                        "title": "Missing Keyword",
                        "description": keyword
                    })
        
        if not sections["summary"]:
            sections["summary"] = "Unable to determine exact percentage match"
        
        return sections
    elif query_type == "custom":
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
            
            # Detect sections
            if "Summary of Analysis" in line or "Analysis Result" in line:
                current_section = "summary"
                continue
            elif "Strengths" in line:
                current_section = "strengths"
                continue
            elif "Weaknesses" in line:
                current_section = "weaknesses"
                continue
            elif "Suggestions for Improvement" in line:
                current_section = "suggestions"
                continue
            elif "Custom Analysis" in line or "Key Points" in line:
                # Keep current section if we're in summary, otherwise set to suggestions
                if current_section != "summary":
                    current_section = "suggestions"
                continue
            
            # Process content based on current section
            if current_section == "summary":
                if not line.startswith("**"):  # Ignore markdown headers
                    sections["summary"] += line + " "
            elif current_section in ["strengths", "weaknesses", "suggestions"]:
                # Check if it's a point with title and description
                if "**" in line:  # Handle markdown formatted points
                    line = line.replace("**", "").strip()
                    if ":" in line:
                        title, description = line.split(":", 1)
                        point = {
                            "title": title.strip(),
                            "description": description.strip()
                        }
                    else:
                        point = {
                            "title": "Key Point",
                            "description": line.strip()
                        }
                    sections[current_section].append(point)
                elif line.startswith("-"):  # Handle bullet points
                    point = {
                        "title": "Key Point",
                        "description": line[1:].strip()
                    }
                    sections[current_section].append(point)
                elif ":" in line:  # Handle regular points with colons
                    title, description = line.split(":", 1)
                    point = {
                        "title": title.strip(),
                        "description": description.strip()
                    }
                    sections[current_section].append(point)
                elif line and not line.startswith("**"):  # Handle other non-empty, non-header lines
                    point = {
                        "title": "Key Point",
                        "description": line.strip()
                    }
                    sections[current_section].append(point)
        
        # Clean up summary by removing extra whitespace and markdown
        sections["summary"] = " ".join(sections["summary"].split())
        sections["summary"] = re.sub(r'\*\*', '', sections["summary"])
        
        # Move any non-categorized points to suggestions
        if not any([sections["strengths"], sections["weaknesses"], sections["suggestions"]]):
            current_points = []
            for line in lines:
                line = line.strip()
                if line and "**" in line:
                    line = line.replace("**", "").strip()
                    if ":" in line:
                        title, description = line.split(":", 1)
                        point = {
                            "title": title.strip(),
                            "description": description.strip()
                        }
                        current_points.append(point)
            if current_points:
                sections["suggestions"] = current_points
        
        return sections
    
    else:
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
                if line[0].isdigit():
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
            # Combine the template with the custom query
            prompt = PROMPT_TEMPLATES["custom_query"] + "\n\nCustom Query: " + custom_query
        else:
            prompt = PROMPT_TEMPLATES.get(query_type)
            if not prompt:
                return {"error": "Invalid query type"}
        
        response = get_gemini_response(prompt, pdf_content, job_description)
        structured_response = format_response(response, query_type)
        return structured_response
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)