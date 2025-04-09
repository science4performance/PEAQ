def calculate_scores(answers):
    """
    Calculate average scores for each category from the user's answers.
    
    Args:
        answers: Dictionary with question index as key and answer data as value
        
    Returns:
        Dictionary with category as key and average score as value
    """
    category_scores = {}
    category_counts = {}
    
    # category = "physical"
    # # Add BMI score to the physical category
    # if category in category_scores:
    #     category_scores[category] += bmi_score + lowest_bmi_score
    #     category_counts[category] += 2
    # else:
    #     category_scores[category] = bmi_score + lowest_bmi_score
    #     category_counts[category] = 2


    # Sum scores by category
    for q_idx, answer_data in answers.items():
        category = answer_data["category"]
        
        # Skip info category
        if category == "info":
            continue
        # Skip numeric input questions which don't have scores
        if "score" not in answer_data:
            continue
            
        score = answer_data["score"]
        
        if category in category_scores:
            category_scores[category] += score
            category_counts[category] += 1
        else:
            category_scores[category] = score
            category_counts[category] = 1
    
    # Calculate average for each category
    #average_scores = {}
    #for category, total in category_scores.items():
    #    average_scores[category] = total / category_counts[category]
    
    return category_scores

def get_interpretation(overall_score):
    """
    Get interpretation text based on the overall health score.
    
    Args:
        overall_score: Numerical score between 0-10
        
    Returns:
        String with interpretation of the score
    """
    if overall_score >= 5:
        return "Reassuring result, suggesting that you have a healthy balance between training load, nutrition and recovery. Looking forwards, you may wish to consider seeking advice on future maintenance and improvement."
    elif overall_score >= -3:
        return "Room for improvement, suggesting some areas could be better. You should consider seeking expert help to explore ways to improve your health and performance."
    else:
        return "Potential concern, suggesting that you may need to address imbalances between you training load, nutrition and recovery.  You are strongly advised to consider seeking expert help to explore ways to improve your health and performance."
