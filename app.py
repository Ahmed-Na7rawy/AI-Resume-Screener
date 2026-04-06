import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
import json
import pandas as pd
import time

# -----------------------------------------------------
# SETUP & CONFIGURATION
# -----------------------------------------------------
# Configure Streamlit page details
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner, premium look
st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
        margin-bottom: 1rem;
    }
    .metric-score {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2e6c80;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------
def extract_text_from_pdf(file_obj):
    """
    Extracts text from an uploaded PDF file object.
    Uses PyPDF to iterate through pages and concatenate text.
    """
    try:
        reader = PdfReader(file_obj)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        st.error(f"Failed to read {file_obj.name}: {e}")
        return ""

@st.cache_data(show_spinner=False)
def get_available_models(api_key):
    """Fetches text generation models available to the provided API key."""
    genai.configure(api_key=api_key)
    try:
        models = genai.list_models()
        valid_models = [m.name.replace('models/', '') for m in models if 'generateContent' in m.supported_generation_methods]
        # Filter mostly for flash/pro models to keep the list clean
        return [m for m in valid_models if 'gemini' in m.lower()]
    except Exception:
        # Fallback list if fetching fails
        return ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro"]

def analyze_resume(resume_text, job_description, api_key, model_name="gemini-1.5-flash"):
    """
    Sends the resume text and job description to the Gemini API
    to evaluate the candidate. Expects a JSON response.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    You are an expert technical recruiter and HR professional analyzing a candidate's resume against a job description.
    
    Job Description:
    ----------
    {job_description}
    ----------
    
    Resume Text:
    ----------
    {resume_text}
    ----------
    
    Task:
    Analyze the match between the resume and the job description. Be objective and critical.
    
    Output Requirements:
    You MUST output ONLY a valid JSON object. Do not include markdown code block syntax (like ```json).
    The JSON object must contain exactly these keys:
    {{
        "CandidateName": "The name of the candidate extracted from the resume (use 'Unknown' if not clearly stated)",
        "Score": An integer from 0 to 100 representing the match quality (0 = no match, 100 = perfect match),
        "Summary": "A concise, plain English summary (2-3 sentences) explaining the score, highlighting key strengths and major gaps."
    }}
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        data = json.loads(response.text)
        
        # Validate data
        if not isinstance(data.get("Score"), int):
            data["Score"] = int(data.get("Score", 0))
            
        return data
    except Exception as e:
        return {
            "CandidateName": "Error Processing",
            "Score": 0,
            "Summary": f"API Evaluation failed. Detail: {str(e)}"
        }

# -----------------------------------------------------
# UI LAYOUT & LOGIC
# -----------------------------------------------------
def main():
    st.title("💼 AI Resume Screener")
    st.markdown("Upload a job description and a batch of resumes to get instant, AI-driven candidate match rankings.")
    
    # Sidebar: Config
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("Google Gemini API Key", type="password", help="Get your API key from Google AI Studio.")
        
        selected_model = "gemini-1.5-flash"
        if api_key:
            available_models = get_available_models(api_key)
            if available_models:
                # Try to default to a 1.5 flash variant
                default_idx = 0
                for i, m in enumerate(available_models):
                    if "1.5-flash" in m and "8b" not in m:
                        default_idx = i
                        break
                selected_model = st.selectbox("Select API Model", available_models, index=default_idx)
                
        st.markdown("---")
        st.markdown(
            "**How it works**\n"
            "1. Enter your Gemini API key.\n"
            "2. Select a valid model.\n"
            "3. Paste the Job Description.\n"
            "4. Upload PDF resumes.\n"
            "5. Click **Run Screening**."
        )

    # Main content layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📝 Job Description")
        job_desc = st.text_area(
            "Paste the complete job description here...",
            height=300,
            placeholder="e.g. We are looking for a Senior Software Engineer with 5+ years of Python experience..."
        )
        
    with col2:
        st.subheader("📄 Candidate Resumes")
        uploaded_files = st.file_uploader(
            "Upload one or more resume PDFs", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.info(f"{len(uploaded_files)} file(s) uploaded ready for processing.")

    st.markdown("---")
    
    # Execution triggering
    if st.button("🚀 Run Screening Analysis", type="primary"):
        # Validation checks
        if not api_key:
            st.error("⚠️ Please enter your Google Gemini API Key in the sidebar.")
            st.stop()
        if not job_desc.strip():
            st.error("⚠️ Please provide a job description.")
            st.stop()
        if not uploaded_files:
            st.error("⚠️ Please upload at least one PDF resume.")
            st.stop()
            
        st.info("Starting analysis... this may take a moment depending on the number of resumes.")
        
        results = []
        progress_bar = st.progress(0)
        
        # Process each file
        for idx, file in enumerate(uploaded_files):
            with st.spinner(f"Processing candidate {idx+1} of {len(uploaded_files)}: {file.name}..."):
                # 1. Extract Text
                resume_text = extract_text_from_pdf(file)
                
                # 2. Analyze via AI
                if resume_text.strip():
                    ai_result = analyze_resume(resume_text, job_desc, api_key, selected_model)
                else:
                    ai_result = {
                        "CandidateName": "Unknown",
                        "Score": 0,
                        "Summary": "Could not extract readability text from this PDF file."
                    }
                    
                # 3. Store result with filename context
                results.append({
                    "Filename": file.name,
                    "Candidate Name": ai_result.get("CandidateName", "Unknown"),
                    "Match Score": ai_result.get("Score", 0),
                    "Summary": ai_result.get("Summary", "No summary provided.")
                })
                
                # Manage rate limiting slightly
                time.sleep(1)
                
            progress_bar.progress((idx + 1) / len(uploaded_files))
            
        st.success("✅ Analysis Complete!")
        
        # Process results
        if results:
            df = pd.DataFrame(results)
            # Sort by highest score first
            df = df.sort_values(by="Match Score", ascending=False).reset_index(drop=True)
            
            st.subheader("🏆 Ranked Candidates")
            
            # Overview visual table
            st.dataframe(
                df[["Match Score", "Candidate Name", "Filename", "Summary"]],
                use_container_width=True,
                hide_index=True
            )
            
            # Detailed Expanding Cards
            st.markdown("### Detailed Match Summaries")
            for index, row in df.iterrows():
                with st.expander(f"**{row['Match Score']}/100** - {row['Candidate Name']} ({row['Filename']})", expanded=(index==0)):
                    st.markdown(f"**AI Evaluation Summary:**")
                    st.write(row['Summary'])

if __name__ == "__main__":
    main()
