#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 读取文件内容，使用二进制模式
with open('github_checker.py', 'rb') as f:
    raw_content = f.read()

# 尝试用不同编码读取
encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']

content = None
for encoding in encodings:
    try:
        content = raw_content.decode(encoding)
        print(f"✅ 成功使用 {encoding} 编码读取文件")
        break
    except UnicodeDecodeError:
        continue

if content is None:
    # 如果所有编码都失败，使用 latin-1（可以解码任何字节序列）
    content = raw_content.decode('latin-1')
    print("⚠️ 使用 latin-1 编码（可能包含非法字符）")

# 修复文件头编码声明
content = content.replace('# -*- coding: ascii -*-', '# -*- coding: utf-8 -*-')

# 写入文件，使用UTF-8编码
with open('github_checker.py', 'w', encoding='utf-8', errors='replace') as f:
    f.write(content)

print("✅ 编码修复完成！文件已重新保存为 UTF-8 编码")
