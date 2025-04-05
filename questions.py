def get_categories():
    """Return the categories used in the health assessment."""
    return {
        "physical": "Physical Health",
        "physiological": "Physiological Health",
        "psychological": "Psychological Wellbeing"
    }

def get_questions():
    """Return a list of questions for the health assessment."""
    return [
        {
            "id": 1,
            "text": "Please enter your current height (in metres e.g. 1.65)",
            "type": "numeric_input",
            "min": 1.2,
            "max": 2.2,
            "category": "physiological",
            "unit": "m"
        },
        {
            "id": 2,
            "text": "Please enter your current weight (in kg)",
            "type": "numeric_input",
            "min": 30,
            "max": 100,
            "category": "physiological",
            "unit": "kg"
        },
        {
            "id": 3,
            "text": "Please enter your lowest weight for your current height (in kg)",
            "type": "numeric_input",
            "min": 30,
            "max": 100,
            "category": "physiological",
            "unit": "kg"
        },
        {
            "id": 4,
            "text": "How would you rate your overall physical health?",
            "type": "scale",
            "min": 1,
            "max": 10,
            "category": "physical"
        },
        {
            "id": 5,
            "text": "How often do you engage in moderate to vigorous physical activity?",
            "type": "multiple_choice",
            "options": [
                "Never",
                "Rarely (once a month or less)",
                "Occasionally (a few times a month)",
                "Regularly (1-2 times a week)",
                "Frequently (3-5 times a week)",
                "Daily"
            ],
            "scores": [0, 2, 4, 6, 8, 10],
            "category": "physical"
        },
        {
            "id": 6,
            "text": "How would you rate your stress levels on average?",
            "type": "scale",
            "min": 1,  # 1 = Very high stress
            "max": 10, # 10 = No stress
            "category": "psychological"
        },
        {
            "id": 7,
            "text": "How often do you feel anxious or overwhelmed?",
            "type": "multiple_choice",
            "options": [
                "Constantly (every day)",
                "Frequently (several times a week)",
                "Occasionally (once a week)",
                "Rarely (once a month)",
                "Almost never"
            ],
            "scores": [0, 2.5, 5, 7.5, 10],
            "category": "psychological"
        },
        {
            "id": 8,
            "text": "How satisfied are you with your social connections and relationships?",
            "type": "scale",
            "min": 1,
            "max": 10,
            "category": "psychological"
        },
        {
            "id": 9,
            "text": "How often do you interact meaningfully with friends or family?",
            "type": "multiple_choice",
            "options": [
                "Rarely or never",
                "Monthly",
                "Weekly",
                "A few times a week",
                "Daily"
            ],
            "scores": [0, 2.5, 5, 7.5, 10],
            "category": "psychological"
        },
        {
            "id": 10,
            "text": "How would you rate the overall quality of your diet?",
            "type": "scale",
            "min": 1,
            "max": 10,
            "category": "physiological"
        },
        {
            "id": 11,
            "text": "How often do you consume fruits and vegetables?",
            "type": "multiple_choice",
            "options": [
                "Rarely or never",
                "Occasionally (a few times a week)",
                "Once daily",
                "2-4 servings daily",
                "5 or more servings daily"
            ],
            "scores": [0, 2.5, 5, 7.5, 10],
            "category": "physiological"
        },
        {
            "id": 12,
            "text": "How would you rate your sleep quality?",
            "type": "scale",
            "min": 1,
            "max": 10,
            "category": "physiological"
        },
        {
            "id": 13,
            "text": "On average, how many hours of sleep do you get per night?",
            "type": "multiple_choice",
            "options": [
                "Less than 5 hours",
                "5-6 hours",
                "6-7 hours",
                "7-8 hours",
                "More than 8 hours"
            ],
            "scores": [0, 2.5, 7.5, 10, 7.5],  # Note: both too little and too much sleep can be suboptimal
            "category": "physiological"
        },
        {
            "id": 14,
            "text": "How often do you have difficulty falling asleep or staying asleep?",
            "type": "multiple_choice",
            "options": [
                "Almost every night",
                "Several times a week",
                "About once a week",
                "A few times a month",
                "Rarely or never"
            ],
            "scores": [0, 2.5, 5, 7.5, 10],
            "category": "physiological"
        },
        {
            "id": 15,
            "text": "How often do you consume processed foods or sugary drinks?",
            "type": "multiple_choice",
            "options": [
                "Multiple times daily",
                "Once daily",
                "A few times a week",
                "Occasionally (once a week or less)",
                "Rarely or never"
            ],
            "scores": [0, 2.5, 5, 7.5, 10],
            "category": "physiological"
        },
        {
            "id": 16,
            "text": "How often do you experience feelings of depression or persistent sadness?",
            "type": "multiple_choice",
            "options": [
                "Daily",
                "Several times a week",
                "About once a week",
                "Occasionally (a few times a month)",
                "Rarely or never"
            ],
            "scores": [0, 2.5, 5, 7.5, 10],
            "category": "psychological"
        },
        {
            "id": 17,
            "text": "How often do you engage in activities you enjoy or find meaningful?",
            "type": "multiple_choice",
            "options": [
                "Rarely or never",
                "Occasionally (once a month)",
                "Sometimes (a few times a month)",
                "Often (weekly)",
                "Very frequently (multiple times per week)"
            ],
            "scores": [0, 2.5, 5, 7.5, 10],
            "category": "psychological"
        },
        {
            "id": 18,
            "text": "How would you rate your ability to manage and recover from physical exertion?",
            "type": "scale",
            "min": 1,
            "max": 10,
            "category": "physical"
        }
    ]
