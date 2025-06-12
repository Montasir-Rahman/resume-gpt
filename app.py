import os
from dotenv import load_dotenv
from docx import Document
import gradio as gr
import google.generativeai as genai


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file!")


genai.configure(api_key=api_key)


model_name_to_use = "models/gemini-2.0-flash-thinking-exp-1219" 


try:
    model = genai.GenerativeModel(model_name=model_name_to_use)
except Exception as e:
    print(f"Error initializing model '{model_name_to_use}': {e}")
    print("Please run `list_available_models()` to verify the correct model name.")
    exit() 


def read_docx(file_obj):
    try:
        doc = Document(file_obj)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        return f"Error reading .docx file: {str(e)}"


def analyze_resume(resume_file, job_desc):
    resume_text = read_docx(resume_file)
    prompt = f"""
You are an experienced AI resume reviewer and recruiter.

Your task is to:
1. Analyze the overall resume,
2. Find the key positive and negative parts of the resume
3. Give a overall relvancy score out of 10
4. Give any short feedback if there is any

Resume:
{resume_text}

Job Description:
{job_desc}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini API: {str(e)}"

# Gradio UI
iface = gr.Interface(
    fn=analyze_resume,
    inputs=[
        gr.File(label="Upload Resume (.docx)"),
        gr.Textbox(lines=10, label="Paste Job Description")
    ],
    outputs=gr.Textbox(label="Gemini AI Feedback"),
    title="Resume Reviewer (Gemini Pro)",
    description="Upload your resume (.docx) and paste a job description. Get AI-powered feedback using Gemini Pro."
)

# Launch the app
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
