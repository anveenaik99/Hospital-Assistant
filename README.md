# Pediatric Care System - AI-Powered Healthcare Assistant

**Portfolio Project for Product Manager**  
Demonstrating product thinking, user-centric design, and AI implementation in healthcare


## 🎯 Product Vision

**"Making pediatric healthcare accessible, proactive, and stress-free for parents while empowering practitioners with efficient care management."**

---

## 📊 Working Backwards: From Customer Pain Points to Solution

### Customer Research & Pain Points Identified

#### For Parents:
1. **Information Overload & Anxiety**
   - "I'm not sure if my child's symptoms need a doctor visit"
   - "I keep forgetting when vaccines are due"
   - "Scheduling appointments is time-consuming and require to call and wait for the receptionist"

2. **Accessibility Gaps**
   - Difficulty getting timely medical guidance
   - Confusion about vaccine schedules
   - No centralized place for child's medical history

#### For Practitioners:
1. **Administrative Burden**
   - Time spent on routine queries that could be automated
   - Manual vaccine schedule tracking
   - Fragmented patient records

2. **Patient Engagement**
   - Low vaccination compliance due to missed reminders
   - Parents don't follow up on health concerns early enough

### Our Solution

An AI-powered pediatric care system that:
- Provides 24/7 intelligent health guidance to parents
- Automates vaccine tracking and reminders
- Streamlines appointment scheduling
- Centralizes child health records

---

## User Personas

### Primary Persona: Priya (Working Parent)
- **Age:** 32, Software Engineer
- **Family:** Mother of 6-month-old daughter
- **Pain Points:** 
  - Works full-time, limited time for doctor visits
  - Anxious about child's health, googles everything
  - Forgets vaccine dates
- **Goals:** Quick access to reliable health information, proactive care

### Secondary Persona: Dr. Meera (Pediatrician)
- **Age:** 45, Pediatrician with 15 years experience
- **Practice:** Small clinic, 30-40 patients/day
- **Pain Points:**
  - Spends time answering routine questions
  - Manual appointment management
  - Patients miss vaccine schedules
- **Goals:** Efficient practice management, better patient compliance

---

## Product Features & User Stories

### Feature 1: AI Health Assistant for Parents

**User Story:** *"As a parent, I want to ask health questions and get reliable guidance so that I can make informed decisions without always visiting the doctor."*

**Acceptance Criteria:**
- ✅ Natural language conversation interface
- ✅ Access to child's medical history and allergies
- ✅ Contextual responses based on child's age and history
- ✅ Clear disclaimers (not medical advice)
- ✅ Escalation to practitioner when needed

**Product Decisions:**
- Used GPT-4o-mini for cost-effective, accurate responses
- Implemented conversational AI with memory
- Added safety guardrails (no medication dosing)

### Feature 2: Proactive Vaccine Management

**User Story:** *"As a parent, I want to be automatically reminded about upcoming vaccines so that my child stays on schedule."*

**Acceptance Criteria:**
- ✅ Automatic tracking based on India UIP schedule
- ✅ Overdue vaccine identification
- ✅ Upcoming vaccine reminders (28-day window)
- ✅ One-click appointment booking for vaccines

**Product Decisions:**
- 28 vaccines from birth to 16 years
- Smart reminders at conversation end (not intrusive)
- Integration with appointment system

### Feature 3: Intelligent Appointment Scheduling

**User Story:** *"As a parent, I want to easily book appointments at convenient times so that I don't have to call the clinic multiple times."*

**Acceptance Criteria:**
- ✅ View available time slots
- ✅ Book appointments through chat
- ✅ Conflict prevention (double-booking)
- ✅ Clear confirmation with details

**Product Decisions:**
- 30-minute slot cadence (25-min appointments + 5-min buffer)
- Working hours: Mon-Sat 10AM-2PM, Mon-Fri 4PM-7PM
- Real-time availability checking

### Feature 4: Practitioner Admin Portal

**User Story:** *"As a practitioner, I want to efficiently manage patient records so that I can focus on care rather than paperwork."*

**Acceptance Criteria:**
- ✅ Quick patient search
- ✅ Comprehensive medical history view
- ✅ Easy prescription and vaccine recording
- ✅ Appointment schedule overview

**Product Decisions:**
- Streamlit for rapid development
- Tabbed interface for organized information
- Search-first design for quick access

---

## 📈 Success Metrics (KPIs)

