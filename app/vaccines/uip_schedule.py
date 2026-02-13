"""India Universal Immunization Programme (UIP) vaccine schedule.

Based on: https://www.mohfw.gov.in/sites/default/files/National%20Immunization%20Schedule.pdf
"""
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta
from typing import List


@dataclass
class VaccineScheduleItem:
    """Represents a scheduled vaccine dose."""
    vaccine_name: str
    dose_label: str  # e.g., "0", "1", "2", "Booster-1"
    due_offset: relativedelta  # Time from birth
    notes: str = ""


# India UIP Full Childhood Schedule
UIP_SCHEDULE: List[VaccineScheduleItem] = [
    # At birth
    VaccineScheduleItem("BCG", "0", relativedelta(days=0), "At birth"),
    VaccineScheduleItem("OPV", "0", relativedelta(days=0), "At birth (OPV-0)"),
    VaccineScheduleItem("Hepatitis B", "0", relativedelta(days=0), "At birth"),
    
    # 6 weeks
    VaccineScheduleItem("OPV", "1", relativedelta(weeks=6), "6 weeks"),
    VaccineScheduleItem("Pentavalent", "1", relativedelta(weeks=6), "DTwP + Hib + Hepatitis B"),
    VaccineScheduleItem("IPV", "1", relativedelta(weeks=6), "Inactivated Polio Vaccine"),
    VaccineScheduleItem("Rotavirus", "1", relativedelta(weeks=6), "Rotavirus vaccine"),
    VaccineScheduleItem("PCV", "1", relativedelta(weeks=6), "Pneumococcal Conjugate Vaccine"),
    
    # 10 weeks
    VaccineScheduleItem("OPV", "2", relativedelta(weeks=10), "10 weeks"),
    VaccineScheduleItem("Pentavalent", "2", relativedelta(weeks=10), "DTwP + Hib + Hepatitis B"),
    VaccineScheduleItem("Rotavirus", "2", relativedelta(weeks=10), "Rotavirus vaccine"),
    
    # 14 weeks
    VaccineScheduleItem("OPV", "3", relativedelta(weeks=14), "14 weeks"),
    VaccineScheduleItem("Pentavalent", "3", relativedelta(weeks=14), "DTwP + Hib + Hepatitis B"),
    VaccineScheduleItem("IPV", "2", relativedelta(weeks=14), "Inactivated Polio Vaccine"),
    VaccineScheduleItem("Rotavirus", "3", relativedelta(weeks=14), "Rotavirus vaccine"),
    VaccineScheduleItem("PCV", "2", relativedelta(weeks=14), "Pneumococcal Conjugate Vaccine"),
    
    # 9 months
    VaccineScheduleItem("Measles-Rubella", "1", relativedelta(months=9), "MR-1 / MMR-1"),
    VaccineScheduleItem("PCV", "Booster", relativedelta(months=9), "PCV Booster"),
    VaccineScheduleItem("JE", "1", relativedelta(months=9), "Japanese Encephalitis (endemic areas)"),
    
    # 12 months
    VaccineScheduleItem("Hepatitis A", "1", relativedelta(months=12), "Hepatitis A (optional)"),
    
    # 16-24 months
    VaccineScheduleItem("DPT", "Booster-1", relativedelta(months=16), "DPT Booster 1"),
    VaccineScheduleItem("OPV", "Booster", relativedelta(months=16), "OPV Booster"),
    VaccineScheduleItem("Measles-Rubella", "2", relativedelta(months=16), "MR-2 / MMR-2"),
    VaccineScheduleItem("JE", "2", relativedelta(months=16), "Japanese Encephalitis (endemic areas)"),
    
    # 18 months
    VaccineScheduleItem("Hepatitis A", "2", relativedelta(months=18), "Hepatitis A (optional)"),
    
    # 5-6 years
    VaccineScheduleItem("DPT", "Booster-2", relativedelta(years=5), "DPT Booster 2"),
    
    # 10 years
    VaccineScheduleItem("Td", "1", relativedelta(years=10), "Tetanus-Diphtheria"),
    
    # 16 years
    VaccineScheduleItem("Td", "2", relativedelta(years=16), "Tetanus-Diphtheria"),
]


def get_vaccine_names() -> List[str]:
    """Get unique vaccine names for dropdowns."""
    return sorted(list(set(item.vaccine_name for item in UIP_SCHEDULE)))


def get_dose_labels_for_vaccine(vaccine_name: str) -> List[str]:
    """Get dose labels for a specific vaccine."""
    doses = [item.dose_label for item in UIP_SCHEDULE if item.vaccine_name == vaccine_name]
    return sorted(doses, key=lambda x: (x.replace("Booster", "9"), x))
