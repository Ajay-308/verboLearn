# Verbo Learn

Verbo Learn is a project designed to assist individuals in their job search journey by
providing various features to enhance their resume, interview preparation, and English
language skills.

# Features

### 1. Resume Score Calculator :

Verbo Learn's Resume Score Calculator evaluates the suitability of a user's resume for a
specific job position. It provides:

1. **Resume Upload**: Users can upload their resume document.
2. **Job Description Input**: Users provide a job description or details about the position
   they are interested in.
3. **Matching Analysis**: The system compares the resume with the job requirements.
4. **Score Generation**: Verbo Learn generates a score reflecting the alignment
   between the resume and job requirements.
5. **Feedback**: Detailed feedback is provided along with the score.

### 2. Interview Preparation with AI :

Verbo Learn's Interview Preparation feature simulates interview scenarios to help users
refine their skills. It includes:

1. **AI Chatbot Jarvis**: Conducts mock interviews with users.
2. **Job-Specific Questions**: Users input the job description.
3. **Mock Interview**: Jarvis asks job-specific interview questions.
4. **Realistic Simulation**: The experience closely simulates real interviews.
5. **Feedback and Improvement**: Users receive constructive feedback on their
   answers.

### 3. English Language Improvement :

Verbo Learn's English Language Improvement feature enhances users' English skills
through interactive conversations:

- **Interactive Chatbot**: Users engage in conversations in English.
- **Conversational Practice**: The chatbot initiates conversations on various topics.
- **Grammar Correction**: Identifies and corrects grammar errors in real-time.
- **Vocabulary Enhancement**: Offers suggestions to improve vocabulary and phrasing.
- **Personalized Guidance**: Provides tailored advice based on users' proficiency levels.

## Usage

1. **Resume Score Calculation**:

- Upload your resume.
- Input a job description.
- Receive a score indicating how well your resume matches the job requirements.

2. **Interview Preparation with AI**:

- Input a job description.
- Engage in a mock interview with Jarvis.
- Practice answering interview questions and receive feedback.

3. **English Language Improvement**:

- Interact with the chatbot in English.
- Engage in conversations, receive corrections, and improve your English skills.

## Contribution Guidelines

Contributions to Verbo Learn are welcome! If you'd like to contribute, please follow these
guidelines:

- Fork the repository and create a new branch for your contributions.
- Ensure your code follows the project's coding standards and guidelines.
- Submit a pull request detailing the changes you've made and the problem they address.

## Getting Started:

- To use Verbo Learn, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Ajay-308/verboLearn.git

   ```

2.Navigate to the project directory:

    cd verboLearn

3. Install any necessary dependencies specified in the documentation.
   ```bash
   npm install
   4.Run the Backend in you local sytem:
   ```bash
      cd model
      python api.py
      uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

5.Run the frontend application:
npm run dev
