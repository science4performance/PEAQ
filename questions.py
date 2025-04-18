def get_categories():
    """Return the categories used in the energy availability assessment."""
    return {
        "physical": "Physical Health",
        "physiological": "Physiological Health",
        "psychological": "Psychological Wellbeing",
        "info": "Information"  # Added new category
    }


def get_female_questions():
    """Return a list of questions for female energy availability assessment."""
    return [{
        "id": 1,
        "text": "Please enter your age",
        "type": "numeric_input",
        "min": 16,
        "max": 80,
        "category": "info",
        "unit": "years",
        "default": 25,
        "step": 1
    }, {
        "id": 2,
        "text": "What is your main exercise type?",
        "type": "multiple_choice",
        "options": ["Dance", "Running", "Cycling", "Triathlon", "Football", "Rugby", "Rowing", "Climbing", "Tennis", "Swimming",  "Other"],
        "scores": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "category": "info"
    }, {
        "id": 3,
        "text": "How many hours of exercise do you perform each week?",
        "type": "multiple_choice",
        "options": ["0-5", "6-10", "11-15", "16 or more"],
        "scores": [0, 0, 0, 0],
        "category": "info"
    }, {
        "id": 4,
        "text": "How do you feel if you have to miss exercise/training?",
        "type": "multiple_choice",
        "options": ["Relieved, I need more rest", "These things happen", "Worried or anxious"],
        "scores": [0, 0, 0],
        "category": "info"
    }, {
        "id": 5,
        "text": "Please enter your current height (in metres e.g. 1.65)",
        "type": "numeric_input",
        "min": 1.20,
        "max": 2.20,
        "category": "info",  # Changed from "physical" to "info"
        "unit": "m",
        "default": 1.65,
        "step": 0.01
    }, {
        "id": 6,
        "text": "Please enter your current weight (in kg)",
        "type": "numeric_input",
        "min": 30,
        "max": 100,
        "category": "info",  # Changed from "physical" to "info"
        "unit": "kg",
        "default": 65,
        "step": 1
    }, {
        "id": 7,
        "text": "Please enter your lowest weight for your current height (in kg)",
        "type": "numeric_input",
        "min": 30,
        "max": 100,
        "category": "info",  # Changed from "physical" to "info"
        "unit": "kg",
        "default": 60,
        "step": 1
    }, {
        "id": 8,
        "text": "How often do you weigh yourself per week?",
        "type": "multiple_choice",
        "options": ["Never", "1 to 6 times", "7 or more"],
        "scores": [0, 0, -1],
        "category": "psychological"
    }, {
        "id": 9,
        "text": "How old were you when you had your first period?",
        "type": "multiple_choice",
        "options": ["14 or younger",  "15 or older", "Never started"],
        "scores": [1, -1, -2],
        "category": "physiological"
    }, {
        "id": 10,
        "text": "To assess your current menstrual hormones, please indicate the regularity of your menstrual periods.",
        "type": "multiple_choice",
        "options": [
            "I am on hormonal contraception or HRT so I don't have natural menstrual periods",
            "I have regular menstrual periods (9 or more per calendar year)",
            "I have irregular menstrual periods (less than 9 per calendar year)",
            "I no longer have menstrual periods, as I have reached menopause"
        ],
        "scores": [0, 1, -1, 0],
        "category": "physiological"
    }, {
        "id":
        11,
        "text":
        "Have your periods ever stopped for 3 or more consecutive months (besides pregnancy or taking hormonal contraception or reaching menopause)?",
        "type":
        "multiple_choice",
        "options": [
            "No, never", "Yes, it has happened before",
            "Yes, that is the situation now"
        ],
        "scores": [1, -1, -1],
        "category":
        "physiological"
    }, {
        "id": 12,
        "text":
        "During the last year how many days off exercise/training have you had due to injury?",
        "type": "multiple_choice",
        "options": ["0 to 6 days", "7 to 13 days", "14 days or more"],
        "scores": [0, -1, -2],
        "category": "physical"
    }, {
        "id": 13,
        "text":
        "During the last year how many soft tissue injuries, e.g. muscle, ligament, tendon, joint (excluding fractures) have you had?",
        "type": "multiple_choice",
        "options": ["None", "One", "Two or more"],
        "scores": [0, -1, -2],
        "category": "physical"
    }, {
        "id": 14,
        "text":
        "Of these soft tissue injuries, how many were recurrent (i.e. in the same place, or same type of injury)?",
        "type": "multiple_choice",
        "options": ["None", "One", "Two", "More than two"],
        "scores": [0, 0, 0, -1],
        "category": "physical"
    }, {
        "id": 15,
        "text":
        "If you had bone injuries how many of these were recurrent, i.e. same place, or same type of injury?",
        "type": "multiple_choice",
        "options": ["None", "One", "Two", "More than two"],
        "scores": [0, 0, 0, -1],
        "category": "physical"
    }, {
        "id": 16,
        "text":
        "If you have had any type of fractures, where have these been located? Check all that apply.",
        "type": "checkbox",
        "options": ["Legs", "Feet", "Pelvis", "Spine", "Arms", "Other"],
        "scores": [-1, -1, -2, -2, -1, 0],
        "category": "physical"
    }, {
        "id": 17,
        "text": "Are you vegetarian?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [1, -1],
        "category": "psychological"
    }, {
        "id": 18,
        "text": "Are you vegan?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [1, -2],
        "category": "psychological"
    }, {
        "id": 19,
        "text": "Do you exclude carbohydrates from your diet?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [0, -1],
        "category": "psychological"
    }, {
        "id": 20,
        "text": "Do you smoke?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [1, -1],
        "category": "psychological"
    }, {
        "id": 21,
        "text":
        "How would you rate your levels of freshness over the past year?",
        "type": "multiple_choice",
        "options": ["Extremely fatigued", "Frequently fatigued", "Occasionally fatigued", "Reasonably fresh", "Usually fresh", "Always fresh"],
        "scores": [-2, -1, 0, 0, 1, 2],
        "category": "physiological"
    }, {
        "id": 22,
        "text": "How would you rate your sleep quality over the past year?",
        "type": "multiple_choice",
        "options": ["Terrible", "Frequently bad", "Occasionally bad", "Reasonably good", "Usually good", "Always a good night's sleep"],
        "scores": [-2, -1, 0, 0, 1, 2],
        "category": "physiological"
    }, {
        "id": 23,
        "text": "How would you rate your digestive system over the past year?",
        "type": "multiple_choice",
        "options": ["Terrible", "Frequently bad", "Occasionally bad", "Reasonably good", "Usually good", "No problems at all"],
        "scores": [-2, -1, 0, 0, 1, 2],
       "category": "physiological"
    }, {
        "id":
        24,
        "text":
        "How does controlling what you eat affect the way you feel about yourself?",
        "type":
        "multiple_choice",
        "options": [
            "Doesn't affect me", "Not a big issue", "Something I manage",
            "On my mind", "Important", "Very important"
        ],
        "scores": [2, 1, 0, 0, -1, -2],
        "category":
        "psychological"
    }, {
        "id":
        25,
        "text":
        "How does controlling what you weigh affect the way you feel about yourself?",
        "type":
        "multiple_choice",
        "options": [
            "Doesn't affect me", "Not a big issue", "Something I manage",
            "On my mind", "Important", "Very important"
        ],
        "scores": [2, 1, 0, 0, -1, -2],
        "category":
        "psychological"
    }, {
        "id": 26,
        "text": "Have you ever been diagnosed with an eating disorder?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [1, -2],
        "category": "psychological"
    }]


