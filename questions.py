def get_categories():
    """Return the categories used in the health assessment."""
    return {
        "physical": "Physical Health",
        "physiological": "Physiological Health",
        "psychological": "Psychological Wellbeing",
        "womens_health": "Women's Health",
        "injuries": "Injury History"
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
            "text": "How often do you weight yourself per week?",
            "type": "numeric_input",
            "min": 0,
            "max": 20,
            "category": "physiological",
            "unit": "times",
            "default": 0
        },
        {
            "id": 5,
            "text": "How old were you when you had your first period?",
            "type": "multiple_choice",
            "options": [
                "13 or younger",
                "14-15",
                "16 or older",
                "Never started"
            ],
            "scores": [5, 7.5, 5, 2.5],
            "category": "womens_health"
        },
        {
            "id": 6,
            "text": "Have your periods stopped for 6 or more consecutive months (besides pregnancy or taking hormonal contraception)?",
            "type": "multiple_choice",
            "options": [
                "No, never",
                "Yes, it has happened before",
                "Yes, that is the situation now"
            ],
            "scores": [10, 5, 2.5],
            "category": "womens_health"
        },
        {
            "id": 7,
            "text": "If your periods stopped at some time in your life, for how many years did this last?",
            "type": "numeric_input",
            "min": 0,
            "max": 30,
            "category": "womens_health",
            "unit": "years"
        },
        {
            "id": 8,
            "text": "During the last year how many days off dancing have you had due to injury?",
            "type": "multiple_choice",
            "options": [
                "0 to 6 days",
                "7 to 13 days",
                "14 days or more"
            ],
            "scores": [10, 5, 2.5],
            "category": "injuries"
        },
        {
            "id": 9,
            "text": "During the last year how many soft tissue injuries, e.g. muscle, ligament, tendon, joint (excluding fractures) have you had?",
            "type": "multiple_choice",
            "options": [
                "None",
                "One",
                "Two or more"
            ],
            "scores": [10, 5, 2.5],
            "category": "injuries"
        },
        {
            "id": 10,
            "text": "Of these soft tissue injuries, how many were recurrent (i.e. in the same place, or same type of injury)?",
            "type": "multiple_choice",
            "options": [
                "None",
                "One",
                "Two or more"
            ],
            "scores": [10, 5, 2.5],
            "category": "injuries"
        },
        {
            "id": 11,
            "text": "If you had bone injuries how many of these were recurrent, i.e. same place, or same type of injury?",
            "type": "multiple_choice",
            "options": [
                "Two or fewer",
                "More than two"
            ],
            "scores": [7.5, 2.5],
            "category": "injuries"
        },
        {
            "id": 12,
            "text": "If you have had any type of fractures, where have these been located? Check all that apply.",
            "type": "checkbox",
            "options": [
                "Legs",
                "Feet",
                "Pelvis",
                "Spine",
                "Arms",
                "Other"
            ],
            "category": "injuries"
        },
        {
            "id": 13,
            "text": "Are you vegetarian?",
            "type": "multiple_choice",
            "options": [
                "No",
                "Yes"
            ],
            "scores": [5, 7.5],
            "category": "physiological"
        },
        {
            "id": 14,
            "text": "Are you vegan?",
            "type": "multiple_choice",
            "options": [
                "No",
                "Yes"
            ],
            "scores": [5, 7.5],
            "category": "physiological"
        },
        {
            "id": 15,
            "text": "Do you exclude carbohydrates from your diet?",
            "type": "multiple_choice",
            "options": [
                "No",
                "Yes"
            ],
            "scores": [7.5, 3],
            "category": "physiological"
        },
        {
            "id": 16,
            "text": "Do you smoke?",
            "type": "multiple_choice",
            "options": [
                "No",
                "Yes"
            ],
            "scores": [10, 0],
            "category": "physical"
        },
        {
            "id": 17,
            "text": "How would you rate your levels of freshness over the past year?",
            "type": "scale",
            "min": 1,
            "max": 6,
            "min_label": "Extremely fatigued",
            "max_label": "Always fresh",
            "category": "physiological"
        },
        {
            "id": 18,
            "text": "How would you rate your sleep quality over the past year?",
            "type": "scale",
            "min": 1,
            "max": 6,
            "min_label": "Terrible",
            "max_label": "Always a good night's sleep",
            "category": "physiological"
        },
        {
            "id": 19,
            "text": "How would you rate your digestive system over the past year?",
            "type": "scale",
            "min": 1,
            "max": 6,
            "min_label": "Continual problems",
            "max_label": "Always fine",
            "category": "physiological"
        },
        {
            "id": 20,
            "text": "How does controlling what you eat affect the way you feel about yourself?",
            "type": "multiple_choice",
            "options": [
                "Doesn't affect me",
                "Not a big issue",
                "Something I manage",
                "On my mind",
                "Important",
                "Very important"
            ],
            "scores": [10, 8, 6, 4, 2, 0],
            "category": "psychological"
        },
        {
            "id": 21,
            "text": "How does controlling what you weigh affect the way you feel about yourself?",
            "type": "multiple_choice",
            "options": [
                "Doesn't affect me",
                "Not a big issue",
                "Something I manage",
                "On my mind",
                "Important",
                "Very important"
            ],
            "scores": [10, 8, 6, 4, 2, 0],
            "category": "psychological"
        },
        {
            "id": 22,
            "text": "Have you ever been diagnosed with an eating disorder?",
            "type": "multiple_choice",
            "options": [
                "Yes",
                "No"
            ],
            "scores": [0, 10],
            "category": "psychological"
        }
    ]
