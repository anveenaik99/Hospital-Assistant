"""Vaccine status logic."""
from datetime import date, timedelta
from typing import List, Dict, Any, Tuple
from dateutil.relativedelta import relativedelta

from app.vaccines.uip_schedule import UIP_SCHEDULE, VaccineScheduleItem
from app.db.crud import get_child_by_id, list_vaccines_by_child


def compute_vaccine_status(
    child_id: str,
    window_days: int = 28
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Compute vaccine status for a child.
    
    Returns:
        Dict with keys:
        - 'given': List of administered vaccines
        - 'overdue': List of overdue/missing vaccines
        - 'upcoming': List of vaccines due within window_days
        - 'future': List of vaccines due after window_days
    """
    # Get child record
    child = get_child_by_id(child_id)
    if not child:
        return {
            'given': [],
            'overdue': [],
            'upcoming': [],
            'future': []
        }
    
    # Parse DOB
    if isinstance(child['dob'], str):
        dob = date.fromisoformat(child['dob'])
    else:
        dob = child['dob']
    
    # Get administered vaccines
    administered = list_vaccines_by_child(child_id)
    
    # Create set of (vaccine_name, dose_label) for quick lookup
    given_set = {
        (v['vaccine_name'], v['dose_number'])
        for v in administered
    }
    
    today = date.today()
    window_end = today + timedelta(days=window_days)
    
    result = {
        'given': [],
        'overdue': [],
        'upcoming': [],
        'future': []
    }
    
    # Process each scheduled vaccine
    for schedule_item in UIP_SCHEDULE:
        due_date = dob + schedule_item.due_offset
        key = (schedule_item.vaccine_name, schedule_item.dose_label)
        
        vaccine_info = {
            'vaccine_name': schedule_item.vaccine_name,
            'dose_label': schedule_item.dose_label,
            'due_date': due_date.isoformat(),
            'notes': schedule_item.notes
        }
        
        if key in given_set:
            # Find the administered record
            for admin in administered:
                if admin['vaccine_name'] == schedule_item.vaccine_name and \
                   admin['dose_number'] == schedule_item.dose_label:
                    vaccine_info['date_given'] = admin['date_given']
                    vaccine_info['admin_notes'] = admin.get('notes', '')
                    break
            result['given'].append(vaccine_info)
        elif due_date < today:
            # Overdue/missing
            vaccine_info['days_overdue'] = (today - due_date).days
            result['overdue'].append(vaccine_info)
        elif due_date <= window_end:
            # Upcoming within window
            vaccine_info['days_until_due'] = (due_date - today).days
            result['upcoming'].append(vaccine_info)
        else:
            # Future (beyond window)
            result['future'].append(vaccine_info)
    
    return result


def get_vaccine_summary(child_id: str) -> Dict[str, Any]:
    """
    Get a summary of vaccine status for use in chat agent.
    
    Returns:
        Dict with:
        - total_scheduled: Total vaccines in schedule
        - given_count: Number administered
        - overdue_count: Number overdue
        - upcoming_count: Number upcoming (within 28 days)
        - overdue_details: List of overdue vaccines
        - upcoming_details: List of upcoming vaccines
    """
    status = compute_vaccine_status(child_id, window_days=28)
    
    return {
        'total_scheduled': len(UIP_SCHEDULE),
        'given_count': len(status['given']),
        'overdue_count': len(status['overdue']),
        'upcoming_count': len(status['upcoming']),
        'overdue_details': status['overdue'],
        'upcoming_details': status['upcoming']
    }


def format_vaccine_reminders(status: Dict[str, List[Dict[str, Any]]]) -> str:
    """Format vaccine status into human-readable reminders."""
    lines = []
    
    if status['overdue']:
        lines.append("⚠️ OVERDUE/MISSING VACCINES:")
        for v in status['overdue']:
            lines.append(
                f"  • {v['vaccine_name']} (Dose {v['dose_label']}) - "
                f"Due: {v['due_date']} ({v['days_overdue']} days overdue)"
            )
        lines.append("")
    
    if status['upcoming']:
        lines.append("📅 UPCOMING VACCINES (Next 4 Weeks):")
        for v in status['upcoming']:
            days = v['days_until_due']
            if days == 0:
                due_str = "DUE TODAY"
            elif days == 1:
                due_str = "due tomorrow"
            else:
                due_str = f"due in {days} days"
            lines.append(
                f"  • {v['vaccine_name']} (Dose {v['dose_label']}) - "
                f"Due: {v['due_date']} ({due_str})"
            )
        lines.append("")
    
    if not status['overdue'] and not status['upcoming']:
        lines.append("✅ All vaccines are up to date!")
        lines.append("")
    
    return "\n".join(lines)
