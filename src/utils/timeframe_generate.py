# Generate time range options dynamically
from datetime import timedelta, datetime


def generate_time_range_options():
    options = []
    current_date = datetime.now()

    # Add past hour option
    past_hour_start = current_date - timedelta(hours=1)
    past_hour_end = current_date
    options.append({'label': 'Past Hour',
                    'value': f'{past_hour_start.strftime("%Y-%m-%dT%H")} {past_hour_end.strftime("%Y-%m-%dT%H")}'})

    # Add past 4 hours option
    past_4_hours_start = current_date - timedelta(hours=4)
    past_4_hours_end = current_date
    options.append({'label': 'Past 4 Hours',
                    'value': f'{past_4_hours_start.strftime("%Y-%m-%dT%H")} {past_4_hours_end.strftime("%Y-%m-%dT%H")}'})

    # Add past day option
    past_day_start = current_date - timedelta(days=1)
    past_day_end = current_date
    options.append(
        {'label': 'Past Day', 'value': f'{past_day_start.strftime("%Y-%m-%d")} {past_day_end.strftime("%Y-%m-%d")}'})

    # Add past week option
    past_week_start = current_date - timedelta(weeks=1)
    past_week_end = current_date
    options.append(
        {'label': 'Past Week', 'value': f'{past_week_start.strftime("%Y-%m-%d")} {past_week_end.strftime("%Y-%m-%d")}'})

    # Add past 30 days option
    past_30_days_start = current_date - timedelta(days=30)
    past_30_days_end = current_date
    options.append({'label': 'Past 30 Days',
                    'value': f'{past_30_days_start.strftime("%Y-%m-%d")} {past_30_days_end.strftime("%Y-%m-%d")}'})

    # Add past 90 days option
    past_90_days_start = current_date - timedelta(days=90)
    past_90_days_end = current_date
    options.append({'label': 'Past 90 Days',
                    'value': f'{past_90_days_start.strftime("%Y-%m-%d")} {past_90_days_end.strftime("%Y-%m-%d")}'})

    # Add past 12 months option
    past_12_months_start = current_date - timedelta(days=365)
    past_12_months_end = current_date
    options.append({'label': 'Past 12 Months',
                    'value': f'{past_12_months_start.strftime("%Y-%m-%d")} {past_12_months_end.strftime("%Y-%m-%d")}'})

    # Add past 5 years option
    past_5_years_start = current_date - timedelta(days=365 * 5)
    past_5_years_end = current_date
    options.append({'label': 'Past 5 Years',
                    'value': f'{past_5_years_start.strftime("%Y-%m-%d")} {past_5_years_end.strftime("%Y-%m-%d")}'})

    # Add since 2004 option
    since_2004_start = datetime(2004, 1, 1)
    since_2004_end = current_date
    options.append({'label': 'Since 2004',
                    'value': f'{since_2004_start.strftime("%Y-%m-%d")} {since_2004_end.strftime("%Y-%m-%d")}'})

    return options


def generate_time_slices(start_time, end_time, interval, count, unit):
    slices = []
    current_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    interval = timedelta(**{unit: interval})
    format_str = '%Y-%m-%dT%H'
    if unit == 'days':
        format_str = '%Y-%m-%d'
    while len(slices) < count and current_time <= end_time:
        end_of_slice = current_time + interval - timedelta(**{unit: 1})
        slice_str = f"{current_time.strftime(format_str)} {end_of_slice.strftime(format_str)}"
        slices.append(slice_str)
        current_time += interval

    return slices
