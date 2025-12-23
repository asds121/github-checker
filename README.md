# GitHub网络状态检测工具

## 简介

这是一个极简的命令行工具，用于检测GitHub的访问状态。

## 功能

- 检测GitHub主页和API的可访问性
- 显示网络延迟（毫秒）
- 根据检测结果提供操作建议
- 简单的加载动画

## 使用方法

直接运行 `start.bat` 即可：

```batch
start.bat
```

或者直接运行Python脚本：

```batch
python github_checker.py
```

## 输出示例

```
GitHub Network Status Checker v1.0
========================================
Checking GitHub accessibility...

Results:
----------------------------------------
  homepage   : OK   (120ms)
  api        : OK   (85ms)
----------------------------------------

Status: [OK] GitHub is accessible

Suggestion: You can push code normally.
```

## 技术说明

- 依赖：Python 3.x + requests库
- 超时：8秒
- 检测目标：github.com + api.github.com

## 作者

GitHub Checker Project
