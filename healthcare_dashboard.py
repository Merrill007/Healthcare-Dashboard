
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set a modern color palette
colors = sns.color_palette("viridis", 10).as_hex()
plt.style.use('seaborn-v0_8-whitegrid')

# Load the dataset
df = pd.read_excel('Healthcare Analysis Dataset.xlsx')

# Calculate Length of Stay if not already present
if 'Length of Stay' not in df.columns:
    df['Length of Stay'] = (df['Discharge Date'] - df['Date of Admission']).dt.days

st.set_page_config(layout="wide")

st.title("Healthcare Analysis Dashboard")

# Add Filters
st.sidebar.header("Filter Options")
selected_gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), df['Gender'].unique())
selected_blood_type = st.sidebar.multiselect("Select Blood Type", df['Blood Type'].unique(), df['Blood Type'].unique())
selected_medical_condition = st.sidebar.multiselect("Select Medical Condition", df['Medical Condition'].unique(), df['Medical Condition'].unique())
selected_hospital = st.sidebar.multiselect("Select Hospital", df['Hospital'].unique(), df['Hospital'].unique())
selected_insurance = st.sidebar.multiselect("Select Insurance Provider", df['Insurance Provider'].unique(), df['Insurance Provider'].unique())
selected_admission_type = st.sidebar.multiselect("Select Admission Type", df['Admission Type'].unique(), df['Admission Type'].unique())

