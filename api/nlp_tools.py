import re


# Load SpaCy's English model
import spacy
from spacy.cli import download

# Download the SpaCy model if it's not installed
model_name = "en_core_web_sm"
try:
    nlp = spacy.load(model_name)
except OSError:
    # Install the model if it's not found
    download(model_name)
    nlp = spacy.load(model_name)  # Now load it after installation


def extract_skills(text):
    skills_section = re.search(r"Skills[:\s]*(.*?)(?=\n[A-Z])", text, re.DOTALL)
    if skills_section:
        skills = skills_section.group(1).replace('\n', ', ').split(',')
        return [skill.strip() for skill in skills if skill.strip()]
    return []

def extract_education(text):
    education_section = re.search(r"Education[:\s]*(.*?)(?=\nSkills)", text, re.DOTALL)
    if education_section:
        return education_section.group(1).strip()
    return ""

def extract_experience(text):
    experience_section = re.search(r"Experience[:\s]*(.*?)(?=\n[A-Z])", text, re.DOTALL)
    if experience_section:
        return experience_section.group(1).strip()
    return ""


# Main function to process the resume text
def process_resume(resume_text):
    # Extract information from resume
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    experience = extract_experience(resume_text)

    # Output the extracted information (you may want to store this instead of printing)
    print("Extracted Skills:")
    print(skills)
    print("\nExtracted Education:")
    print(education)
    print("\nExtracted Experience:")
    print(experience)
    
    # Return a structured dict instead of printing for further use
    return {
        "skills": skills,
        "education": education,
        "experience": experience
    }
