import os
import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define patient data
patient_data = {
    "name": "Ben Hackett",
    "age": 45,
    "gender": "Male",
    "conditions": [
        "Type 2 Diabetes",
        "Hypertension",
        "Hyperlipidemia",
        "Obesity",
        "Chronic Kidney Disease (Stage 3)",
        "Sleep Apnea"
    ],
    "labs": {
        "HbA1c": 7.5,
        "Fasting Blood Glucose": 140,
        "Total Cholesterol": 220,
        "LDL": 140,
        "HDL": 40,
        "Triglycerides": 180,
        "Blood Pressure": "145/90",
        "eGFR": 50,
        "BMI": 32,
        "Urine Albumin-to-Creatinine Ratio (UACR)": 45
    },
    "summary": "Ben Hackett is a 45-year-old male with a history of type 2 diabetes, hypertension, hyperlipidemia, obesity, chronic kidney disease (stage 3), and sleep apnea. He has been managing his diabetes with metformin and lifestyle modifications but has been struggling with maintaining good glycemic control. His blood pressure and lipid levels are also elevated, and his kidney function is impaired."
}

def generate_plan(prompt):
    print("Generating plan with prompt:")
    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    print("Generated plan:")
    print(response.choices[0].message['content'])
    return response.choices[0].message['content']

def display_plan(plan):
    lines = plan.strip().split('\n')
    for line in lines:
        if line.startswith('- '):
            if 'medication' in line.lower():
                icon = '💊'
            elif 'lifestyle' in line.lower():
                icon = '🏃'
            elif 'remind' in line.lower() or 'recommend' in line.lower():
                icon = '📋'
            else:
                icon = '📈'
            st.markdown(f"{icon} {line}")
        else:
            st.write(line)

def main():
    st.title("Physician Prep for Patient Visit")
    st.write("Patient Data:")
    st.write(patient_data)

    prompt = f"""
    You are a physician preparing for a patient visit. The patient has the following medical records:

    Name: {patient_data['name']}
    Age: {patient_data['age']}
    Gender: {patient_data['gender']}
    Conditions: {', '.join(patient_data['conditions'])}
    Labs:
    - HbA1c: {patient_data['labs']['HbA1c']}
    - Fasting Blood Glucose: {patient_data['labs']['Fasting Blood Glucose']}
    - Total Cholesterol: {patient_data['labs']['Total Cholesterol']}
    - LDL: {patient_data['labs']['LDL']}
    - HDL: {patient_data['labs']['HDL']}
    - Triglycerides: {patient_data['labs']['Triglycerides']}
    - Blood Pressure: {patient_data['labs']['Blood Pressure']}
    - eGFR: {patient_data['labs']['eGFR']}
    - BMI: {patient_data['labs']['BMI']}
    - Urine Albumin-to-Creatinine Ratio (UACR): {patient_data['labs']['Urine Albumin-to-Creatinine Ratio (UACR)']}
    Summary: {patient_data['summary']}

    Based on this information, provide a concise bullet-point summary (no more than 3 bullet points) of the key points to discuss and potential treatment adjustments for the upcoming patient visit. Each bullet point should be around 25 words, with an absolute maximum of 50 words. Be as concise as possible.
    """

    if 'follow_up_questions' not in st.session_state:
        st.session_state.follow_up_questions = []

    if 'follow_up_responses' not in st.session_state:
        st.session_state.follow_up_responses = []

    if 'generated_plan' not in st.session_state:
        st.session_state.generated_plan = ""

    if st.button("Generate Patient Visit Plan", key="generate_plan_button"):
        plan = generate_plan(prompt)
        st.session_state.generated_plan = plan

    if st.session_state.generated_plan:
        st.write("Patient Visit Plan:")
        display_plan(st.session_state.generated_plan)

        follow_up_container = st.container()
        with follow_up_container:
            st.write("Follow-up Questions and Responses:")

            question = st.chat_input("Ask a follow-up question:")
            print(f"Follow-up question {len(st.session_state.follow_up_questions) + 1}:", question)

            if question:
                print(f"Question {len(st.session_state.follow_up_questions) + 1} is not empty")
                follow_up_prompt = f"""
                Based on the patient's medical records and the previously generated visit plan:

                {st.session_state.generated_plan}

                The doctor has the following follow-up question:
                {question}

                Please provide a concise response to the doctor's question, keeping it around 25 words if possible.
                """

                follow_up_response = generate_plan(follow_up_prompt)
                print(f"Follow-up response {len(st.session_state.follow_up_questions) + 1}:", follow_up_response)

                st.session_state.follow_up_questions.append(question)
                st.session_state.follow_up_responses.append(follow_up_response)

                st.write(f"Question {len(st.session_state.follow_up_questions)}: {question}")
                st.write(f"Response {len(st.session_state.follow_up_responses)}: {follow_up_response}")
                st.write("---")
            else:
                print(f"Question {len(st.session_state.follow_up_questions) + 1} is empty")

            print("Follow-up questions:", st.session_state.follow_up_questions)
            print("Follow-up responses:", st.session_state.follow_up_responses)

if __name__ == "__main__":
    main()