"""Seed the database with realistic sample data."""
from datetime import date, datetime, timedelta
from app.db.schema import init_db
from app.db import crud

def seed_database():
    """Populate database with sample data."""
    
    print("Initializing database...")
    init_db()
    
    print("\n" + "="*80)
    print("SEEDING DATABASE WITH SAMPLE DATA")
    print("="*80)
    
    # Sample Child 1: Aarav Sharma (3 years old, well-vaccinated)
    print("\n1. Creating Child: Aarav Sharma")
    child1_id = crud.create_child(
        child_name="Aarav Sharma",
        dob=date(2023, 3, 15),
        sex="M",
        parent_name="Priya Sharma",
        parent_phone="+91-9876543210",
        parent_email="priya.sharma@email.com"
    )
    print(f"   ✓ Created: {child1_id}")
    
    # Update medical history
    crud.update_child(
        child_id=child1_id,
        allergies_text="Mild peanut allergy",
        family_history_text="Maternal grandmother has diabetes",
        surgeries_text="None",
        medical_free_text="Generally healthy child. Had chickenpox at age 2."
    )
    print("   ✓ Added medical history")
    
    # Add prescriptions
    crud.add_prescription(
        child_id=child1_id,
        date=date(2025, 11, 15),
        prescriber="Dr. Rajesh Kumar",
        dosage="Paracetamol syrup 5ml, 3 times daily",
        duration="3 days",
        notes_summary="For fever associated with viral infection"
    )
    print("   ✓ Added prescription")
    
    # Add vaccines (well-vaccinated)
    vaccines_aarav = [
        ("BCG", "0", date(2023, 3, 16)),
        ("OPV", "0", date(2023, 3, 16)),
        ("Hepatitis B", "0", date(2023, 3, 16)),
        ("OPV", "1", date(2023, 4, 26)),
        ("Pentavalent", "1", date(2023, 4, 26)),
        ("IPV", "1", date(2023, 4, 26)),
        ("Rotavirus", "1", date(2023, 4, 26)),
        ("PCV", "1", date(2023, 4, 26)),
        ("OPV", "2", date(2023, 5, 24)),
        ("Pentavalent", "2", date(2023, 5, 24)),
        ("Rotavirus", "2", date(2023, 5, 24)),
        ("OPV", "3", date(2023, 6, 21)),
        ("Pentavalent", "3", date(2023, 6, 21)),
        ("IPV", "2", date(2023, 6, 21)),
        ("Rotavirus", "3", date(2023, 6, 21)),
        ("PCV", "2", date(2023, 6, 21)),
        ("Measles-Rubella", "1", date(2024, 3, 18)),
        ("PCV", "Booster", date(2024, 3, 18)),
        ("JE", "1", date(2024, 3, 18)),
    ]
    for vaccine_name, dose, date_given in vaccines_aarav:
        crud.add_vaccine(child1_id, vaccine_name, dose, date_given, "")
    print(f"   ✓ Added {len(vaccines_aarav)} vaccines")
    
    # Sample Child 2: Ananya Patel (6 months old, some vaccines pending)
    print("\n2. Creating Child: Ananya Patel")
    child2_id = crud.create_child(
        child_name="Ananya Patel",
        dob=date(2025, 7, 20),
        sex="F",
        parent_name="Amit Patel",
        parent_phone="+91-9123456789",
        parent_email="amit.patel@email.com"
    )
    print(f"   ✓ Created: {child2_id}")
    
    crud.update_child(
        child_id=child2_id,
        allergies_text="None known",
        family_history_text="No significant family history",
        surgeries_text="None",
        medical_free_text="Healthy infant. Birth weight 3.2 kg. Normal development."
    )
    print("   ✓ Added medical history")
    
    # Add some vaccines
    vaccines_ananya = [
        ("BCG", "0", date(2025, 7, 21)),
        ("OPV", "0", date(2025, 7, 21)),
        ("Hepatitis B", "0", date(2025, 7, 21)),
        ("OPV", "1", date(2025, 8, 31)),
        ("Pentavalent", "1", date(2025, 8, 31)),
        ("IPV", "1", date(2025, 8, 31)),
        ("Rotavirus", "1", date(2025, 8, 31)),
        ("PCV", "1", date(2025, 8, 31)),
    ]
    for vaccine_name, dose, date_given in vaccines_ananya:
        crud.add_vaccine(child2_id, vaccine_name, dose, date_given, "")
    print(f"   ✓ Added {len(vaccines_ananya)} vaccines")
    
    # Sample Child 3: Rohan Verma (18 months, missed several vaccines)
    print("\n3. Creating Child: Rohan Verma")
    child3_id = crud.create_child(
        child_name="Rohan Verma",
        dob=date(2024, 7, 10),
        sex="M",
        parent_name="Kavita Verma",
        parent_phone="+91-9988776655",
        parent_email="kavita.verma@email.com"
    )
    print(f"   ✓ Created: {child3_id}")
    
    crud.update_child(
        child_id=child3_id,
        allergies_text="None known",
        family_history_text="Father has asthma",
        surgeries_text="None",
        medical_free_text="Active and playful. Had a mild ear infection at 10 months."
    )
    print("   ✓ Added medical history")
    
    crud.add_prescription(
        child_id=child3_id,
        date=date(2025, 5, 15),
        prescriber="Dr. Meera Singh",
        dosage="Amoxicillin suspension 5ml, twice daily",
        duration="7 days",
        notes_summary="For ear infection"
    )
    print("   ✓ Added prescription")
    
    # Partially vaccinated
    vaccines_rohan = [
        ("BCG", "0", date(2024, 7, 11)),
        ("OPV", "0", date(2024, 7, 11)),
        ("Hepatitis B", "0", date(2024, 7, 11)),
        ("OPV", "1", date(2024, 8, 21)),
        ("Pentavalent", "1", date(2024, 8, 21)),
        ("IPV", "1", date(2024, 8, 21)),
        ("PCV", "1", date(2024, 8, 21)),
        # Missing several doses intentionally
    ]
    for vaccine_name, dose, date_given in vaccines_rohan:
        crud.add_vaccine(child3_id, vaccine_name, dose, date_given, "")
    print(f"   ✓ Added {len(vaccines_rohan)} vaccines (several overdue)")
    
    # Sample Child 4: Diya Singh (Newborn, just birth vaccines)
    print("\n4. Creating Child: Diya Singh")
    child4_id = crud.create_child(
        child_name="Diya Singh",
        dob=date(2026, 1, 15),
        sex="F",
        parent_name="Rahul Singh",
        parent_phone="+91-9876501234",
        parent_email="rahul.singh@email.com"
    )
    print(f"   ✓ Created: {child4_id}")
    
    crud.update_child(
        child_id=child4_id,
        allergies_text="None known (newborn)",
        family_history_text="No significant family history",
        surgeries_text="None",
        medical_free_text="Healthy newborn. Birth weight 3.5 kg. Normal delivery."
    )
    print("   ✓ Added medical history")
    
    # Birth vaccines only
    vaccines_diya = [
        ("BCG", "0", date(2026, 1, 16)),
        ("OPV", "0", date(2026, 1, 16)),
        ("Hepatitis B", "0", date(2026, 1, 16)),
    ]
    for vaccine_name, dose, date_given in vaccines_diya:
        crud.add_vaccine(child4_id, vaccine_name, dose, date_given, "")
    print(f"   ✓ Added {len(vaccines_diya)} vaccines")
    
    # Sample Child 5: Harsh Kumar (10 months, no vaccines - for testing)
    print("\n5. Creating Child: Harsh Kumar")
    child5_id = crud.create_child(
        child_name="Harsh Kumar",
        dob=date(2025, 3, 20),
        sex="M",
        parent_name="Neha Kumar",
        parent_phone="+91-9123450987",
        parent_email="neha.kumar@email.com"
    )
    print(f"   ✓ Created: {child5_id}")
    
    crud.update_child(
        child_id=child5_id,
        allergies_text="None known",
        family_history_text="No significant family history",
        surgeries_text="None",
        medical_free_text="Moved from another city recently. Previous vaccination records pending."
    )
    print("   ✓ Added medical history")
    print("   ✓ No vaccines added (for testing overdue scenarios)")
    
    # Add some appointments
    print("\n6. Adding Sample Appointments")
    
    # Future appointment for Aarav
    appt1 = crud.book_appointment(
        child_id=child1_id,
        appointment_type="consult",
        start_datetime=datetime(2026, 2, 5, 10, 0),
        end_datetime=datetime(2026, 2, 5, 10, 25),
        subject="Routine checkup",
        case_summary="Regular 6-month checkup"
    )
    print(f"   ✓ Appointment {appt1} booked for {child1_id}")
    
    # Future appointment for Ananya
    appt2 = crud.book_appointment(
        child_id=child2_id,
        appointment_type="vaccine",
        start_datetime=datetime(2026, 2, 8, 11, 0),
        end_datetime=datetime(2026, 2, 8, 11, 25),
        subject="OPV Dose 2",
        case_summary="Second dose of OPV vaccine due"
    )
    print(f"   ✓ Appointment {appt2} booked for {child2_id}")
    
    print("\n" + "="*80)
    print("DATABASE SEEDING COMPLETE!")
    print("="*80)
    print("\nSample Data Summary:")
    print(f"1. {child1_id} - Aarav Sharma (3y, M) - Well vaccinated, 1 prescription")
    print(f"2. {child2_id} - Ananya Patel (6m, F) - Partially vaccinated")
    print(f"3. {child3_id} - Rohan Verma (18m, M) - Missing vaccines, 1 prescription")
    print(f"4. {child4_id} - Diya Singh (newborn, F) - Birth vaccines only")
    print(f"5. {child5_id} - Harsh Kumar (10m, M) - No vaccines (testing)")
    print("\nYou can now test the system with these realistic child records!")
    print("="*80 + "\n")

if __name__ == "__main__":
    seed_database()
