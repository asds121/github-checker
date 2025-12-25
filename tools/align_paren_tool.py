#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PEP 8 缩进对齐工具
用于修复E128/E127缩进错误
"""

import re
from pathlib import Path

def analyze_paren_position(file_path, line_number):
    """分析括号位置，计算正确的缩进量"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 续行符通常在前一行
    prev_line = lines[line_number - 2].rstrip()
    
    # 查找常见的函数调用模式
    patterns = [
        (r'sum\(', 'sum'),
        (r'len\(', 'len'),
        (r'max\(', 'max'),
        (r'min\(', 'min'),
        (r'str\(', 'str'),
        (r'int\(', 'int'),
        (r'float\(', 'float'),
        (r'list\(', 'list'),
        (r'dict\(', 'dict')
    ]
    
    for pattern, func_name in patterns:
        match = re.search(pattern, prev_line)
        if match:
            paren_pos = match.start() + len(func_name) + 1  # 函数名长度 + 1(括号)
            return paren_pos
    
    # 如果没有找到特定函数，查找第一个左括号
    paren_pos = prev_line.find('(')
    if paren_pos != -1:
        return paren_pos + 1
    
    return None

def fix_indentation(file_path, target_lines):
    """修复指定行的缩进问题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes_made = 0
    
    for line_num in target_lines:
        if line_num < 2 or line_num >= len(lines):
            continue
            
        paren_pos = analyze_paren_position(file_path, line_num)
        if paren_pos is None:
            print(f"⚠️  无法分析第{line_num}行的括号位置")
            continue
        
        # 修复缩进
        old_line = lines[line_num - 1]
        new_line = ' ' * paren_pos + old_line.lstrip()
        
        if old_line != new_line:
            lines[line_num - 1] = new_line
            changes_made += 1
            print(f"✅ 修复第{line_num}行缩进: {paren_pos}个空格")
    
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"📝 共修复 {changes_made} 行缩进问题")
    else:
        print("ℹ️  未发现需要修复的缩进问题")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("用法: python align_paren_tool.py <文件路径> <行号1,行号2,...>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    line_numbers = [int(x) for x in sys.argv[2].split(',')]
    
    fix_indentation(file_path, line_numbers)
