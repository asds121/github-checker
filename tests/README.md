# 测试文档

## 文档信息

| 项目     | 值           |
| -------- | ------------ |
| 文档版本 | v1.0.0       |
| 创建日期 | 2025-01-26   |
| 最后更新 | 2025-01-26   |
| 作者     | 项目开发团队 |
| 状态     | 已发布       |

---

## 1. 概述

### 1.1 文档目的

本文档提供GitHub Status Checker项目测试相关的说明和指南，包括测试结构、执行方法和维护规范。

### 1.2 适用范围

适用于项目开发人员、测试人员和维护人员。

### 1.3 参考资料

- [测试管理规范](TEST_MANAGEMENT.md)
- [Mock规范](MOCK_SPECIFICATION.md)
- [测试文档索引](TEST_INDEX.md)

---

## 2. 测试目录结构

```
tests/
├── __init__.py                 # 测试包初始化
├── README.md                   # 本文档
├── TEST_INDEX.md              # 测试文档索引
├── TEST_MANAGEMENT.md         # 测试管理规范
├── MOCK_SPECIFICATION.md      # Mock规范
├── test_checker.py            # 核心检查器测试
├── test_colors.py             # 颜色处理测试
├── test_themes.py             # 主题测试
├── test_animation.py          # 动画效果测试
├── test_main.py               # 主函数测试
├── conftest.py                # pytest配置
├── EXECUTION_GUIDE.md         # 测试执行指南
├── REPORT_TEMPLATE.md         # 测试报告模板
└── COVERAGE_REPORT.md         # 覆盖率报告
```

---

## 3. 测试类型说明

### 3.1 单元测试

测试单个函数或类的方法，位于各个`test_*.py`文件中。

### 3.2 集成测试

测试多个模块之间的交互。

### 3.3 系统测试

测试整个系统的功能。

---

## 4. 测试执行

### 4.1 环境准备

```bash
# 安装项目依赖
pip install -r requirements.txt

# 安装测试依赖
pip install pytest pytest-cov
```

### 4.2 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_checker.py

# 运行特定测试函数
pytest tests/test_checker.py::test_function_name

# 运行测试并显示详细输出
pytest -v

# 运行测试并生成覆盖率报告
pytest --cov=core
```

### 4.3 测试标记

- `@pytest.mark.slow`：标记耗时较长的测试
- `@pytest.mark.integration`：标记集成测试
- `@pytest.mark.unit`：标记单元测试

---

## 5. 测试编写规范

### 5.1 命名规范

- 测试文件：`test_{module_name}.py`
- 测试类：`Test{ModuleName}`
- 测试方法：`test_{action}_{condition}_{expected_result}`

### 5.2 结构规范

遵循AAA模式（Arrange-Act-Assert）：

```python
def test_github_checker_success():
    # Arrange - 设置测试环境
    checker = GitHubChecker(['github.com'])

    # Act - 执行被测功能
    result = checker.check_targets()

    # Assert - 验证结果
    assert result[0]['status'] == 'success'
```

### 5.3 Mock使用

- Mock外部依赖
- 避免Mock内部实现
- 保持Mock简单明了

---

## 6. 测试维护

### 6.1 添加新测试

1. 确定测试类型和位置
2. 遵循命名和结构规范
3. 编写清晰的测试用例
4. 更新相关文档

### 6.2 更新现有测试

1. 分析变更影响范围
2. 更新相关测试用例
3. 验证测试结果正确性
4. 更新文档

### 6.3 废弃测试处理

1. 标记废弃测试
2. 添加废弃原因说明
3. 计划移除时间
4. 更新文档

---

## 7. 常见问题解决

### 7.1 测试失败

- 检查代码变更是否影响测试
- 验证Mock配置是否正确
- 确认测试环境设置

### 7.2 性能问题

- 检查是否有外部依赖
- 验证Mock使用是否恰当
- 优化测试数据生成

### 7.3 环境问题

- 确认依赖包已安装
- 验证配置文件路径
- 检查权限设置

---

## 8. 相关文档

- [测试管理规范](TEST_MANAGEMENT.md) - 测试管理相关文档
- [Mock规范](MOCK_SPECIFICATION.md) - Mock使用规范
- [测试文档索引](TEST_INDEX.md) - 测试文档索引
- [测试用例编写指南](../docs/TEST_CASE_GUIDELINES.md) - 测试用例编写指南

---

## 9. 最新更新记录

| 日期       | 版本   | 变更说明       |
| ---------- | ------ | -------------- |
| 2025-01-26 | v1.0.0 | 初始化测试文档 |

---

## 修订历史

| 版本   | 日期       | 作者         | 变更说明     |
| ------ | ---------- | ------------ | ------------ |
| v1.0.0 | 2025-01-26 | 项目开发团队 | 创建测试文档 |

---

最后更新: 2025-01-26
