from openpyxl import Workbook

workbook = Workbook()
worksheet = workbook.active()

worksheet.title = "Contacts"
worksheet.append(["Website", "Type", "Value"])