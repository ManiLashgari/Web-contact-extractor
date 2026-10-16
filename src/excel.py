"""
Initialize an Excel workbook for storing extracted website contacts.

Creates a worksheet named "Contacts" and adds column headers
for the website, contact type, and extracted value.
"""

import os
from openpyxl import Workbook


def save_contacts(excel_path: str, website_url: str, contacts: dict[str: list[str]]) -> None:
    """
    Save extracted contact addresses to an Excel file.
    """

    row_number = 2

    if os.path.exists(excel_path):
        workbook = Workbook()
        worksheet = workbook.active

    else:
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Contacts"

        worksheet.cell(row= 1, column= 1, value="URL")
        worksheet.cell(row= 1, column= 2, value="Type")
        worksheet.cell(row= 1, column= 3, value="Value")

    for contact_type in contacts:
        for contact in contacts[contact_type]:
            #URL
            worksheet.cell(row= row_number, column= 1, value=website_url)
            #Type
            worksheet.cell(row= row_number, column= 2, value=contact_type)
            #Value
            worksheet.cell(row= row_number, column= 3, value=contact)

        row_number =+ 1

    workbook.save(excel_path)
