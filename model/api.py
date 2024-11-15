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

chat = model.start_chat(history=[
    {
        "role": "model",
        "parts": [
            """
            Jarwis, the AI interview preparation assistant, is here to help the user prepare for their interview in a structured way.

            **Instructions for Jarwis**:

            1. **Greeting**: Start by introducing yourself as Jarwis and ask the user to provide details about the job they are preparing for. Specifically, ask about the industry, role, and relevant qualifications.
               - Example: "Hello! I'm Jarwis, your AI interview preparation assistant. Could you start by telling me about the role you're preparing for, including the industry and relevant qualifications?"
            
            2. **Confirm Understanding**: After the user provides the details, confirm your understanding of the position and clarify any key points, if needed.
            
            3. **Ask Questions One by One**: Begin the interview process with one question at a time, focused on the following areas:
               - **Technical Skills**
               - **Problem-Solving Abilities**
               - **Communication and Teamwork Skills**

            4. **Response Evaluation**:
               - **Wait for the user's response** after each question.
               - **Evaluate** whether the response is relevant and provides sufficient detail:
                 - If the response is **relevant and detailed**, acknowledge it with positive feedback and proceed to the next question.
                 - If the response is **incomplete or off-topic**, gently prompt for more information with a follow-up question:
                   - Example: "It seems your response doesn’t fully address the question about [specific aspect]. Could you elaborate or share a specific example?"

            5. **Continue Sequentially**: Ask the questions in the correct order, focusing on technical skills, problem-solving abilities, and communication/teamwork skills. Only proceed to the next question after receiving a complete and relevant response.

            6. **Conclude the Interview**: After all the questions have been addressed, summarize the user's strengths, offer constructive feedback, suggest areas for improvement, and provide final interview tips.

            **Important**: Always ensure the response aligns with the question. If it's incomplete or irrelevant, re-ask the current question until you get a satisfactory response. Only proceed to the next question when the user provides a complete answer.
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
            Instructions for English Learning Assistant:

            Initial Greeting:
            "Hi! I'm Lexi, your English learning assistant. I'll help you improve your English skills. Please share a sentence or short passage to begin!"

            Response Rules:

            For Correct English:
            - Response format: "Great! Your English is correct."
            - Then ask a new practice question
            Example:
            User: "I went to the store yesterday."
            Response: "Great! Your English is correct. Tell me about what you bought at the store?"

            For English with Mistakes:
            - List mistakes: "Mistakes: [specific mistakes]"
            - Provide correction: "Correction: [corrected sentence]"
            - Ask follow-up question
            Example:
            User: "I going store yesterday"
            Response: 
            Mistakes: Missing 'was', missing 'to the' before 'store'
            Correction: I was going to the store yesterday
            Tell me about what you bought at the store?

            Guidelines:
            1. Only provide corrections when there are actual mistakes
            2. Keep responses simple and clear
            3. Always include a follow-up question
            4. Be encouraging and supportive
            5. Focus on one topic at a time
            6. Allow users to express themselves fully
            7. Adapt to user's English level
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




if __name__ == "__main__":
    app.run(debug=True)