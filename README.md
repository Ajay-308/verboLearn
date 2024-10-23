![image](https://github.com/user-attachments/assets/244ae382-3583-4354-91ba-e514f1156d81)



# VerboLearn

VerboLearn is a project designed to assist individuals in their job search journey by providing various features to enhance their resume, interview preparation, and English language skills.

Features
### 1. Resume Score Calculator:
VerboLearn's Resume Score Calculator evaluates the suitability of a user's resume for a specific job position. It provides:

1. **Resume Upload**: Users can upload their resume document. 
2. **Job Description Input**: Users provide a job description or details about the position they are interested in.
3. **Matching Analysis**: The system compares the resume with the job requirements.
4. **Score Generation**: VerboLearn generates a score reflecting the alignment between the resume and job requirements.
5. **Feedback**: Detailed feedback is provided along with the score.

### 2. Interview Preparation with AI:
VerboLearn's Interview Preparation feature simulates interview scenarios to help users refine their skills. It includes:

1. **AI Chatbot Jarvis**: Conducts mock interviews with users.
2. **Job-Specific Questions**: Users input the job description.
3. **Mock Interview**: Jarvis asks job-specific interview questions.
4. **Realistic Simulation**: The experience closely simulates real interviews.
5. **Feedback and Improvement**: Users receive constructive feedback on their answers.

### 3. English Language Improvement:
VerboLearn's English Language Improvement feature enhances users' English skills through interactive conversations:

1. **Interactive Chatbot**: Users engage in conversations in English.
2. **Engage in a mock interview with Jarvis**: Practice answering interview questions tailored to the role.
3. **Conversational Practice**: The chatbot initiates conversations on various topics.
4. **Grammar Correction**: Identifies and corrects grammar errors in real-time.
5. **Vocabulary Enhancement**: Offers suggestions to improve vocabulary and phrasing.
6.**Personalized Guidance**: Provides tailored advice based on users' proficiency levels.
   
## Contribution Guidelines
Contributions to TALK USER are welcome! If you'd like to contribute, please follow these
guidelines:
- Fork the repository and create a new branch for your contributions.
- Ensure your code follows the project's coding standards and guidelines.
- Submit a pull request detailing the changes you've made and the problem they address.


## Getting Started:
- To use TALK USER, follow these steps:
1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Ajay-308/TALK_user.git
   
2.Navigate to the project directory:

    cd Talk_user

3. Install any necessary dependencies specified in the documentation.
    ```bash
    npm install
4. Run the Backend in your Local System:
    ```bash
    cd model
    python api.py

5.Run the Frontend Application:
   ```bash
     npm run dev
```
6.Start an ngrok Server and Put the ngrok Domain into Clerk Webhook for User Creation and Sync to Database:

 ```bash
ngrok htttp 3000
