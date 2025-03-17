# AI-Powered Hiring Assistant Chatbot

## Project Overview
The AI-Powered Hiring Assistant Chatbot is designed to streamline the hiring process by assisting recruiters and job seekers. It leverages Together AI's open-source models to analyze resumes, generate interview questions, and provide insights based on job descriptions.

## Installation Instructions
### Prerequisites
- Python 3.x
- Pip package manager
- Virtual environment (optional but recommended)

### Setup
1. Clone the repository:
   ```sh
   git clone <repository-link>
   cd hiring-assistant-chatbot
   ```
2. Create and activate a virtual environment (optional):
   ```sh
   python -m venv venv
   source venv/bin/activate   # For macOS/Linux
   venv\Scripts\activate      # For Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   streamlit run app.py
   ```

## Usage Guide
- Enter a job description or upload a resume.
- The chatbot analyzes the input and generates interview questions.
- It provides hiring insights and suitability recommendations.

## Technical Details
### Libraries Used
- Streamlit: Web-based UI framework
- Together AI API: AI model for resume analysis and interview question generation

### Architecture
- **Frontend:** Built using Streamlit
- **Backend:** AI model processing using Together AI
- **Integration:** API calls to Together AI for response generation

## Prompt Design
- Prompts are structured to extract key information from resumes and job descriptions.
- Follow-up prompts ensure detailed and relevant insights.
- Adjusted to handle various job roles and industries dynamically.

## Challenges & Solutions
### Challenges
- Ensuring the chatbot understands various job descriptions accurately.
- Handling multiple resume formats effectively.
- Optimizing API calls for efficiency.

### Solutions
- Used structured parsing techniques to improve text analysis.
- Implemented robust error handling for API requests.
- Designed modular functions for scalability and maintainability.

## Demo
[Live Demo Link (https://www.loom.com/share/a0026e761aba469892f12bfaada0dde2?sid=743b2268-0262-44c9-b4c1-285090442902)]

## Submission Guidelines
- Deadline: 48 Hours
- Submit Git repository and demo link via the Career Portal.
- Ensure all files are accessible and the repository is public or has shared access.

## Code Quality & Documentation
- **Structure & Readability:** Well-organized codebase following best practices.
- **Documentation:** Inline comments and docstrings for clarity.
- **Version Control:** Git repository with meaningful commit messages.

---
This README provides a clear overview of your Hiring Assistant Chatbot, installation steps, usage guide, and technical details. Let me know if you need any modifications! 🚀

