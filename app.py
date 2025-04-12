import streamlit as st
import pandas as pd
import uuid
import datetime
from questions import get_female_questions, get_male_questions, get_categories
from utils import calculate_scores, get_interpretation
from data_handler import save_assessment, create_pdf
from visualization import  create_category_bar_chart, overall_fig
from pathlib import Path



st.set_page_config(page_title="Personal Energy Availability Questionnaire",
                   page_icon="🏥",
                   layout="wide")
st.markdown(
    """
    <style>
    /* Set the background color */
    .stApp {
        background-color: #dcd3f2; /* NJK brand */
    }
    </style>
    """,
    unsafe_allow_html=True
)
PIC_DIR = Path("./pics")

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
if 'sex' not in st.session_state:
    st.session_state.sex = "None"

# Load all questions
#questions = get_female_questions()
#categories = get_categories()
#total_questions = len(questions)


def reset_assessment():
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.assessment_complete = False
    st.session_state.show_previous = False
    st.session_state.sex = "None"


def navigate_to_question(question_index):
    st.session_state.current_question = question_index


def save_answer(question_index, answer, total_questions):
    st.session_state.answers[question_index + 1] = answer
    if question_index < total_questions - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.assessment_complete = True
    st.rerun()

def save_BMI_score(id, height_value, weight_value):
    bmi = weight_value / (height_value * height_value)
    # Find BMI and cores 
    if bmi < 18.0:
        bmi_score = -2 
    elif bmi < 20:
        bmi_score = -1
    else:
        bmi_score = 1
    st.session_state.answers[id] = {
        "text": id,
        "answer": bmi,
        "score": bmi_score,
        "category": "physical"
        }
    
    
    
