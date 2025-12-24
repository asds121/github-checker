# 贡献指南 (Contributing Guide)

欢迎为 GitHub 网络状态检测工具做出贡献！我们感谢任何形式的贡献，包括但不限于代码提交、问题报告、文档完善和功能建议。

## 目录 (Table of Contents)

- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [提交指南](#提交指南)
- [问题报告](#问题报告)
- [功能建议](#功能建议)

## 开发环境设置

1. 克隆项目到本地：

   ```bash
   git clone https://github.com/asds121/github-checker.git
   cd github-checker
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 运行测试：
   ```bash
   python -m pytest tests/
   ```

## 代码规范

- 使用 Python 3.8+ 编写代码
- 遵循 PEP 8 代码风格指南
- 使用 flake8 进行代码质量检查
- 函数和类需要包含详细的文档字符串（docstring）
- 重要代码逻辑需要添加注释说明
- 变量命名应具有描述性，避免使用缩写

## 提交指南

1. Fork 项目仓库
2. 创建新分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 提交信息规范

- 使用英文提交信息
- 格式：`type(scope): description`
- Type 包括：feat, fix, docs, style, refactor, test, chore
- 示例：`feat(checker): add full test mode`

## 问题报告

当您发现 bug 或需要报告问题时，请遵循以下步骤：

1. 搜索现有 Issue，确认问题未被报告
2. 创建新 Issue，包含以下信息：
   - 问题描述
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（操作系统、Python 版本等）

## 功能建议

我们欢迎功能建议！请在 Issue 中详细描述：

- 建议的功能
- 使用场景
- 预期效果
- 实现思路（如果有的话）

## 代码质量

项目使用 flake8 进行代码质量检查，确保您的代码通过检查：

```bash
flake8 github_checker.py
```

## 测试

提交代码前，请确保：

1. 编写相应的单元测试
2. 运行所有测试并确保通过
3. 代码覆盖率不低于 80%

## 联系方式

如有任何疑问，请通过以下方式联系：

- 提交 Issue
- 邮件：[维护者邮箱]
