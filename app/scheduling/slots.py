"""Appointment slot generation and validation."""
from datetime import datetime, date, time, timedelta
from typing import List, Dict, Any, Optional
import os
import pytz

from app.db.crud import check_appointment_overlap, list_appointments_in_range


# Get timezone from environment or default to Asia/Kolkata
TIMEZONE = pytz.timezone(os.getenv("APP_TIMEZONE", "Asia/Kolkata"))

# Slot configuration
SLOT_DURATION_MINUTES = 25
BUFFER_MINUTES = 5
SLOT_CADENCE_MINUTES = 30  # Start every 30 minutes

# Doctor availability
# Morning: Mon-Sat 10:00-14:00
# Evening: Mon-Fri 16:00-19:00
MORNING_START = time(10, 0)
MORNING_END = time(14, 0)
EVENING_START = time(16, 0)
EVENING_END = time(19, 0)


def is_working_day(dt: datetime) -> bool:
    """Check if date is a working day (Mon-Sat)."""
    return dt.weekday() < 6  # 0=Monday, 6=Sunday


def generate_slot_times_for_date(target_date: date) -> List[datetime]:
    """
    Generate all candidate slot start times for a given date.
    
    Returns list of datetime objects representing slot start times.
    """
    slots = []
    dt = datetime.combine(target_date, time(0, 0))
    
    # Skip Sunday
    if dt.weekday() == 6:
        return slots
    
    # Morning slots (Mon-Sat)
    current = dt.replace(hour=MORNING_START.hour, minute=MORNING_START.minute)
    morning_end = dt.replace(hour=MORNING_END.hour, minute=MORNING_END.minute)
    
    while current < morning_end:
        slots.append(current)
        current += timedelta(minutes=SLOT_CADENCE_MINUTES)
    
    # Evening slots (Mon-Fri only)
    if dt.weekday() < 5:  # Monday to Friday
        current = dt.replace(hour=EVENING_START.hour, minute=EVENING_START.minute)
        evening_end = dt.replace(hour=EVENING_END.hour, minute=EVENING_END.minute)
        
        while current < evening_end:
            slots.append(current)
            current += timedelta(minutes=SLOT_CADENCE_MINUTES)
    
    return slots


def is_slot_available(start_datetime: datetime) -> bool:
    """
    Check if a slot is available (no overlapping appointments).
    
    Args:
        start_datetime: Proposed slot start time
        
    Returns:
        True if slot is available, False if overlapping
    """
    end_datetime = start_datetime + timedelta(minutes=SLOT_DURATION_MINUTES)
    return not check_appointment_overlap(start_datetime, end_datetime)


def validate_slot(
    start_datetime: datetime,
    appointment_type: str
) -> Dict[str, Any]:
    """
    Validate a proposed appointment slot.
    
    Args:
        start_datetime: Proposed start time
        appointment_type: Type of appointment ('consult' or 'vaccine')
        
    Returns:
        Dict with 'ok' (bool) and optional 'reason' (str)
    """
    # Check if in the past
    now = datetime.now()
    if start_datetime < now:
        return {'ok': False, 'reason': 'Appointment time is in the past'}
    
    # Check if working day
    if start_datetime.weekday() == 6:  # Sunday
        return {'ok': False, 'reason': 'Not a working day (Sunday)'}
    
    # Check if within working hours
    slot_time = start_datetime.time()
    
    is_morning = MORNING_START <= slot_time < MORNING_END
    is_evening = EVENING_START <= slot_time < EVENING_END and start_datetime.weekday() < 5
    
    if not (is_morning or is_evening):
        return {'ok': False, 'reason': 'Not within working hours'}
    
    # Check if aligned to cadence
    minutes_from_midnight = start_datetime.hour * 60 + start_datetime.minute
    if minutes_from_midnight % SLOT_CADENCE_MINUTES != 0:
        return {'ok': False, 'reason': f'Not aligned to {SLOT_CADENCE_MINUTES}-minute cadence'}
    
    # Check for overlaps
    if not is_slot_available(start_datetime):
        return {'ok': False, 'reason': 'Time slot already booked'}
    
    return {'ok': True}


def get_available_slots_for_dates(
    dates: List[date],
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get available slots for specific dates.
    
    Args:
        dates: List of dates to check
        limit: Maximum number of slots to return (optional)
        
    Returns:
        List of dicts with 'start_datetime' and 'end_datetime'
    """
    available_slots = []
    
    for target_date in dates:
        slot_times = generate_slot_times_for_date(target_date)
        
        for start_time in slot_times:
            if is_slot_available(start_time):
                end_time = start_time + timedelta(minutes=SLOT_DURATION_MINUTES)
                available_slots.append({
                    'start_datetime': start_time,
                    'end_datetime': end_time
                })
                
                if limit and len(available_slots) >= limit:
                    return available_slots
    
    return available_slots


def get_next_available_slots(
    count: int = 5,
    start_from_date: Optional[date] = None
) -> List[Dict[str, Any]]:
    """
    Get the next N available slots starting from a given date.
    
    Args:
        count: Number of slots to return
        start_from_date: Date to start searching from (default: tomorrow)
        
    Returns:
        List of dicts with 'start_datetime' and 'end_datetime'
    """
    if start_from_date is None:
        start_from_date = date.today() + timedelta(days=1)
    
    available_slots = []
    current_date = start_from_date
    max_days_to_search = 60  # Search up to 2 months ahead
    
    days_searched = 0
    while len(available_slots) < count and days_searched < max_days_to_search:
        slot_times = generate_slot_times_for_date(current_date)
        
        for start_time in slot_times:
            if is_slot_available(start_time):
                end_time = start_time + timedelta(minutes=SLOT_DURATION_MINUTES)
                available_slots.append({
                    'start_datetime': start_time,
                    'end_datetime': end_time
                })
                
                if len(available_slots) >= count:
                    return available_slots
        
        current_date += timedelta(days=1)
        days_searched += 1
    
    return available_slots


def find_first_available_slot_on_or_after(
    target_date: date
) -> Optional[Dict[str, Any]]:
    """
    Find the first available slot on or after a given date.
    
    Useful for vaccine appointments that should be scheduled on/after due date.
    
    Args:
        target_date: Earliest date for the appointment
        
    Returns:
        Dict with 'start_datetime' and 'end_datetime', or None if none found
    """
    slots = get_next_available_slots(count=1, start_from_date=target_date)
    return slots[0] if slots else None


def format_slot_time(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%A, %B %d, %Y at %I:%M %p")
