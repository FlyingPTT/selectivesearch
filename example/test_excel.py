import openpyxl as opx
import os

root = r'D:\Github\selectivesearch\out'
excel_name = '1.xlsx'
excel_path = os.path.join(root, excel_name)
wb = opx.load_workbook(excel_path)
ws = wb.active
print(ws.cell(1,1).value)
for i in range(3):
    ws.append([1,2,3,1212])
wb.save(excel_path)