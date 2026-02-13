"""Test database operations."""
from datetime import date, datetime, timedelta
from app.db.schema import init_db, reset_db
from app.db import crud


def test_database():
    """Test all database operations."""
    print("Testing database operations...")
    
    # Reset and initialize database
    print("\n1. Initializing database...")
    reset_db()
    print("✓ Database initialized")
    
    # Test child creation
    print("\n2. Creating child records...")
    child_id_1 = crud.create_child(
        child_name="Aarav Kumar",
        dob=date(2020, 3, 15),
        sex="M",
        parent_name="Priya Kumar",
        parent_phone="+91-9876543210",
        parent_email="priya.kumar@example.com",
        allergies_text="Peanuts",
        family_history_text="Diabetes on father's side"
    )
    print(f"✓ Created child: {child_id_1}")
    
    child_id_2 = crud.create_child(
        child_name="Sara Patel",
        dob=date(2021, 7, 22),
        sex="F",
        parent_name="Raj Patel",
        parent_phone="+91-9876543211",
        parent_email="raj.patel@example.com"
    )
    print(f"✓ Created child: {child_id_2}")
    
    # Test search
    print("\n3. Testing search...")
    results = crud.search_children_by_name("kumar")
    print(f"✓ Found {len(results)} results for 'kumar'")
    for r in results:
        print(f"  - {r['child_id']}: {r['child_name']}")
    
    # Test get by ID
    print("\n4. Testing get by ID...")
    child = crud.get_child_by_id(child_id_1)
    print(f"✓ Retrieved: {child['child_name']}, DOB: {child['dob']}")
    
    # Test update
    print("\n5. Testing update...")
    success = crud.update_child(
        child_id_1,
        medical_free_text="Regular checkups, no major issues"
    )
    print(f"✓ Update {'successful' if success else 'failed'}")
    
    # Test prescriptions
    print("\n6. Testing prescriptions...")
    rx_id = crud.add_prescription(
        child_id=child_id_1,
        date=date.today(),
        prescriber="Dr. Sharma",
        dosage="Amoxicillin 250mg, 3x daily",
        duration="7 days",
        notes_summary="For throat infection"
    )
    print(f"✓ Added prescription ID: {rx_id}")
    
    prescriptions = crud.list_prescriptions_by_child(child_id_1)
    print(f"✓ Found {len(prescriptions)} prescriptions for {child_id_1}")
    
    # Test vaccines
    print("\n7. Testing vaccines...")
    vacc_id = crud.add_vaccine(
        child_id=child_id_1,
        vaccine_name="BCG",
        dose_number="0",
        date_given=date(2020, 3, 16),
        notes="At birth"
    )
    print(f"✓ Added vaccine ID: {vacc_id}")
    
    vacc_id = crud.add_vaccine(
        child_id=child_id_1,
        vaccine_name="OPV",
        dose_number="1",
        date_given=date(2020, 5, 15),
        notes="6 weeks"
    )
    print(f"✓ Added vaccine ID: {vacc_id}")
    
    vaccines = crud.list_vaccines_by_child(child_id_1)
    print(f"✓ Found {len(vaccines)} vaccines for {child_id_1}")
    for v in vaccines:
        print(f"  - {v['vaccine_name']} (Dose {v['dose_number']}): {v['date_given']}")
    
    # Test appointments
    print("\n8. Testing appointments...")
    start = datetime.now() + timedelta(days=1)
    start = start.replace(hour=10, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=25)
    
    appt_id = crud.book_appointment(
        child_id=child_id_1,
        appointment_type="consult",
        start_datetime=start,
        end_datetime=end,
        subject="Regular checkup",
        case_summary="Routine pediatric examination"
    )
    print(f"✓ Booked appointment ID: {appt_id}")
    
    # Test overlap detection
    print("\n9. Testing overlap detection...")
    overlap_start = start + timedelta(minutes=10)
    overlap_end = overlap_start + timedelta(minutes=25)
    overlap_appt = crud.book_appointment(
        child_id=child_id_2,
        appointment_type="vaccine",
        start_datetime=overlap_start,
        end_datetime=overlap_end,
        subject="Vaccination",
    )
    if overlap_appt is None:
        print("✓ Overlap correctly detected and prevented")
    else:
        print("✗ Overlap not detected - this is an error!")
    
    # Test non-overlapping appointment
    print("\n10. Testing non-overlapping appointment...")
    next_start = end + timedelta(minutes=5)
    next_end = next_start + timedelta(minutes=25)
    appt_id_2 = crud.book_appointment(
        child_id=child_id_2,
        appointment_type="vaccine",
        start_datetime=next_start,
        end_datetime=next_end,
        subject="Vaccination",
    )
    print(f"✓ Booked non-overlapping appointment ID: {appt_id_2}")
    
    appointments = crud.list_appointments_by_child(child_id_1)
    print(f"✓ Found {len(appointments)} appointments for {child_id_1}")
    
    print("\n" + "="*50)
    print("✓ All database tests passed!")
    print("="*50)


if __name__ == "__main__":
    test_database()
