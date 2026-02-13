# Sample Data Documentation

This file contains all the sample data that has been seeded into the database for testing purposes.

## Overview

The database contains 5 sample children with varying vaccination statuses, medical histories, prescriptions, and appointments. This provides a realistic test environment for the Pediatric Care System.

---

## Child Records

### 1. CH-000003 - Aarav Sharma (Well-Vaccinated 3-Year-Old)

**Demographics:**
- **Name:** Aarav Sharma
- **Date of Birth:** March 15, 2023 (3 years old)
- **Sex:** Male
- **Parent/Guardian:** Priya Sharma
- **Phone:** +91-9876543210
- **Email:** priya.sharma@email.com

**Medical History:**
- **Allergies:** Mild peanut allergy
- **Family History:** Maternal grandmother has diabetes
- **Surgeries:** None
- **Other Notes:** Generally healthy child. Had chickenpox at age 2.

**Prescriptions:**
1. Date: November 15, 2025
   - Prescriber: Dr. Rajesh Kumar
   - Dosage: Paracetamol syrup 5ml, 3 times daily
   - Duration: 3 days
   - Notes: For fever associated with viral infection

**Vaccines Administered (19 vaccines):**
- BCG (Dose 0) - March 16, 2023
- OPV (Dose 0) - March 16, 2023
- Hepatitis B (Dose 0) - March 16, 2023
- OPV (Dose 1) - April 26, 2023
- Pentavalent (Dose 1) - April 26, 2023
- IPV (Dose 1) - April 26, 2023
- Rotavirus (Dose 1) - April 26, 2023
- PCV (Dose 1) - April 26, 2023
- OPV (Dose 2) - May 24, 2023
- Pentavalent (Dose 2) - May 24, 2023
- Rotavirus (Dose 2) - May 24, 2023
- OPV (Dose 3) - June 21, 2023
- Pentavalent (Dose 3) - June 21, 2023
- IPV (Dose 2) - June 21, 2023
- Rotavirus (Dose 3) - June 21, 2023
- PCV (Dose 2) - June 21, 2023
- Measles-Rubella (Dose 1) - March 18, 2024
- PCV (Booster) - March 18, 2024
- JE (Dose 1) - March 18, 2024

**Appointments:**
- February 5, 2026 at 10:00 AM - Routine checkup (Consult)

---

### 2. CH-000004 - Ananya Patel (6-Month-Old with Partial Vaccination)

**Demographics:**
- **Name:** Ananya Patel
- **Date of Birth:** July 20, 2025 (6 months old)
- **Sex:** Female
- **Parent/Guardian:** Amit Patel
- **Phone:** +91-9123456789
- **Email:** amit.patel@email.com

**Medical History:**
- **Allergies:** None known
- **Family History:** No significant family history
- **Surgeries:** None
- **Other Notes:** Healthy infant. Birth weight 3.2 kg. Normal development.

**Prescriptions:** None

**Vaccines Administered (8 vaccines):**
- BCG (Dose 0) - July 21, 2025
- OPV (Dose 0) - July 21, 2025
- Hepatitis B (Dose 0) - July 21, 2025
- OPV (Dose 1) - August 31, 2025
- Pentavalent (Dose 1) - August 31, 2025
- IPV (Dose 1) - August 31, 2025
- Rotavirus (Dose 1) - August 31, 2025
- PCV (Dose 1) - August 31, 2025

**Status:** Several vaccines are now due or overdue (Dose 2 series)

**Appointments:**
- February 8, 2026 at 11:00 AM - OPV Dose 2 (Vaccine appointment)

---

### 3. CH-000005 - Rohan Verma (18-Month-Old with Missed Vaccines)

**Demographics:**
- **Name:** Rohan Verma
- **Date of Birth:** July 10, 2024 (18 months old)
- **Sex:** Male
- **Parent/Guardian:** Kavita Verma
- **Phone:** +91-9988776655
- **Email:** kavita.verma@email.com

**Medical History:**
- **Allergies:** None known
- **Family History:** Father has asthma
- **Surgeries:** None
- **Other Notes:** Active and playful. Had a mild ear infection at 10 months.

**Prescriptions:**
1. Date: May 15, 2025
   - Prescriber: Dr. Meera Singh
   - Dosage: Amoxicillin suspension 5ml, twice daily
   - Duration: 7 days
   - Notes: For ear infection

