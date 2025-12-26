# API文档

## 文档信息

| 项目     | 值                        |
| -------- | ------------------------- |
| 文档版本 | v1.0.0                    |
| 创建日期 | 2025-01-26                |
| 最后更新 | 2025-01-26                |
| 作者     | 项目开发团队              |
| 状态     | 已发布                    |
| API版本  | v1.0                      |
| 基础URL  | http://localhost:8000/api |

---

## 1. API概述

### 1.1 文档目的

本文档提供GitHub Status Checker项目的API接口规范，包括接口定义、参数说明和使用示例。

### 1.2 API范围

定义项目内部模块间的接口和可能的外部API接口。

### 1.3 参考资料

- [系统架构设计](ARCHITECTURE.md)
- [开发工作流程](../dev_workflow/README.md)
- [测试规范](../dev_workflow/TESTING.md)

---

## 2. API端点

### 2.1 状态检查接口

#### 2.1.1 检查单一目标

- **端点**: `POST /api/check`
- **描述**: 检查单个目标的连接状态
- **认证**: 无需认证

**路径参数**: 无

**查询参数**: 无

**请求体参数**:

```json
{
  "target": "github.com",
  "timeout": 10,
  "method": "get"
}
```

| 参数    | 类型    | 必需 | 描述                          |
| ------- | ------- | ---- | ----------------------------- |
| target  | string  | 是   | 要检查的目标URL或域名         |
| timeout | integer | 否   | 超时时间（秒），默认为10      |
| method  | string  | 否   | HTTP方法，get/post，默认为get |

**响应格式**:

```json
{
  "status": "success",
  "target": "github.com",
  "response_time": 0.123,
  "message": "Connection successful",
  "timestamp": "2025-01-26T10:00:00Z"
}
```

| 字段          | 类型   | 描述                        |
| ------------- | ------ | --------------------------- |
| status        | string | 检查结果状态(success/error) |
| target        | string | 检查的目标                  |
| response_time | number | 响应时间（秒）              |
| message       | string | 详细消息                    |
| timestamp     | string | 时间戳                      |

**错误码**:
| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| 400 | BAD_REQUEST | 请求参数错误 |
| 408 | TIMEOUT | 请求超时 |
| 500 | INTERNAL_ERROR | 服务器内部错误 |

**示例请求**:

```bash
curl -X POST http://localhost:8000/api/check \
  -H "Content-Type: application/json" \
  -d '{
    "target": "github.com",
    "timeout": 10,
    "method": "get"
  }'
```

### 2.2 批量检查接口

#### 2.2.1 检查多个目标

- **端点**: `POST /api/check-batch`
- **描述**: 批量检查多个目标的连接状态
- **认证**: 无需认证

**请求体参数**:

```json
{
  "targets": ["github.com", "api.github.com"],
  "timeout": 10,
  "concurrent": true
}
```

| 参数       | 类型    | 必需 | 描述                     |
| ---------- | ------- | ---- | ------------------------ |
| targets    | array   | 是   | 要检查的目标列表         |
| timeout    | integer | 否   | 超时时间（秒），默认为10 |
| concurrent | boolean | 否   | 是否并发检查，默认为true |

**响应格式**:

```json
{
  "results": [
    {
      "status": "success",
      "target": "github.com",
      "response_time": 0.123,
      "message": "Connection successful"
    },
    {
      "status": "error",
      "target": "api.github.com",
      "response_time": 0.0,
      "message": "Connection failed"
    }
  ],
  "summary": {
    "total": 2,
    "success": 1,
    "failed": 1,
    "average_response_time": 0.123
  }
}
```

### 2.3 配置管理接口

#### 2.3.1 获取配置

- **端点**: `GET /api/config`
- **描述**: 获取当前系统配置
- **认证**: 无需认证

**响应格式**:

```json
{
  "default_timeout": 10,
  "max_concurrent_checks": 10,
  "retry_count": 3,
  "user_agent": "GitHub-Status-Checker/1.0"
}
```

#### 2.3.2 更新配置

- **端点**: `PUT /api/config`
- **描述**: 更新系统配置
- **认证**: 需要管理员权限

