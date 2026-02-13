"""Main Streamlit application entry point."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.schema import init_db

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Pediatric Care System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on startup
init_db()

# Main page
st.title("🏥 Pediatric Care System")
st.markdown("---")

st.markdown("""
## Welcome to the Pediatric Care System

This system provides two main interfaces:

### 👨‍⚕️ Practitioner Admin
- Search and manage child records
- Add/edit medical history
- Record prescriptions and vaccines
- View appointment schedules

### 👪 Parent Chat
- AI-powered health guidance assistant
- Vaccine reminders and tracking
- Appointment scheduling
- General pediatric health questions

**⚠️ Important:** This is a proof-of-concept system. All medical decisions should be made in consultation with qualified healthcare professionals.

---

👈 **Select a page from the sidebar to get started**
""")

# Sidebar info
with st.sidebar:
    st.markdown("### 📋 System Info")
    st.info("""
    **Features:**
    - Child record management
    - India UIP vaccine schedule
    - AI chat assistant
    - Appointment scheduling
    
    **Note:** This is a demo system with no authentication.
    """)
