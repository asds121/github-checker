# GitHub Network Status Checker

一个简洁高效的命令行工具，用于检测GitHub网站和API的可访问性。

## 功能特性

- **快速检测**：单轮检测约8-16秒，获得GitHub访问状态
- **多轮测试**：完整测试模式执行3轮检测，计算平均值和成功率
- **多种主题**：支持default、minimal、fun、share四种输出主题
- **JSON输出**：支持JSON格式输出，便于程序集成
- **响应时间**：以毫秒为单位显示各目标响应时间
- **状态判断**：自动判断网络状态（good/warn/bad）
- **彩色输出**：终端彩色显示，绿色正常，黄色警告，红色失败
- **反馈收集**：支持用户反馈功能，帮助改进工具

## 快速开始

### 环境要求

- Python 3.6+
- requests库

### 安装

```bash
pip install -r requirements.txt
```

### 使用

```bash
# 基础检测（默认）
python cli.py

# 完整测试（3轮检测）
python cli.py --full-test

# JSON格式输出
python cli.py --json

# 指定主题
python cli.py --theme fun

# 显示工具介绍
python cli.py --intro

# 设置超时时间
python cli.py --timeout 10

# 安静模式
python cli.py --quiet

# 运行后收集反馈
python cli.py --feedback
```

## 命令行参数

| 参数                | 说明                                      |
| ------------------- | ----------------------------------------- |
| 无参数              | 执行单轮基础检测                          |
| `-f`, `--full-test` | 执行完整测试模式（3轮）                   |
| `-j`, `--json`      | 以JSON格式输出结果                        |
| `-t`, `--theme`     | 选择输出主题（default/minimal/fun/share） |
| `-s`, `--share`     | 生成简洁的可分享文本                      |
| `-i`, `--intro`     | 显示工具价值介绍                          |
| `-q`, `--quiet`     | 安静模式，最小化输出                      |
| `--timeout`         | 请求超时时间（秒），默认8秒               |
| `--feedback`        | 运行后收集用户反馈                        |
| `-h`, `--help`      | 显示帮助信息                              |

## 输出示例

### 正常状态

```
GitHub Network Status Checker
========================================
homepage  : OK   (1381ms)
api       : OK   (1649ms)
----------------------------------------
Status: OK - GitHub is accessible (avg 1515ms)
```

### 警告状态

```
Status: WARN - GitHub is accessible but slow (avg 3200ms)
```

### 失败状态

```
Status: FAIL - GitHub is not accessible
```

### JSON输出

```json
{
  "status": "good",
  "msg": "GitHub is accessible",
  "ms": 1500,
  "results": [
    ["homepage", { "ok": true, "ms": 1381, "status_code": 200 }],
    ["api", { "ok": true, "ms": 1649, "status_code": 200 }]
  ]
}
```

## 项目结构

```
├── cli.py              # 命令行入口
├── core/
│   ├── checker.py      # 核心检测逻辑
│   └── colors.py       # 颜色工具
├── ui/
│   └── themes.py       # 主题渲染
├── utils/
│   ├── animation.py    # 动画效果
│   └── constants.py    # 常量定义
└── tests/              # 测试文件
```

## 测试

```bash
python -m pytest tests/ -v
```

## 版本

当前版本：v1.3.0

详见 [CHANGELOG.md](CHANGELOG.md)