def get_male_questions():
    """Return a list of questions for male energy availability assessment."""
    return [{
        "id": 1,
        "text": "Please enter your age",
        "type": "numeric_input",
        "min": 16,
        "max": 80,
        "category": "info",
        "unit": "years",
        "default": 25,
        "step": 1
    }, {
        "id": 2,
        "text": "What is your main exercise type?",
        "type": "multiple_choice",
        "options": ["Dance", "Running", "Cycling", "Triathlon", "Football", "Rugby", "Rowing", "Climbing", "Tennis", "Swimming",  "Other"],
        "scores": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "category": "info"
    }, {
        "id": 3,
        "text": "How many hours of exercise do you perform each week?",
        "type": "multiple_choice",
        "options": ["0-5", "6-10", "11-15", "16 or more"],
        "scores": [0, 0, 0, 0],
        "category": "info"
    }, {
        "id": 4,
        "text": "How do you feel if you have to miss exercise/training?",
        "type": "multiple_choice",
        "options": ["Relieved, I need more rest", "These things happen", "Worried or anxious"],
        "scores": [0, 0, 0],
        "category": "info"
    }, {
        "id": 5,
        "text": "Please enter your current height (in metres e.g. 1.75)",
        "type": "numeric_input",
        "min": 1.20,
        "max": 2.20,
        "category": "info",  # Changed from "physical" to "info"
        "unit": "m",
        "default": 1.75,
        "step": 0.01
    }, {
        "id": 6,
        "text": "Please enter your current weight (in kg)",
        "type": "numeric_input",
        "min": 30,
        "max": 100,
        "category": "info",  # Changed from "physical" to "info"
        "unit": "kg",
        "default": 75,
        "step": 1
    }, {
        "id": 7,
        "text": "Please enter your lowest weight for your current height (in kg)",
        "type": "numeric_input",
        "min": 30,
        "max": 100,
        "category": "info",  # Changed from "physical" to "info"
        "unit": "kg",
        "default": 70,
        "step": 1
    }, {
        "id": 8,
        "text": "How often do you weigh yourself per week?",
        "type": "multiple_choice",
        "options": ["Never", "1 to 6 times", "7 or more"],
        "scores": [0, 0, -1],
        "category": "psychological"
    }, {
        "id": 9,
        "text":
        "As an indication of your hormone levels, how often do you have morning erections per week?",
        "type": "multiple_choice",
        "options": ["4 or more times", "2 or 3 times", "once or none"],
        "scores": [1, -1, -2],
        "category": "physiological"
    }, {
        "id": 10,
        "text":
        "During the last year how many days off exercise/training have you had due to injury?",
        "type": "multiple_choice",
        "options": ["0 to 6 days", "7 to 13 days", "14 days or more"],
        "scores": [0, -1, -2],
        "category": "physical"
    }, {
        "id": 11,
        "text":
        "During the last year how many soft tissue injuries, e.g. muscle, ligament, tendon, joint (excluding fractures) have you had?",
        "type": "multiple_choice",
        "options": ["None", "One", "Two or more"],
        "scores": [0, -1, -2],
        "category": "physical"
    }, {
        "id": 12,
        "text":
        "Of these soft tissue injuries, how many were recurrent (i.e. in the same place, or same type of injury)?",
        "type": "multiple_choice",
        "options": ["None", "One", "Two", "More than two"],
        "scores": [0, 0, 0, -1],
        "category": "physical"
    }, {
        "id": 13,
        "text":
        "If you had bone injuries how many of these were recurrent, i.e. same place, or same type of injury?",
        "type": "multiple_choice",
        "options": ["None", "One", "Two", "More than two"],
        "scores": [0, 0, 0, -1],
        "category": "physical"
    }, {
        "id": 14,
        "text":
        "If you have had any type of fractures, where have these been located? Check all that apply.",
        "type": "checkbox",
        "options": ["Legs", "Feet", "Pelvis", "Spine", "Arms", "Other"],
        "scores": [-1, -1, -2, -2, -1, 0],
        "category": "physical"
    }, {
        "id": 15,
        "text": "Are you vegetarian?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [1, -1],
        "category": "psychological"
    }, {
        "id": 16,
        "text": "Are you vegan?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [1, -2],
        "category": "psychological"
    }, {
        "id": 17,
        "text": "Do you exclude carbohydrates from your diet?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [0, -1],
        "category": "psychological"
    }, {
        "id": 18,
        "text": "Do you smoke?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [1, -1],
        "category": "psychological"
    }, {
        "id": 19,
        "text":
        "How would you rate your levels of freshness over the past year?",
        "type": "multiple_choice",
        "options": ["Extremely fatigued", "Frequently fatigued", "Occasionally fatigued", "Reasonably fresh", "Usually fresh", "Always fresh"],
        "scores": [-2, -1, 0, 0, 1, 2],
        "category": "physiological"
    }, {
        "id": 20,
        "text": "How would you rate your sleep quality over the past year?",
        "type": "multiple_choice",
        "options": ["Terrible", "Frequently bad", "Occasionally bad", "Reasonably good", "Usually good", "Always a good night's sleep"],
        "scores": [-2, -1, 0, 0, 1, 2],
        "category": "physiological"
    }, {
        "id": 21,
        "text": "How would you rate your digestive system over the past year?",
        "type": "multiple_choice",
        "options": ["Terrible", "Frequently bad", "Occasionally bad", "Reasonably good", "Usually good", "No problems at all"],
        "scores": [-2, -1, 0, 0, 1, 2],
       "category": "physiological"    }, {
        "id":
        22,
        "text":
        "How does controlling what you eat affect the way you feel about yourself?",
        "type":
        "multiple_choice",
        "options": [
            "Doesn't affect me", "Not a big issue", "Something I manage",
            "On my mind", "Important", "Very important"
        ],
        "scores": [2, 1, 0, 0, -1, -2],
        "category":
        "psychological"
    }, {
        "id":
        23,
        "text":
        "How does controlling what you weigh affect the way you feel about yourself?",
        "type":
        "multiple_choice",
        "options": [
            "Doesn't affect me", "Not a big issue", "Something I manage",
            "On my mind", "Important", "Very important"
        ],
        "scores": [2, 1, 0, 0, -1, -2],
        "category":
        "psychological"
    }, {
        "id": 24,
        "text": "Have you ever been diagnosed with an eating disorder?",
        "type": "multiple_choice",
        "options": ["No", "Yes"],
        "scores": [1, -2],
        "category": "psychological"
    }]
