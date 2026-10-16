"""
Initialize an Excel workbook for storing extracted website contacts.

Creates a worksheet named "Contacts" and adds column headers
for the website, contact type, and extracted value.
"""

import os
from openpyxl import Workbook, load_workbook


def save_contacts(
    excel_path: str,
    website_url: str,
    contacts: dict[str, list[str]],
) -> None:
    """
    Save extracted contacts to an Excel file.

    Create a new workbook with headers if the file does not exist.
    Otherwise, append contacts to the existing workbook.

    Args:
        excel_path: Path to the Excel file.
        website_url: URL of the website being processed.
        contacts: Dictionary mapping contact types to lists of values.
    """
    if os.path.exists(excel_path):
        workbook = load_workbook(excel_path)
        worksheet = (
            workbook["Contacts"]
            if "Contacts" in workbook.sheetnames
            else workbook.create_sheet("Contacts")
        )

        if worksheet.max_row == 1 and worksheet["A1"].value is None:
            worksheet.append(["URL", "Type", "Value"])
    else:
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Contacts"
        worksheet.append(["URL", "Type", "Value"])

    row_number = worksheet.max_row + 1

    for contact_type, contact_list in contacts.items():
        for contact in contact_list:
            worksheet.cell(row=row_number, column=1, value=website_url)
            worksheet.cell(row=row_number, column=2, value=contact_type)
            worksheet.cell(row=row_number, column=3, value=contact)
            row_number += 1

    workbook.save(excel_path)
