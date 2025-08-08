import json
import os
import uuid
import datetime
from pathlib import Path
from fpdf import FPDF
import streamlit as st

# This relies on AWS credentials being stored in .streamlit/secrets.toml or Streamlit Community Cloud app secrets

from st_files_connection import FilesConnection

# Create connection object 
conn = st.connection('s3', type=FilesConnection)
AWS_DIR = Path("peaq-streamlit/data")




# Create data directory if it doesn't exist
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

def datetime_decoder(json_dict):
    """Custom JSON decoder for datetime objects."""
    for key, value in json_dict.items():
        if key == "timestamp" and isinstance(value, str):
            try:
                json_dict[key] = datetime.datetime.fromisoformat(value)
            except ValueError:
                pass
    return json_dict

def save_assessment(user_id, sex, answers, scores, overall_score, interpretation, timestamp):
    """
    Save the assessment results to a JSON file.
    
    Args:
        user_id: Unique identifier for the user
        answers: Dictionary of answers given by the user
        scores: Dictionary of category scores
        overall_score: Overall health score
        timestamp: Datetime when the assessment was completed
    """
    # Generate unique ID for this assessment
    assessment_id = str(uuid.uuid4())
    
    # Create user directory if it doesn't exist
    user_dir = DATA_DIR / user_id
    user_dir.mkdir(exist_ok=True)
    
    # Prepare assessment data
    assessment_data = {
        "id": assessment_id,
        "user_id": user_id,
        "timestamp": timestamp,
        "sex": sex,
        "answers": answers,
        "scores": scores,
        "overall_score": overall_score,
        "interpretation": interpretation
    }
    
    # Save assessment to file
    file_path = AWS_DIR / f"{assessment_id}.json"
    with conn.open(file_path, 'w') as f:
        json.dump(assessment_data, f, cls=DateTimeEncoder, indent=4)
    
    
    return assessment_id

# def load_assessments(user_id):
#     """
#     Load all assessments for a given user.
    
#     Args:
#         user_id: Unique identifier for the user
        
#     Returns:
#         List of assessment data dictionaries, sorted by timestamp (newest first)
#     """
#     user_dir = DATA_DIR / user_id
    
#     if not user_dir.exists():
#         return []
    
#     # Load assessment index
#     index_path = user_dir / "index.json"
#     if not index_path.exists():
#         return []
    
#     with open(index_path, 'r') as f:
#         index = json.load(f)
    
#     # Load full assessment data for each entry in the index
#     assessments = []
#     for entry in index:
#         assessment_id = entry["id"]
#         file_path = user_dir / f"{assessment_id}.json"
        
#         if file_path.exists():
#             with open(file_path, 'r') as f:
#                 assessment = json.load(f, object_hook=datetime_decoder)
#                 assessments.append(assessment)
    
#     # Sort by timestamp (newest first)
#     assessments.sort(key=lambda x: x["timestamp"], reverse=True)
    
#     return assessments

# def get_assessment(user_id, assessment_id):
#     """
#     Retrieve a specific assessment by ID.
    
#     Args:
#         user_id: Unique identifier for the user
#         assessment_id: Unique identifier for the assessment
        
#     Returns:
#         Assessment data dictionary or None if not found
#     """
#     file_path = DATA_DIR / user_id / f"{assessment_id}.json"
    
#     if not file_path.exists():
#         return None
    
#     with open(file_path, 'r') as f:
#         assessment = json.load(f, object_hook=datetime_decoder)
    
#     return assessment

def create_pdf(user_id, assessment_id, sex, overall_score, interpretation, comment, date):
    # # Create a PDF object
    user_dir = DATA_DIR / user_id
    user_dir.mkdir(exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    # Heading
    pdf.set_font("Arial", style="B", size=20, )
    pdf.set_xy(10,20)
    pdf.cell(180,10,txt=f"{sex if sex != 'None' else ''} Personal Energy Availability Questionnaire (PEAQ)\n\n")

    # Subheading
    pdf.set_font("Arial", style="B", size=16)
    pdf.write( 10, txt=f"Your Personal Energy Availability Results ({date})\n")
    pdf.set_font("Arial",  size=12)
    pdf.write(8, txt=comment)
    # Label charts
    pdf.set_font("Arial", style="B", size=16)    
    pdf.cell(20,10)
    pdf.cell(80, 10, txt=f"REDs Risk Score: {overall_score:+.0f}")
    pdf.cell(10,)
    pdf.cell(80,10, txt="Category Breakdown")
    pdf.image(f'{user_dir/"overall.jpeg"}', x=0, y=90, w=100)
    pdf.image(f'{user_dir/"categories.jpeg"}', x=100, y=90, w=100)
    # Add the interpretation text
    pdf.set_font("Arial",  size=12)
    pdf.set_xy(10, 140)
    pdf.write(8, txt=f"Interpretation: {interpretation}"+"\n\n")
    #pdf.set_xy(10, 140)
    
    pdf.write(8, "If you would like more information about energy availability and relative energy deficiency you may wish to have a look at ")
    pdf.set_text_color(0,0,255)  
    pdf.write(8,"nickykeayfitness.com ", link="https://nickykeayfitness.com")
    pdf.set_text_color(0,0,0)
    pdf.write(8, "and read Dr Nicky Keay's book ")
    pdf.set_text_color(0,0,255)  
    pdf.write(8,'Hormones, Health and Human Potential', link="https://hhhp.neocities.org/")
    pdf.set_text_color(0,0,0)
    pdf.write(8, "\nFor individual, personal advice, Dr Nicky Keay offers ")
    pdf.set_text_color(0,0,255)  
    pdf.write(8, "health advisory appointments", link="https://nickykeayfitness.com/appointments/")
    #pdf.set_xy(10, 140)
   
    pdf.image("pics/PEAQw.png", x=0, y=210, w=210)
    pdf.set_xy(10, 260)
    pdf.set_text_color(0,0,0)
    pdf.write(8,f"PEAQ id: {assessment_id}")
    #pdf.cell(0, 10, f"Assessment Date: {date}", ln=True)
    pdf.output(user_dir/"PEAQ_results.pdf")  # Save the PDF to a
