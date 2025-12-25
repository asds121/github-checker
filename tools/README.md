# 工具目录说明

## align_paren_tool.py
PEP 8 缩进对齐工具，用于修复E128/E127缩进错误

### 使用方法
```bash
python tools/align_paren_tool.py github_checker.py 145,147
```

### 功能
- 自动分析括号位置
- 精确计算续行缩进量
- 修复视觉缩进不匹配问题

## force_encoding_fix.py
文件编码修复工具

### 功能
- 检测文件编码问题
- 修复编码声明与实际编码不一致
- 统一使用UTF-8编码
