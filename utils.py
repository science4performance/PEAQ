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
    
    # Sum scores by category
    for q_idx, answer_data in answers.items():
        category = answer_data["category"]
        
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
    average_scores = {}
    for category, total in category_scores.items():
        average_scores[category] = total / category_counts[category]
    
    return average_scores

def get_interpretation(overall_score):
    """
    Get interpretation text based on the overall health score.
    
    Args:
        overall_score: Numerical score between 0-10
        
    Returns:
        String with interpretation of the score
    """
    if overall_score >= 8.5:
        return "Excellent: Your overall health appears to be exceptionally good. You're making great choices that support your well-being."
    elif overall_score >= 7:
        return "Very Good: Your health metrics show strong results. Continue with your current healthy practices while looking for small areas to improve."
    elif overall_score >= 5.5:
        return "Good: Your health is generally good, but there's room for improvement in some areas. Review your category scores to identify areas for focus."
    elif overall_score >= 4:
        return "Fair: Your health assessment indicates some concerns. Consider making lifestyle adjustments in the lower-scoring categories."
    elif overall_score >= 2.5:
        return "Concerning: Several aspects of your health appear to need attention. Consider consulting with healthcare professionals about the categories with lower scores."
    else:
        return "Poor: Your assessment results suggest significant health concerns. We strongly recommend consulting with healthcare professionals to create an improvement plan."
