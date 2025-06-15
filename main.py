import streamlit as st                            # For Web Interface (Front-End)
from pdfminer.high_level import extract_text      # To Extract Text from Resume PDF
from sentence_transformers import SentenceTransformer      # To generate Embeddings of text
from sklearn.metrics.pairwise import cosine_similarity     # To get Similarity Score of Resume and Job Description
from groq import Groq                             # API to use LLM's
import re                                         # To perform Regular Expression Functions
from dotenv import load_dotenv                    # Loading API Key from .env file
import os


# Load environment variables from .env
load_dotenv()

# Fetch the key from the environment
api_key = os.getenv("GROQ_API_KEY")


#  Session States to store values 
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if "resume" not in st.session_state:
    st.session_state.resume=""

if "job_desc" not in st.session_state:
    st.session_state.job_desc=""



st.set_page_config(page_title="SmartHire AI", layout="wide")
st.markdown("""
    <style>
        .stApp {
            background-color: #e8f0fe;
        }
        .main-title {
            font-size: 40px;
            font-weight: 700;
            color: #003366;
        }
        .section-title {
            font-size: 22px;
            font-weight: 600;
            margin-top: 20px;
            color: #222222;
        }
        .score-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            color: #111111;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }
        .heading-text {
            color: #1a1a1a;
            font-size: 18px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stFileUploader"] ul li {
        color: #1a1a1a !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)


# ---------- Page Title ----------
st.markdown("<div class='main-title'>SmartHire AI 🔍</div>", unsafe_allow_html=True)
st.markdown(
    '<h4 style="color:#1a1a1a;">Get AI-powered insights on your resume alignment with the job role</h4>',
    unsafe_allow_html=True
)

# <------- Defining Functions ------->

# Function to extract text from PDF
def extract_pdf_text(uploaded_file):
    try:
        extracted_text = extract_text(uploaded_file)
        return extracted_text
    except Exception as e:
        st.markdown(
        f'<p style="color: #FF4500; font-weight: bold;">Error extracting text from PDF: {str(e)}</p>',
        unsafe_allow_html=True
        )
        return "Could not extract text from the PDF file."


# Function to calculate similarity 
def calculate_similarity_bert(text1, text2):
    ats_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')      # Use BERT or SBERT or any model you want
    # Encode the texts directly to embeddings
    embeddings1 = ats_model.encode([text1])
    embeddings2 = ats_model.encode([text2])
    
    # Calculate cosine similarity without adding an extra list layer
    similarity = cosine_similarity(embeddings1, embeddings2)[0][0]
    return similarity


def get_report(resume,job_desc):
    client = Groq(api_key=api_key)

    # Change the prompt to get the results in your style
    prompt=f"""
    # Context:
    - You are an AI Resume Analyzer, you will be given Candidate's resume and Job Description of the role he is applying for.

    # Instruction:
    - Analyze candidate's resume based on the possible points that can be extracted from job description,and give your evaluation on each point with the criteria below:  
    - Consider all points like required skills, experience,etc that are needed for the job role.
    - Calculate the score to be given (out of 5) for every point based on evaluation at the beginning of each point with a detailed explanation.  
    - If the resume aligns with the job description point, mark it with ✅ and provide a detailed explanation.  
    - If the resume doesn't align with the job description point, mark it with ❌ and provide a reason for it.  
    - If a clear conclusion cannot be made, use a ⚠️ sign with a reason.  
    - The Final Heading should be "Suggestions to improve your resume:" and give where and what the candidate can improve to be selected for that job role.

    # Inputs:
    Candidate Resume: {resume}
    ---
    Job Description: {job_desc}

    # Output:
    - Each any every point should be given a score (example: 3/5 ). 
    - Mention the scores and  relevant emoji at the beginning of each point and then explain the reason.
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def extract_scores(text):
    # Regular expression pattern to find scores in the format x/5, where x can be an integer or a float
    pattern = r'(\d+(?:\.\d+)?)/5'
    # Find all matches in the text
    matches = re.findall(pattern, text)
    # Convert matches to floats
    scores = [float(match) for match in matches]
    return scores




# <--------- Starting the Work Flow ---------> 

# Displays Form only if the form is not submitted
if not st.session_state.form_submitted:
    with st.form("my_form"):

        # Taking input a Resume (PDF) file 
         st.markdown('<h6 style="color:#1a1a1a;">📄 Upload Your Resume (PDF only)</h6>', unsafe_allow_html=True)
         resume_file = st.file_uploader("", type="pdf")

         st.markdown('<h6 style="color:#1a1a1a;">📝 Paste the Job Description here:</h6>', unsafe_allow_html=True)
         st.session_state.job_desc = st.text_area("", placeholder="Job Description...")

         submitted = st.form_submit_button("🚀Analyze Resume")

         if submitted:
            if st.session_state.job_desc and resume_file:
                st.markdown('<h6 style="color:#1a1a1a;">🔍 Extracting resume content and job details...</h6>', unsafe_allow_html=True)
                st.session_state.resume = extract_pdf_text(resume_file)
                st.session_state.form_submitted = True

                st.rerun()                 # Refresh the page to close the form and give results

            # Donot allow if not uploaded
            else:
                st.markdown('<h5 style="color:#1a1a1a;">⚠️ Please upload a resume and paste the job description</h5>', unsafe_allow_html=True)


if st.session_state.form_submitted:
    score_place = st.markdown(
    """
    <div style="background-color:#E3F2FD; padding:10px; border-radius:10px;">
        <span style="color:#1565C0; font-weight:bold;"> Generating Scores...</span>
    </div>
    """,
    unsafe_allow_html=True
)


    # Call the function to get ATS Score
    ats_score = calculate_similarity_bert(st.session_state.resume,st.session_state.job_desc)

    col1,col2 = st.columns(2,border=True)
    with col1:
         st.markdown(
            "<div class='score-box'><b>🔗 Resume Match Score:</b><br>"
            f"<span style='font-size:24px; color:#0047ab;'>{ats_score:.2f}</span><br>"
            "<small>Based on similarity between resume & job description.</small></div>",
            unsafe_allow_html=True,
        )

         

    # Call the function to get the Analysis Report from LLM (Groq)
    report = get_report(st.session_state.resume,st.session_state.job_desc)

    # Calculate the Average Score from the LLM Report
    report_scores = extract_scores(report)                 # Example : [3/5, 4/5, 5/5,...]
    avg_score = sum(report_scores) / (5*len(report_scores))  # Example: 2.4


    with col2:
        st.markdown(
            "<div class='score-box'><b>📊 Overall AI Rating:</b><br>"
            f"<span style='font-size:24px; color:#228B22;'>{avg_score:.2f}</span><br>"
            "<small>Calculated from detailed analysis.</small></div>",
            unsafe_allow_html=True,
        )

        
    score_place.markdown(
    """
    <div style="background-color:#DFF6DD; padding:10px; border-radius:10px;">
        <span style="color:#2E7D32; font-weight:bold;">✅ Report generated!</span>
    </div>
    """,
    unsafe_allow_html=True
)



    st.markdown('<h4 style="color:#1a1a1a;">📋 Detailed Resume Evaluation Report</h4>', unsafe_allow_html=True)


    # Displaying Report 
    st.markdown(f"""
            <div style='text-align: left; background-color: #000000; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                {report}
            </div>
            """, unsafe_allow_html=True)
    
    # Download Button
    st.download_button(
        label="💾 Download Analysis Report",
        data=report,
        file_name="report.txt",
        icon=":material/download:",
        )
    
    # Output GIF Demo (Optional)
    st.markdown("""
        <h5 style="color:#1a1a1a;">🎥 Output Demo</h5>
        <img src="assets\video.gif" style="width:100%; border-radius:10px;" alt="SmartHire Output"/>
    """, unsafe_allow_html=True)

    

# <-------------- End of the Work Flow --------------->
