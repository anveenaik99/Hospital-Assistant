"""Practitioner Admin page for managing child records."""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import date, datetime

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.db import crud
from app.vaccines.uip_schedule import get_vaccine_names, get_dose_labels_for_vaccine

st.set_page_config(page_title="Practitioner Admin", page_icon="👨‍⚕️", layout="wide")

st.title("👨‍⚕️ Practitioner Admin")
st.markdown("Manage child records, medical history, prescriptions, and vaccines")
st.markdown("---")

# Initialize session state
if 'selected_child_id' not in st.session_state:
    st.session_state.selected_child_id = None

# Search section
st.subheader("🔍 Search Children")
col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input("Search by child name", placeholder="Enter name or partial name...")
with col2:
    st.write("")  # Spacing
    search_button = st.button("Search", type="primary")

if search_button and search_query:
    results = crud.search_children_by_name(search_query)
    
    if results:
        st.success(f"Found {len(results)} result(s)")
        
        # Display results in a table
        df = pd.DataFrame(results)
        df['dob'] = pd.to_datetime(df['dob']).dt.strftime('%Y-%m-%d')
        
        # Store results in session state for button handling
        st.session_state.search_results = results
        
        # Add select buttons
        for idx, row in df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
            with col1:
                st.write(f"**{row['child_id']}**")
            with col2:
                st.write(row['child_name'])
            with col3:
                st.write(f"DOB: {row['dob']}")
            with col4:
                st.write(row['parent_name'])
            with col5:
                if st.button("Select", key=f"select_{row['child_id']}", type="primary"):
                    st.session_state.selected_child_id = row['child_id']
                    st.rerun()
    else:
        st.warning("No children found matching your search")
elif 'search_results' in st.session_state and st.session_state.search_results:
    # Show previous search results if they exist
    results = st.session_state.search_results
    st.info(f"Showing {len(results)} previous result(s)")
    
    df = pd.DataFrame(results)
    df['dob'] = pd.to_datetime(df['dob']).dt.strftime('%Y-%m-%d')
    
    for idx, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        with col1:
            st.write(f"**{row['child_id']}**")
        with col2:
            st.write(row['child_name'])
        with col3:
            st.write(f"DOB: {row['dob']}")
        with col4:
            st.write(row['parent_name'])
        with col5:
            if st.button("Select", key=f"select_prev_{row['child_id']}", type="primary"):
                st.session_state.selected_child_id = row['child_id']
                st.rerun()

# Create new child section
st.markdown("---")
st.subheader("➕ Create New Child Record")
with st.expander("Create New Child"):
    with st.form("create_child_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Child Name*", placeholder="Full name")
            new_dob = st.date_input("Date of Birth*", max_value=date.today())
            new_sex = st.selectbox("Sex*", ["M", "F", "Other", "Unknown"])
        
        with col2:
            new_parent_name = st.text_input("Parent/Guardian Name*", placeholder="Full name")
            new_parent_phone = st.text_input("Parent Phone*", placeholder="+91-XXXXXXXXXX")
            new_parent_email = st.text_input("Parent Email*", placeholder="email@example.com")
        
        submitted = st.form_submit_button("Create Child Record", type="primary")
        
        if submitted:
            if all([new_name, new_dob, new_sex, new_parent_name, new_parent_phone, new_parent_email]):
                child_id = crud.create_child(
                    child_name=new_name,
                    dob=new_dob,
                    sex=new_sex,
                    parent_name=new_parent_name,
                    parent_phone=new_parent_phone,
                    parent_email=new_parent_email
                )
                st.success(f"✓ Created child record: {child_id}")
                st.session_state.selected_child_id = child_id
                st.rerun()
            else:
                st.error("Please fill in all required fields")

