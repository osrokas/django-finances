import calendar
from datetime import datetime


def current_month_range() -> tuple[str, str]:
    """
    Returns the start and end date of the current month.
    """
    current_date = datetime.today()

    current_year = current_date.year
    current_month = current_date.month

    curent_date_str = f"{current_year}-{current_month}-01"
    current_date = datetime.strptime(curent_date_str, "%Y-%m-%d")

    start_day, end_day = calendar.monthrange(current_year, current_month)

    if current_month < 10:
        current_month = f"0{current_month}"

    if start_day < 10:
        start_day = f"0{start_day}"

    start_date = f"{current_year}-{current_month}-{start_day}"
    end_date = f"{current_year}-{current_month}-{end_day}"

    return start_date, end_date


def total_month_data_parser(data) -> tuple[list[float], list[str]]:
    """
    Parses the data to get the total amount and labels for each month.
    """
    if data:
        total_by_month_amounts = [row.get('amount__sum') for row in data]
        total_by_month_labels = [row.get('month') for row in data]
    else:
        total_by_month_amounts = []
        total_by_month_labels = []

    return total_by_month_amounts, total_by_month_labels
