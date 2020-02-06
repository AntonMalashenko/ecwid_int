# -*- coding: UTF-8 -*-

import os
from datetime import datetime

import openpyxl
from openpyxl.styles import Alignment, Color, PatternFill, Font, Border, Side
from openpyxl.styles.colors import YELLOW, BLACK, DARKYELLOW

from settings.app_settings import FILES_PATH
from settings.table_constants import HEADER, SITE_URL
from src.utils import clean_phone


def make_table(data, products):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    header_allignment = Alignment(horizontal='center',
                                  vertical='center',
                                  text_rotation=0,
                                  wrap_text=False,
                                  shrink_to_fit=False,
                                  indent=0)

    for index, col in enumerate(HEADER, start=1):
        cell = sheet.cell(row=1, column=index, value=col)

        cell.alignment = header_allignment
        cell.border = Border(
            left=Side(border_style='thin',
                      color=BLACK),
            right=Side(border_style='thin',
                       color=BLACK),
            top=Side(border_style='thin',
                     color=BLACK),
            bottom=Side(border_style='thin',
                        color=BLACK
                        )
        )
        cell.font = Font(size=12, )
        if index % 2 == 0:
            cell.fill = PatternFill(start_color=YELLOW,
                                    end_color=YELLOW,
                                    fill_type='solid')
        else:
            cell.fill = PatternFill(start_color=DARKYELLOW,
                                    end_color=DARKYELLOW,
                                    fill_type='solid')
        sheet.column_dimensions[cell.column_letter].width = 40
    sheet.row_dimensions[1].height = 60

    row =2
    for order in data:
        person = order.get('shippingPerson') \
            if order.get('shippingPerson') \
            else order.get('billingPerson')
        if person.get('countryCode') != 'RU':
            continue

        product = products.get(order.get('productId')) or dict()

        sheet.cell(row=row, column=1, value=order.get('vendorOrderNumber'))
        sheet.cell(row=row, column=2, value=order.get("Barcode_of_pallet"))  # not found
        sheet.cell(row=row, column=3, value=order.get("Barcode_of_main_box"))  # not found
        sheet.cell(row=row, column=4, value=order.get("barcode_of_parcel"))  # not found
        try:
            sheet.cell(row=row, column=5, value=order.get('predictedPackage')[0].get('length') * 10)
            sheet.cell(row=row, column=6, value=order.get('predictedPackage')[0].get("width") * 10)
            sheet.cell(row=row, column=7, value=order.get('predictedPackage')[0].get("height") * 10)
        except:
            sheet.cell(row=row, column=5, value='Unknown')
            sheet.cell(row=row, column=6, value='Unknown')
            sheet.cell(row=row, column=7, value='Unknown')
        sheet.cell(row=row, column=8, value=order.get('delivery_type'))  # not found
        sheet.cell(row=row, column=9, value=order.get('pup_code'))  # not found
        name = person.get('name')
        sheet.cell(row=row, column=10, value=name)  # "Фамилия Имя Отчество  получателя/\nName Surname Middle name",

        phone = person.get('phone')
        if phone:
            phone = clean_phone(phone)
        sheet.cell(row=row, column=11, value=phone)  # "Телефон получателя  (7 XXX XXX XXXX)/\nRecipient's phone number",

        country_code = person.get('countryCode')
        sheet.cell(row=row, column=12, value=country_code)  #  "Код страны назначения\n(ISO 3166-1, 643 для России)/\nCode of country of destina

        postal_code = person.get('postalCode')
        sheet.cell(row=row, column=13, value=postal_code)  # "Почтовый индекс получателя/\nRecipient's ZIP code",

        city = person.get('city')
        sheet.cell(row=row, column=14, value=city)  # "Город получателя/\nRecipient's city",

        address = "{}({}), {}".format(
            person.get('stateOrProvinceName'),
            person.get('stateOrProvinceCode'),
            person.get('street')
        )
        sheet.cell(row=row, column=15, value=address)  #  "Адрес получателя/\nRecipient's address",
        sheet.cell(row=row, column=16, value=order.get('sku'))  #   "Артикул товара/\nItem ID or SKU",

        try:
            prod_attrs = product.get('attributes')
        except AttributeError:
            prod_attrs = dict()
        brand = ''
        if prod_attrs:
            for attr in prod_attrs:
                if attr.get('type') == 'BRAND':
                    brand = attr.get('value')
        sheet.cell(row=row, column=17, value=brand)  #  "Производитель/\nБренд/\nBrand/\nProducer/\nTrademark",
        sheet.cell(row=row, column=18, value=product.get('name'))  #   "Наименование/\nItem name (Model)",
        sheet.cell(row=row, column=19, value=order.get('quantity'))  # "Количество/\nQuantity",
        sheet.cell(row=row, column=20, value=product.get('price'))  #   "Цена 1 единицы/\nPrice for 1 item",
        sheet.cell(row=row, column=21, value="USD")  # "Валюта цены  (EUR, USD, GBP, RUB)/\nCurrency",
        try:
            sheet.cell(row=row, column=22, value=product.get('weight'))  # "Вес брутто 1 единицы (грамм)/\nGross weight of 1 item (gr)",
        except TypeError:
            sheet.cell(row=row, column=22, value='Unknown')

        url = product.get('url') if product else ''
        sheet.cell(row=row, column=23, value=url)  # "Ссылка на товар в \nинтернет-магазине/\nLink to the item innan online-store",
        sheet.cell(row=row, column=24, value=SITE_URL)  #  "Адрес интернет-магазина/\nOnline shop website",
        sheet.cell(row=row, column=25, value=order.get('HS_Code'))  # not found   "Код ТН ВЭД/\nHS Code",
        sheet.cell(row=row, column=26, value=order.get('shortDescription'))  #   "Краткое описание \n(на языке поставщика)/\nItem Description in English",

        translated_descr = order.get('shortDescriptionTranslated').get(
            'ru') if order.get('shortDescriptionTranslated') else ''
        sheet.cell(row=row, column=27, value=translated_descr)  # "Краткое описание (рус)/\nItem description in Russian",
        sheet.cell(row=row, column=28, value=order.get('email'))  #    "Customer's E-mail/\nE-mail получателя",
        sheet.cell(row=row, column=29, value=order.get('passport country'))  # not found   "Код страны выдавшей паспорт/\nPassport country code(ISO 3166-1)",
        sheet.cell(row=row, column=30, value=order.get('Passport series '))  # not found   "Серия и номер паспорта/\nPassport series and number",
        sheet.cell(row=row, column=31, value=order.get('Passport date'))  # not found   "Дата выдачи паспорта ДД.ММ.ГГГГ/\nPassport date of issue DD.MM.YYYY",
        sheet.cell(row=row, column=32, value=order.get('assport issued by'))  # not found   "Кем выдан паспорт/\nPassport issued by",
        sheet.cell(row=row, column=33, value=order.get('Notification number'))  # not found   "Номер нотификации/\nNotification number",
        sheet.cell(row=row, column=34, value=order.get('otification expiration date'))  # not found   "Дата окончания\nдействия нотификации/\nNotification expiration date",
        sheet.cell(row=row, column=35, value=order.get('Notification code'))  # not found   "Код нотификации/\nNotification code",
        sheet.cell(row=row, column=36, value=order.get('Individual Tax ID'))  # not found   "ИНН получателя/\nIndividual Tax ID (INN)",
        row += 1

    for col in [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 16, 19, 20, 21,
                22, 25, 29, 30, 31, 32, 33, 34, 35, 36,]:
        sheet.column_dimensions[
            sheet.cell(row=row, column=col).column_letter].width = 20

    for col in [18, 23, 26]:
        sheet.column_dimensions[
            sheet.cell(row=row, column=col).column_letter].width = 100

    save_table(workbook)


def save_table(wb):
    now = datetime.now().strftime("%d_%m_%Y_%H_%M")
    filename = now + ".xls"
    path = os.path.join(FILES_PATH, filename)
    wb.save(filename=path)
    print("### file {} created".format(path))