"""Database schema initialization."""
from app.db.connection import get_cursor


def init_db():
    """Initialize the database schema."""
    with get_cursor() as cursor:
        # Children table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS children (
                child_id TEXT PRIMARY KEY,
                child_name TEXT NOT NULL,
                dob DATE NOT NULL,
                sex TEXT NOT NULL,
                parent_name TEXT NOT NULL,
                parent_phone TEXT NOT NULL,
                parent_email TEXT NOT NULL,
                allergies_text TEXT,
                family_history_text TEXT,
                surgeries_text TEXT,
                medical_free_text TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on child_name for search
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_child_name 
            ON children(child_name)
        """)
        
        # Prescriptions table (append-only)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id TEXT NOT NULL,
                date DATE NOT NULL,
                prescriber TEXT NOT NULL,
                dosage TEXT NOT NULL,
                duration TEXT,
                notes_summary TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(child_id)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_prescriptions_child_id 
            ON prescriptions(child_id)
        """)
        
        # Vaccines administered table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vaccines_administered (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id TEXT NOT NULL,
                vaccine_name TEXT NOT NULL,
                dose_number TEXT NOT NULL,
                date_given DATE NOT NULL,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(child_id)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_vaccines_child_id 
            ON vaccines_administered(child_id)
        """)
        
        # Appointments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id TEXT NOT NULL,
                appointment_type TEXT NOT NULL,
                start_datetime DATETIME NOT NULL,
                end_datetime DATETIME NOT NULL,
                subject TEXT NOT NULL,
                case_summary TEXT,
                status TEXT DEFAULT 'booked',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(child_id)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_appointments_child_id 
            ON appointments(child_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_appointments_start_datetime 
            ON appointments(start_datetime)
        """)


def reset_db():
    """Drop all tables and reinitialize (for testing)."""
    with get_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS appointments")
        cursor.execute("DROP TABLE IF EXISTS vaccines_administered")
        cursor.execute("DROP TABLE IF EXISTS prescriptions")
        cursor.execute("DROP TABLE IF EXISTS children")
    init_db()
