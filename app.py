import streamlit as st
import requests
from textblob import TextBlob
from googletrans import Translator, LANGUAGES
from langdetect import detect
import PyPDF2
import random

# --- Page Configuration ---
st.set_page_config(page_title="TalentScout AI", layout="wide", initial_sidebar_state="expanded")

# --- Improved Custom Styling (with Font Size Adjustments and Color Palette Refinement) ---
st.markdown("""
<style>
/* General Body Styling */
body {
    color: #333333; /* Darker gray for better readability */
    background-color: #f8f8f8; /* Slightly darker background */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Modern, clean font */
}

/* Chat Container */
.chat-container {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.08); /* Softer shadow */
    margin-bottom: 15px;
    border: 1px solid #e0e0e0; /* Light gray border */
}

/* Chatbot Title */
.chatbot-title {
    font-size: 38px; /* Slightly larger title */
    font-weight: bold;
    color: #2962FF; /* Primary blue color (brighter) */
    text-align: center;
    margin-bottom: 25px; /* Reduced bottom margin */
    text-shadow: 1px 1px 2px rgba(0,0,0,0.05); /* Subtle text shadow */
}

/* Section Titles */
.section-title {
    font-size: 26px; /* Adjusted size */
    font-weight: bold;
    color: #4CAF50; /* Green accent color (Material Design green) */
    margin-top: 25px; /* Adjusted top margin */
    margin-bottom: 15px; /* Adjusted bottom margin */
    border-bottom: 3px solid #4CAF50;
    padding-bottom: 6px; /* Reduced padding */
}

/* User Text */
.user-text {
    background-color: #e3f2fd; /* Light blue background */
    padding: 12px 18px;
    border-radius: 20px; /* More rounded corners */
    margin-bottom: 8px;
    color: #1565C0; /* Darker blue text */
    border: 1px solid #bbdefb; /* Light blue border */
    font-size: 16px;
}

/* Bot Text */
.bot-text {
    background-color: #fffde7; /* Light yellow background */
    padding: 12px 18px;
    border-radius: 20px; /* More rounded corners */
    margin-bottom: 8px;
    color: #512DA8; /* Deep purple text */
    border: 1px solid #fff9c4; /* Light yellow border */
    font-size: 16px;
}

/* Sentiment */
.sentiment {
    font-size: 16px;
    color: #616161; /* Medium gray color */
    font-weight: bold;
    margin-bottom: 10px;
}

/* Language */
.language {
    font-size: 14px;
    color: #757575; /* Slightly lighter gray */
}

/* Sidebar */
.sidebar .sidebar-content {
    background-color: #f9f9f9; /* Lighter sidebar background */
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06); /* Softer sidebar shadow */
    border: 1px solid #e0e0e0; /* Light gray border for sidebar */
}

/* Buttons */
.stButton button {
    background-color: #2962FF; /* Primary blue button color */
    color: white;
    border-radius: 25px; /* More rounded buttons */
    padding: 12px 28px; /* Slightly wider buttons */
    font-size: 18px;
    font-weight: 500; /* Medium font weight */
    border: none;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Softer button shadow */
    transition: all 0.3s ease;
}

.stButton button:hover {
    background-color: #1A237E; /* Darker blue on hover */
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15); /* Increased shadow on hover */
}

/* Input Fields (Text Input, Text Area, Selectbox, File Uploader) */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    color: white !important; /* Make text black and important to override defaults */
}
.stFileUploader > div > div > div {
    border-radius: 12px; /* Rounded input fields */
    border: 1.5px solid #bdbdbd; /* Slightly thicker border */
    padding: 12px;
    background-color: #fafafa; /* Very light gray background */
    transition: border-color 0.3s ease, box-shadow 0.3s ease; /* Smooth transitions */
    font-size: 16px;
    color: #424242; /* Darker input text color */
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > div:focus-within,
.stFileUploader > div > div > div:focus-within {
    border-color: #2962FF; /* Focus color (primary blue) */
    box-shadow: 0 0 6px rgba(41, 98, 255, 0.4); /* Focus shadow */
}

/* Checkbox */
.stCheckbox label {
  font-size: 16px;
  color: #333333; /* Checkbox label color */
}

/* Footer */
.footer {
  margin-top: 40px; /* Adjusted margin */
  padding-top: 15px; /* Adjusted padding */
  border-top: 1px solid #e0e0e0; /* Lighter border */
  text-align: center;
  font-size: 14px;
  color: #757575; /* Footer text color */
}

/* Summary Title */
.summary-title {
    font-size: 18px;
    font-weight: bold;
    color: #2962FF; /* Summary title color (primary blue) */
    margin-top: 10px;
}

/* Summary Container - Increased Size and Refined Style */
.summary-container {
    background-color: #e8f0fe; /* Light blue summary background */
    border: 1.5px solid #bbdefb; /* Light blue border */
    border-radius: 12px; /* Rounded summary container */
    padding: 15px;
    margin-top: 10px;
    font-size: 16px; /* Consistent font size */
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); /* Subtle inner shadow */
}

""", unsafe_allow_html=True)

