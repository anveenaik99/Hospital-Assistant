"""CRUD operations for database."""
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from app.db.connection import get_cursor


# ========== CHILDREN ==========

def generate_child_id() -> str:
    """Generate a new child_id in format CH-XXXXXX."""
    with get_cursor() as cursor:
        cursor.execute("SELECT child_id FROM children ORDER BY child_id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            last_id = row["child_id"]
            num = int(last_id.split("-")[1]) + 1
        else:
            num = 1
        return f"CH-{num:06d}"


def create_child(
    child_name: str,
    dob: date,
    sex: str,
    parent_name: str,
    parent_phone: str,
    parent_email: str,
    allergies_text: Optional[str] = None,
    family_history_text: Optional[str] = None,
    surgeries_text: Optional[str] = None,
    medical_free_text: Optional[str] = None,
) -> str:
    """Create a new child record and return child_id."""
    child_id = generate_child_id()
    with get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO children (
                child_id, child_name, dob, sex, parent_name, parent_phone, 
                parent_email, allergies_text, family_history_text, 
                surgeries_text, medical_free_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            child_id, child_name, dob, sex, parent_name, parent_phone,
            parent_email, allergies_text, family_history_text,
            surgeries_text, medical_free_text
        ))
    return child_id


def search_children_by_name(name_substring: str) -> List[Dict[str, Any]]:
    """Search children by name substring (case-insensitive)."""
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT child_id, child_name, dob, parent_name, parent_phone
            FROM children
            WHERE child_name LIKE ?
            ORDER BY child_name
        """, (f"%{name_substring}%",))
        return [dict(row) for row in cursor.fetchall()]


def get_child_by_id(child_id: str) -> Optional[Dict[str, Any]]:
    """Get child record by ID."""
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM children WHERE child_id = ?", (child_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_child(
    child_id: str,
    child_name: Optional[str] = None,
    dob: Optional[date] = None,
    sex: Optional[str] = None,
    parent_name: Optional[str] = None,
    parent_phone: Optional[str] = None,
    parent_email: Optional[str] = None,
    allergies_text: Optional[str] = None,
    family_history_text: Optional[str] = None,
    surgeries_text: Optional[str] = None,
    medical_free_text: Optional[str] = None,
) -> bool:
    """Update child record. Only updates provided fields."""
    updates = []
    values = []
    
    if child_name is not None:
        updates.append("child_name = ?")
        values.append(child_name)
    if dob is not None:
        updates.append("dob = ?")
        values.append(dob)
    if sex is not None:
        updates.append("sex = ?")
        values.append(sex)
    if parent_name is not None:
        updates.append("parent_name = ?")
        values.append(parent_name)
    if parent_phone is not None:
        updates.append("parent_phone = ?")
        values.append(parent_phone)
    if parent_email is not None:
        updates.append("parent_email = ?")
        values.append(parent_email)
    if allergies_text is not None:
        updates.append("allergies_text = ?")
        values.append(allergies_text)
    if family_history_text is not None:
        updates.append("family_history_text = ?")
        values.append(family_history_text)
    if surgeries_text is not None:
        updates.append("surgeries_text = ?")
        values.append(surgeries_text)
    if medical_free_text is not None:
        updates.append("medical_free_text = ?")
        values.append(medical_free_text)
    
    if not updates:
        return False
    
    updates.append("updated_at = ?")
    values.append(datetime.now())
    values.append(child_id)
    
    with get_cursor() as cursor:
        cursor.execute(f"""
            UPDATE children
            SET {', '.join(updates)}
            WHERE child_id = ?
        """, values)
        return cursor.rowcount > 0


# ========== PRESCRIPTIONS ==========

def add_prescription(
    child_id: str,
    date: date,
    prescriber: str,
    dosage: str,
    duration: Optional[str] = None,
    notes_summary: Optional[str] = None,
) -> int:
    """Add a prescription (append-only). Returns prescription ID."""
    with get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO prescriptions (
                child_id, date, prescriber, dosage, duration, notes_summary
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (child_id, date, prescriber, dosage, duration, notes_summary))
        return cursor.lastrowid


def list_prescriptions_by_child(child_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """List prescriptions for a child, most recent first."""
    with get_cursor() as cursor:
        query = """
            SELECT * FROM prescriptions
            WHERE child_id = ?
            ORDER BY date DESC, created_at DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        cursor.execute(query, (child_id,))
        return [dict(row) for row in cursor.fetchall()]


# ========== VACCINES ==========

def add_vaccine(
    child_id: str,
    vaccine_name: str,
    dose_number: str,
    date_given: date,
    notes: Optional[str] = None,
) -> int:
    """Add a vaccine record. Returns vaccine ID."""
    with get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO vaccines_administered (
                child_id, vaccine_name, dose_number, date_given, notes
            ) VALUES (?, ?, ?, ?, ?)
        """, (child_id, vaccine_name, dose_number, date_given, notes))
        return cursor.lastrowid


def list_vaccines_by_child(child_id: str) -> List[Dict[str, Any]]:
    """List all vaccines for a child, most recent first."""
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT * FROM vaccines_administered
            WHERE child_id = ?
            ORDER BY date_given DESC
        """, (child_id,))
        return [dict(row) for row in cursor.fetchall()]


# ========== APPOINTMENTS ==========

def check_appointment_overlap(
    start_datetime: datetime,
    end_datetime: datetime,
    exclude_id: Optional[int] = None,
) -> bool:
    """Check if a time slot overlaps with existing appointments."""
    with get_cursor() as cursor:
        query = """
            SELECT COUNT(*) as count FROM appointments
            WHERE status = 'booked'
            AND start_datetime < ?
            AND end_datetime > ?
        """
        params = [end_datetime, start_datetime]
        
        if exclude_id:
            query += " AND id != ?"
            params.append(exclude_id)
        
        cursor.execute(query, params)
        return cursor.fetchone()["count"] > 0


def book_appointment(
    child_id: str,
    appointment_type: str,
    start_datetime: datetime,
    end_datetime: datetime,
    subject: str,
    case_summary: Optional[str] = None,
) -> Optional[int]:
    """
    Book an appointment if no overlap exists.
    Returns appointment ID if successful, None if overlap detected.
    """
    if check_appointment_overlap(start_datetime, end_datetime):
        return None
    
    with get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO appointments (
                child_id, appointment_type, start_datetime, end_datetime,
                subject, case_summary, status
            ) VALUES (?, ?, ?, ?, ?, ?, 'booked')
        """, (child_id, appointment_type, start_datetime, end_datetime, subject, case_summary))
        return cursor.lastrowid


def list_appointments_by_child(child_id: str) -> List[Dict[str, Any]]:
    """List all appointments for a child, most recent first."""
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT * FROM appointments
            WHERE child_id = ?
            ORDER BY start_datetime DESC
        """, (child_id,))
        return [dict(row) for row in cursor.fetchall()]


def list_appointments_in_range(
    start_date: datetime,
    end_date: datetime,
) -> List[Dict[str, Any]]:
    """List all appointments in a date range."""
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT * FROM appointments
            WHERE status = 'booked'
            AND start_datetime >= ?
            AND start_datetime < ?
            ORDER BY start_datetime
        """, (start_date, end_date))
        return [dict(row) for row in cursor.fetchall()]
