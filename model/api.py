from flask import Flask, request, jsonify
from flask_cors import CORS
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
import base64
import io
import pdf2image
import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3

# Load environment variables from .env file
load_dotenv()  
genai.configure(api_key=os.getenv('API_KEY')) 

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Create the model instance
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

def get_gemini_response(input_text, pdf_content, job_description):
    response = model.generate_content([input_text, pdf_content[0], job_description])
    return response.text

def input_pdf_setup(uploaded_file):
    try:
        # Convert the PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file)
        first_page = images[0]

        # Convert the first page to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Prepare image data as base64
        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
        }]
        return pdf_parts
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")

# Initialize chat history for different contexts
chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["Certainly! Here's a modified prompt to ensure Jarwis doesn't provide all the questions at once and refrains from giving answers:\n\n---\n\n**Prompt:**\n\n\"Jarwis, the personal interview preparation assistant, is now simulating a recruiter role. The user has approached Jarwis for interview preparation. In this scenario, Jarwis is conducting a mock interview and needs to gather information about the job position the user is preparing for. The goal is to assist the user in their interview preparation by tailoring the guidance to the specific job role.\n\n**Instructions for the AI model:**\n\n1. Start the conversation by introducing yourself as Jarwis, the interview preparation assistant.\n2. Politely ask the user about the job position they are preparing for.\n3. Encourage the user to provide details such as the industry, specific role, or any other relevant information.\n4. Express genuine interest and assure the user that Jarwis is here to help them prepare effectively.\n5. Rather than providing all the interview questions at once, ask the user one question related to the job position to keep the interaction dynamic.\n6. Refrain from giving answers; instead, guide the user on how to approach and structure their responses.\n7. After the user responds, provide constructive feedback, tips, or additional questions to help them refine their answers.\n8. Continue the conversation in a conversational and helpful tone, guiding the user through a mock interview experience."]
    },
    {
        "role": "model",
        "parts": ["Certainly! Here's a refined prompt that incorporates your suggestions:\n\n**Prompt:**\n\n\"Jarwis, the AI interview preparation assistant, is assuming the role of a recruiter conducting a mock interview. The user seeks guidance from Jarwis to prepare for an upcoming job interview. Jarwis aims to assist the user by tailoring the mock interview to the specific job position.\n\n**Instructions for the AI model:**\n\n1. Initiate the conversation by introducing yourself as Jarwis, the AI interview preparation assistant.\n2. Politely inquire about the job position the user is preparing for.\n3. Encourage the user to provide details such as the industry, specific role, or any other relevant information.\n4. Express genuine interest and assure the user that Jarwis is dedicated to helping them prepare effectively.\n5. Instead of providing all the interview questions at once, ask the user one question related to the job position to maintain a dynamic interaction.\n6. Refrain from giving direct answers; instead, guide the user on how to approach and structure their responses effectively.\n7. After the user's response, provide constructive feedback, tips, or additional questions to help them refine their answers further.\n8. Continue the conversation in a conversational and supportive tone, guiding the user through a comprehensive mock interview experience.\n\n**Additional Guidelines:**\n\n* Maintain a friendly and professional demeanor throughout the interaction.\n* Be patient and understanding, allowing the user to elaborate on their thoughts and experiences.\n* Avoid using jargon or overly technical language that may confuse the user.\n* Adapt your responses based on the user's inputs and demonstrate flexibility in your approach.\n* Always keep the user's goals and the specific job position in mind when providing guidance."]
    }
])

chat2 = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["Certainly! here is jarwis my english is not good so i need your help to improve my english and i am preparing for an job interview where english is needed to talk, and to crack interview i need to improve my english so please help me to improve my spoken english"]
    },
    {
        "role": "model",
        "parts": ["Jarwis, an AI English instructor, is here to assist you in improving your English skills. Begin the conversation by introducing yourself as Jarwis, the AI English instructor. Politely engage with the user, inquire about their details, and await their response. Provide specific feedback on their English by identifying mistakes in their sentences, followed by corrections. Use concise responses, keeping them under 100 words. Prompt the user with examples they won't forget, such as stories about their loved ones. Help them understand where their English may be incorrect and guide them toward correct usage in subsequent prompts. Continue the conversation in a conversational and supportive tone, guiding the user to a comprehensive English learning experience."]
    }
])

@app.route("/chat", methods=["POST"])
def chat_handler():
    user_message = request.get_json()

    response = chat.send_message(user_message["message"], stream=True)
    full_response = "".join(chunk.text for chunk in response)

    return jsonify({"message": full_response})

@app.route("/role", methods=["POST"])
def role_handler():
    user_message = request.get_json()

    response = chat2.send_message(user_message["message"], stream=True)
    full_response = "".join(chunk.text for chunk in response)
    
    return jsonify({"message": full_response})

@app.post('/process')
async def evaluate_resume(
    file: UploadFile = File(...),  # Ensure you're using UploadFile
    job_description: str = "", 
    task: str = "evaluation"
):
    # Check if the file has been uploaded
    if not file:
        raise HTTPException(status_code=400, detail="No file part")

    # Check if the file type is PDF by checking the filename
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File type not allowed")

    # Prompts for different tasks
    prompts = {
        "evaluation": """
        You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
        Please share your professional evaluation on whether the candidate's profile aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """,
        "improvement": """
        You are an experienced Technical Human Resource Manager with expertise in data science, 
        your role is to scrutinize the resume in light of the job description provided. 
        Share your insights on the candidate's suitability for the role from an HR perspective. 
        Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
        """,
        "keywords": """
        You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
        Your task is to evaluate the resume against the provided job description. As a Human Resource Manager,
        assess the compatibility of the resume with the role. Provide a list of missing keywords and offer recommendations for improving the resume.
        """,
        "percentage_match": """
        You are a skilled ATS scanner with expertise in data science. Your task is to evaluate the resume against the provided job description and provide the percentage match.
        Then, list the missing keywords and provide your final thoughts.
        """
    }

    if task not in prompts:
        raise HTTPException(status_code=400, detail="Invalid task specified.")

    try:
        pdf_content = await file.read()

        processed_pdf_content = input_pdf_setup(pdf_content)

        response_text = get_gemini_response(prompts[task], processed_pdf_content, job_description)

        # Return response
        return JSONResponse(content={"response": response_text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in processing: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
