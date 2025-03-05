import openpyxl
from openpyxl.styles import Font

def format_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    # Bold headers and autofit columns
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for col in sheet.columns:
        max_length = max(len(str(cell.value)) for cell in col)
        sheet.column_dimensions[col[0].column_letter].width = max_length + 2
    wb.save('formatted_' + file_path)
    print("Excel file formatted!")

# Example usage:
format_excel('data.xlsx')