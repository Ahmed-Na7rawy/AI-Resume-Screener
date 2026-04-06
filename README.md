# AI Resume Screener 💼

A proof-of-concept AI-powered resume screening tool built for internal recruitment teams. 

This tool allows recruiters to:
1. Upload a Job Description.
2. Upload multiple candidate resumes (in PDF format).
3. Automatically score each candidate out of 100 based on the job description.
4. Generate a short, plain-English summary explaining the match.
5. View a ranked list of candidates from highest match score to lowest.

## Technology Stack
- **Python 3**
- **Streamlit**: For the web interface.
- **PyPDF**: For extracting text from PDF resumes.
- **Google Gemini API** (`gemini-1.5-flash`): For fast, cost-effective, and intelligent resume analysis.
- **Pandas**: For data structuring and sorting.

## Setup Instructions

### 1. Install Dependencies
Make sure you have Python installed. Then, run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Get a Google Gemini API Key
To use the AI evaluation, you need an API key from Google AI Studio. 
- Go to [Google AI Studio](https://aistudio.google.com/) and create a free API key.

### 3. Run the Application
Start the Streamlit development server:
```bash
streamlit run app.py
```
This will open the application in your default web browser (usually at `http://localhost:8501`).

## Testing the Application (Sample Data)

If you'd like to test the tool but do not have resumes on hand, a dummy data generation script has been provided.

1. Ensure the `fpdf` library is installed (`pip install fpdf`).
2. Run the script:
```bash
python generate_samples.py
```
3. A new folder named `sample_data` will be created containing:
   - `sample_job_description.txt` (A job description for a Senior Python Engineer)
   - `Resume_Alice_Smith.pdf` (A strong match)
   - `Resume_Bob_Jones.pdf` (A poor match)
   - `Resume_Charlie_Brown.pdf` (A partial/moderate match)

You can copy the job description into the app and upload these 3 PDFs to see the ranking system in action!
