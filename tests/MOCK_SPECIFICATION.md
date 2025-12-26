# Mock规范

## 文档信息

| 项目 | 值 |
|------|-----|
| 文档版本 | v1.0.0 |
| 创建日期 | 2025-01-26 |
| 最后更新 | 2025-01-26 |
| 作者 | 项目开发团队 |
| 状态 | 已发布 |

---

## 1. 概述

### 1.1 文档目的
本文档定义GitHub Status Checker项目的Mock规范，包括Mock对象的创建、使用和管理。

### 1.2 适用范围
适用于项目中所有需要Mock的测试场景。

### 1.3 参考资料
- [测试管理规范](TEST_MANAGEMENT.md)
- [Python Mock文档](https://docs.python.org/3/library/unittest.mock.html)
- [测试文档索引](TEST_INDEX.md)

---

## 2. Mock类型

### 2.1 网络请求Mock
用于模拟HTTP请求和响应：

```python
from unittest.mock import patch, Mock
import requests

def test_network_request():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'ok'}
        mock_get.return_value = mock_response
        
        # 执行测试
        result = requests.get('https://api.example.com')
        assert result.status_code == 200
```

### 2.2 文件系统Mock
用于模拟文件操作：

```python
from unittest.mock import patch, mock_open

def test_file_operations():
    with patch('builtins.open', mock_open(read_data='file content')) as mock_file:
        # 执行文件操作测试
        with open('test.txt', 'r') as f:
            content = f.read()
        
        mock_file.assert_called_once_with('test.txt', 'r')
        assert content == 'file content'
```

### 2.3 数据库Mock
用于模拟数据库操作：

```python
from unittest.mock import Mock, patch

def test_database_operations():
    mock_db = Mock()
    mock_db.query.return_value = [{'id': 1, 'name': 'test'}]
    
    with patch('your_module.get_database', return_value=mock_db):
        # 执行数据库操作测试
        result = your_function_that_uses_db()
        assert len(result) == 1
```

### 2.4 系统调用Mock
用于模拟系统调用：

```python
from unittest.mock import patch

def test_system_call():
    with patch('os.system') as mock_system:
        mock_system.return_value = 0  # 模拟成功执行
        
        # 执行系统调用测试
        result = your_function_that_calls_system()
        
        mock_system.assert_called_once()
```

---

## 3. Mock创建规范

### 3.1 Mock对象命名
- 使用描述性的命名
- 遵循`mock_`前缀约定
- 保持命名一致性

```python
# 好的命名
mock_response = Mock()
mock_file_handler = Mock()
mock_network_client = Mock()

# 避免的命名
m = Mock()
obj = Mock()
x = Mock()
```

### 3.2 Mock配置
- 在测试开始时配置Mock行为
- 使用清晰的配置方式
- 避免过度配置

```python
# 好的配置方式
mock_api = Mock()
mock_api.get_status.return_value = 'online'
mock_api.get_response_time.return_value = 100

# 避免复杂配置
mock_api.configure_mock(
    get_status=Mock(return_value='online'),
    get_response_time=Mock(return_value=100)
)
```

---

## 4. Mock使用最佳实践

### 4.1 使用上下文管理器
```python
from unittest.mock import patch

def test_with_context_manager():
    with patch('requests.get') as mock_get:
        # 在这里进行测试
        pass
    # Mock会自动清理
```

### 4.2 使用装饰器
```python
from unittest.mock import patch

@patch('requests.get')
def test_with_decorator(mock_get):
    # 测试代码
    pass
```

### 4.3 验证Mock调用
```python
def test_mock_calls():
    with patch('requests.get') as mock_get:
        # 执行被测试的函数
        your_function()
        
        # 验证调用
        mock_get.assert_called_once()
        mock_get.assert_called_with('https://api.example.com')
```

---

## 5. Mock测试示例

### 5.1 GitHub API Mock测试
```python
import pytest
from unittest.mock import patch, Mock
from core.checker import GitHubChecker

def test_github_api_success():
    """测试GitHub API成功响应"""
    with patch('requests.get') as mock_get:
        # 配置Mock响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': {'description': 'All systems operational'}
        }
        mock_get.return_value = mock_response
        
        # 创建检查器实例并测试
        checker = GitHubChecker(['github.com'])
        result = checker.check_targets()
        
        # 验证结果
        assert result[0]['status'] == 'success'
        mock_get.assert_called_once()

def test_github_api_failure():
    """测试GitHub API失败响应"""
    with patch('requests.get') as mock_get:
        # 配置Mock失败响应
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        # 创建检查器实例并测试
        checker = GitHubChecker(['github.com'])
        result = checker.check_targets()
        
        # 验证结果
        assert result[0]['status'] == 'error'
        mock_get.assert_called_once()
```

### 5.2 配置文件Mock测试
```python
from unittest.mock import patch, mock_open
import json

def test_config_loading():
    """测试配置文件加载"""
    config_data = {
        'targets': ['github.com', 'api.github.com'],
        'timeout': 10,
        'retries': 3
    }
    
    with patch('builtins.open', mock_open(read_data=json.dumps(config_data))) as mock_file:
        # 测试配置加载逻辑
        with open('config.json', 'r') as f:
            loaded_config = json.load(f)
        
        # 验证文件操作
        mock_file.assert_called_once_with('config.json', 'r')
        assert loaded_config == config_data
```

---

## 6. Mock维护指南

### 6.1 Mock更新
- 当被Mock的接口发生变化时，更新Mock定义
- 保持Mock与实际接口的一致性
- 定期审查过时的Mock

### 6.2 Mock清理
- 在测试完成后清理Mock状态
- 避免Mock状态泄漏到其他测试
- 使用适当的Mock作用域

---

## 7. 常见问题解决

### 7.1 Mock不生效
- 检查Mock路径是否正确
- 确认Mock对象在被测试代码之前创建
- 验证Mock的作用域

### 7.2 Mock过度模拟
- 避免模拟过多依赖
- 保持测试的真实性和有效性
- 仅Mock必要的外部依赖

### 7.3 Mock状态泄漏
- 使用上下文管理器确保Mock清理
- 避免全局Mock状态
- 在测试间重置Mock状态

---

## 8. 相关文档

- [测试管理规范](TEST_MANAGEMENT.md) - 测试管理相关文档
- [测试文档索引](TEST_INDEX.md) - 测试文档索引
- [Python Mock文档](https://docs.python.org/3/library/unittest.mock.html) - Python Mock官方文档
- [测试用例编写指南](../docs/TEST_CASE_GUIDELINES.md) - 测试用例编写相关文档

---

## 9. 最新更新记录

| 日期 | 版本 | 变更说明 |
|------|------|----------|
| 2025-01-26 | v1.0.0 | 初始化Mock规范文档 |

---

## 修订历史

| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|----------|
| v1.0.0 | 2025-01-26 | 项目开发团队 | 创建Mock规范文档 |

---

最后更新: 2025-01-26