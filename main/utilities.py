from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(regex=r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$')
date_of_birth_validator = RegexValidator(regex=r'^(?:0[1-9]|[12]\d|3[01])([\/.-])(?:0[1-9]|1[012])\1(?:19|20)\d\d$',
                                         message='Example: 21.01.2001')

villages_of_Bershad_district = [
    'Баланівка', 'Березівка', 'Берізки-Бершадські', 'Бирлівка', 'Велика Киріївка',
    'Війтівка', 'Вовчок', 'Глинське', 'Голдашівка', 'Джулинка', 'Дяківка',
    'Звітне', 'Кавкули', 'Кидрасівка', 'Кошаринці', 'Красносілка', 'Крушинівка',
    'Лісниче', 'Лугова', 'Мала Киріївка', 'Маньківка', "М'якохід", 'Осіївка',
    "П'ятківка", 'Партизанське', 'Поташня', 'Романівка', 'Серебрія', 'Серединка',
    'Ставки', 'Сумівка', 'Теофілівка', 'Тернівка', 'Тирлівка', 'Устя',
    'Флорине', 'Хмарівка', 'Чернятка', 'Шляхова', 'Шумилів', 'Яланець'
]