### User Engagement Metrics
- **Parent Satisfaction:** Chat completion rate, positive feedback
- **Appointment Conversion:** Chat → Booking rate
- **Response Time:** Average AI response time < 3 seconds

### Health Outcome Metrics
- **Vaccination Compliance:** % of children on schedule
- **Early Detection:** % of concerns caught before escalation
- **Access:** Reduction in unnecessary clinic visits

### Operational Metrics
- **Practitioner Time Saved:** Hours saved per week on routine queries
- **Appointment No-shows:** Reduction through automated reminders
- **Data Accuracy:** % of complete and accurate records

---

## 🛠️ Product Requirements

### Functional Requirements

#### Must Have (MVP)
1. ✅ AI chat interface for health queries
2. ✅ Child record management (CRUD)
3. ✅ Vaccine schedule tracking
4. ✅ Appointment booking system
5. ✅ Practitioner admin dashboard

#### Should Have (Phase 2)
- [ ] SMS/Email notifications for appointments
- [ ] Multi-language support (Hindi, Tamil, etc.)
- [ ] Growth charts and milestone tracking
- [ ] Prescription history export (PDF)



## Technical Architecture

### Technology Stack

**Frontend:** Streamlit (Python)
- Rapid prototyping
- Native Python integration
- Built-in state management

**Backend:** Python with SQLite
- Lightweight for MVP
- Easy migration to PostgreSQL later
- Strong ecosystem (pandas, langchain)

**AI Layer:** LangChain + OpenAI GPT-4o-mini
- Flexible tool integration
- Cost-effective ($0.150 per 1M input tokens)
- Strong healthcare domain knowledge

### System Design Principles

1. **Modularity:** Separated concerns (db, vaccines, scheduling, agent)
2. **Testability:** Unit tests for core logic
3. **Scalability:** Easy migration to cloud databases
4. **Maintainability:** Clear code structure, documentation

### Data Model

```
Children
├── Demographics (name, DOB, sex, parent info)
├── Medical History (allergies, family history, surgeries)
├── Prescriptions (date, prescriber, dosage, notes)
├── Vaccines Administered (vaccine, dose, date)
└── Appointments (type, datetime, status, summary)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Conda environment manager
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Hospital

# Create conda environment
conda create -n hospital python=3.12 -y
conda activate hospital

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Seed sample data
python seed_data.py

# Run the application
streamlit run app/main.py
```

### Quick Start

1. **Open Browser:** Navigate to http://localhost:8501
2. **Practitioner Admin:** Create or search for child records
3. **Parent Chat:** Use child ID (e.g., CH-000001) to start conversation
4. **Try It:** Ask health questions, check vaccines, book appointments

---

## 📚 Documentation

- **[SAMPLE_DATA.md](SAMPLE_DATA.md)** - Test data and scenarios
- **[plan.md](plan.md)** - Original development plan

---

## 🧪 Testing

### Sample Test Scenarios

**Scenario 1: New Parent Onboarding**
```
Child: CH-000006 (Diya Singh - Newborn)
Test: Ask about feeding, sleep, upcoming vaccines
Expected: Contextual guidance + reminder about 6-week vaccines
```

**Scenario 2: Vaccine Catch-up**
```
Child: CH-000007 (Harsh Kumar - 10 months, no vaccines)
Test: Check vaccine status
Expected: List of 26 overdue vaccines + appointment booking offer
```

**Scenario 3: Health Concern**
```
Child: CH-000003 (Aarav - has peanut allergy)
Test: Ask about skin rash
Expected: AI considers allergy, asks clarifying questions
```
---

## 🎓 Key Learnings (PM Perspective)

### What Worked Well
1. **User-Centric Design:** Starting with pain points led to clear features
2. **Iterative Development:** MVP approach validated core assumptions
3. **AI as Enabler:** LLMs significantly enhanced user experience
4. **Realistic Test Data:** Good sample data enabled meaningful demos

### What Could Be Improved
1. **User Testing:** Need real parent feedback (current: assumptions)
2. **Mobile Experience:** Streamlit limitations became apparent
3. **Scalability Planning:** Should have considered multi-tenancy earlier
4. **Compliance:** HIPAA/data privacy addressed too late

### PM Skills Demonstrated
- ✅ Customer empathy & problem identification
- ✅ Requirements gathering & prioritization
- ✅ Working backwards from customer needs
- ✅ Trade-off analysis & decision making
- ✅ Success metrics definition
- ✅ Roadmap planning
- ✅ Cross-functional thinking (product + tech)
