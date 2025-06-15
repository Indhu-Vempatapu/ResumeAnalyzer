## 💼 SmartHire AI – Resume Analyzer Using BERT & LLM

# 🧠 Introduction

SmartHire AI is an intelligent resume analysis tool designed to help job applicants understand how well their resumes align with a given job description. By leveraging cutting-edge BERT-based embeddings and LLM-powered evaluation (via Groq's LLaMA-3 model), the system delivers deep insights, match scores, and actionable suggestions to improve the chances of landing a dream job.

# What It Does

- Accepts a PDF resume and a job description input.

- Uses Sentence-BERT to compute a similarity score between the resume and job description.

- Interacts with Groq’s LLaMA-3.3-70b model to perform a detailed resume evaluation.

- Displays both a Resume Match Score and an AI Rating based on qualitative analysis.

- Generates a detailed feedback report on strengths, weaknesses, and suggestions.

- Allows users to download the analysis report for offline reference.

# ⚙️ How It Works

- Frontend Interface: Built with Streamlit for a seamless and responsive web experience.

- Resume Extraction: Uses pdfminer to extract text content from uploaded PDF resumes.

- Semantic Matching:

  - Utilizes SentenceTransformer with all-mpnet-base-v2 to encode resume and job description into embeddings.

  - Computes cosine similarity for an initial ATS-style match score.

- AI-Powered Evaluation:

   - Sends the resume and job description to the Groq API with a tailored prompt.

   - The LLM evaluates and scores each section of the resume.

- Scoring Logic:

    - Extracts individual scores from the AI's feedback.

     - Calculates an average rating based on the total score out of 5 for each point.
 
# 🧰 Technologies Used

Streamlit - Web interface

pdfminer - Extract text from resume PDF

SentenceTransformer - Generate BERT embeddings

scikit-learn - Compute cosine similarity

Groq API (LLaMA-3) - Detailed AI evaluation of resume

dotenv	- Manage API key securely

re (Regex) - Extract scores from text

#  Installation Steps

Follow these steps to set up and run the **AI Resume Analyzer** locally:


Make sure you have Python and Git installed.

### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/Altoks-AI/AI-Resume-Analyzer.git
```
```
cd FolderName
```

### 2️⃣ Set Up a Virtual Environment
```
python -m venv myenv
```
```
./myenv/Scripts/activate
```

### 3️⃣ Install Dependencies
Make sure you have pip updated, then install all required packages:
```
pip install -r requirements.txt
```

### 4️⃣ Set Up Your .env File
Create a .env file in the root directory and add your Groq API key from [Groq](https://groq.com/) 

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5️⃣ Run the Streamlit App
Launch the app locally using Streamlit:
```
streamlit run main.py
```
### 6️⃣ Open in Browser
Once the app starts, it will automatically open in your default web browser at:
```
http://localhost:8501
```
---
✅ Now you’re all set!
Upload a resume, paste a job description, and let the AI analyze your resume for job-fit and provide suggestions. 

# Output 
![Demo](assets\video.gif)
