import os
import string
from datetime import datetime
from functools import partial

import openpyxl
from openpyxl.styles import Alignment, Font

from settings.app_settings import FILES_PATH
from settings.table_constants import HEADER, SITE_URL
from src.utils import clean_phone

CYRILLIC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
ALLOWED_SYMBOLS = string.printable + CYRILLIC


def clean_description(text: str) -> str:
    result = filter(lambda x: x if x in ALLOWED_SYMBOLS else '', text)
    return ''.join(result)


def make_table(data, products, multiplier, dimensions, delivery_type, dimconv, country_code):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    header_alignment = Alignment(
        horizontal='center',
        vertical='center',
        text_rotation=0,
        wrap_text=False,
        shrink_to_fit=False,
        indent=0)

    for index, col in enumerate(HEADER, start=1):
        set_cell = sheet.cell(row=1, column=index, value=col)

        set_cell.alignment = header_alignment
        set_cell.font = Font(size=12, )
        sheet.column_dimensions[set_cell.column_letter].width = 40

    sheet.row_dimensions[1].height = 60

    row = 2
    for order in data:
        set_cell = partial(sheet.cell, row=row)
        person = order.get('shippingPerson') \
            if order.get('shippingPerson') \
            else order.get('billingPerson')
        if person.get('countryCode') != 'RU':
            continue

        product = products.get(order.get('productId')) or dict()

        set_cell(column=1, value=order.get('vendorOrderNumber'))
        # set_cell(column=2-2, value=order.get("Barcode_of_pallet"))  # not found
        # set_cell(column=3-2, value=order.get("Barcode_of_main_box"))  # not found
        set_cell(column=2, value=order.get("barcode_of_parcel"))  # not found
        try:
            dimension_multiplier = 10 if dimconv else 1
            set_cell(column=3, value=order.get('predictedPackage')[0].get('length', 3) * dimension_multiplier)
            set_cell(column=4, value=order.get('predictedPackage')[0].get("width", 3) * dimension_multiplier)
            set_cell(column=5, value=order.get('predictedPackage')[0].get("height", 3) * dimension_multiplier)
        except:
            set_cell(column=3, value=dimensions[0])
            set_cell(column=4, value=dimensions[1])
            set_cell(column=5, value=dimensions[2])

        set_cell(column=6, value=delivery_type)  # not found
        set_cell(column=7, value=order.get('pup_code'))  # not found
        name = person.get('name')
        set_cell(column=8, value=name)  # "Фамилия Имя Отчество  получателя/\nName Surname Middle name",

        phone = person.get('phone')
        if phone:
            phone = clean_phone(phone)
        set_cell(column=9, value=phone)  # "Телефон получателя  (7 XXX XXX XXXX)/\nRecipient's phone number",

        # country_code = person.get('countryCode')
        set_cell(column=10, value=country_code)  # "Код страны назначения\n(ISO 3166-1, 643 для России)/\nCode of country of destina

        postal_code = person.get('postalCode')
        try:
            postal_code = int(postal_code)
        except:
            postal_code = ''
        set_cell(column=11, value=postal_code)  # "Почтовый индекс получателя/\nRecipient's ZIP code",

        city = person.get('city')
        set_cell(column=12, value=city)  # "Город получателя/\nRecipient's city",

        address = "{}({}), {}".format(
            person.get('stateOrProvinceName'),
            person.get('stateOrProvinceCode'),
            person.get('street')
        )
        set_cell(column=13, value=address)  # "Адрес получателя/\nRecipient's address",
        set_cell(column=14, value=order.get('sku'))  # "Артикул товара/\nItem ID or SKU",

        try:
            prod_attrs = product.get('attributes')
        except AttributeError:
            prod_attrs = dict()
        brand = 'unknown'
        if prod_attrs:
            for attr in prod_attrs:
                if attr.get('type') == 'BRAND':
                    brand = attr.get('value')
        set_cell(column=15, value=brand)  # "Производитель/\nБренд/\nBrand/\nProducer/\nTrademark",
        set_cell(column=16, value=product.get('name'))  # "Наименование/\nItem name (Model)",
        set_cell(column=17, value=order.get('quantity'))  # "Количество/\nQuantity",

        price = product.get('price')
        if price:
            price = round(float(price * multiplier), 2)
        set_cell(column=18, value=price)  # "Цена 1 единицы/\nPrice for 1 item",
        set_cell(column=19, value="USD")  # "Валюта цены  (EUR, USD, GBP, RUB)/\nCurrency",
        try:
            set_cell(column=20, value=product.get('weight'))  # "Вес брутто 1 единицы (грамм)/\nGross weight of 1 item (gr)",
        except TypeError:
            set_cell(column=20, value='Unknown')

        url = product.get('url') if product else ''
        set_cell(column=21, value=url)  # "Ссылка на товар в \nинтернет-магазине/\nLink to the item innan online-store",
        set_cell(column=22, value=SITE_URL)  # "Адрес интернет-магазина/\nOnline shop website",
        set_cell(column=23, value=order.get('HS_Code'))  # not found   "Код ТН ВЭД/\nHS Code",
        set_cell(column=24, value=clean_description(order.get('shortDescription', '')))  # "Краткое описание \n(на языке поставщика)/\nItem Description in English",

        translated_descr = order\
            .get('shortDescriptionTranslated')\
            .get('ru') \
            if order.get('shortDescriptionTranslated') \
            else ''

        set_cell(column=25, value=clean_description(translated_descr))  # "Краткое описание (рус)/\nItem description in Russian",
        set_cell(column=26, value=order.get('email'))  # "Customer's E-mail/\nE-mail получателя",
        set_cell(column=27, value=order.get('passport country'))  # not found   "Код страны выдавшей паспорт/\nPassport country code(ISO 3166-1)",
        set_cell(column=28, value=order.get('Passport series '))  # not found   "Серия и номер паспорта/\nPassport series and number",
        set_cell(column=29, value=order.get('Passport date'))  # not found   "Дата выдачи паспорта ДД.ММ.ГГГГ/\nPassport date of issue DD.MM.YYYY",
        set_cell(column=30, value=order.get('assport issued by'))  # not found   "Кем выдан паспорт/\nPassport issued by",
        set_cell(column=31, value=order.get('Notification number'))  # not found   "Номер нотификации/\nNotification number",
        set_cell(column=32, value=order.get('otification expiration date'))  # not found   "Дата окончания\nдействия нотификации/\nNotification expiration date",
        set_cell(column=33, value=order.get('Notification code'))  # not found   "Код нотификации/\nNotification code",
        set_cell(column=34, value=order.get('Individual Tax ID'))  # not found   "ИНН получателя/\nIndividual Tax ID (INN)",
        row += 1

    # no need to set cols size
    # for col in [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 16, 19, 20, 21, 22, 25, 29, 30, 31, 32, 33, 34, 35, 36, ]:
    #     sheet.column_dimensions[set_cell(column=col).column_letter].width = 20
    #
    # for col in [18, 23, 26]:
    #     sheet.column_dimensions[set_cell(column=col).column_letter].width = 100

    save_table(workbook)


def save_table(wb):
    now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    filename = now + ".xls"
    path = os.path.join(FILES_PATH, filename)
    wb.save(filename=path)
    print("### file {} created".format(path))
