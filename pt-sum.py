import os
import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define patient data
patient_data = {
    "name": "Pamela Rogers",
    "age": 56,
    "gender": "Female",
    "summary": "Ms. Rogers is a 56 y/o WF who has been having chest pains for the last week. She was in her usual state of good health until one week prior to admission when she noticed the abrupt onset of chest pain, which she describes as dull and aching in character. The pain began in the left para-sternal area and radiated up to her neck. She has had 3 episodes of pain since the initial onset, with the most recent episode lasting 30 minutes and prompting her visit to the Emergency Department.",
    "conditions": [
        "Chest pain with features of angina pectoris",
        "Dyspnea",
        "Recent onset hypertension",
        "Abdominal bruit",
        "Systolic murmur",
        "Epigastric discomfort",
        "History of peptic ulcer disease",
        "Lumbo-sacral back pain",
        "Fibrocystic breast disease",
        "Penicillin allergy"
    ],
    "labs": {
        "Blood Pressure": "168/98",
        "Pulse": "90",
        "Respirations": "20",
        "Temperature": "37 degrees"
    },
    "specialist_visit": {
        "specialty": "Cardiology",
        "facility": "Emergency Department",
        "date": "6/2/04",
        "summary": "Patient referred for evaluation of cardiovascular risk factors and potential complications related to her existing conditions. ECG and cardiac enzymes should be obtained to rule out myocardial infarction. Cardiac catheterization may be necessary to assess coronary artery disease.",
        "cardiac_summary": "Chest pain with features of angina pectoris, dyspnea, and risk factors for coronary artery disease. Further evaluation and management required."
    },
    "patient_input": "The patient describes the onset of chest pain one week ago while working in her garden. She has had 2 additional episodes of pain since then, with the most recent episode lasting 30 minutes and prompting her visit to the Emergency Department. She becomes short of breath during these episodes but describes no other associated symptoms.",
    "prescriptions": [
        "Lisinopril 10 mg orally once daily: Initiated for hypertension management. Lisinopril, as an angiotensin-converting enzyme (ACE) inhibitor, is prescribed to reduce systemic vascular resistance via vasodilation, with the therapeutic goal of lowering blood pressure to target levels, thus reducing the risk of hypertensive cardiovascular complications.",
        "Metoprolol succinate 50 mg extended-release orally once daily: Indicated for angina pectoris and blood pressure control. This selective beta1-adrenergic receptor blocker is intended to decrease myocardial oxygen demand by lowering heart rate and contractility, thereby providing symptomatic relief from anginal episodes and contributing to the long-term management of ischemic heart disease.",
        "Atorvastatin 20 mg orally once daily at bedtime: Prescribed for dyslipidemia with a family history of premature coronary artery disease (CAD). This HMG-CoA reductase inhibitor is aimed at reducing hepatic cholesterol synthesis, leading to an increase in the clearance of low-density lipoprotein (LDL) and a resultant decrease in plasma cholesterol levels. The goal is the primary prevention of atherosclerotic cardiovascular disease by mitigating hypercholesterolemia."
    ]
}

def generate_doctor_name():
    prompt = "Generate a random doctor name."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()

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

    st.header("Patient Data")
    st.write(f"Name: {patient_data['name']}")
    st.write(f"Age: {patient_data['age']}")
    st.write(f"Gender: {patient_data['gender']}")
    st.write(f"Summary: {patient_data['summary']}")

    conditions_expander = st.expander("Conditions")
    with conditions_expander:
        conditions_list = '\n'.join([f"- {condition}" for condition in patient_data['conditions']])
        st.write(conditions_list)

    labs_expander = st.expander("Labs")
    with labs_expander:
        labs_list = '\n'.join([f"- {lab}: {value}" for lab, value in patient_data['labs'].items()])
        st.write(labs_list)

    prescriptions_expander = st.expander("Prescriptions")
    with prescriptions_expander:
        prescriptions_list = '\n'.join([f"- {prescription}" for prescription in patient_data['prescriptions']])
        st.write(prescriptions_list)

    doctor_name = generate_doctor_name()
    specialist_visit_title = f"{patient_data['specialist_visit']['specialty']} Visit at {patient_data['specialist_visit']['facility']}"
    specialist_expander = st.expander(specialist_visit_title)
    with specialist_expander:
        specialist_visit_list = f"Date: {patient_data['specialist_visit']['date']}\nSummary: {patient_data['specialist_visit']['summary']}\nCardiac Summary: {patient_data['specialist_visit']['cardiac_summary']}"
        st.write(specialist_visit_list)

    patient_input_expander = st.expander("Patient Input")
    with patient_input_expander:
        st.write(patient_data['patient_input'])

    st.divider()

    prompt = f"""
    You are a physician preparing for a patient visit. The patient has the following medical records:

    Name: {patient_data['name']}
    Age: {patient_data['age']}
    Gender: {patient_data['gender']}
    Summary: {patient_data['summary']}
    Conditions: {', '.join(patient_data['conditions'])}
    Labs:
    - Blood Pressure: {patient_data['labs']['Blood Pressure']}
    - Pulse: {patient_data['labs']['Pulse']}
    - Respirations: {patient_data['labs']['Respirations']}
    - Temperature: {patient_data['labs']['Temperature']}
    
    Specialist Visit:
    - Specialty: {patient_data['specialist_visit']['specialty']}
    - Facility: {patient_data['specialist_visit']['facility']}
    - Date: {patient_data['specialist_visit']['date']}
    - Summary: {patient_data['specialist_visit']['summary']}
    - Cardiac Summary: {patient_data['specialist_visit']['cardiac_summary']}
    
    Prescriptions:
    {chr(10).join([f"- {prescription}" for prescription in patient_data['prescriptions']])}

    Patient Input: {patient_data['patient_input']}

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
        st.header("Patient Visit Plan")
        display_plan(st.session_state.generated_plan)

        follow_up_container = st.container()
        with follow_up_container:
            st.subheader("Follow-up Questions and Responses")

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