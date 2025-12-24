# GitHub网络状态检测工具

## 📋 简介

GitHub Network Status Checker 是一个极简的命令行工具，专门用于检测GitHub的访问状态。无论您是开发者、运维工程师还是普通用户，当需要了解GitHub连接状况时，这个工具都能提供快速、准确的检测结果。

该工具通过检测GitHub主页（github.com）和API端点（api.github.com）的可访问性，结合响应时间分析，帮助您判断当前网络环境是否适合进行代码推送、仓库克隆或其他GitHub相关操作。

## ✨ 功能特性

本工具提供以下核心功能，满足不同场景下的网络状态检测需求：

- **基础检测** - 快速检测GitHub主页和API的可访问性，单轮检测即可获得结果
- **延迟显示** - 以毫秒为单位显示各个目标的响应时间，便于评估网络质量
- **完整测试模式** - 执行多轮检测（默认3轮），计算平均值和成功率，提供更可靠的评估
- **状态判断** - 根据预设阈值（3000ms）自动判断网络状态，标记为[OK]或[WARN]
- **操作建议** - 根据检测结果提供针对性的操作建议，如使用代理、检查网络设置等
- **加载动画** - 检测执行过程中显示旋转光标动画，实时反馈运行状态
- **跨平台兼容** - 支持Windows、macOS、Linux等主流操作系统

## 🚀 快速开始

### 环境要求

在开始使用之前，请确保您的系统满足以下要求：

- **操作系统**：Windows 7及以上版本、macOS、Linux
- **Python版本**：Python 3.6或更高版本
- **网络环境**：能够访问互联网（用于检测GitHub连接状态）

### 安装步骤

本工具仅依赖Python标准库和一个常用的第三方HTTP库：

1. **克隆或下载项目**

   ```bash
   # 克隆项目（如果使用Git）
   git clone https://github.com/asds121/github-checker.git

   # 或直接下载ZIP文件并解压
   ```

2. **进入项目目录**

   ```bash
   cd github-checker-检测状态
   ```

3. **安装依赖库**

   ```bash
   # 安装requests库（用于发送HTTP请求）
   pip install requests
   ```

4. **直接运行**

   ```bash
   # Windows系统
   start.bat

   # 或直接运行Python脚本
   python github_checker.py
   ```

### 验证安装

运行以下命令验证工具是否正常工作：

```bash
python github_checker.py
```

如果看到类似以下输出，说明安装成功：

```
GitHub Network Status Checker v1.0
========================================
Checking GitHub accessibility... \
Results:
  homepage  : OK   (1381ms)
  api       : OK   (1649ms)
----------------------------------------

Status: [OK] GitHub is accessible (avg 1515ms)

Suggestion: Network is stable, you can push code normally.
```

## 📖 使用说明

### 基本用法

工具支持两种运行模式，您可以根据需求选择合适的方式：

#### 模式一：基础检测（默认）

执行单轮检测，快速获取GitHub访问状态：

```bash
python github_checker.py
```

此模式适合日常快速检查，检测过程约需8-16秒（取决于网络环境）。

#### 模式二：完整测试模式

执行多轮检测，获得更准确的网络评估结果：

```bash
python github_checker.py --full-test
```

完整测试会进行3轮检测（每轮约8-16秒），然后计算平均响应时间和成功率，给出更稳定的评估结论。

### 命令行参数

工具支持以下命令行参数，满足不同使用场景的需求：

| 参数             | 说明                    | 示例                                   |
| ---------------- | ----------------------- | -------------------------------------- |
| 无参数           | 执行单轮基础检测        | `python github_checker.py`             |
| `--full-test`    | 执行完整测试模式（3轮） | `python github_checker.py --full-test` |
| `-h` 或 `--help` | 显示帮助信息            | `python github_checker.py --help`      |

### 使用场景示例

**场景一：日常开发前检查**

在开始编码工作前，快速确认GitHub是否可访问：

```bash
# 进入项目目录
cd C:\Users\Administrator\Desktop\代码\github工具合集\github-checker-检测状态

# 运行检测
python github_checker.py
```