**Vaccines Administered (7 vaccines - SEVERAL OVERDUE):**
- BCG (Dose 0) - July 11, 2024
- OPV (Dose 0) - July 11, 2024
- Hepatitis B (Dose 0) - July 11, 2024
- OPV (Dose 1) - August 21, 2024
- Pentavalent (Dose 1) - August 21, 2024
- IPV (Dose 1) - August 21, 2024
- PCV (Dose 1) - August 21, 2024

**Status:** Missing multiple vaccine doses - good case for testing overdue reminders

**Appointments:** None scheduled

---

### 4. CH-000006 - Diya Singh (Newborn)

**Demographics:**
- **Name:** Diya Singh
- **Date of Birth:** January 15, 2026 (newborn)
- **Sex:** Female
- **Parent/Guardian:** Rahul Singh
- **Phone:** +91-9876501234
- **Email:** rahul.singh@email.com

**Medical History:**
- **Allergies:** None known (newborn)
- **Family History:** No significant family history
- **Surgeries:** None
- **Other Notes:** Healthy newborn. Birth weight 3.5 kg. Normal delivery.

**Prescriptions:** None

**Vaccines Administered (3 vaccines - birth vaccines only):**
- BCG (Dose 0) - January 16, 2026
- OPV (Dose 0) - January 16, 2026
- Hepatitis B (Dose 0) - January 16, 2026

**Status:** First set of vaccines due at 6 weeks (late February 2026)

**Appointments:** None scheduled

---

### 5. CH-000007 - Harsh Kumar (10-Month-Old with NO Vaccines)

**Demographics:**
- **Name:** Harsh Kumar
- **Date of Birth:** March 20, 2025 (10 months old)
- **Sex:** Male
- **Parent/Guardian:** Neha Kumar
- **Phone:** +91-9123450987
- **Email:** neha.kumar@email.com

**Medical History:**
- **Allergies:** None known
- **Family History:** No significant family history
- **Surgeries:** None
- **Other Notes:** Moved from another city recently. Previous vaccination records pending.

**Prescriptions:** None

**Vaccines Administered:** NONE (0 vaccines)

**Status:** This child has NO vaccines on record - ideal for testing scenarios with maximum overdue vaccines

**Appointments:** None scheduled

---

## Test Scenarios

### Use Case 1: Well-Child Checkup
**Child:** CH-000003 (Aarav Sharma)
- Well-vaccinated child
- Has scheduled appointment
- Parent asks routine health questions

### Use Case 2: Vaccine Catch-Up
**Child:** CH-000005 (Rohan Verma) or CH-000007 (Harsh Kumar)
- Multiple overdue vaccines
- System should highlight need for catch-up
- Can test appointment booking for vaccinations

### Use Case 3: Infant Care
**Child:** CH-000004 (Ananya Patel) or CH-000006 (Diya Singh)
- Young infant
- Regular vaccination schedule
- Common infant health questions

### Use Case 4: Health Concern with Medical History
**Child:** CH-000003 (Aarav Sharma - has peanut allergy)
- Test AI awareness of allergies
- Test historical prescription access
- Test medical history context

### Use Case 5: New Patient
**Child:** CH-000007 (Harsh Kumar)
- No vaccination history
- Demonstrates need for comprehensive catch-up
- Tests system with minimal data

---

## How to Use This Data

1. **In Practitioner Admin:**
   - Search for any child by name (e.g., "Aarav", "Sharma", "Patel")
   - View complete records, medical history, prescriptions
   - Add new prescriptions or vaccines
   - View scheduled appointments

2. **In Parent Chat:**
   - Use any child ID (CH-000003 through CH-000007)
   - Ask health questions related to their history
   - Request vaccine status
   - Book appointments

3. **Testing Scenarios:**
   - Test vaccine reminders with CH-000005 or CH-000007 (many overdue)
   - Test appointment booking with any child
   - Test medical history awareness with CH-000003 (has allergies)
   - Test infant care with CH-000004 or CH-000006

---

## Resetting Data

If you need to reset the database and reload sample data:

```bash
# Delete the database file
rm data/app.db

# Run the seed script again to recreate the database with sample data
conda run -n hospital python seed_data.py
```

Alternatively, you can do it in one command:

```bash
rm data/app.db && conda run -n hospital python seed_data.py
```

---

**Note:** All data is synthetic and created for testing purposes only. Names, phone numbers, and email addresses are fictional.
