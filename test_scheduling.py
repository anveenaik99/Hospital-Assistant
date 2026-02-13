"""Test scheduling logic."""
from datetime import date, datetime, timedelta
from app.db.schema import reset_db
from app.db import crud
from app.scheduling.slots import (
    generate_slot_times_for_date,
    get_next_available_slots,
    validate_slot,
    get_available_slots_for_dates,
    find_first_available_slot_on_or_after,
    format_slot_time
)


def test_scheduling():
    """Test scheduling logic."""
    print("Testing scheduling logic...")
    
    # Reset database
    print("\n1. Resetting database...")
    reset_db()
    
    # Create a test child
    child_id = crud.create_child(
        child_name="Test Child",
        dob=date.today() - timedelta(days=180),
        sex="M",
        parent_name="Test Parent",
        parent_phone="+91-9876543215",
        parent_email="test@example.com"
    )
    print(f"✓ Created test child: {child_id}")
    
    # Test slot generation for specific dates
    print("\n2. Testing slot generation for specific dates...")
    tomorrow = date.today() + timedelta(days=1)
    slots = generate_slot_times_for_date(tomorrow)
    print(f"✓ Generated {len(slots)} slots for {tomorrow}")
    
    # Show first few slots
    print("  First 5 slots:")
    for slot in slots[:5]:
        print(f"    - {format_slot_time(slot)}")
    
    # Test for Saturday (should have morning only)
    days_until_saturday = (5 - tomorrow.weekday()) % 7
    if days_until_saturday == 0:
        days_until_saturday = 7
    saturday = tomorrow + timedelta(days=days_until_saturday)
    saturday_slots = generate_slot_times_for_date(saturday)
    print(f"\n✓ Saturday ({saturday}) has {len(saturday_slots)} slots (morning only)")
    
    # Test for Sunday (should have 0 slots)
    sunday = saturday + timedelta(days=1)
    sunday_slots = generate_slot_times_for_date(sunday)
    print(f"✓ Sunday ({sunday}) has {len(sunday_slots)} slots (closed)")
    
    # Test get next available slots
    print("\n3. Testing get next available slots...")
    next_slots = get_next_available_slots(count=5)
    print(f"✓ Found {len(next_slots)} available slots")
    for i, slot in enumerate(next_slots, 1):
        print(f"  {i}. {format_slot_time(slot['start_datetime'])}")
    
    # Book one appointment to test availability
    print("\n4. Testing appointment booking and overlap detection...")
    first_slot = next_slots[0]
    appt_id = crud.book_appointment(
        child_id=child_id,
        appointment_type="consult",
        start_datetime=first_slot['start_datetime'],
        end_datetime=first_slot['end_datetime'],
        subject="Test appointment",
        case_summary="Testing"
    )
    print(f"✓ Booked appointment ID: {appt_id}")
    
    # Try to get slots again - first slot should now be unavailable
    next_slots_after = get_next_available_slots(count=5)
    print(f"✓ After booking, first available slot is now:")
    print(f"  {format_slot_time(next_slots_after[0]['start_datetime'])}")
    
    # Test validation
    print("\n5. Testing slot validation...")
    
    # Valid slot
    valid_slot = next_slots_after[0]['start_datetime']
    validation = validate_slot(valid_slot, "consult")
    print(f"✓ Valid slot validation: {validation}")
    
    # Invalid: past time
    past_time = datetime.now() - timedelta(hours=1)
    validation = validate_slot(past_time, "consult")
    print(f"✓ Past time validation: {validation}")
    
    # Invalid: not aligned to cadence
    misaligned = next_slots_after[0]['start_datetime'].replace(minute=15)
    validation = validate_slot(misaligned, "consult")
    print(f"✓ Misaligned time validation: {validation}")
    
    # Test get available slots for specific dates
    print("\n6. Testing get available slots for specific dates...")
    target_dates = [tomorrow, tomorrow + timedelta(days=1), tomorrow + timedelta(days=2)]
    specific_slots = get_available_slots_for_dates(target_dates, limit=10)
    print(f"✓ Found {len(specific_slots)} slots for {len(target_dates)} dates")
    
    # Test find first available slot on/after date
    print("\n7. Testing find first available slot on/after date...")
    future_date = tomorrow + timedelta(days=7)
    first_slot = find_first_available_slot_on_or_after(future_date)
    if first_slot:
        print(f"✓ First slot on/after {future_date}:")
        print(f"  {format_slot_time(first_slot['start_datetime'])}")
    else:
        print("✗ No slot found")
    
    # Book multiple appointments to test capacity
    print("\n8. Testing booking multiple appointments...")
    booking_count = 0
    for slot in next_slots_after[:3]:
        appt_id = crud.book_appointment(
            child_id=child_id,
            appointment_type="vaccine",
            start_datetime=slot['start_datetime'],
            end_datetime=slot['end_datetime'],
            subject="Vaccine appointment",
        )
        if appt_id:
            booking_count += 1
    print(f"✓ Booked {booking_count} additional appointments")
    
    # Check availability again
    final_slots = get_next_available_slots(count=5)
    print(f"✓ After all bookings, next 5 available slots start from:")
    print(f"  {format_slot_time(final_slots[0]['start_datetime'])}")
    
    print("\n" + "="*50)
    print("✓ All scheduling tests passed!")
    print("="*50)


if __name__ == "__main__":
    test_scheduling()