**场景二：排查网络问题**

当GitHub操作（如clone、push）失败时，进行详细测试：

```bash
# 执行完整测试模式
python github_checker.py --full-test
```

完整测试会显示各轮次的详细结果，帮助您判断网络是否稳定。

**场景三：持续监控（可配合计划任务）**

将检测命令添加到系统计划任务中，定期执行并记录结果，实现网络状态监控。

## 📊 输出解读

### 基础检测输出示例

执行基础检测后，您将看到以下格式的输出：

```
GitHub Network Status Checker v1.0
========================================
Checking GitHub accessibility... \
Results:
  homepage  : OK   (1381ms)
  api       : OK   (1649ms)
----------------------------------------

Status: [OK] GitHub is accessible (avg 1515ms)

Suggestion: Network is stable, you can push code normally.
```

**输出字段说明：**

- `homepage` - GitHub主页（github.com）的检测结果
- `api` - GitHub API端点（api.github.com）的检测结果
- `OK/FAIL` - 检测状态，OK表示成功，FAIL表示失败
- 括号内的数字 - 响应时间（毫秒）
- `Status` - 综合判断的网络状态
- `Suggestion` - 针对性的操作建议

### 完整测试输出示例

执行完整测试模式后，输出包含更多统计信息：

```
GitHub Network Status Checker v1.0
========================================
Checking GitHub accessibility... Running full test (3 iterations)...
  Iteration 3/3...
Results:
----------------------------------------
Full test completed (3 iterations)
Successful checks: 3/3
Average total time: 2932ms

  homepage  : Avg 1247ms, Success rate: 100.0%
  api       : Avg 1677ms, Success rate: 100.0%
----------------------------------------

Status: [OK] GitHub is accessible (avg 1462ms)

Suggestion: Network is stable, you can push code normally.
```

**新增字段说明：**

- `Avg` - 多轮检测的平均响应时间
- `Success rate` - 成功检测的比例（百分比）
- `Successful checks` - 成功的检测轮次数

### 状态标识含义

工具使用以下两种状态标识来描述网络状况：

- **[OK]** - 绿色标识，表示网络状态良好，GitHub可正常访问，响应时间在可接受范围内
- **[WARN]** - 黄色标识，表示GitHub可访问但速度较慢，响应时间超过阈值，可能影响使用体验
- **[FAIL]** - 红色标识，表示无法访问GitHub，需要检查网络设置或使用代理

## ❓ 常见问题解答

### Q1: 检测失败怎么办？

当检测结果显示[FAIL]时，您可以按以下步骤排查问题：

1. **检查本地网络**
   - 确认计算机已连接到互联网
   - 尝试访问其他网站（如百度、谷歌）验证网络连通性
   - 检查网络电缆或WiFi连接是否正常

2. **检查防火墙和安全软件**
   - 暂时关闭防火墙或安全软件，测试是否是它们阻止了连接
   - 确保Python程序未被安全软件拦截

3. **尝试更换网络环境**
   - 如果使用的是公司网络，尝试切换到手机热点
   - 或反之，切换到更稳定的网络环境

4. **使用代理或VPN**
   - 如果在中国大陆，可能需要配置代理或VPN才能访问GitHub
   - 配置代理后重新运行检测命令

5. **检查DNS设置**
   - 尝试将DNS服务器设置为公共DNS（如8.8.8.8）
   - 或清除本地DNS缓存：`ipconfig /flushdns`

### Q2: 响应时间过长正常吗？

响应时间受多种因素影响：

- **正常范围**：500-2000ms 通常表示网络状况良好
- **可接受范围**：2000-3000ms 表示网络略有延迟，但基本可用
- **需要关注**：超过3000ms 会被标记为[WARN]，建议检查网络

如果经常遇到高延迟，建议：

- 考虑使用更快的网络连接
- 配置合适的代理服务器
- 避开网络高峰期使用

### Q3: 什么是完整测试模式？

完整测试模式（`--full-test`）会执行多轮检测，通过统计分析提供更可靠的结果：

