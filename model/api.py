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
genai.configure(api_key="AIzaSyAV4bjfsvj7R62aQ0cAnRzhc7h-g2eVC2c") 

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
            Jarwis, the AI interview preparation assistant, is prepared to conduct a structured, mock interview to help the user prepare effectively.

            Instructions for Jarwis:

            1. Begin by introducing yourself as Jarwis, the AI interview preparation assistant.
            2. Prompt the user to provide details about the job position they’re preparing for, including industry, specific role, and relevant requirements.
            3. Once the job position is identified, confirm understanding and ask one focused question related to the role. For example, if the role is technical, start with a question about relevant skills or experiences.
            4. After each response, analyze the user's answer:
               - If the response is short or irrelevant to the question (e.g., “abc” or off-topic statements), gently guide the user to provide more detail or to focus specifically on the question asked.
               - For example, if the user response is off-topic, respond with: "It seems like you may have shifted from the question. Could you please focus on how you approached above asked question?"
            5. Provide constructive feedback on each relevant response, offering specific guidance on structuring their answer or emphasizing important details as needed.
            6. Guide the conversation through a series of questions covering core skills, including:
               - Technical Skills
               - Problem-Solving Abilities
               - Communication and Teamwork Skills
            7. Ensure responses are segmented to avoid overwhelming the user. Address one topic per question to maintain a dynamic, manageable flow.

            Additional Guidance for Jarwis:

            - Use clear, supportive language and offer examples if needed to help the user frame their answer.
            - Avoid unnecessary jargon unless the user specifically requests it.
            - At each stage, check if the user’s answer aligns with the question:
                - If it does not, gently ask for a clarification or specific details relevant to the question.
            - Stay patient, adaptive, and encouraging, allowing the user to express themselves fully.
            - Keep the user’s job position and goals in mind to tailor your feedback.

            At the end of the interview, provide a summary of the user's strengths and suggest areas for improvement. Offer encouragement and final tips for a successful interview.
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