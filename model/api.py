from flask import Flask, request, jsonify
import google.generativeai as genai
import base64
import io
from PIL import Image
import pdf2image
from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os


load_dotenv()  
genai.configure(api_key=os.getenv("Gemini_Api")) 

app = Flask(__name__)
CORS(app,supports_credentials=True)

model = genai.GenerativeModel(model_name="gemini-pro") 

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
chat = model.start_chat(history=[
    {
        "role": "model",
        "parts": [
            """
            Jarwis, the AI interview preparation assistant, is assuming the role of a recruiter conducting a mock interview.

            The user seeks guidance from Jarwis to prepare for an upcoming job interview.

            Jarwis aims to assist the user by tailoring the mock interview to the specific job position.

            Instructions for the AI model:

            1. Initiate the conversation by introducing yourself as Jarwis, the AI interview preparation assistant.
            2. Politely inquire about the job position the user is preparing for.
            3. Encourage the user to provide details such as the industry, specific role, or any other relevant information.
            4. Express genuine interest and assure the user that Jarwis is dedicated to helping them prepare effectively.
            5. Instead of providing all the interview questions at once, ask the user one question related to the job position to maintain a dynamic interaction.
            6. Refrain from giving direct answers; instead, guide the user on how to approach and structure their responses effectively.
            7. After the user's response, provide constructive feedback, tips, or additional questions to help them refine their answers further.
            8. Continue the conversation in a conversational and supportive tone, guiding the user through a comprehensive mock interview experience.

            Additional Guidelines:

            - Maintain a friendly and professional demeanor throughout the interaction.
            - Be patient and understanding, allowing the user to elaborate on their thoughts and experiences.
            - Avoid using jargon or overly technical language that may confuse the user.
            - Adapt your responses based on the user's inputs and demonstrate flexibility in your approach.
            - Always keep the user's goals and the specific job position in mind when providing guidance.
            """
        ]
    },
])


@app.route("/chat", methods=["POST"])
def chat_handler():

    user_message = request.get_json()

    if not user_message or "message" not in user_message:
        return jsonify({"error": "Invalid request. 'message' key is required."}), 400

    try:
        response = chat.send_message(user_message["message"], stream=True)  
        full_response = ""
        for chunk in response:
            full_response += chunk.text
        lines = full_response.split("\n")
        formatted_lines = [line.strip().replace("*", "").replace("**", "") for line in lines if line.strip()]
        questions = [line for line in formatted_lines if line.endswith("?")] 
        other_lines = [line for line in formatted_lines if not line.endswith("?")] 
        response_lines = other_lines + questions
        return jsonify({"message": response_lines})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form.get('input_text')
    uploaded_file = request.files.get('uploaded_file')

    if not (input_text and uploaded_file):
        return jsonify({"error": "Invalid data format. Make sure to provide 'input_text' and 'uploaded_file'."}), 400

    pdf_content = input_pdf_setup(uploaded_file)
    input_prompt1 = """
    I hope this message finds you well. As an experienced Technical Human Resource Manager, your expertise is needed to evaluate a candidate's profile against a specific job description. Your task is to provide a professional assessment of whether the candidate's profile aligns with the role, highlighting their strengths and weaknesses in relation to the specified job requirements. Please organize your evaluation in a structured manner using bullet points, ensuring the text does not exceed 150 words.
    """
    input_prompt2 = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality and NLP For this task, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match with  job description . First the output should come in percentage and then keyword-present , than that word if which present in resume this resume should to crack any job and then  last final thoughts"""

    strength = get_gemini_response(input_text, pdf_content, input_prompt1)
    ats_score = get_gemini_response(input_text, pdf_content, input_prompt2)
    
    return jsonify({"strength": strength, "ats_score": ats_score})

if __name__ == "__main__":
    app.run(debug=True)