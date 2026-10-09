"""
Initialize an Excel workbook for storing extracted website contacts.

Creates a worksheet named "Contacts" and adds column headers
for the website, contact type, and extracted value.
"""

import os
from openpyxl import Workbook


def save_contacts(excel_path: str, website_url: str, data: list[str]) -> None:
    """
    Save extracted email addresses to an Excel file.
    """

    if os.path.exists(excel_path):
        workbook = Workbook()
        worksheet = workbook.active

    else:
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Contacts"
        worksheet.append(["Website", "Type", "Value"])

    for email in data:
        worksheet.append([website_url, "Email", email])

    workbook.save(excel_path)
