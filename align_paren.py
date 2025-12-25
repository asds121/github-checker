#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""精确对齐到括号位置"""

with open('github_checker.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# 找到括号的确切位置
line_144 = lines[143]
sum_pos = line_144.find('sum(')
paren_pos_144 = sum_pos + 4  # 找到 "sum(" 后 '(' 的下一个字符位置
print(f"Line 144 'sum(' 分析: sum在{sum_pos}, 括号在{paren_pos_144-1}")

line_146 = lines[145]
sum_pos = line_146.find('sum(')
paren_pos_146 = sum_pos + 4  # 找到 "sum(" 后 '(' 的下一个字符位置
print(f"Line 146 'sum(' 分析: sum在{sum_pos}, 括号在{paren_pos_146-1}")

# 修复 Line 145: 与 sum( 后第一个字符对齐
lines[144] = ' ' * paren_pos_144 + 'if "ms" in r) / len(target_results)'

# 修复 Line 147: 与 sum( 后第一个字符对齐
lines[146] = ' ' * paren_pos_146 + 'if r.get("ok", False))'

print(f"\n修复后:")
print(f"Line 145: {repr(lines[144])}")
print(f"Line 147: {repr(lines[146])}")

with open('github_checker.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("\n已修复")