# --- API Setup ---
def get_ai_response(prompt):
    """Fetch AI-generated responses from Together AI."""
    API_URL = "https://api.together.xyz/v1/completions"
    headers = {"Authorization": "Bearer Together api key"} # Replace with your API key
    data = {
        "model": "mistralai/mistral-7b-instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 256,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1.1
    }
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "No response received.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with AI service: {e}")
        return "Failed to get AI response."

# --- Sentiment Analysis ---
def analyze_sentiment(response):
    blob = TextBlob(response)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0.2:
        return "Positive 😊 Confident ✅", "Great! You seem confident! 👍"
    elif sentiment_score < -0.2:
        return "Negative 😞 Needs Assistance ❌", "Let's work on areas for improvement."
    else:
        return "Neutral 😐 Unsure ⚠️", "It seems you're unsure. Let's clarify."

# --- Language Detection & Translation ---
def detect_and_translate(text, target_lang='en'):
    try:
        detected_lang = detect(text)
        if detected_lang != target_lang:
            translator = Translator()
            translated_text = translator.translate(text, src=detected_lang, dest=target_lang).text
            return translated_text, detected_lang
        return text, detected_lang
    except Exception as e:
        st.error(f"Language detection/translation error: {e}")
        return text, 'en'

# --- Resume Analysis ---
def analyze_resume(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# --- Sidebar (Removed History Section) ---
with st.sidebar:
    # Removed History Section
    st.markdown("<hr style='border-top: 1px dashed #D0D3D4;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #2962FF;'>📌 Additional Information</h2>", unsafe_allow_html=True) # Sidebar title color changed
    st.markdown("""
        **TalentScout AI** assists with technical interviews.

        **Features:**
        - AI-powered question generation.
        - Sentiment analysis.
        - Multi-language support.
        - Resume analysis.

        **How to Use:**
        1. Fill out the form.
        2. Upload a resume.
        3. Chat with the AI.
    """)

# --- Header ---
st.markdown("<h1 class='chatbot-title'>🤖 TalentScout AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px; color: #757575;'>AI-Powered Candidate Assessment</p>", unsafe_allow_html=True) # Header subtitle color changed

# --- Main Content ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h2 class='section-title'>📋 Candidate Form</h2>", unsafe_allow_html=True)
    with st.form("candidate_form"):
        if "candidate_form_data" not in st.session_state:
            st.session_state.candidate_form_data = {}

        name = st.text_input("Full Name", value=st.session_state.candidate_form_data.get('name', ''))
        email = st.text_input("Email", value=st.session_state.candidate_form_data.get('email', ''))
        phone = st.text_input("Phone", value=st.session_state.candidate_form_data.get('phone', ''))
        experience = st.selectbox("Years of Experience", ["0-1", "2-3", "4-6", "7+"], index=["0-1", "2-3", "4-6", "7+"].index(st.session_state.candidate_form_data.get('experience', "0-1")))
        position = st.text_input("Desired Position", value=st.session_state.candidate_form_data.get('position', ''))
        location = st.text_input("Location", value=st.session_state.candidate_form_data.get('location', ''))
        tech_stack = st.text_area("Tech Stack (comma-separated)", value=st.session_state.candidate_form_data.get('tech_stack', ''))
        submit = st.form_submit_button("🚀 Generate Questions")

        if submit:
            st.session_state.candidate_form_data.update({
                'name': name, 'email': email, 'phone': phone,
                'experience': experience, 'position': position,
                'location': location, 'tech_stack': tech_stack
            })

            if all([name, email, phone, tech_stack]):
                st.success(f"✅ Generating questions for {position} based on: {tech_stack}...")
                prompt = f"Generate 3-5 unique technical questions for a {experience} year experienced {position} candidate skilled in {tech_stack}. Focus on practical skills and problem-solving. Questions should be diverse, specific to: {tech_stack}."
                questions = get_ai_response(prompt)
                if questions:
                    st.markdown(f"<h3 style='color: #2E86C1;'>💡 Questions for {tech_stack}:</h3>", unsafe_allow_html=True)
                    st.write(questions)
                else:
                    st.error("Failed to generate questions.")
            else:
                st.error("⚠️ Please fill all fields.")

    st.markdown("<h2 class='section-title'>📄 Resume Analysis</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf", key="file_uploader")
    if uploaded_file:
        resume_text = analyze_resume(uploaded_file)
        st.session_state.resume_text = resume_text

        with st.expander("Show Analysis", expanded=True):
            if resume_text:
                st.markdown("<h4 style='color: #2E86C1;'>Extracted Text:</h4>", unsafe_allow_html=True)
                st.info("Preview (full text analyzed):")
                st.write(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
                if len(resume_text) > 500:
                    if st.checkbox("Show Full Text", key="full_resume_checkbox"):
                        st.write(resume_text)

                st.markdown("<h4 style='color: #2E86C1;'>Resume Summary:</h4>", unsafe_allow_html=True)
                summary_prompt = f"Summarize for a recruiter: {resume_text}"
                resume_summary = get_ai_response(summary_prompt)
                st.session_state.resume_summary = resume_summary
                if resume_summary:
                    st.write(resume_summary)
                else:
                    st.error("Failed to generate summary.")
            else:
                st.error("Failed to extract text.")
    else:
        if st.session_state.get('resume_text'):
            st.info("Analysis cleared. Upload to analyze.")

with col2:
    st.markdown("<h2 class='section-title'>💬 Chat with TalentScout AI</h2>", unsafe_allow_html=True)

    # Language Selection
    target_language = st.selectbox("Select Language:", options=list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("english"), format_func=lambda x: x.title())
    target_lang_code = [code for code, lang in LANGUAGES.items() if lang == target_language][0]

   # Initialize chat and greeting 
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        greeting = "Hello! I am TalentScout AI, your technical interview assistant. Tell me about your skills or ask questions!"
        translated_greeting, _ = detect_and_translate(greeting, target_lang=target_lang_code)
        st.session_state.first_message = ("TalentScout AI", translated_greeting, "Neutral 😐", target_lang_code)

    # Display the initial greeting  
    if "first_message" in st.session_state:
      sender, text, _, _ = st.session_state.first_message
      st.markdown(f"<div class='chat-container bot-text'><b>{sender}:</b> {text}</div>", unsafe_allow_html=True)


    user_input = st.text_area("Your Message:", "", height=150, key="user_input_area")

    if st.button("Send"):
        if user_input:
            translated_text, lang = detect_and_translate(user_input, target_lang=target_lang_code)
            sentiment_label, sentiment_message = analyze_sentiment(translated_text)

            exit_keywords = ["bye", "goodbye", "exit", "end", "quit", "thanks"]
            if any(keyword in translated_text.lower() for keyword in exit_keywords):
                exit_message = "Thank you! This concludes our session."
                translated_exit, _ = detect_and_translate(exit_message, target_lang=target_lang_code)
                st.session_state.chat_history.append(("TalentScout AI", translated_exit, "Neutral 😐", target_lang_code))
                st.rerun() 

            else:
                personalized_intro = ""
                if 'name' in st.session_state.candidate_form_data and st.session_state.candidate_form_data['name']:
                    personalized_intro = f"Considering {st.session_state.candidate_form_data['name']}'s info, "

                chatbot_prompt = f"""
                {personalized_intro}
                You are TalentScout AI, a technical interview assistant in {target_language}.
                Candidate: "{translated_text}"
                Analyze as a recruiter. Provide feedback on correctness, relevance, clarity, confidence.
                If a question, answer if related to interviews. If irrelevant, guide back: "I help with technical interviews.  Let's discuss skills. Ask questions, or I'll ask some."
                Avoid comments, repetition. Be concise, helpful. Respond in {target_language}.
                """
                bot_response = get_ai_response(chatbot_prompt)

                if bot_response == "Failed to get AI response.":
                    st.error("Failed to get response.")
                    if st.button("Retry"):
                        translated_text, lang = detect_and_translate(user_input, target_lang=target_lang_code)
                        sentiment_label, sentiment_message = analyze_sentiment(translated_text) #Re-analyze
                        chatbot_prompt = f"""{personalized_intro} ... (rest of prompt)"""
                        bot_response = get_ai_response(chatbot_prompt)
                        translated_bot_response, _ = detect_and_translate(bot_response, target_lang=target_lang_code)
                else:
                    translated_bot_response, _ = detect_and_translate(bot_response, target_lang=target_lang_code)

                # --- Improved Summary Prompt ---
                summary_prompt = f"""
                    In {target_language}, briefly (1-2 sentences) summarize for a recruiter:
                    Candidate: "{translated_text}"
                    Highlight:
                    - Technical understanding.
                    - Communication.
                    - Confidence.
                    - Relevance.
                    - Strengths/weaknesses.
                    Be concise, insightful for suitability. Respond in {target_language}.
                    """
                candidate_summary = get_ai_response(summary_prompt)
                translated_candidate_summary, _ = detect_and_translate(candidate_summary, target_lang=target_lang_code)

                if candidate_summary:
                    translated_bot_response += f"\n\n<div class='summary-container'><div class='summary-title'>📝 Recruiter's Summary:</div>{translated_candidate_summary}</div>"


                st.session_state.chat_history.append(("TalentScout AI", translated_bot_response, sentiment_label, target_lang_code))
                st.rerun() 

    # Display chat history 
    for i, (sender, text, sentiment, language) in enumerate(reversed(st.session_state.get('chat_history', []))):
      if i < len(st.session_state.get('chat_history', [])) - 1: 
        if sender == "TalentScout AI":
            st.markdown(f"<div class='chat-container bot-text'><b>TalentScout AI:</b> {text}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-container sentiment'><b>Sentiment:</b> {sentiment}</div>", unsafe_allow_html=True) 


# --- Footer ---
st.markdown("<div class='footer'>🎯 **Built by TalentScout AI | Smart Assessment**</div>", unsafe_allow_html=True)