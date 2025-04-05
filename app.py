import streamlit as st
import pandas as pd
import uuid
import datetime
from questions import get_questions, get_categories
from utils import calculate_scores, get_interpretation
from data_handler import save_assessment, load_assessments
from visualization import create_radar_chart, create_category_bar_chart

st.set_page_config(
    page_title="Health Assessment Questionnaire",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False
if 'show_previous' not in st.session_state:
    st.session_state.show_previous = False

# Load all questions
questions = get_questions()
categories = get_categories()
total_questions = len(questions)

def reset_assessment():
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.assessment_complete = False
    st.session_state.show_previous = False

def navigate_to_question(question_index):
    st.session_state.current_question = question_index

def save_answer(question_index, answer):
    st.session_state.answers[question_index] = answer
    if question_index < total_questions - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.assessment_complete = True
    st.rerun()

def main():
    st.title("Health Assessment Questionnaire")
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        
        if st.button("Start New Assessment"):
            reset_assessment()
            st.rerun()
            
        if st.button("View Previous Assessments"):
            st.session_state.show_previous = True
            st.session_state.assessment_complete = False
            st.rerun()
            
    # Main content area
    if st.session_state.show_previous:
        display_previous_assessments()
    elif st.session_state.assessment_complete:
        display_results()
    else:
        display_questionnaire()

def display_questionnaire():
    current_q = st.session_state.current_question
    question = questions[current_q]
    
    # Progress bar
    progress = (current_q) / total_questions
    st.progress(progress)
    st.write(f"Question {current_q + 1} of {total_questions}")
    
    # Display the current question
    st.subheader(question["text"])
    
    # Handle different question types
    if question["type"] == "multiple_choice":
        options = question["options"]
        choice = st.radio("Select one option:", options, key=f"q{current_q}")
        
        if st.button("Next", key=f"next_{current_q}"):
            option_index = options.index(choice)
            save_answer(current_q, {
                "answer": choice,
                "score": question["scores"][option_index],
                "category": question["category"]
            })
            
    elif question["type"] == "scale":
        # Create a more descriptive slider label if min_label and max_label are provided
        slider_label = "Select a value:"
        if "min_label" in question and "max_label" in question:
            slider_label = f"Select a value (1 = {question['min_label']}, {question['max']} = {question['max_label']}):"
        
        value = st.slider(
            slider_label, 
            min_value=question["min"], 
            max_value=question["max"],
            step=1,
            key=f"q{current_q}"
        )
        
        if st.button("Next", key=f"next_{current_q}"):
            # Calculate normalized score based on min-max values
            normalized_score = (value - question["min"]) / (question["max"] - question["min"])
            score = normalized_score * 10  # Scale to 0-10
            save_answer(current_q, {
                "answer": value,
                "score": score,
                "category": question["category"]
            })
            
    elif question["type"] == "numeric_input":
        # Display unit if provided
        label = f"Enter a value between {question['min']} and {question['max']}"
        if "unit" in question:
            label += f" ({question['unit']})"
            
        # Calculate default value as midpoint of range
        default_value = question["min"]
        
        # Set default values for questions 1, 2, and 3
        if question["id"] == 1:  # Height
            default_value = (1.2 + 2.2) / 2  # 1.7m
            
            # Input with validation for height (float value)
            value = st.number_input(
                label,
                min_value=float(question["min"]),
                max_value=float(question["max"]),
                value=float(default_value),
                step=0.01,
                key=f"q{current_q}"
            )
        elif question["id"] == 2:  # Current weight
            default_value = (30 + 100) / 2  # 65kg
            
            # Input with validation for weight (float value)
            value = st.number_input(
                label,
                min_value=float(question["min"]),
                max_value=float(question["max"]),
                value=float(default_value),
                step=0.01,
                key=f"q{current_q}"
            )
        elif question["id"] == 3:  # Lowest weight
            default_value = (30 + 100) / 2  # 65kg
            
            # Input with validation for lowest weight (float value)
            value = st.number_input(
                label,
                min_value=float(question["min"]),
                max_value=float(question["max"]),
                value=float(default_value),
                step=0.01,
                key=f"q{current_q}"
            )
        elif question["id"] in [4, 7, 8, 9, 10, 11]:  # Integer questions
            # Calculate midpoint for default value
            default_value = int((question["min"] + question["max"]) / 2)
            
            # Input with validation for integer values
            value = st.number_input(
                label,
                min_value=int(question["min"]),
                max_value=int(question["max"]),
                value=int(default_value),
                step=1,
                key=f"q{current_q}"
            )
        else:
            # Default numeric input handling with float values
            value = st.number_input(
                label,
                min_value=float(question["min"]),
                max_value=float(question["max"]),
                value=float(default_value),
                step=0.01,
                key=f"q{current_q}"
            )
        
        if st.button("Next", key=f"next_{current_q}"):
            # We don't calculate a score for numeric inputs, just store the value
            save_answer(current_q, {
                "answer": value,
                "value": value,  # Raw value without scoring
                "unit": question.get("unit", ""),
                "category": question["category"]
            })
            
    elif question["type"] == "checkbox":
        options = question["options"]
        # Create a dictionary to store checkbox states
        checkbox_values = {}
        
        for option in options:
            checkbox_values[option] = st.checkbox(option, key=f"q{current_q}_{option}")
        
        if st.button("Next", key=f"next_{current_q}"):
            # Get selected options
            selected_options = [option for option, selected in checkbox_values.items() if selected]
            
            # Store the answer without scoring
            save_answer(current_q, {
                "answer": selected_options,
                "category": question["category"]
            })
    
    # Allow navigation between questions
    cols = st.columns(3)
    with cols[0]:
        if current_q > 0:
            if st.button("Previous", key=f"prev_{current_q}"):
                navigate_to_question(current_q - 1)
                st.rerun()

def display_results():
    st.header("Your Health Assessment Results")
    
    # Display metric input values first
    st.subheader("Your Measurements")
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    
    # Extract metrics from answers (first 3 questions)
    height_value = None
    weight_value = None
    lowest_weight_value = None
    
    if 0 in st.session_state.answers:
        height_value = st.session_state.answers[0].get("value")
    if 1 in st.session_state.answers:
        weight_value = st.session_state.answers[1].get("value")
    if 2 in st.session_state.answers:
        lowest_weight_value = st.session_state.answers[2].get("value")
    
    # Display the metric values
    with metrics_col1:
        if height_value is not None:
            st.metric("Height", f"{height_value} m")
    
    with metrics_col2:
        if weight_value is not None:
            st.metric("Current Weight", f"{weight_value} kg")
    
    with metrics_col3:
        if lowest_weight_value is not None:
            st.metric("Lowest Weight", f"{lowest_weight_value} kg")
    
    # Display weighing frequency if available
    if 3 in st.session_state.answers:
        weighing_frequency = st.session_state.answers[3].get("value")
        st.metric("Weighing Frequency", f"{int(weighing_frequency)} times/week")
    
    # Calculate BMI if both height and weight are available
    if height_value and weight_value:
        bmi = weight_value / (height_value * height_value)
        st.metric("Current BMI", f"{bmi:.1f}")
        
        # Calculate lowest BMI if lowest weight is available
        if lowest_weight_value:
            lowest_bmi = lowest_weight_value / (height_value * height_value)
            st.metric("Lowest BMI", f"{lowest_bmi:.1f}")
        
        # Display BMI category (based on current BMI)
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25:
            bmi_category = "Normal weight"
        elif bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"
            
        st.write(f"BMI Category: **{bmi_category}**")
    
    # Display injury information if available
    injury_data_available = False
    for q_idx in [7, 8, 9, 10, 11]:  # Injury questions indices
        if q_idx in st.session_state.answers:
            injury_data_available = True
            break
    
    if injury_data_available:
        st.subheader("Injury Information")
        
        # Days off dancing due to injury
        if 7 in st.session_state.answers:
            days_off = st.session_state.answers[7].get("value")
            st.metric("Days off dancing due to injury (last year)", f"{int(days_off)} days")
        
        # Soft tissue injuries
        if 8 in st.session_state.answers:
            soft_injuries = st.session_state.answers[8].get("value")
            st.metric("Soft tissue injuries (last year)", f"{int(soft_injuries)}")
        
        # Recurrent soft tissue injuries
        if 9 in st.session_state.answers:
            recurrent_soft = st.session_state.answers[9].get("value")
            st.metric("Recurrent soft tissue injuries", f"{int(recurrent_soft)}")
        
        # Recurrent bone injuries
        if 10 in st.session_state.answers:
            recurrent_bone = st.session_state.answers[10].get("value")
            st.metric("Recurrent bone injuries", f"{int(recurrent_bone)}")
        
        # Fracture locations (checkbox)
        if 11 in st.session_state.answers:
            fracture_locations = st.session_state.answers[11].get("answer", [])
            if fracture_locations:
                st.write("**Fracture locations:**")
                for location in fracture_locations:
                    st.write(f"- {location}")
            else:
                st.write("**No fracture locations selected**")
                
    # Display lifestyle information if available
    lifestyle_data_available = False
    for q_idx in [12, 13, 14, 15]:  # Diet and Smoking questions indices
        if q_idx in st.session_state.answers:
            lifestyle_data_available = True
            break
    
    if lifestyle_data_available:
        st.subheader("Lifestyle Information")
        
        # Create two columns for displaying lifestyle data
        lifestyle_col1, lifestyle_col2 = st.columns(2)
        
        with lifestyle_col1:
            # Vegetarian status
            if 12 in st.session_state.answers:
                vegetarian = st.session_state.answers[12].get("answer", "")
                st.metric("Vegetarian", vegetarian)
            
            # Vegan status
            if 13 in st.session_state.answers:
                vegan = st.session_state.answers[13].get("answer", "")
                st.metric("Vegan", vegan)
        
        with lifestyle_col2:
            # Carb exclusion
            if 14 in st.session_state.answers:
                carb_exclusion = st.session_state.answers[14].get("answer", "")
                st.metric("Excludes Carbohydrates", carb_exclusion)
            
            # Smoking status
            if 15 in st.session_state.answers:
                smoking = st.session_state.answers[15].get("answer", "")
                st.metric("Smokes", smoking)
    
    # Display wellbeing information if available
    wellbeing_data_available = False
    for q_idx in [16, 17, 18, 19, 20, 21]:  # Wellbeing questions indices
        if q_idx in st.session_state.answers:
            wellbeing_data_available = True
            break
    
    if wellbeing_data_available:
        st.subheader("Wellbeing Information")
        
        # Create columns for displaying wellbeing data
        wellbeing_col1, wellbeing_col2, wellbeing_col3 = st.columns(3)
        
        with wellbeing_col1:
            # Freshness rating
            if 16 in st.session_state.answers:
                freshness = st.session_state.answers[16].get("answer", "")
                st.metric("Freshness Rating (1-6)", freshness)
            
            # Sleep quality
            if 17 in st.session_state.answers:
                sleep = st.session_state.answers[17].get("answer", "")
                st.metric("Sleep Quality (1-6)", sleep)
        
        with wellbeing_col2:
            # Digestive system
            if 18 in st.session_state.answers:
                digestive = st.session_state.answers[18].get("answer", "")
                st.metric("Digestive Health (1-6)", digestive)
            
            # Eating control
            if 19 in st.session_state.answers:
                eating_control = st.session_state.answers[19].get("answer", "")
                st.write(f"**Control over eating:** {eating_control}")
        
        with wellbeing_col3:
            # Weight control
            if 20 in st.session_state.answers:
                weight_control = st.session_state.answers[20].get("answer", "")
                st.write(f"**Control over weight:** {weight_control}")
            
            # Eating disorder diagnosis
            if 21 in st.session_state.answers:
                eating_disorder = st.session_state.answers[21].get("answer", "")
                st.metric("Diagnosed with Eating Disorder", eating_disorder)
    
    st.markdown("---")
    
    # Calculate scores
    scores_by_category = calculate_scores(st.session_state.answers)
    overall_score = sum(scores_by_category.values()) / len(scores_by_category)
    
    # Get interpretation
    interpretation = get_interpretation(overall_score)
    
    # Display overall score
    st.subheader(f"Overall Health Score: {overall_score:.1f}/10")
    st.write(f"Interpretation: {interpretation}")
    
    # Display category scores
    st.subheader("Category Breakdown")
    
    # Two columns layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        radar_fig = create_radar_chart(scores_by_category, categories)
        st.plotly_chart(radar_fig)
    
    with col2:
        bar_fig = create_category_bar_chart(scores_by_category)
        st.plotly_chart(bar_fig)
    
    # Save assessment
    if st.button("Save Results"):
        save_assessment(
            user_id=st.session_state.user_id,
            answers=st.session_state.answers,
            scores=scores_by_category,
            overall_score=overall_score,
            timestamp=datetime.datetime.now()
        )
        st.success("Assessment saved successfully!")
    
    # Export options
    export_format = st.selectbox("Export Format", ["CSV", "JSON"])
    if st.button("Export Results"):
        if export_format == "CSV":
            df = pd.DataFrame({
                'Category': list(scores_by_category.keys()),
                'Score': list(scores_by_category.values())
            })
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="health_assessment_results.csv",
                mime="text/csv"
            )
        else:
            import json
            export_data = {
                'user_id': st.session_state.user_id,
                'timestamp': datetime.datetime.now().isoformat(),
                'overall_score': overall_score,
                'categories': dict(scores_by_category),
                'interpretation': interpretation
            }
            json_str = json.dumps(export_data, indent=4)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="health_assessment_results.json",
                mime="application/json"
            )

