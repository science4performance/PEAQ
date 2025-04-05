import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_radar_chart(scores_by_category, categories_metadata):
    """
    Create a radar chart to visualize category scores.
    
    Args:
        scores_by_category: Dictionary with category as key and score as value
        categories_metadata: Dictionary with category IDs and display names
        
    Returns:
        Plotly figure object
    """
    # Get category names for display
    categories = [categories_metadata[cat] for cat in scores_by_category.keys()]
    values = list(scores_by_category.values())
    
    # Add the first value again to close the polygon
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Health Score',
        line_color='rgba(54, 162, 235, 0.8)',
        fillcolor='rgba(54, 162, 235, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False,
        title="Health Score by Category"
    )
    
    return fig

def create_category_bar_chart(scores_by_category):
    """
    Create a bar chart to visualize category scores.
    
    Args:
        scores_by_category: Dictionary with category as key and score as value
        
    Returns:
        Plotly figure object
    """
    # Create DataFrame for plotting
    df = pd.DataFrame({
        'Category': list(scores_by_category.keys()),
        'Score': list(scores_by_category.values())
    })
    
    # Map category codes to readable names
    category_names = {
        'physical': 'Physical Health',
        'mental': 'Mental Health',
        'social': 'Social Wellbeing',
        'nutrition': 'Nutrition',
        'sleep': 'Sleep Quality'
    }
    
    df['Category'] = df['Category'].map(category_names)
    
    # Create horizontal bar chart
    fig = px.bar(
        df, 
        x='Score', 
        y='Category',
        orientation='h',
        range_x=[0, 10],
        color='Score',
        color_continuous_scale='blues',
        title="Category Scores"
    )
    
    fig.update_layout(
        xaxis_title="Score (0-10)",
        yaxis_title="",
        coloraxis_showscale=False
    )
    
    return fig
