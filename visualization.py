import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np  # Ensure numpy is imported

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
        'physical': 'Physical Health<br>BMI and injuries',
        'physiological': 'Physiological Health<br>Hormones, sleep and nutrition',
        'psychological': 'Psychological Wellbeing<br>Habits and anxiety',
        'overall': 'Overall Score',
    }
    
    df['Category'] = df['Category'].map(category_names)

    # Reverse the order of rows in the DataFrame
    #df = df.iloc[::-1]

    # Replace zero values with a small value for visibility
    df['Adjusted Score'] = df['Score'].apply(lambda x: 0.01 if x == 0 else x)

    # Assign colors based on positive or negative scores
    df["Color"] = np.where(df["Score"] < 0, 'red', 'green')
    title = "REDs Risk Score" if "Overall Score" in df['Category'].values else "Net Category Scores"

    # Create horizontal bar chart with text values
    fig = px.bar(
        df, 
        x='Adjusted Score',  # Use the adjusted score for the bar width
        y='Category',
        orientation='h',
        title=title,
        text='Score'  # Add text to display the original score values
    )
    
    # Set bar colors explicitly based on df["Color"]
    fig.update_traces(
        marker_color=df["Color"], 
        showlegend=False,  # Disable legend
        textposition='outside',  # Position text outside the bars
        texttemplate='%{text:+}'  # Add + sign for positive numbers
    )
    
    # Set x-axis range and reduce chart height
    fig.update_layout(
        xaxis=dict(range=[-20, 20]),  # Set x-axis range
        yaxis=dict(),  # Default y-axis order
        xaxis_title="Score",
        yaxis_title="",
        coloraxis_showscale=False,  # Hide the color scale
        height=350,  # Reduce the height of the chart (adjust as needed)
        margin=dict(l=200, r=20, t=50, b=50)  # Default margins
    )
    
    return fig

def overall_fig(overall_score):
    """
    Generate a chart to display the overall score with a horizontal bar and a vertical arrow.
    
    Args:
        overall_score: The overall score to be displayed on the chart.
        
    Returns:
        Plotly figure object
    """
    # Create the figure
    fig = go.Figure()

    # Add the horizontal bar with a continuous color gradient using Heatmap
    fig.add_trace(go.Heatmap(
        z=[[i for i in np.linspace(-20, 20, 500)]],  # Increase resolution for smoother gradient
        x=np.linspace(-20, 20, 500),  # x-axis values from -20 to 20 with higher resolution
        y=["Overall Score"],  # Single row for the heatmap
        colorscale="RdYlGn",  # Use the "RdYlGn" colorscale
        zmin=-20,  # Minimum value for the color scale
        zmax=20,   # Maximum value for the color scale
        showscale=False  # Hide the color scale legend
    ))

    # Add a vertical arrow to indicate the overall score
    fig.add_trace(go.Scatter(
        x=[overall_score],
        y=["Overall Score"],
        mode='markers+text',
        marker=dict(
            symbol='triangle-up',
            size=20,  # Default size of the triangle
            color='black'
        ),
        text=[f"{overall_score:+}"],  # Display the score as text
        textposition='top center',  # Default position of the text
        textfont=dict(
            size=16,  # Default font size
            color='black',  # Default font color
            family="Arial"  # Default font family
        ),
        showlegend=False
    ))

    # Update layout
    fig.update_layout(
        xaxis=dict(
            range=[-20, 20],  # Set x-axis range
            title="Score",
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=1
        ),
        yaxis=dict(
            showticklabels=False,  # Hide y-axis tick labels
            title=""
        ),
        title="REDs Risk Score",
        height=200,  # Default height for the chart
        margin=dict(l=50, r=50, t=50, b=50)  # Default margins
    )

    return fig