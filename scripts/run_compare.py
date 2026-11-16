# -*- coding: utf-8 -*-
import xlrd
import openpyxl
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment
from openpyxl.utils import get_column_letter
import os
import glob

DOWNLOAD_DIR = r"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\.playwright-cli"
OUTPUT_FILE = os.path.join(os.path.expanduser('~'), 'Desktop', '当日携转查询清单.xlsx')

file1_list = glob.glob(os.path.join(DOWNLOAD_DIR, 'CocExportMnpindex-*.xls'))
file2_list = glob.glob(os.path.join(DOWNLOAD_DIR, '*号码*.xls'))

if not file1_list:
    print("错误：找不到 CocExportMnpindex 文件")
    exit(1)
if not file2_list:
    print("错误：找不到 np 号码信息文件")
    exit(1)

file1 = file1_list[0]
file2 = file2_list[0]

print("文件 1:", os.path.basename(file1))
print("文件 2:", os.path.basename(file2))

print("\n[1/4] 正在读取携号转网申请查询文件...")
wb1 = xlrd.open_workbook(file1)
sheet1 = wb1.sheet_by_index(0)
print("      共 %d 条数据，%d 列" % (sheet1.nrows - 1, sheet1.ncols))

print("[2/4] 正在读取携号转网号码查询文件...")
wb2 = xlrd.open_workbook(file2)
sheet2 = wb2.sheet_by_index(0)
print("      共 %d 条数据，%d 列" % (sheet2.nrows - 1, sheet2.ncols))

print("[3/4] 正在提取携出方为中国移动的号码...")
mobile_numbers = set()
for row in range(1, sheet2.nrows):
    port_out = sheet2.cell_value(row, 4)
    if port_out == '中国移动':
        phone = str(sheet2.cell_value(row, 0)).strip()
        if phone:
            mobile_numbers.add(phone)
print("      共找到 %d 个号码" % len(mobile_numbers))

print("[4/4] 正在生成比对报告...")
new_wb = openpyxl.Workbook()
new_sheet = new_wb.active
new_sheet.title = "当日携转查询清单"

header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
header_font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
red_font = Font(name="微软雅黑", size=10, color="FFFFFF")
data_font = Font(name="微软雅黑", size=10)
alignment = Alignment(horizontal="center", vertical="center")
border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

headers = [sheet1.cell_value(0, col) for col in range(sheet1.ncols)]
for col_idx, header in enumerate(headers, 1):
    cell = new_sheet.cell(row=1, column=col_idx, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = alignment
    cell.border = border

marked_count = 0
for row_idx in range(1, sheet1.nrows):
    phone = str(sheet1.cell_value(row_idx, 3)).strip()
    is_marked = phone in mobile_numbers
    if is_marked:
        marked_count += 1
    for col_idx in range(sheet1.ncols):
        value = sheet1.cell_value(row_idx, col_idx)
        cell = new_sheet.cell(row=row_idx + 1, column=col_idx + 1, value=value)
        cell.font = data_font
        cell.alignment = alignment
        cell.border = border
        if is_marked and col_idx == 3:
            cell.fill = red_fill
            cell.font = red_font

for col_idx in range(1, sheet1.ncols + 1):
    col_letter = get_column_letter(col_idx)
    new_sheet.column_dimensions[col_letter].width = 15

new_wb.save(OUTPUT_FILE)

print("\n" + "="*60)
print("  处理完成！")
print("="*60)
print("  - 申请查询总数：%d 条" % (sheet1.nrows - 1))
print("  - 号码查询总数：%d 条" % (sheet2.nrows - 1))
print("  - 携出方为中国移动的号码：%d 个" % len(mobile_numbers))
print("  - 匹配并标红的号码：%d 条" % marked_count)
print("  - 输出文件：%s" % OUTPUT_FILE)
print("="*60)