- 默认执行3轮检测
- 计算各目标的平均响应时间和成功率
- 适合需要准确评估网络稳定性的场景

与单轮检测相比，完整测试模式能够：

- 排除偶发的网络波动影响
- 发现间歇性的连接问题
- 提供成功率指标，更客观地反映网络质量

### Q4: 支持自定义检测目标吗？

当前版本固定检测以下两个目标：

- `github.com` - GitHub主页
- `api.github.com` - GitHub API端点

这是工具的核心设计，用于全面评估GitHub服务的可访问性。暂时不支持用户自定义检测目标。

### Q5: 可以集成到CI/CD流程吗？

是的，您可以将检测命令集成到CI/CD流程中：

```yaml
# GitHub Actions 示例
- name: Check GitHub Connectivity
  run: |
    python github_checker.py
    if [ $? -ne 0 ]; then
      echo "GitHub is not accessible"
      exit 1
    fi
```

这在需要确保构建环境能够访问GitHub资源的场景中非常有用。

### Q6: 如何报告问题或提出建议？

如果您在使用过程中遇到问题或有改进建议，欢迎：

- 在GitHub仓库提交Issue
- 检查现有Issue是否已有类似问题
- 详细描述问题现象和复现步骤

## 🔧 技术文档

### 技术规格

本工具采用极简的技术架构，确保轻量级和易用性：

- **编程语言**：Python 3
- **依赖库**：
  - Python标准库（sys、time、argparse）
  - requests库（用于发送HTTP请求）
- **超时设置**：8秒（单次请求超时时间）
- **检测目标**：
  - GitHub主页：`https://github.com`
  - GitHub API：`https://api.github.com`
- **状态判断阈值**：3000毫秒
  - 响应时间 < 3000ms → [OK]
  - 响应时间 >= 3000ms → [WARN]

### 架构说明

工具采用单文件架构设计，所有功能集中在一个Python文件中：

- `github_checker.py` - 核心检测逻辑和命令行入口
- 无需额外的配置文件或依赖
- 便于分发和部署

### 文件结构

```
github-checker-检测状态/
├── github_checker.py    # 主程序文件
├── README.md            # 使用说明文档
├── start.bat            # Windows快速启动脚本
├── start-full.bat       # Windows完整测试启动脚本
├── tests/
│   └── test_github_checker.py  # 单元测试
└── docs/                # 详细设计文档
    ├── 01-需求分析.md
    ├── 02-系统设计.md
    ├── 03-详细设计.md
    └── ...（更多文档）
```

### 测试说明

项目包含完整的单元测试，确保代码质量和功能正确性：

```bash
# 运行所有测试
python -m unittest tests.test_github_checker -v
```

测试覆盖：

- 基础检测功能
- 完整测试模式
- 状态判断逻辑
- 消息生成功能
- 错误处理能力

## 🤝 贡献指南

欢迎社区贡献者参与项目改进！如果您想为项目贡献代码或文档，请阅读以下指南：

### 贡献方式

- **报告问题**：发现Bug或有改进建议，请在GitHub仓库提交Issue
- **提交代码**：Fork项目，修改后提交Pull Request
- **完善文档**：帮助改进README或添加其他文档
- **测试验证**：帮助验证修复的问题或新功能

### 贡献流程

1. Fork本项目到您的GitHub账户
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交修改：`git commit -m "Add your feature"`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交Pull Request，等待代码审查

### 代码规范

- 遵循PEP 8 Python代码规范
- 新功能需添加对应的单元测试
- 确保所有测试通过后再提交Pull Request
- 代码注释使用英文，保持一致性

详细贡献指南请参考：[CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 版本历史

项目版本更新记录请查看：[CHANGELOG.md](CHANGELOG.md)

## 📄 许可证

本项目采用MIT许可证开源，详情请查看：[LICENSE](LICENSE)

## 📞 联系方式

- **项目仓库**：https://github.com/asds121/github-checker.git
- **问题反馈**：https://github.com/asds121/github-checker/issues

## 🙏 致谢

感谢所有为这个项目贡献代码、文档和建议的开发者！
