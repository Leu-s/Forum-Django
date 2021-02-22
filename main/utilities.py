import datetime


def available_birth_years(min_year=1900):
    return [f'{year}' for year in range(min_year, datetime.datetime.now().year+1)]