def main():
    st.title(
        f"{st.session_state.sex if st.session_state.sex != 'None' else ''} Personal Energy Availability Questionnaire (PEAQ) "
    )
    #st.write(st.session_state)
    if st.session_state.sex == 'None':

        st.markdown(
            """
            <style>
            /* Style the Male PEAQ button */
            div.stButton > button:first-child {
                font-size: 40px; /* Increase font size */
                font-weight: bold; /* Make the text bold */
                padding: 20px 40px; /* Add padding to make the button bigger */
                background-color: #4CAF50; /* Set a green background color */
                color: white; /* Set the text color to white */
                border: none; /* Remove borders */
                border-radius: 8px; /* Add rounded corners */
                cursor: pointer; /* Change cursor to pointer on hover */
            }
            div.stButton > button:first-child:hover {
                background-color: #45a049; /* Darker green on hover */
            }

            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        col2, col1 = st.columns(2)
        with col1:
            if st.button("Start Male PEAQ", key="male_peaq"):
                st.session_state.sex = "Male"
                st.rerun()
        with col2:
            if st.button("Start     Female PEAQ", key="female_peaq"):
                st.session_state.sex = "Female"
                st.rerun()
            
        
        st.markdown(
            "The personal energy availability questionnaire (PEAQ) is designed to assess your energy availability status. Click on a button to begin.")
        st.subheader("What is Energy Availability?")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                "Matching your energy intake to your energy demands helps you reach your personal peak health and exercise performance. "
                "Failing to meet your energy demands results in low energy availability. This increases your risk of developing relative energy deficiency (REDs) and its adverse health and performance consequences.<br>"
                        ,
                unsafe_allow_html=True)
        with col2:
            st.image(PIC_DIR / "NK.png", width=200)

        

        st.subheader("PEAQ - Personal Energy Availability Questionnaire")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("People of any age, whatever their level and type of exercise, can be at risk of developing REDs; from elite dancers and athletes to recreational exercisers. "
                "The PEAQ will guide you through a series of questions about exercise, physical characteristics, nutrition, hormone function and well-being. It just takes a few minutes."
                ,
                unsafe_allow_html=True)
        with col2:
            st.image(PIC_DIR / "GF.png", width=200)
        st.subheader("Benefits of the PEAQ")
        st.markdown(
           "Your personal report instantly generates a REDs Risk Score and provides valuable insights into your energy status and potential risks, along with guidance. The PEAQ is intended for those 16 years of age and over. <br>"
            "The PEAQ has been used in several published research studies; however, it is not a substitute for seeking medical advice. Dr Nicky Keay offers personalised health advisory appointments https://nickykeayfitness.com/appointments/."
           ,
             unsafe_allow_html=True)
        st.image(PIC_DIR / "PEAQ3.png")

        # Sidebar
    # with st.sidebar:
    #     st.title("Navigation")

    #     if st.button("Start New Assessment"):
    #         reset_assessment()
    #         st.rerun()

    #     if st.button("View Previous Assessments"):
    #         st.session_state.show_previous = True
    #         st.session_state.assessment_complete = False
    #         st.rerun()
    #     if st.button("Load Dataset"):
    #         st.session_state.user_id = '45a07288-caec-43f3-9191-1421ddff5aa9'
    #         st.session_state.assessment_id = '0bc96938-33e4-40d6-836c-2f374949697c'
    #         selected = get_assessment(st.session_state.user_id, st.session_state.assessment_id)
    #         st.session_state.sex = selected['sex']
    #         st.session_state.answers = selected['answers']
    #         st.session_state.assessment_complete = True
    #         #st.write(selected)
           


    # Main content area
    if st.session_state.show_previous:
        display_previous_assessments()
    elif st.session_state.assessment_complete:
        display_results()
    elif st.session_state.sex != 'None':
        display_questionnaire()


def display_questionnaire():
    if st.session_state.sex == "Female":
        questions = get_female_questions()
    elif st.session_state.sex == "Male":
        questions = get_male_questions()

    total_questions = len(questions)
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
            save_answer(
                current_q, {
                    "text": question["text"],
                    "answer": choice,
                    "score": question["scores"][option_index],
                    "category": question["category"]
                }, total_questions)

    elif question["type"] == "numeric_input":
        # Display unit if provided
        label = f"Enter a value between {question['min']} and {question['max']}"
        if "unit" in question:
            label += f" ({question['unit']})"
        value = st.number_input(label,
                                    min_value=question["min"],
                                    max_value=question["max"],
                                    value=question["default"],
                                    step=question["step"],
                                    key=f"q{current_q}")

        # Calculate default value as midpoint of range
        #default_value = question["min"]

        # Set default values for questions 1, 2, and 3
 
        if st.button("Next", key=f"next_{current_q}"):
            # We don't calculate a score for numeric inputs, just store the value
            save_answer(
                current_q,
                {
                    "text": question["text"],
                    "answer": value,
                    "value": value,  # Raw value without scoring
                    "unit": question.get("unit", ""),
                    "category": question["category"]
                },
                total_questions)

    elif question["type"] == "checkbox":
        options = question["options"]
        scores = question["scores"]
        # Create a dictionary to store checkbox states
        checkbox_values = {}

        for option in options:
            checkbox_values[option] = st.checkbox(option,
                                                  key=f"q{current_q}_{option}")

        if st.button("Next", key=f"next_{current_q}"):
            # Get selected options
            selected_options = [
                option for option, selected in checkbox_values.items()
                if selected
            ]
            value = sum([
                score for score, (option, selected) in zip(scores,checkbox_values.items())
                if selected
            ])

            # Store the answer without scoring
            save_answer(current_q, {
                "text": question["text"],
                "answer": selected_options,
                "score": value,  # Raw value without scoring
                "category": question["category"]
            }, total_questions)

    # Allow navigation between questions
    cols = st.columns(3)
    with cols[0]:
        if current_q > 0:
            if st.button("Previous", key=f"prev_{current_q}"):
                navigate_to_question(current_q - 1)
                st.rerun()


def display_results():
    # Display the results of the assessment
    st.header("Your Personal Energy Availability Results")
    comment = (
        "For most people, the REDs Risk Score is between -10 and +10. "
        "A strong positive score indicates good energy availability, "
        "while a negative score suggests low energy availability and a higher risk of REDs. "
        "This score is a general guideline and should not replace professional medical advice. "
        "If you have concerns about your energy availability or health, consider consulting a healthcare professional.\n"
    )
    st.markdown(comment)
        
    # Load the appropriate questions based on the user's sex
    if st.session_state.sex == "Female":
        questions = get_female_questions()
    elif st.session_state.sex == "Male":
        questions = get_male_questions()
    else:
        st.error("Sex not specified. Please restart the questionnaire.")
        return

    # Dynamically find the question IDs
    height_question_id = next(
        (q["id"] for q in questions if "Please enter your current height" in q["text"]), None)
    weight_question_id = next(
        (q["id"] for q in questions if "Please enter your current weight" in q["text"]), None)
    lowest_weight_question_id = next(
        (q["id"] for q in questions if "Please enter your lowest weight" in q["text"]), None)

    # Extract metric values from answers
    height_value = st.session_state.answers.get(height_question_id, {}).get("value")
    weight_value = st.session_state.answers.get(weight_question_id, {}).get("value")
    lowest_weight_value = st.session_state.answers.get(lowest_weight_question_id, {}).get("value")

    if height_value:
        save_BMI_score("BMI", height_value, weight_value)
        save_BMI_score("Lowest BMI", height_value, lowest_weight_value)

        

    # Calculate scores
    scores_by_category = calculate_scores(st.session_state.answers)
    overall_score = sum(scores_by_category.values()) 

    # Get interpretation
    interpretation = get_interpretation(overall_score)

   # Save assessment
    if not Path(f"data/{st.session_state.user_id}/PEAQ_results.pdf").exists():
        #st.write(Path(f"data/{st.session_state.user_id}/PEAQ_results.pdf"))
        st.session_state['assessment_id'] = save_assessment(user_id=st.session_state.user_id,
                        sex=st.session_state.sex,
                        answers=st.session_state.answers,
                        scores=scores_by_category,
                        overall_score=overall_score,
                        interpretation=interpretation,
                        timestamp=datetime.datetime.now())
   

    # Display overall score
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"REDs Risk Score: {overall_score:+.0f}")
        bar_fig1 = overall_fig(overall_score)
        st.plotly_chart(bar_fig1)
        bar_fig1.write_image(f"data/{st.session_state.user_id}/overall.jpeg")
        st.write(f"Interpretation: {interpretation}")

    with col2:
        st.subheader("Category Breakdown")
        bar_fig = create_category_bar_chart(scores_by_category)
        st.plotly_chart(bar_fig)
        bar_fig.write_image(f"data/{st.session_state.user_id}/categories.jpeg")

    final_comment1 = "If you would like more information about energy availability and relative energy deficiency you may wish to have a look at www.nickykeayfitness.com and read Dr Nicky Keay's book 'Hormones, Health and Human Potential' https://hhhp.neocities.org/ References to relevant studies where this questionnaire has been used are provided below."
    final_comment2 = "For individual, personal advice, Dr Nicky Keay offers health advisory appointments https://nickykeayfitness.com/appointments/ "       
    
    st.markdown(final_comment1 , unsafe_allow_html=True)
    st.markdown(final_comment2 , unsafe_allow_html=True)
 
    # Export options
    #export_format = st.selectbox("Export Format", ["CSV", "JSON"])
    #if st.button("Export Results"):
    #    if export_format == "CSV":
    # df = pd.DataFrame({
    #     'Category': list(scores_by_category.keys()),
    #     'Score': list(scores_by_category.values())
    # })
    # csv = df.to_csv(index=False)
    # st.download_button(label="Download CSV",
    #                     data=csv,
    #                     file_name="health_assessment_results.csv",
    #                     mime="text/csv")
    create_pdf(user_id=st.session_state.user_id, 
               assessment_id=st.session_state.assessment_id, 
               sex=st.session_state.sex, 
                     overall_score=overall_score, interpretation=interpretation, comment=comment)
    

    # Save the PDF to a buffer
    #pdf_buffer = io.BytesIO()
    #pdf.output(pdf_buffer)  # Write the PDF content directly to the buffer
    #pdf_buffer.seek(0)
    with open(f"data/{st.session_state.user_id}/PEAQ_results.pdf", "rb") as file:
        # Provide a download button for the PDF
        st.download_button(
            label="Download PDF",
            data=file,
            file_name="PEAQ_results.pdf",
            mime="application/pdf"
        )
            #else:
         #   import json
         #   export_data = {
          #      'user_id': st.session_state.user_id,
           #     'timestamp': datetime.datetime.now().isoformat(),
            #    'overall_score': overall_score,
            #     'categories': dict(scores_by_category),
            #     'interpretation': interpretation
            # }
            # json_str = json.dumps(export_data, indent=4)
            # st.download_button(label="Download JSON",
            #                    data=json_str,
            #                    file_name="health_assessment_results.json",
            #                    mime="application/json")
    st.image("pics/PEAQ3.png")

    st.subheader("References")
    st.markdown("Mountjoy M, Ackerman KE, Bailey DM et al 2023 International Olympic Committee’s (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs) British Journal of Sports Medicine 2023;57:1073-1098<br>"
             "Keay N Hormones, Health and Human Potential: A guide to understanding your hormones to optimise your health and performance, Sequoia books 2022<br>"             
             "Keay N, Francis G, AusDancersOverseas  Indicators and correlates of low energy availability in male and female dancers. BMJ Open in Sports and Exercise Medicine 2020<br>"
             "Nicolas J, Grafenuer S. Investigating pre-professional dancer health status and preventative health knowledge Front. Nutr. Sec. Sport and Exercise Nutrition. 2023 (10) <br>"
             "Keay N, Francis G. Longitudinal investigation of the range of adaptive responses of the female hormone network in pre- professional dancers in training March 2025 ResearchGate DOI: 10.13140/RG.2.2.30046.34880<br>"
             "Keay N. Current views on relative energy deficiency in sport (REDs). Focus Issue 6: Eating disorders. Cutting Edge Psychiatry in Practice CEPiP. 2024.1.98-102<br>"
             "Assessment of Relative Energy Deficiency in Sport, Malnutrition Prevalence in Female Endurance Runners by Energy Availability Questionnaire, Bioelectrical Impedance Analysis and Relationship with Ovulation status. Clinical Nutrition Open Science 2025S.  <br>"
             "Sharp S, Keay N, Slee A. Body composition, malnutrition, and ovulation status as RED-S risk assessors in female endurance athletes, Clinical Nutrition ESPEN 2023, 58 :720-721<br>"
             "Keay N, Craghill E, Francis G Female Football Specific Energy Availability Questionnaire and Menstrual Cycle Hormone Monitoring. Sports Injr Med 2022; 6: 177<br>"
             "Nicola Keay, Martin Lanfear, Gavin Francis. Clinical application of monitoring indicators of female dancer health, including application of artificial intelligence in female hormone networks. Internal Journal of Sports Medicine and Rehabilitation, 2022; 5:24.<br>"  
             "Nicola Keay, Martin Lanfear, Gavin Francis. Clinical application of interactive monitoring of indicators of health in professional dancers J Forensic Biomech, 2022, 12 (5) No:1000380 " 
            , unsafe_allow_html=True)


   
def display_previous_assessments():
    st.header("Previous Assessment Results")
    categories = get_categories()

    assessments = load_assessments(st.session_state.user_id)

    if not assessments:
        st.info("No previous assessments found.")
        return

    # Create a dataframe from assessments for display
    assessment_list = []
    for assessment in assessments:
        assessment_list.append({
            'Date':
            assessment['timestamp'].strftime('%Y-%m-%d %H:%M'),
            'Overall Score':
            f"{assessment['overall_score']:+.0f}",
            'ID':
            assessment['id']
        })

    df = pd.DataFrame(assessment_list)
    st.dataframe(df)

    # Allow selection of an assessment to view details
    selected_assessment_id = st.selectbox(
        "Select an assessment to view details:",
        options=[a['id'] for a in assessments],
        format_func=lambda x: next((a['timestamp'].strftime('%Y-%m-%d %H:%M')
                                    for a in assessments if a['id'] == x), x))

    if selected_assessment_id:
        selected = next(
            (a for a in assessments if a['id'] == selected_assessment_id),
            None)
        if selected:
            st.subheader(
                f"Assessment from {selected['timestamp'].strftime('%Y-%m-%d %H:%M')} Sex: {selected['sex']}"
            )

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"REDs Risk Score: {selected['overall_score']:+.0f}")
                bar_fig1 = overall_fig(selected['overall_score'])
                st.plotly_chart(bar_fig1)
                st.write(f"Interpretation: {selected['interpretation']}")

            with col2:
                # Display category scores
                st.subheader("Category Breakdown")  
                bar_fig = create_category_bar_chart(selected['scores'])
                st.plotly_chart(bar_fig)

            df = pd.DataFrame.from_dict(selected['answers']).T.sort_values("category")
            df

if __name__ == "__main__":
    main()
