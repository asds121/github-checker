# GitHub 网络状态检测工具

一个轻量级的命令行工具，用于检测 GitHub 的可访问性和网络状态。

## 功能特点

- **快速检测**：几秒钟内检测 GitHub 主页和 API 的可访问性
- **多种模式**：支持单次检测和多次迭代的完整测试
- **丰富输出**：支持人类可读的彩色输出，也支持 JSON 格式便于自动化集成
- **跨平台**：支持 Windows、macOS 和 Linux

## 安装

```bash
# 克隆仓库
git clone https://github.com/asds121/github-checker.git
cd github-checker

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 基本检测

```bash
python github_checker.py
```

### 完整测试（多次迭代）

```bash
python github_checker.py -f
```

### JSON 输出

```bash
python github_checker.py -j
```

### 简洁主题

```bash
python github_checker.py -t minimal
```

### 趣味主题

```bash
python github_checker.py -t fun
```

### 显示介绍

```bash
python github_checker.py -i
```

### 组合使用

```bash
python github_checker.py -f -j  # 完整测试并输出 JSON 格式
```

## 命令行选项

| 选项              | 描述                                             |
| ----------------- | ------------------------------------------------ |
| `-f, --full-test` | 执行多次迭代的完整测试                           |
| `-j, --json`      | 以 JSON 格式输出结果                             |
| `-t, --theme`     | 输出主题：default、minimal、fun（默认：default） |
| `-i, --intro`     | 显示工具价值介绍                                 |
| `-h, --help`      | 显示帮助信息                                     |

## 退出码

- `0`：GitHub 可访问（状态良好）
- `1`：GitHub 不稳定（状态警告）
- `2`：GitHub 不可达（状态失败）

## 环境要求

- Python 3.6+
- requests>=2.25.1

## 测试

项目包含 63 个单元测试，覆盖以下方面：

| 测试类                      | 测试内容                                              |
| --------------------------- | ----------------------------------------------------- |
| `TestColorize`              | 颜色格式化函数                                        |
| `TestFormatStatus`          | 状态格式化函数（good/warn/bad/unknown）               |
| `TestFormatFunStatus`       | 趣味主题状态格式化                                    |
| `TestCheckerJudge`          | 状态判断逻辑（全部成功/部分失败/全部失败/边界情况）   |
| `TestCheckerMsg`            | 消息生成逻辑                                          |
| `TestCheckerTestMethod`     | URL 测试与异常处理（超时/连接错误/HTTP错误/重定向等） |
| `TestCheckerCheckMethod`    | 单次检测方法                                          |
| `TestCheckerTestFullMethod` | 完整测试方法（多次迭代）                              |
| `TestCheckerTargets`        | 目标 URL 配置                                         |
| `TestConstants`             | 常量值验证                                            |
| `TestColors`                | 颜色常量                                              |
| `TestSpinningCursor`        | 加载动画                                              |
| `TestMainFunction`          | 主函数行为与退出码                                    |
| `TestJsonOutputStructure`   | JSON 输出结构                                         |
| `TestEdgeCases`             | 边界情况处理                                          |

运行测试：

```bash
python -m pytest test_github_checker.py -v
```

## 许可证

MIT License
