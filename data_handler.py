import json
import os
import uuid
import datetime
from pathlib import Path

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

def save_assessment(user_id, answers, scores, overall_score, timestamp):
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
        "answers": answers,
        "scores": scores,
        "overall_score": overall_score
    }
    
    # Save assessment to file
    file_path = user_dir / f"{assessment_id}.json"
    with open(file_path, 'w') as f:
        json.dump(assessment_data, f, cls=DateTimeEncoder, indent=4)
    
    # Update assessment index
    index_path = user_dir / "index.json"
    
    if index_path.exists():
        with open(index_path, 'r') as f:
            index = json.load(f)
    else:
        index = []
    
    # Add this assessment to the index
    index.append({
        "id": assessment_id,
        "timestamp": timestamp.isoformat(),
        "overall_score": overall_score
    })
    
    # Sort index by timestamp (newest first)
    index.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Save updated index
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=4)
    
    return assessment_id

def load_assessments(user_id):
    """
    Load all assessments for a given user.
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        List of assessment data dictionaries, sorted by timestamp (newest first)
    """
    user_dir = DATA_DIR / user_id
    
    if not user_dir.exists():
        return []
    
    # Load assessment index
    index_path = user_dir / "index.json"
    if not index_path.exists():
        return []
    
    with open(index_path, 'r') as f:
        index = json.load(f)
    
    # Load full assessment data for each entry in the index
    assessments = []
    for entry in index:
        assessment_id = entry["id"]
        file_path = user_dir / f"{assessment_id}.json"
        
        if file_path.exists():
            with open(file_path, 'r') as f:
                assessment = json.load(f, object_hook=datetime_decoder)
                assessments.append(assessment)
    
    # Sort by timestamp (newest first)
    assessments.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return assessments

def get_assessment(user_id, assessment_id):
    """
    Retrieve a specific assessment by ID.
    
    Args:
        user_id: Unique identifier for the user
        assessment_id: Unique identifier for the assessment
        
    Returns:
        Assessment data dictionary or None if not found
    """
    file_path = DATA_DIR / user_id / f"{assessment_id}.json"
    
    if not file_path.exists():
        return None
    
    with open(file_path, 'r') as f:
        assessment = json.load(f, object_hook=datetime_decoder)
    
    return assessment