# Apply filters
filtered_df = df[
    df['Gender'].isin(selected_gender) &
    df['Blood Type'].isin(selected_blood_type) &
    df['Medical Condition'].isin(selected_medical_condition) &
    df['Hospital'].isin(selected_hospital) &
    df['Insurance Provider'].isin(selected_insurance) &
    df['Admission Type'].isin(selected_admission_type)
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    # --- KPIs ---
    st.header("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    total_patients = filtered_df['Patient ID'].nunique()
    col1.metric("Total Patients", total_patients)

    average_stay = filtered_df['Length of Stay'].mean()
    col2.metric("Average Length of Stay", f"{average_stay:.2f} days")

    average_billing = filtered_df['Billing Amount'].mean()
    col3.metric("Average Billing Amount", f"${average_billing:.2f}")

    most_common_condition = filtered_df['Medical Condition'].mode()[0]
    col4.metric("Most Common Condition", most_common_condition)


    # --- Charts ---
    st.header("Data Visualizations")

    # Layout for charts (simulating Power BI arrangement)
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    row3_col1, row3_col2 = st.columns(2)
    row4_col1, row4_col2 = st.columns(2)
    row5_col1, row5_col2 = st.columns(2)


    # 1. Patient Demographics
    with row1_col1:
        st.subheader("Gender Distribution")
        gender_counts = filtered_df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        fig = px.bar(gender_counts, x='Gender', y='Count', title='Gender Distribution', color='Gender', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Number of Patients')
        fig.update_traces(text=gender_counts['Count'], textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with row1_col2:
        st.subheader("Blood Type Distribution")
        blood_type_counts = filtered_df['Blood Type'].value_counts().reset_index()
        blood_type_counts.columns = ['Blood Type', 'Count']
        fig = px.bar(blood_type_counts, x='Blood Type', y='Count', title='Blood Type Distribution', color='Blood Type', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Number of Patients')
        fig.update_traces(text=blood_type_counts['Count'], textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # 2. Medical Conditions
    with row2_col1:
        st.subheader("Most Common Medical Conditions")
        condition_counts = filtered_df['Medical Condition'].value_counts().reset_index()
        condition_counts.columns = ['Medical Condition', 'Count']
        fig = px.bar(condition_counts, x='Medical Condition', y='Count', title='Most Common Medical Conditions', color='Medical Condition', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Number of Patients', xaxis={'categoryorder':'total descending'})
        fig.update_traces(text=condition_counts['Count'], textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with row2_col2:
        st.subheader("Medical Condition by Gender")
        medical_condition_gender = filtered_df.groupby(['Medical Condition', 'Gender']).size().reset_index(name='Count')
        fig = px.bar(medical_condition_gender, x='Medical Condition', y='Count', color='Gender', title='Medical Condition by Gender', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Number of Patients', barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

    # 3. Length of Hospital Stay
    with row3_col1:
        st.subheader("Average Length of Stay by Medical Condition")
        average_stay_by_condition = filtered_df.groupby('Medical Condition')['Length of Stay'].mean().reset_index()
        average_stay_by_condition.columns = ['Medical Condition', 'Average Stay']
        fig = px.bar(average_stay_by_condition, x='Medical Condition', y='Average Stay', title='Average Length of Stay by Medical Condition', color='Medical Condition', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Average Days', xaxis={'categoryorder':'total descending'})
        fig.update_traces(text=average_stay_by_condition['Average Stay'].round(2), textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with row3_col2:
        st.subheader("Average Length of Stay by Admission Type")
        average_stay_by_admission_type = filtered_df.groupby('Admission Type')['Length of Stay'].mean().reset_index()
        average_stay_by_admission_type.columns = ['Admission Type', 'Average Stay']
        fig = px.bar(average_stay_by_admission_type, x='Admission Type', y='Average Stay', title='Average Length of Stay by Admission Type', color='Admission Type', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Average Days', xaxis={'categoryorder':'total descending'})
        fig.update_traces(text=average_stay_by_admission_type['Average Stay'].round(2), textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # 4. Treatment Costs
    with row4_col1:
        st.subheader("Average Billing Amount by Medical Condition")
        average_billing_by_condition = filtered_df.groupby('Medical Condition')['Billing Amount'].mean().reset_index()
        average_billing_by_condition.columns = ['Medical Condition', 'Average Billing']
        fig = px.bar(average_billing_by_condition, x='Medical Condition', y='Average Billing', title='Average Billing Amount by Medical Condition', color='Medical Condition', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Average Billing Amount ($)', xaxis={'categoryorder':'total descending'})
        fig.update_traces(text=average_billing_by_condition['Average Billing'].round(2), textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with row4_col2:
        st.subheader("Average Billing Amount by Insurance Provider")
        average_billing_by_insurance = filtered_df.groupby('Insurance Provider')['Billing Amount'].mean().reset_index()
        average_billing_by_insurance.columns = ['Insurance Provider', 'Average Billing']
        fig = px.bar(average_billing_by_insurance, x='Insurance Provider', y='Average Billing', title='Average Billing Amount by Insurance Provider', color='Insurance Provider', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Average Billing Amount ($)', xaxis={'categoryorder':'total descending'})
        fig.update_traces(text=average_billing_by_insurance['Average Billing'].round(2), textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # 5. Hospital Performance
    with row5_col1:
        st.subheader("Number of Patients Treated by Each Hospital")
        patients_by_hospital = filtered_df['Hospital'].value_counts().reset_index()
        patients_by_hospital.columns = ['Hospital', 'Count']
        fig = px.bar(patients_by_hospital, x='Hospital', y='Count', title='Number of Patients Treated by Each Hospital', color='Hospital', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Number of Patients', xaxis={'categoryorder':'total descending'})
        fig.update_traces(text=patients_by_hospital['Count'], textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with row5_col2:
        st.subheader("Test Results Distribution by Hospital")
        hospital_test_results = filtered_df.groupby(['Hospital', 'Test Results']).size().reset_index(name='Count')
        fig = px.bar(hospital_test_results, x='Hospital', y='Count', color='Test Results', title='Test Results Distribution by Hospital', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Number of Patients', barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

    # 6. Medication Usage (Additional rows can be added for more charts)
    st.header("Medication Usage")
    col6_1, col6_2 = st.columns(2)

    with col6_1:
        st.subheader("Medication Prescribed by Medical Condition")
        medication_by_condition = filtered_df.groupby(['Medical Condition', 'Medication']).size().reset_index(name='Count')
        fig = px.bar(medication_by_condition, x='Medical Condition', y='Count', color='Medication', title='Medication Prescribed by Medical Condition', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Number of Prescriptions', barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

    with col6_2:
        st.subheader("Medication Prescribed by Hospital")
        medication_by_hospital = filtered_df.groupby(['Hospital', 'Medication']).size().reset_index(name='Count')
        fig = px.bar(medication_by_hospital, x='Hospital', y='Count', color='Medication', title='Medication Prescribed by Hospital', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='', yaxis_title='Number of Prescriptions', barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

    # 9. Hospital Location and Regional Analysis (Using Plotly for interactive map)
    st.header("Hospital Location and Regional Analysis")

    st.subheader("Hospital Locations and Average Billing Amount")
    average_billing_by_location = filtered_df.groupby(['Hospital Latitude', 'Hospital Longitude', 'Hospital'])['Billing Amount'].mean().reset_index()
    fig = px.scatter_mapbox(average_billing_by_location,
                            lat="Hospital Latitude",
                            lon="Hospital Longitude",
                            size="Billing Amount",
                            color="Billing Amount",
                            hover_name="Hospital",
                            size_max=15,
                            zoom=3,
                            height=500,
                            title="Average Billing Amount by Hospital Location",
                            color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Hospital Locations and Average Length of Stay")
    average_stay_by_location = filtered_df.groupby(['Hospital Latitude', 'Hospital Longitude', 'Hospital'])['Length of Stay'].mean().reset_index()
    fig = px.scatter_mapbox(average_stay_by_location,
                            lat="Hospital Latitude",
                            lon="Hospital Longitude",
                            size="Length of Stay",
                            color="Length of Stay",
                            hover_name="Hospital",
                            size_max=15,
                            zoom=3,
                            height=500,
                            title="Average Length of Stay by Hospital Location",
                            color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)
