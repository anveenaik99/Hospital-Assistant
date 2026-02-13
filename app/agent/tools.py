"""LangGraph agent tools."""
import json
from datetime import datetime, date
from typing import Optional, List
from langchain_core.tools import tool

from app.db.crud import (
    get_child_by_id,
    list_prescriptions_by_child,
    book_appointment as db_book_appointment
)
from app.vaccines.logic import compute_vaccine_status, get_vaccine_summary
from app.scheduling.slots import (
    get_next_available_slots,
    get_available_slots_for_dates,
    validate_slot as validate_slot_func,
    find_first_available_slot_on_or_after,
    format_slot_time,
    SLOT_DURATION_MINUTES
)


@tool
def load_child_record(child_id: str) -> str:
    """
    Load complete child record including demographics, medical history, 
    recent prescriptions, and vaccine summary.
    
    Args:
        child_id: The child ID (e.g., CH-000001)
        
    Returns:
        JSON string with child profile
    """
    print(f"[TOOL] load_child_record called with child_id: {child_id}")
    child = get_child_by_id(child_id)
    if not child:
        print(f"[TOOL] Child not found: {child_id}")
        return json.dumps({"error": "Child not found"})
    
    print(f"[TOOL] Child found: {child['child_name']}")
    
    # Get recent prescriptions (last 5)
    prescriptions = list_prescriptions_by_child(child_id, limit=5)
    
    # Get vaccine summary
    vaccine_summary = get_vaccine_summary(child_id)
    
    profile = {
        "child_id": child["child_id"],
        "child_name": child["child_name"],
        "dob": child["dob"],
        "age_months": _calculate_age_months(child["dob"]),
        "sex": child["sex"],
        "parent_name": child["parent_name"],
        "parent_phone": child["parent_phone"],
        "parent_email": child["parent_email"],
        "medical_history": {
            "allergies": child.get("allergies_text", "None recorded"),
            "family_history": child.get("family_history_text", "None recorded"),
            "surgeries": child.get("surgeries_text", "None recorded"),
            "other_notes": child.get("medical_free_text", "None recorded")
        },
        "recent_prescriptions": [
            {
                "date": rx["date"],
                "prescriber": rx["prescriber"],
                "dosage": rx["dosage"],
                "duration": rx.get("duration", ""),
                "notes": rx.get("notes_summary", "")
            }
            for rx in prescriptions
        ],
        "vaccine_summary": vaccine_summary
    }
    
    return json.dumps(profile, indent=2)


@tool
def vaccine_check(child_id: str, window_days: int = 28) -> str:
    """
    Check vaccine status for a child, identifying overdue and upcoming vaccines.
    
    Args:
        child_id: The child ID
        window_days: Number of days to look ahead for upcoming vaccines (default 28)
        
    Returns:
        JSON string with overdue and upcoming vaccine lists
    """
    status = compute_vaccine_status(child_id, window_days=window_days)
    
    result = {
        "overdue": status["overdue"],
        "upcoming": status["upcoming"],
        "summary": {
            "overdue_count": len(status["overdue"]),
            "upcoming_count": len(status["upcoming"]),
            "given_count": len(status["given"])
        }
    }
    
    return json.dumps(result, indent=2)