# Selected child management
if st.session_state.selected_child_id:
    st.markdown("---")
    child = crud.get_child_by_id(st.session_state.selected_child_id)
    
    if child:
        st.subheader(f"📋 Managing: {child['child_name']} ({child['child_id']})")
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Demographics", "Medical History", "Prescriptions", "Vaccines", "Appointments"
        ])
        
        # Tab 1: Demographics
        with tab1:
            with st.form("demographics_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Child Name", value=child['child_name'])
                    dob = st.date_input("Date of Birth", value=date.fromisoformat(child['dob']))
                    sex = st.selectbox("Sex", ["M", "F", "Other", "Unknown"], 
                                      index=["M", "F", "Other", "Unknown"].index(child['sex']))
                
                with col2:
                    parent_name = st.text_input("Parent/Guardian Name", value=child['parent_name'])
                    parent_phone = st.text_input("Parent Phone", value=child['parent_phone'])
                    parent_email = st.text_input("Parent Email", value=child['parent_email'])
                
                if st.form_submit_button("Update Demographics"):
                    success = crud.update_child(
                        child_id=child['child_id'],
                        child_name=name,
                        dob=dob,
                        sex=sex,
                        parent_name=parent_name,
                        parent_phone=parent_phone,
                        parent_email=parent_email
                    )
                    if success:
                        st.success("✓ Demographics updated")
                        st.rerun()
        
        # Tab 2: Medical History
        with tab2:
            with st.form("medical_history_form"):
                allergies = st.text_area("Allergies", value=child.get('allergies_text', ''),
                                        placeholder="List any known allergies")
                family_history = st.text_area("Family History", value=child.get('family_history_text', ''),
                                             placeholder="Relevant family medical history")
                surgeries = st.text_area("Surgeries/Procedures", value=child.get('surgeries_text', ''),
                                        placeholder="Past surgeries or procedures")
                medical_notes = st.text_area("Other Medical Notes", value=child.get('medical_free_text', ''),
                                            placeholder="Any other relevant medical information")
                
                if st.form_submit_button("Update Medical History"):
                    success = crud.update_child(
                        child_id=child['child_id'],
                        allergies_text=allergies,
                        family_history_text=family_history,
                        surgeries_text=surgeries,
                        medical_free_text=medical_notes
                    )
                    if success:
                        st.success("✓ Medical history updated")
                        st.rerun()
        
        # Tab 3: Prescriptions
        with tab3:
            st.markdown("### Current Prescriptions")
            prescriptions = crud.list_prescriptions_by_child(child['child_id'])
            
            if prescriptions:
                for rx in prescriptions:
                    with st.expander(f"📅 {rx['date']} - {rx['prescriber']}"):
                        st.write(f"**Dosage:** {rx['dosage']}")
                        if rx['duration']:
                            st.write(f"**Duration:** {rx['duration']}")
                        if rx['notes_summary']:
                            st.write(f"**Notes:** {rx['notes_summary']}")
            else:
                st.info("No prescriptions recorded")
            
            st.markdown("### ➕ Add New Prescription")
            with st.form("add_prescription_form"):
                col1, col2 = st.columns(2)
                with col1:
                    rx_date = st.date_input("Date", value=date.today())
                    rx_prescriber = st.text_input("Prescriber", placeholder="Dr. Name")
                with col2:
                    rx_duration = st.text_input("Duration", placeholder="e.g., 7 days")
                
                rx_dosage = st.text_area("Dosage/Medications*", 
                                        placeholder="e.g., Amoxicillin 250mg, 3x daily")
                rx_notes = st.text_area("Notes", placeholder="Additional notes or summary")
                
                if st.form_submit_button("Add Prescription"):
                    if rx_dosage and rx_prescriber:
                        crud.add_prescription(
                            child_id=child['child_id'],
                            date=rx_date,
                            prescriber=rx_prescriber,
                            dosage=rx_dosage,
                            duration=rx_duration,
                            notes_summary=rx_notes
                        )
                        st.success("✓ Prescription added")
                        st.rerun()
                    else:
                        st.error("Please fill in prescriber and dosage")
        
        # Tab 4: Vaccines
        with tab4:
            st.markdown("### Vaccine History")
            vaccines = crud.list_vaccines_by_child(child['child_id'])
            
            if vaccines:
                df_vaccines = pd.DataFrame(vaccines)
                df_vaccines = df_vaccines[['vaccine_name', 'dose_number', 'date_given', 'notes']]
                st.dataframe(df_vaccines, use_container_width=True)
            else:
                st.info("No vaccines recorded")
            
            st.markdown("### ➕ Add Vaccine Record")
            with st.form("add_vaccine_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    vaccine_name = st.selectbox("Vaccine*", get_vaccine_names())
                    dose_number = st.selectbox("Dose Number*", 
                                              get_dose_labels_for_vaccine(vaccine_name) if vaccine_name else ["0"])
                
                with col2:
                    date_given = st.date_input("Date Given*", value=date.today())
                
                vaccine_notes = st.text_input("Notes", placeholder="Optional notes")
                
                if st.form_submit_button("Add Vaccine Record"):
                    crud.add_vaccine(
                        child_id=child['child_id'],
                        vaccine_name=vaccine_name,
                        dose_number=dose_number,
                        date_given=date_given,
                        notes=vaccine_notes
                    )
                    st.success("✓ Vaccine record added")
                    st.rerun()
        
        # Tab 5: Appointments
        with tab5:
            st.markdown("### Scheduled Appointments")
            appointments = crud.list_appointments_by_child(child['child_id'])
            
            if appointments:
                for appt in appointments:
                    start = datetime.fromisoformat(appt['start_datetime'])
                    with st.expander(f"📅 {start.strftime('%Y-%m-%d %H:%M')} - {appt['subject']}"):
                        st.write(f"**Type:** {appt['appointment_type']}")
                        st.write(f"**Status:** {appt['status']}")
                        if appt['case_summary']:
                            st.write(f"**Summary:** {appt['case_summary']}")
            else:
                st.info("No appointments scheduled")
        
        # Clear selection button
        if st.button("← Clear Selection"):
            st.session_state.selected_child_id = None
            st.rerun()
    else:
        st.error("Child record not found")
        st.session_state.selected_child_id = None