def display_previous_assessments():
    st.header("Previous Assessment Results")
    
    assessments = load_assessments(st.session_state.user_id)
    
    if not assessments:
        st.info("No previous assessments found.")
        return
    
    # Create a dataframe from assessments for display
    assessment_list = []
    for assessment in assessments:
        assessment_list.append({
            'Date': assessment['timestamp'].strftime('%Y-%m-%d %H:%M'),
            'Overall Score': f"{assessment['overall_score']:.1f}",
            'ID': assessment['id']
        })
    
    df = pd.DataFrame(assessment_list)
    st.dataframe(df)
    
    # Allow selection of an assessment to view details
    selected_assessment_id = st.selectbox(
        "Select an assessment to view details:", 
        options=[a['id'] for a in assessments],
        format_func=lambda x: next((a['timestamp'].strftime('%Y-%m-%d %H:%M') for a in assessments if a['id'] == x), x)
    )
    
    if selected_assessment_id:
        selected = next((a for a in assessments if a['id'] == selected_assessment_id), None)
        if selected:
            st.subheader(f"Assessment from {selected['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            
            # Display metrics if they exist in the answers
            if 'answers' in selected:
                # Extract metrics from answers (first 3 questions)
                height_value = None
                weight_value = None
                lowest_weight_value = None
                
                if 0 in selected['answers']:
                    height_value = selected['answers'][0].get("value")
                if 1 in selected['answers']:
                    weight_value = selected['answers'][1].get("value")
                if 2 in selected['answers']:
                    lowest_weight_value = selected['answers'][2].get("value")
                
                if any([height_value, weight_value, lowest_weight_value]):
                    st.subheader("Measurements")
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    
                    # Display the metric values
                    with metrics_col1:
                        if height_value is not None:
                            st.metric("Height", f"{height_value} m")
                    
                    with metrics_col2:
                        if weight_value is not None:
                            st.metric("Current Weight", f"{weight_value} kg")
                    
                    with metrics_col3:
                        if lowest_weight_value is not None:
                            st.metric("Lowest Weight", f"{lowest_weight_value} kg")
                    
                    # Display weighing frequency if available
                    if 3 in selected['answers']:
                        weighing_frequency = selected['answers'][3].get("value")
                        st.metric("Weighing Frequency", f"{int(weighing_frequency)} times/week")
                    
                    # Calculate BMI if both height and weight are available
                    if height_value and weight_value:
                        bmi = weight_value / (height_value * height_value)
                        st.metric("Current BMI", f"{bmi:.1f}")
                        
                        # Calculate lowest BMI if lowest weight is available
                        if lowest_weight_value:
                            lowest_bmi = lowest_weight_value / (height_value * height_value)
                            st.metric("Lowest BMI", f"{lowest_bmi:.1f}")
                        
                        # Display BMI category (based on current BMI)
                        if bmi < 18.5:
                            bmi_category = "Underweight"
                        elif bmi < 25:
                            bmi_category = "Normal weight"
                        elif bmi < 30:
                            bmi_category = "Overweight"
                        else:
                            bmi_category = "Obese"
                            
                        st.write(f"BMI Category: **{bmi_category}**")
                        
                # Display injury information if available
                if 'answers' in selected:
                    injury_data_available = False
                    for q_idx in [7, 8, 9, 10, 11]:  # Injury questions indices
                        if q_idx in selected['answers']:
                            injury_data_available = True
                            break
                    
                    if injury_data_available:
                        st.subheader("Injury Information")
                        
                        # Days off dancing due to injury
                        if 7 in selected['answers']:
                            days_off = selected['answers'][7].get("value")
                            st.metric("Days off dancing due to injury (last year)", f"{int(days_off)} days")
                        
                        # Soft tissue injuries
                        if 8 in selected['answers']:
                            soft_injuries = selected['answers'][8].get("value")
                            st.metric("Soft tissue injuries (last year)", f"{int(soft_injuries)}")
                        
                        # Recurrent soft tissue injuries
                        if 9 in selected['answers']:
                            recurrent_soft = selected['answers'][9].get("value")
                            st.metric("Recurrent soft tissue injuries", f"{int(recurrent_soft)}")
                        
                        # Recurrent bone injuries
                        if 10 in selected['answers']:
                            recurrent_bone = selected['answers'][10].get("value")
                            st.metric("Recurrent bone injuries", f"{int(recurrent_bone)}")
                        
                        # Fracture locations (checkbox)
                        if 11 in selected['answers']:
                            fracture_locations = selected['answers'][11].get("answer", [])
                            if fracture_locations:
                                st.write("**Fracture locations:**")
                                for location in fracture_locations:
                                    st.write(f"- {location}")
                            else:
                                st.write("**No fracture locations selected**")
                                
                    # Display lifestyle information if available
                    lifestyle_data_available = False
                    for q_idx in [12, 13, 14, 15]:  # Diet and Smoking questions indices
                        if q_idx in selected['answers']:
                            lifestyle_data_available = True
                            break
                    
                    if lifestyle_data_available:
                        st.subheader("Lifestyle Information")
                        
                        # Create two columns for displaying lifestyle data
                        lifestyle_col1, lifestyle_col2 = st.columns(2)
                        
                        with lifestyle_col1:
                            # Vegetarian status
                            if 12 in selected['answers']:
                                vegetarian = selected['answers'][12].get("answer", "")
                                st.metric("Vegetarian", vegetarian)
                            
                            # Vegan status
                            if 13 in selected['answers']:
                                vegan = selected['answers'][13].get("answer", "")
                                st.metric("Vegan", vegan)
                        
                        with lifestyle_col2:
                            # Carb exclusion
                            if 14 in selected['answers']:
                                carb_exclusion = selected['answers'][14].get("answer", "")
                                st.metric("Excludes Carbohydrates", carb_exclusion)
                            
                            # Smoking status
                            if 15 in selected['answers']:
                                smoking = selected['answers'][15].get("answer", "")
                                st.metric("Smokes", smoking)
                    
                    # Display wellbeing information if available
                    wellbeing_data_available = False
                    for q_idx in [16, 17, 18, 19, 20, 21]:  # Wellbeing questions indices
                        if q_idx in selected['answers']:
                            wellbeing_data_available = True
                            break
                    
                    if wellbeing_data_available:
                        st.subheader("Wellbeing Information")
                        
                        # Create columns for displaying wellbeing data
                        wellbeing_col1, wellbeing_col2, wellbeing_col3 = st.columns(3)
                        
                        with wellbeing_col1:
                            # Freshness rating
                            if 16 in selected['answers']:
                                freshness = selected['answers'][16].get("answer", "")
                                st.metric("Freshness Rating (1-6)", freshness)
                            
                            # Sleep quality
                            if 17 in selected['answers']:
                                sleep = selected['answers'][17].get("answer", "")
                                st.metric("Sleep Quality (1-6)", sleep)
                        
                        with wellbeing_col2:
                            # Digestive system
                            if 18 in selected['answers']:
                                digestive = selected['answers'][18].get("answer", "")
                                st.metric("Digestive Health (1-6)", digestive)
                            
                            # Eating control
                            if 19 in selected['answers']:
                                eating_control = selected['answers'][19].get("answer", "")
                                st.write(f"**Control over eating:** {eating_control}")
                        
                        with wellbeing_col3:
                            # Weight control
                            if 20 in selected['answers']:
                                weight_control = selected['answers'][20].get("answer", "")
                                st.write(f"**Control over weight:** {weight_control}")
                            
                            # Eating disorder diagnosis
                            if 21 in selected['answers']:
                                eating_disorder = selected['answers'][21].get("answer", "")
                                st.metric("Diagnosed with Eating Disorder", eating_disorder)
            
            st.write(f"Overall Score: {selected['overall_score']:.1f}/10")
            
            # Display category scores
            st.subheader("Category Breakdown")
            
            col1, col2 = st.columns(2)
            with col1:
                radar_fig = create_radar_chart(selected['scores'], categories)
                st.plotly_chart(radar_fig)
            
            with col2:
                bar_fig = create_category_bar_chart(selected['scores'])
                st.plotly_chart(bar_fig)

if __name__ == "__main__":
    main()