@tool
def check_schedule(child_id: str, requested_dates: Optional[str] = None) -> str:
    """
    Check available appointment slots for specific dates or get next available slots.
    
    IMPORTANT: When user asks for slots on a specific day (e.g., "Monday", "next Tuesday", "February 10"),
    you MUST calculate the actual date and provide it in requested_dates parameter.
    
    Args:
        child_id: The child ID
        requested_dates: Optional JSON array of date strings in ISO format (e.g., '["2026-02-10", "2026-02-11"]')
                        - Use this when user asks for specific days/dates
                        - If not provided, returns next 5 available slots across all upcoming days
        
    Returns:
        JSON string with available slots. If requested dates have no slots, it means all slots
        are available (no conflicts) for that day within working hours.
    
    Example:
        - User asks "What about Monday?": Calculate Monday's date and use requested_dates='["2026-02-10"]'
        - User asks "Show me next 5 slots": Don't provide requested_dates
    """
    print(f"[TOOL] check_schedule called with child_id={child_id}, requested_dates={requested_dates}")
    
    if requested_dates:
        try:
            date_strs = json.loads(requested_dates)
            dates = [date.fromisoformat(d) for d in date_strs]
            print(f"[TOOL] Checking slots for specific dates: {dates}")
            slots = get_available_slots_for_dates(dates, limit=50)  # Increased limit for full day view
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"error": f"Invalid date format: {str(e)}"})
    else:
        print("[TOOL] Getting next 5 available slots")
        slots = get_next_available_slots(count=5)
    
    formatted_slots = [
        {
            "start_datetime": slot["start_datetime"].isoformat(),
            "end_datetime": slot["end_datetime"].isoformat(),
            "display": format_slot_time(slot["start_datetime"])
        }
        for slot in slots
    ]
    
    print(f"[TOOL] Found {len(formatted_slots)} available slots")
    return json.dumps({"available_slots": formatted_slots}, indent=2)


@tool
def validate_slot(start_datetime: str, appointment_type: str) -> str:
    """
    Validate if a proposed appointment slot is valid.
    
    Args:
        start_datetime: ISO format datetime string (e.g., "2026-02-01T10:00:00")
        appointment_type: Type of appointment ('consult' or 'vaccine')
        
    Returns:
        JSON string with validation result
    """
    try:
        dt = datetime.fromisoformat(start_datetime)
        result = validate_slot_func(dt, appointment_type)
        return json.dumps(result)
    except ValueError as e:
        return json.dumps({"ok": False, "reason": f"Invalid datetime format: {str(e)}"})


@tool
def book_appointment(
    child_id: str,
    appointment_type: str,
    start_datetime: str,
    subject: str,
    case_summary: str
) -> str:
    """
    Book an appointment for a child.
    
    Args:
        child_id: The child ID
        appointment_type: Type of appointment ('consult' or 'vaccine')
        start_datetime: ISO format datetime string (e.g., "2026-02-01T10:00:00")
        subject: Brief subject/reason for appointment
        case_summary: LLM-generated summary of the case/condition
        
    Returns:
        JSON string with booking confirmation or error
    """
    try:
        start_dt = datetime.fromisoformat(start_datetime)
        end_dt = start_dt + timedelta(minutes=SLOT_DURATION_MINUTES)
        
        # Validate first
        validation = validate_slot_func(start_dt, appointment_type)
        if not validation["ok"]:
            return json.dumps({
                "success": False,
                "error": validation["reason"]
            })
        
        # Book
        appt_id = db_book_appointment(
            child_id=child_id,
            appointment_type=appointment_type,
            start_datetime=start_dt,
            end_datetime=end_dt,
            subject=subject,
            case_summary=case_summary
        )
        
        if appt_id:
            return json.dumps({
                "success": True,
                "appointment_id": appt_id,
                "confirmation": f"Appointment booked for {format_slot_time(start_dt)}",
                "details": {
                    "type": appointment_type,
                    "subject": subject,
                    "start": start_dt.isoformat(),
                    "end": end_dt.isoformat()
                }
            })
        else:
            return json.dumps({
                "success": False,
                "error": "Failed to book appointment (slot may have been taken)"
            })
            
    except ValueError as e:
        return json.dumps({
            "success": False,
            "error": f"Invalid datetime format: {str(e)}"
        })


def _calculate_age_months(dob: str) -> int:
    """Calculate age in months from date of birth."""
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)
    
    today = date.today()
    months = (today.year - dob.year) * 12 + (today.month - dob.month)
    return months


# Import timedelta for book_appointment
from datetime import timedelta


# List of all tools
ALL_TOOLS = [
    load_child_record,
    vaccine_check,
    check_schedule,
    validate_slot,
    book_appointment
]
