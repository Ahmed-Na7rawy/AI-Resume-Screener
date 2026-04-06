import os
from fpdf import FPDF

# Create directory if it doesn't exist
os.makedirs("sample_data", exist_ok=True)

# 1. Job Description
job_description = """
Job Title: Senior Python Engineer
Location: Remote
Experience: 5+ Years

About the Role:
We are looking for a Senior Python Engineer to help build our next-generation AI products. The ideal candidate will have extensive experience in Python, API integration, and full-stack development with a modern web framework.

Key Responsibilities:
- Design, build, and maintain efficient, reusable, and reliable Python code.
- Integrate user-facing elements into applications using Streamlit or React.
- Work closely with data scientists to deploy machine learning models (specifically LLMs and GenAI) into production.
- Write robust unit and integration tests.

Required Skills:
- 5+ years of software engineering experience focusing on Python.
- Strong understanding of REST APIs and JSON data structures.
- Experience with at least one modern web framework (Streamlit, Flask, FastAPI).
- Familiarity with AI/ML tools, specifically Google Gemini or OpenAI APIs.
- Excellent communication and collaboration skills.
"""

with open("sample_data/sample_job_description.txt", "w", encoding="utf-8") as f:
    f.write(job_description.strip())

# 2. Resumes
resumes = {
    "Resume_Alice_Smith.pdf": """Alice Smith
Senior Python Developer
Email: alice.smith@example.com | Phone: (555) 123-4567

Summary:
Highly experienced Python engineer with 6 years of industry experience. Passionate about building robust web applications and integrating with AI models.

Experience:
Senior Software Engineer at TechNova (2020 - Present)
- Developed scalable microservices using FastAPI and Python.
- Integrated OpenAI and Google Gemini APIs into core products to provide conversational AI features.
- Built internal dashboards using Streamlit, saving 20 hours a week for the operations team.

Software Developer at CodeWorks (2018 - 2020)
- Maintained a legacy Django application, adding new REST API endpoints.
- Improved database query performance by 40%.

Education:
B.S. Computer Science, State University (2014 - 2018)

Skills:
Python, FastAPI, Streamlit, Prompt Engineering, SQL, Git, Docker, REST APIs
""",
    
    "Resume_Bob_Jones.pdf": """Bob Jones
Frontend Web Developer
Email: bob.jones@example.com

Summary:
Creative frontend developer specializing in building beautiful user interfaces. 4 years of experience mostly working with JavaScript and web design.

Experience:
Frontend Developer at DesignStudio (2020 - Present)
- Developed responsive websites using HTML, CSS, and React.
- Collaborated with creative directors to ensure pixel-perfect implementations.
- Optimized images and web assets for faster loading times.

Junior Web Developer at Startup Inc. (2018 - 2020)
- Designed email templates and landing pages.
- Maintained CMS content using WordPress.

Education:
BA Graphic Design, Creative Arts College

Skills:
JavaScript, React, HTML, CSS, Figma, Adobe Photoshop
""",

    "Resume_Charlie_Brown.pdf": """Charlie Brown
Data Scientist
Email: charlie.data@example.com

Summary:
Data scientist with a strong background in statistical modeling and machine learning. Focusing on computer vision and predictive analytics.

Experience:
Data Scientist at DataCorp (2021 - Present)
- Developed a computer vision model to detect defects in manufacturing using PyTorch.
- Analyzed large datasets using Pandas and NumPy to identify trends in customer retention.
- Created visualizations using Matplotlib and Tableau.

Data Analyst at FinTech Solutions (2019 - 2021)
- Built automated reporting pipelines.
- Wrote complex SQL queries to extract data for the finance team.

Education:
M.S. Data Science, Tech University
B.S. Mathematics, Tech University

Skills:
Python, Pandas, PyTorch, Machine Learning, Computer Vision, SQL, Tableau
"""
}

for filename, content in resumes.items():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Handle line breaks natively
    for line in content.split('\n'):
        # Ensure ascii compatibility for fpdf
        clean_line = line.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(200, 7, txt=clean_line, ln=True, align="L")
        
    pdf.output(f"sample_data/{filename}")

print("Sample data generated successfully in the 'sample_data' folder.")
