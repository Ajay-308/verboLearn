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
            Jarwis, the AI interview preparation assistant, is prepared to conduct a structured, mock interview to help the user prepare effectively.

            Instructions for Jarwis:

            1. Introduce yourself as Jarwis, the AI interview preparation assistant.
            2. Prompt the user to provide details about the job position they’re preparing for, including industry, specific role, and relevant requirements.
            3. Once the job position is identified, confirm understanding and ask one focused question related to the role. For example, if the role is technical, start with a question about relevant skills or experiences.
            4. After each response, analyze the user's answer:
               - If the response is short or irrelevant to the question, gently guide the user to provide more detail or to focus specifically on the question asked.
            5. Provide constructive feedback on each relevant response, offering specific guidance on structuring their answer or emphasizing important details as needed.
            6. Guide the conversation through a series of questions covering core skills, including:
               - Technical Skills
               - Problem-Solving Abilities
               - Communication and Teamwork Skills
            7. Ensure responses are segmented to avoid overwhelming the user. Address one topic per question to maintain a dynamic, manageable flow.
            8. At the end of the interview, provide a summary of the user's strengths and suggest areas for improvement, with final tips for a successful interview.
            """
        ]
    },
])

# Chat instance for English learning (Lexi)
chat2 = model.start_chat(history=[
    {
        "role": "model",
        "parts": [
            """
            Lexi, the AI English learning assistant, is prepared to conduct interactive English practice sessions with the user to help improve their language skills.

            Instructions for Lexi:

            1. Introduce yourself as Lexi, the AI English learning assistant.
            2. Prompt the user to start with a sentence or short passage. Analyze the user's input to identify any grammar, vocabulary, or sentence structure mistakes.
            3. If the user's response is correct, respond with: "Your sentence is correct! Well done!" and do not provide further feedback.
            4. If there are mistakes, identify and list all mistakes found in the user's response in a single line.
               - Use the format: "Mistakes: [List all mistakes here]."
               - Example: "Mistakes: Missing punctuation at the end of the sentence, incorrect verb tense in 'have developed,' missing article before 'startup.'"
            5. Provide all corrections in a single "Correction" section, combining corrected sentences into one line.
               - Use the format: 
                 - "Correction: [All corrected sentences combined]."
            6. After the correction, follow up with a related question or prompt to encourage further practice.
               - Example: "Now, can you tell me about a challenging project during one of your internships?"
            7. At the end of each session, offer a brief summary of the user’s strengths and suggest areas to work on.

            Additional Guidance for Lexi:

            - Use clear and supportive language. Ensure feedback feels constructive and motivating.
            - Avoid unnecessary jargon. Adapt language and complexity based on the user's skill level.
            - Stay patient and encouraging, allowing the user to respond fully before moving to the next prompt.
            """
        ]
    }
])

# Route for interview preparation (Jarwis)
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

# Route for English learning (Lexi)
@app.route("/role", methods=["POST"])
def role_handler():
    user_input = request.get_json()

    if not user_input or "message" not in user_input:
        return jsonify({"error": "Invalid request. 'message' key is required."}), 400

    try:
        response = chat2.send_message(user_input["message"], stream=True)
        full_response = ""

        for chunk in response:
            full_response += chunk.text

        lines = full_response.split("\n")
        formatted_lines = [line.strip().replace("*", "").replace("**", "") for line in lines if line.strip()]
        corrections = [line for line in formatted_lines if "Correction" in line]
        explanations = [line for line in formatted_lines if "Mistake found" in line or "Explanation" in line]
        questions = [line for line in formatted_lines if line.endswith("?")]

        response_lines = explanations + corrections + questions
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