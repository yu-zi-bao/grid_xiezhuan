# -*- coding: utf-8 -*-
r"""
generate_xlsx.py — 从《携转结果.txt》生成《携转结果.xlsx》
功能：读取桌面的携转结果.txt（Tab分隔），生成含两个Sheet的Excel文件：
  Sheet1「携转明细」：序号/手机号/区县/申请时间/类型/网格（60行数据）
  Sheet2「网格统计」：序号/网格名称/号码数量/手机号列表（20行+合计行）
输出：C:\Users\Administrator\Desktop\携转结果.xlsx

用法：
  python generate_xlsx.py [输入文件路径] [输出文件路径]
  默认输入：C:\Users\Administrator\Desktop\携转结果.txt
  默认输出：C:\Users\Administrator\Desktop\携转结果.xlsx
"""

import os
import sys
import re

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: openpyxl not installed. Run: pip install openpyxl")
    sys.exit(1)


def parse_txt(txt_path):
    """解析携转结果.txt，返回明细记录列表和网格统计列表"""
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 尝试 Tab 分隔格式（SKILL.md 标准格式）
    lines = content.strip().split('\n')
    if '\t' in lines[0]:
        return parse_tab_format(lines, content)
    else:
        return parse_formatted_format(content)


def parse_tab_format(lines, content):
    """解析 Tab 分隔格式：手机号码\t最近一次申请时间\t申请内容\tGRID_NAME"""
    records = []
    for i, line in enumerate(lines):
        if i == 0:  # 跳过表头
            continue
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            records.append({
                'phone': parts[0].strip(),
                'time': parts[1].strip(),
                'type': parts[2].strip(),
                'grid': parts[3].strip(),
            })

    # 生成网格统计
    grid_map = {}  # grid -> [phones]
    for r in records:
        g = r['grid']
        if g:
            if g not in grid_map:
                grid_map[g] = []
            grid_map[g].append(r['phone'])

    grid_stats = [(g, len(phones), ', '.join(phones)) for g, phones in grid_map.items()]  # v29: 顿号改为逗号+空格
    grid_stats.sort(key=lambda x: -x[1])  # 按数量降序

    return records, grid_stats


def parse_formatted_format(content):
    """解析格式化报告格式（含手机号：XXX | 区县：XXX | ... 的报告）"""
    detail_pat = r'手机号：(\S+)\s*\|\s*区县：(\S+)\s*\|\s*申请时间：([\d\-]+ [\d:]+)\s*\|\s*类型：(\S+)\s*\|\s*网格：(\S+)'
    records_raw = re.findall(detail_pat, content)

    records = []
    for r in records_raw:
        records.append({
            'phone': r[0],
            'district': r[1],
            'time': r[2],
            'type': r[3],
            'grid': r[4],
        })

    # 解析网格统计
    grid_pat = r'([\u4e00-\u9fa5]+网格)：(\d+)个[（(](.+?)[）)]'  # v29: 兼容半角和全角括号
    grid_stats_raw = re.findall(grid_pat, content)
    grid_stats = [(g[0], int(g[1]), g[2]) for g in grid_stats_raw]

    return records, grid_stats


def generate_xlsx(records, grid_stats, output_path):
    """生成Excel文件"""
    wb = Workbook()

    # === 样式定义 ===
    header_font = Font(name='Calibri', bold=True, color='FFFFFFFF', size=11)
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    data_font = Font(name='Calibri', size=11)
    total_font = Font(name='Calibri', bold=True, size=11)
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9'),
    )
    center_align = Alignment(horizontal='center', vertical='center')

    # === Sheet1: 携转明细 ===
    ws1 = wb.active
    ws1.title = '携转明细'

    # 检查数据是否有区县字段（格式化报告格式有，Tab格式没有）
    has_district = len(records) > 0 and 'district' in records[0]

    if has_district:
        headers1 = ['序号', '手机号', '区县', '申请时间', '类型', '网格']
        col_widths1 = [6, 15, 10, 22, 22, 22]
    else:
        headers1 = ['序号', '手机号码', '最近一次申请时间', '申请内容', 'GRID_NAME']
        col_widths1 = [6, 15, 22, 22, 22]

    # 写表头
    for col_idx, header in enumerate(headers1, 1):
        cell = ws1.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = center_align

    # 写数据
    for row_idx, r in enumerate(records, 2):
        if has_district:
            values = [row_idx - 1, r['phone'], r['district'], r['time'], r['type'], r['grid']]
        else:
            values = [row_idx - 1, r['phone'], r['time'], r['type'], r['grid']]

        for col_idx, val in enumerate(values, 1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.border = thin_border

    # 设置列宽
    for col_idx, width in enumerate(col_widths1, 1):
        ws1.column_dimensions[get_column_letter(col_idx)].width = width

    # 冻结首行
    ws1.freeze_panes = 'A2'

    # === Sheet2: 网格统计 ===
    ws2 = wb.create_sheet('网格统计')
    headers2 = ['序号', '网格名称', '号码数量', '手机号列表']
    col_widths2 = [6, 22, 10, 80]

    # 写表头
    for col_idx, header in enumerate(headers2, 1):
        cell = ws2.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = center_align

    # 写数据
    for row_idx, g in enumerate(grid_stats, 2):
        values = [row_idx - 1, g[0], g[1], g[2]]
        for col_idx, val in enumerate(values, 1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.border = thin_border

    # 合计行
    total_row = len(grid_stats) + 2
    ws2.cell(row=total_row, column=1, value='合计').font = total_font
    ws2.cell(row=total_row, column=1).border = thin_border
    ws2.cell(row=total_row, column=2).border = thin_border
    # 号码数量合计用公式
    total_cell = ws2.cell(row=total_row, column=3, value=f'=SUM(C2:C{total_row - 1})')
    total_cell.font = total_font
    total_cell.border = thin_border
    ws2.cell(row=total_row, column=4).border = thin_border

    # 设置列宽
    for col_idx, width in enumerate(col_widths2, 1):
        ws2.column_dimensions[get_column_letter(col_idx)].width = width

    # 冻结首行
    ws2.freeze_panes = 'A2'

    # 保存
    wb.save(output_path)
    return len(records), len(grid_stats)


def main():
    txt_path = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Administrator\Desktop\携转结果.txt'
    output_path = sys.argv[2] if len(sys.argv) > 2 else r'C:\Users\Administrator\Desktop\携转结果.xlsx'

    if not os.path.exists(txt_path):
        print(f"ERROR: 输入文件不存在: {txt_path}")
        sys.exit(1)

    records, grid_stats = parse_txt(txt_path)
    print(f"解析到 {len(records)} 条明细记录, {len(grid_stats)} 条网格统计")

    if not records:
        print("ERROR: 未解析到任何记录")
        sys.exit(1)

    n_records, n_grids = generate_xlsx(records, grid_stats, output_path)
    print(f"生成成功: {output_path}")
    print(f"  Sheet1「携转明细」: {n_records} 行数据")
    print(f"  Sheet2「网格统计」: {n_grids} 行数据 + 1 行合计")


if __name__ == '__main__':
    main()