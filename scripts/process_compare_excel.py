import xlrd
import openpyxl
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment
from openpyxl.utils import get_column_letter
import os
import glob
import sys

# 配置
DOWNLOAD_DIR = r"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\.playwright-cli"
OUTPUT_FILE = os.path.join(os.path.expanduser('~'), 'Desktop', '当日携转查询清单.xlsx')

def find_file(pattern):
    """查找匹配的文件"""
    files = glob.glob(os.path.join(DOWNLOAD_DIR, pattern))
    if files:
        return files[0]
    return None

def main():
    print("=" * 60)
    print("  携号转网 Excel 比对处理")
    print("=" * 60)
    
    # 查找文件
    file1_pattern = 'CocExportMnpindex-*.xls'
    file2_pattern = 'np 号码信息*.xls'
    
    file1 = find_file(file1_pattern)
    file2 = find_file(file2_pattern)
    
    if not file1:
        print(f"错误：找不到文件 {file1_pattern}")
        sys.exit(1)
    
    if not file2:
        print(f"错误：找不到文件 {file2_pattern}")
        sys.exit(1)
    
    print(f"\n文件 1: {os.path.basename(file1)}")
    print(f"文件 2: {os.path.basename(file2)}")
    
    # 读取文件 1
    print("\n[1/4] 正在读取携号转网申请查询文件...")
    wb1 = xlrd.open_workbook(file1)
    sheet1 = wb1.sheet_by_index(0)
    print(f"      共 {sheet1.nrows - 1} 条数据，{sheet1.ncols} 列")
    
    # 读取文件 2
    print("[2/4] 正在读取携号转网号码查询文件...")
    wb2 = xlrd.open_workbook(file2)
    sheet2 = wb2.sheet_by_index(0)
    print(f"      共 {sheet2.nrows - 1} 条数据，{sheet2.ncols} 列")
    
    # 提取中国移动号码
    print("[3/4] 正在提取携出方为'中国移动'的号码...")
    mobile_numbers = set()
    for row in range(1, sheet2.nrows):
        port_out = sheet2.cell_value(row, 4)  # E 列 - 携出方网络标识
        if port_out == '中国移动':
            phone = str(sheet2.cell_value(row, 0)).strip()  # A 列 - 用户号码
            if phone:
                mobile_numbers.add(phone)
    
    print(f"      共找到 {len(mobile_numbers)} 个号码")
    
    # 创建新 Excel
    print("[4/4] 正在生成比对报告...")
    new_wb = openpyxl.Workbook()
    new_sheet = new_wb.active
    new_sheet.title = "当日携转查询清单"
    
    # 样式定义
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
    red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
    red_font = Font(name="微软雅黑", size=10, color="FFFFFF")
    data_font = Font(name="微软雅黑", size=10)
    alignment = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # 写入表头
    headers = [sheet1.cell_value(0, col) for col in range(sheet1.ncols)]
    for col_idx, header in enumerate(headers, 1):
        cell = new_sheet.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = alignment
        cell.border = border
    
    # 写入数据
    marked_count = 0
    for row_idx in range(1, sheet1.nrows):
        phone = str(sheet1.cell_value(row_idx, 3)).strip()  # D 列 - 手机号码
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
    
    # 设置列宽
    for col_idx in range(1, sheet1.ncols + 1):
        col_letter = get_column_letter(col_idx)
        new_sheet.column_dimensions[col_letter].width = 15
    
    # 保存文件
    new_wb.save(OUTPUT_FILE)
    
    print(f"\n{'=' * 60}")
    print(f"  处理完成！")
    print(f"{'=' * 60}")
    print(f"\n统计信息:")
    print(f"  - 申请查询总数：{sheet1.nrows - 1} 条")
    print(f"  - 号码查询总数：{sheet2.nrows - 1} 条")
    print(f"  - 携出方为中国移动的号码：{len(mobile_numbers)} 个")
    print(f"  - 匹配并标红的号码：{marked_count} 条")
    print(f"\n输出文件:")
    print(f"  {OUTPUT_FILE}")
    print(f"\n{'=' * 60}")

if __name__ == '__main__':
    main()