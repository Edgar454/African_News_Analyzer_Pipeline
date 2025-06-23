from datetime import datetime, timedelta

def get_week_range(reference_date=None):
    if reference_date is None:
        reference_date = datetime.now()
    
    start_of_week = reference_date - timedelta(days=reference_date.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    
    return start_of_week.date(), end_of_week.date()