**请求体参数**:

```json
{
  "default_timeout": 15,
  "max_concurrent_checks": 20
}
```

---

## 3. 通用响应格式

所有API响应遵循以下格式：

```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "error": null,
  "timestamp": "2025-01-26T10:00:00Z"
}
```

| 字段      | 类型         | 描述                     |
| --------- | ------------ | ------------------------ |
| success   | boolean      | 请求是否成功             |
| data      | object/array | 响应数据                 |
| message   | string       | 响应消息                 |
| error     | object/null  | 错误信息（成功时为null） |
| timestamp | string       | 响应时间戳               |

---

## 4. 数据类型定义

### 4.1 检查结果类型

```typescript
interface CheckResult {
  status: "success" | "error" | "timeout";
  target: string;
  response_time: number;
  message: string;
  timestamp: string;
}
```

### 4.2 配置类型

```typescript
interface Config {
  default_timeout: number;
  max_concurrent_checks: number;
  retry_count: number;
  user_agent: string;
}
```

---

## 5. 使用示例

### 5.1 Python使用示例

```python
import requests

def check_github_status():
    url = "http://localhost:8000/api/check"
    payload = {
        "target": "github.com",
        "timeout": 10
    }

    response = requests.post(url, json=payload)
    result = response.json()

    if result['success']:
        print(f"Status: {result['data']['status']}")
        print(f"Response time: {result['data']['response_time']}s")
    else:
        print(f"Error: {result['error']['message']}")

if __name__ == "__main__":
    check_github_status()
```

### 5.2 JavaScript使用示例

```javascript
async function checkGithubStatus() {
  const response = await fetch("http://localhost:8000/api/check", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      target: "github.com",
      timeout: 10,
    }),
  });

  const result = await response.json();

  if (result.success) {
    console.log(`Status: ${result.data.status}`);
    console.log(`Response time: ${result.data.response_time}s`);
  } else {
    console.error(`Error: ${result.error.message}`);
  }
}
```

---

## 6. 限流和配额

### 6.1 限流策略

- 每分钟最多100个请求
- 每小时最多5000个请求
- 每天最多100000个请求

### 6.2 配额管理

- 未认证用户: 限制为上述标准配额的50%
- 认证用户: 标准配额
- 管理员: 无限制

---

## 7. 错误处理

### 7.1 错误分类

- **客户端错误** (4xx): 请求格式错误、认证失败、权限不足
- **服务端错误** (5xx): 服务器内部错误、依赖服务不可用

### 7.2 错误响应格式

```json
{
  "success": false,
  "data": null,
  "message": "Error message",
  "error": {
    "code": "ERROR_CODE",
    "details": "Error details"
  },
  "timestamp": "2025-01-26T10:00:00Z"
}
```

---

## 8. 版本管理

### 8.1 API版本策略

- 使用URL路径进行版本控制: `/api/v1/endpoint`
- 向后兼容性: 同一主版本内保持向后兼容
- 版本废弃: 提前3个月通知版本废弃

### 8.2 版本兼容性

- v1.x.y: 向后兼容的版本更新
- v2.0.0: 包含破坏性变更的版本

---

## 附录

### A. 术语表

- **API**: Application Programming Interface，应用程序编程接口
- **REST**: Representational State Transfer，表述性状态传递
- **JSON**: JavaScript Object Notation，JavaScript对象表示法
- **HTTP**: HyperText Transfer Protocol，超文本传输协议

### B. 相关文档

- [系统架构设计](ARCHITECTURE.md) - 系统架构相关文档
- [开发工作流程](../dev_workflow/README.md) - 开发流程相关文档
- [测试规范](../dev_workflow/TESTING.md) - 测试相关文档

---

## 最新更新记录

| 日期       | 版本   | 变更说明      |
| ---------- | ------ | ------------- |
| 2025-01-26 | v1.0.0 | 初始化API文档 |

---

## 修订历史

| 版本   | 日期       | 作者         | 变更说明    |
| ------ | ---------- | ------------ | ----------- |
| v1.0.0 | 2025-01-26 | 项目开发团队 | 创建API文档 |

---

最后更新: 2025-01-26
