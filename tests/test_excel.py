"""Tests for excel.py"""
from openpyxl import load_workbook

from src.excel import save_contacts


def test_creates_excel_file_with_headers(tmp_path):
    """Create a new workbook with the expected headers."""
    excel_path = tmp_path / "contacts.xlsx"

    save_contacts(str(excel_path), "https://example.com", {})

    assert excel_path.exists()

    workbook = load_workbook(excel_path)
    worksheet = workbook["Contacts"]

    assert [worksheet.cell(row=1, column=col).value for col in range(1, 4)] == [
        "URL",
        "Type",
        "Value",
    ]

    workbook.close()


def test_saves_contacts(tmp_path):
    """Save email and phone contacts to Excel."""
    excel_path = tmp_path / "contacts.xlsx"
    website_url = "https://example.com"
    contacts = {
        "email": ["info@example.com", "support@example.com"],
        "phone": ["+1234567890"],
    }

    save_contacts(str(excel_path), website_url, contacts)

    workbook = load_workbook(excel_path)
    worksheet = workbook["Contacts"]

    rows = list(
        worksheet.iter_rows(min_row=2, max_col=3, values_only=True)
    )

    assert rows == [
        (website_url, "email", "info@example.com"),
        (website_url, "email", "support@example.com"),
        (website_url, "phone", "+1234567890"),
    ]

    workbook.close()


def test_does_not_add_duplicate_contacts(tmp_path):
    """Calling save_contacts twice should not duplicate records."""
    excel_path = tmp_path / "contacts.xlsx"
    website_url = "https://example.com"
    contacts = {
        "email": ["info@example.com"],
        "phone": ["+1234567890"],
    }

    save_contacts(str(excel_path), website_url, contacts)
    save_contacts(str(excel_path), website_url, contacts)

    workbook = load_workbook(excel_path)
    worksheet = workbook["Contacts"]

    rows = list(
        worksheet.iter_rows(min_row=2, max_col=3, values_only=True)
    )

    assert len(rows) == 2
    assert rows == [
        (website_url, "email", "info@example.com"),
        (website_url, "phone", "+1234567890"),
    ]

    workbook.close()


def test_appends_new_contacts_without_removing_existing_ones(tmp_path):
    """Keep existing records and append only new contacts."""
    excel_path = tmp_path / "contacts.xlsx"
    website_url = "https://example.com"

    save_contacts(
        str(excel_path),
        website_url,
        {"email": ["info@example.com"]},
    )

    save_contacts(
        str(excel_path),
        website_url,
        {
            "email": ["info@example.com", "support@example.com"],
            "phone": ["+1234567890"],
        },
    )

    workbook = load_workbook(excel_path)
    worksheet = workbook["Contacts"]

    rows = list(
        worksheet.iter_rows(min_row=2, max_col=3, values_only=True)
    )

    assert rows == [
        (website_url, "email", "info@example.com"),
        (website_url, "email", "support@example.com"),
        (website_url, "phone", "+1234567890"),
    ]

    workbook.close()


def test_same_contact_for_different_websites_is_kept(tmp_path):
    """A contact record includes its website URL."""
    excel_path = tmp_path / "contacts.xlsx"

    save_contacts(
        str(excel_path),
        "https://example.com",
        {"email": ["info@example.com"]},
    )

    save_contacts(
        str(excel_path),
        "https://another-example.com",
        {"email": ["info@example.com"]},
    )

    workbook = load_workbook(excel_path)
    worksheet = workbook["Contacts"]

    rows = list(
        worksheet.iter_rows(min_row=2, max_col=3, values_only=True)
    )

    assert rows == [
        ("https://example.com", "email", "info@example.com"),
        ("https://another-example.com", "email", "info@example.com"),
    ]

    workbook.close()


def test_creates_missing_parent_directories(tmp_path):
    """Create parent directories when they do not exist."""
    excel_path = tmp_path / "output" / "nested" / "contacts.xlsx"

    save_contacts(
        str(excel_path),
        "https://example.com",
        {"email": ["info@example.com"]},
    )

    assert excel_path.exists()


def test_creates_contacts_sheet_if_missing(tmp_path):
    """Add a Contacts sheet when an existing workbook lacks it."""
    excel_path = tmp_path

    assert excel_path
