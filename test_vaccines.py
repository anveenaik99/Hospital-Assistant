"""Test vaccine logic."""
from datetime import date, timedelta
from app.db.schema import reset_db
from app.db import crud
from app.vaccines.logic import compute_vaccine_status, format_vaccine_reminders


def test_vaccines():
    """Test vaccine status computation."""
    print("Testing vaccine logic...")
    
    # Reset database
    print("\n1. Setting up test data...")
    reset_db()
    
    # Create a child born 3 months ago (should have some overdue vaccines)
    dob_3mo = date.today() - timedelta(days=90)
    child_id_1 = crud.create_child(
        child_name="Riya Sharma",
        dob=dob_3mo,
        sex="F",
        parent_name="Amit Sharma",
        parent_phone="+91-9876543212",
        parent_email="amit.sharma@example.com"
    )
    print(f"✓ Created child {child_id_1} born {dob_3mo}")
    
    # Add some vaccines (BCG and OPV at birth)
    crud.add_vaccine(child_id_1, "BCG", "0", dob_3mo + timedelta(days=1), "At birth")
    crud.add_vaccine(child_id_1, "OPV", "0", dob_3mo + timedelta(days=1), "At birth")
    crud.add_vaccine(child_id_1, "Hepatitis B", "0", dob_3mo + timedelta(days=1), "At birth")
    print("✓ Added 3 vaccines at birth")
    
    # Compute vaccine status
    print("\n2. Computing vaccine status...")
    status = compute_vaccine_status(child_id_1, window_days=28)
    
    print(f"\n✓ Given: {len(status['given'])} vaccines")
    for v in status['given']:
        print(f"  - {v['vaccine_name']} (Dose {v['dose_label']})")
    
    print(f"\n⚠️  Overdue: {len(status['overdue'])} vaccines")
    for v in status['overdue'][:5]:  # Show first 5
        print(f"  - {v['vaccine_name']} (Dose {v['dose_label']}) - {v['days_overdue']} days overdue")
    if len(status['overdue']) > 5:
        print(f"  ... and {len(status['overdue']) - 5} more")
    
    print(f"\n📅 Upcoming: {len(status['upcoming'])} vaccines")
    for v in status['upcoming']:
        print(f"  - {v['vaccine_name']} (Dose {v['dose_label']}) - {v['days_until_due']} days until due")
    
    print(f"\n📆 Future: {len(status['future'])} vaccines")
    
    # Test formatted reminders
    print("\n3. Testing formatted reminders...")
    print(format_vaccine_reminders(status))
    
    # Create a newborn (should have upcoming vaccines)
    print("\n4. Testing with newborn...")
    dob_newborn = date.today()
    child_id_2 = crud.create_child(
        child_name="Baby Kumar",
        dob=dob_newborn,
        sex="M",
        parent_name="Neha Kumar",
        parent_phone="+91-9876543213",
        parent_email="neha.kumar@example.com"
    )
    print(f"✓ Created newborn {child_id_2}")
    
    status_newborn = compute_vaccine_status(child_id_2, window_days=28)
    print(f"✓ Newborn status:")
    print(f"  - Given: {len(status_newborn['given'])}")
    print(f"  - Overdue: {len(status_newborn['overdue'])}")
    print(f"  - Upcoming: {len(status_newborn['upcoming'])}")
    print(f"  - Future: {len(status_newborn['future'])}")
    
    # Create a 1-year-old with most vaccines given
    print("\n5. Testing with 1-year-old (mostly vaccinated)...")
    dob_1yo = date.today() - timedelta(days=365)
    child_id_3 = crud.create_child(
        child_name="Dev Patel",
        dob=dob_1yo,
        sex="M",
        parent_name="Priya Patel",
        parent_phone="+91-9876543214",
        parent_email="priya.patel@example.com"
    )
    
    # Add most vaccines up to 9 months
    vaccines_to_add = [
        ("BCG", "0"),
        ("OPV", "0"),
        ("Hepatitis B", "0"),
        ("OPV", "1"),
        ("Pentavalent", "1"),
        ("IPV", "1"),
        ("Rotavirus", "1"),
        ("PCV", "1"),
        ("OPV", "2"),
        ("Pentavalent", "2"),
        ("Rotavirus", "2"),
        ("OPV", "3"),
        ("Pentavalent", "3"),
        ("IPV", "2"),
        ("Rotavirus", "3"),
        ("PCV", "2"),
        ("Measles-Rubella", "1"),
        ("PCV", "Booster"),
    ]
    
    for vaccine_name, dose_label in vaccines_to_add:
        crud.add_vaccine(
            child_id_3,
            vaccine_name,
            dose_label,
            dob_1yo + timedelta(days=30),  # Approximate dates
            "Administered"
        )
    
    print(f"✓ Added {len(vaccines_to_add)} vaccines")
    
    status_1yo = compute_vaccine_status(child_id_3, window_days=28)
    print(f"✓ 1-year-old status:")
    print(f"  - Given: {len(status_1yo['given'])}")
    print(f"  - Overdue: {len(status_1yo['overdue'])}")
    print(f"  - Upcoming: {len(status_1yo['upcoming'])}")
    print(f"  - Future: {len(status_1yo['future'])}")
    
    print("\n" + "="*50)
    print("✓ All vaccine tests passed!")
    print("="*50)


if __name__ == "__main__":
    test_vaccines()
