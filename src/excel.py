"""
Utilities for saving extracted website contacts to Excel files.
"""

import os
from openpyxl import Workbook, load_workbook


def save_contacts(
    excel_path: str,
    website_url: str,
    contacts: dict[str, list[str]],
) -> None:
    """
    Save extracted contacts to an Excel file without duplicates.

    Create a new workbook with headers if the file does not exist.
    Otherwise, append only contacts that are not already present.

    Args:
        excel_path: Path to the Excel file.
        website_url: URL of the website being processed.
        contacts: Dictionary mapping contact types to lists of values.
    """
    os.makedirs(os.path.dirname(excel_path) or ".", exist_ok=True)

    if os.path.exists(excel_path):
        workbook = load_workbook(excel_path)
        if "Contacts" in workbook.sheetnames:
            worksheet = workbook["Contacts"]
        else:
            worksheet = workbook.create_sheet("Contacts")
    else:
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Contacts"

    # Add headers if the first row is empty.
    if all(
        worksheet.cell(row=1, column=col).value is None
        for col in range(1, 4)
    ):
        worksheet.cell(row=1, column=1, value="URL")
        worksheet.cell(row=1, column=2, value="Type")
        worksheet.cell(row=1, column=3, value="Value")

    # Collect existing contact records, starting after the header.
    existing_contacts = {
        (row[0], row[1], row[2])
        for row in worksheet.iter_rows(
            min_row=2,
            max_col=3,
            values_only=True,
        )
        if all(value is not None for value in row)
    }

    # Insert only new contacts.
    for contact_type, contact_list in contacts.items():
        for contact in contact_list:
            contact_record = (website_url, contact_type, contact)

            if contact_record not in existing_contacts:
                worksheet.append(list(contact_record))
                existing_contacts.add(contact_record)

    workbook.save(excel_path)
