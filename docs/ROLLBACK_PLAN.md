# 回滚计划

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

本文档定义GitHub Status Checker项目的回滚计划，确保在部署失败或出现严重问题时能够快速恢复到稳定状态。

### 1.2 适用范围

适用于系统管理员、开发人员和运维人员。

### 1.3 参考资料

- [部署指南](DEPLOYMENT_GUIDE.md)
- [版本管理策略](VERSION_MANAGEMENT.md)
- [测试规范](../dev_workflow/TESTING.md)

---

## 2. 回滚触发条件

### 2.1 自动回滚条件

- 新版本部署后5分钟内出现严重错误
- 关键功能不可用超过1分钟
- 系统响应时间超过正常值的3倍
- 系统资源使用率超过阈值

### 2.2 手动回滚条件

- 用户反馈大量功能异常
- 安全漏洞被发现
- 数据完整性问题
- 性能严重下降

---

## 3. 回滚策略

### 3.1 快速回滚

适用于紧急情况，直接切换到上一个稳定版本：

- 恢复应用代码到上一版本
- 恢复配置文件到上一版本
- 重启服务

### 3.2 逐步回滚

适用于非紧急情况，允许逐步验证：

- 逐步减少新版本流量
- 监控系统状态
- 完全切换到旧版本

---

## 4. 回滚流程

### 4.1 应急回滚流程

1. **评估问题严重性**
   - 确认问题影响范围
   - 评估业务影响程度
   - 决定是否需要立即回滚

2. **停止新版本部署**
   - 暂停CI/CD流水线
   - 停止新版本服务
   - 阻止新流量进入

3. **执行回滚操作**
   - 恢复备份的应用代码
   - 恢复备份的配置文件
   - 重启旧版本服务

4. **验证回滚结果**
   - 确认服务正常运行
   - 验证核心功能可用性
   - 监控系统指标

5. **通知相关人员**
   - 通知开发团队
   - 通知管理层
   - 更新问题跟踪系统

### 4.2 标准回滚流程

1. **问题确认**
   - 确认需要回滚的问题
   - 记录问题详细信息
   - 通知相关团队

2. **备份当前状态**
   - 备份当前配置
   - 备份当前数据
   - 记录当前版本信息

3. **执行回滚**
   - 按照版本管理策略回滚
   - 验证回滚步骤
   - 监控系统状态

4. **验证和测试**
   - 执行基本功能测试
   - 验证系统性能
   - 确认问题已解决

---

## 5. 回滚工具和脚本

### 5.1 自动回滚脚本

```bash
#!/bin/bash
# rollback.sh - 自动回滚脚本

# 配置变量
BACKUP_DIR="/opt/github-checker/backups"
CURRENT_DIR="/opt/github-checker/current"
PREVIOUS_DIR="/opt/github-checker/previous"
LOG_FILE="/var/log/rollback.log"

# 记录日志
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

# 执行回滚
rollback_version() {
    log_message "开始回滚操作"

    # 停止当前服务
    systemctl stop github-checker
    log_message "已停止当前服务"

    # 恢复上一版本
    if [ -d "$PREVIOUS_DIR" ]; then
        rm -rf $CURRENT_DIR
        cp -r $PREVIOUS_DIR $CURRENT_DIR
        log_message "已恢复上一版本"
    else
        log_message "错误: 上一版本备份不存在"
        exit 1
    fi

    # 恢复配置文件
    cp $BACKUP_DIR/config.json $CURRENT_DIR/config.json
    log_message "已恢复配置文件"

    # 启动服务
    systemctl start github-checker
    log_message "已启动回滚后的服务"

    # 验证服务状态
    sleep 10
    if systemctl is-active --quiet github-checker; then
        log_message "回滚成功，服务正常运行"
    else
        log_message "错误: 回滚后服务未正常运行"
        exit 1
    fi
}

# 执行回滚
rollback_version
```

### 5.2 回滚验证脚本

```bash
#!/bin/bash
# verify_rollback.sh - 回滚验证脚本

# 检查服务状态
check_service_status() {
    if systemctl is-active --quiet github-checker; then
        echo "✓ 服务正在运行"
        return 0
    else
        echo "✗ 服务未运行"
        return 1
    fi
}

# 检查基本功能
check_basic_functionality() {
    # 测试API端点
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health)
    if [ "$response" -eq 200 ]; then
        echo "✓ API健康检查正常"
        return 0
    else
        echo "✗ API健康检查失败，状态码: $response"
        return 1
    fi
}

# 执行验证
echo "开始回滚验证..."
check_service_status && check_basic_functionality
if [ $? -eq 0 ]; then
    echo "✓ 回滚验证通过"
else
    echo "✗ 回滚验证失败"
    exit 1
fi
```

---

## 6. 数据回滚

### 6.1 数据备份策略

- 部署前自动备份当前数据
- 保留最近3个版本的数据备份
- 定期验证备份完整性

### 6.2 数据恢复流程

1. 停止应用程序
2. 备份当前数据（以防需要再次回滚）
3. 恢复目标版本的数据
4. 启动应用程序
5. 验证数据完整性

---

## 7. 配置回滚

### 7.1 配置管理

- 版本化配置文件
- 自动备份部署前配置
- 配置变更审计日志

### 7.2 配置恢复

- 按需恢复特定配置项
- 验证配置文件格式
- 重新加载配置而无需重启服务

---

## 8. 风险管理

### 8.1 回滚风险

- 回滚过程中服务中断
- 数据不一致风险
- 配置错误风险

### 8.2 风险缓解措施

- 在低峰期执行回滚
- 准备完整的回滚验证清单
- 确保有备用回滚方案

---

## 9. 回滚后处理

### 9.1 问题分析

- 分析导致回滚的根本原因
- 评估问题的影响范围
- 记录问题和解决方案

### 9.2 预防措施

- 更新测试用例以覆盖问题场景
- 改进部署前验证流程
- 加强监控和告警

---

## 10. 相关文档

- [部署指南](DEPLOYMENT_GUIDE.md) - 部署相关文档
- [版本管理策略](VERSION_MANAGEMENT.md) - 版本管理相关文档
- [测试规范](../dev_workflow/TESTING.md) - 测试执行规范

---

## 11. 最新更新记录

| 日期       | 版本   | 变更说明       |
| ---------- | ------ | -------------- |
| 2025-01-26 | v1.0.0 | 初始化回滚计划 |

---

## 修订历史

| 版本   | 日期       | 作者         | 变更说明     |
| ------ | ---------- | ------------ | ------------ |
| v1.0.0 | 2025-01-26 | 项目开发团队 | 创建回滚计划 |

---

最后更新: 2025-01-26
