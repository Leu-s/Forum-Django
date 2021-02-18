from django.core.validators import RegexValidator, ValidationError
import re
import datetime


phone_number_validator = RegexValidator(regex=r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$')


def date_of_birth_validator(value):
    """dd/mm/yyyy, dd-mm-yyyy или dd.mm.yyyy. 1900-today"""
    regex = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)'
                       r'(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/'
                       r'|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579]'
                       r'[26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2'
                       r'[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
    result = re.fullmatch(regex, value)
    if result:
        check_result = result[0]
        date_to_str = f'{check_result[:2]}.{check_result[3:5]}.{check_result[6:10]}'
        min_date = datetime.datetime(day=1, month=1, year=1900)
        max_date = datetime.datetime.now()
        user_date = datetime.datetime.strptime(date_to_str, "%d.%m.%Y")
        if user_date > max_date:
            raise ValidationError(f'Вказана дата виходить за допустимі рамки '
                                  f'(01.01.1900-{datetime.datetime.now().strftime("%Y-%m-%d")}')
        elif user_date < min_date:
            raise ValidationError(f'Вказана дата виходить за допустимі рамки '
                                  f'(01.01.1900-{datetime.datetime.now().strftime("%Y-%m-%d")})')
        else:
            return value
    else:
        raise ValidationError('Перевірте, будь-ласка, введені дані на коректність. '
                              'Допустимий формат дати: дд.мм.рррр, та символи - . /')
