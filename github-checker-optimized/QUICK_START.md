# 快速开始指南

## 🚀 立即使用

### 方法1：简单启动
```bash
python simple_start.py
```

### 方法2：增强启动（推荐）
```bash
python enhanced_start.py
```

### 方法3：Windows批处理
双击 `start.bat` 文件

## 📋 功能概览

### ✅ 已实现功能
- **实时GitHub状态检测** - 支持github.com和api.github.com
- **智能重试机制** - 失败后自动重试3次
- **详细日志记录** - 完整的操作日志
- **统计信息** - 检测成功率和响应时间统计
- **现代化界面** - 改进的UI设计
- **菜单系统** - 文件、工具、帮助菜单
- **配置管理** - 可配置的参数设置
- **多线程检测** - 后台执行，不阻塞界面
- **错误处理** - 完善的异常处理

### 🛠️ 使用方法
1. 启动应用后点击 **"Check Now"** 进行手动检测
2. 点击 **"Auto Check: OFF"** 开启自动检测模式
3. 使用菜单栏访问更多功能：
   - **文件** → 导出日志
   - **工具** → 设置 / 清除统计
   - **帮助** → 关于 / 查看完整日志

### ⚙️ 配置选项
编辑 `config.json` 文件可以修改：
- 超时时间 (默认10秒)
- 自动检测间隔 (默认5秒)
- 最大重试次数 (默认3次)
- 日志级别 (INFO/DEBUG/WARNING/ERROR)
- 检测URL列表
- 用户代理字符串

## 🔧 测试和验证

运行测试脚本：
```bash
python ascii_test.py      # 基础功能测试
python test_functionality.py  # 网络功能测试
```

## 📁 文件说明

### 核心文件
- `github_checker.py` - 主应用程序
- `config.json` - 配置文件
- `requirements.txt` - Python依赖

### 启动脚本
- `simple_start.py` - 简单启动（推荐）
- `enhanced_start.py` - 增强启动（高级功能）
- `start.bat` - Windows批处理启动

### 测试文件
- `ascii_test.py` - 本地功能测试
- `test_functionality.py` - 网络功能测试
- `local_test.py` - 完整测试套件

### 其他
- `README.md` - 详细文档
- `.gitignore` - Git忽略文件
- `logs/` - 日志文件目录
- `exports/` - 导出文件目录

## 🎯 下一步

项目已经优化完成，具备以下特性：
1. **完整的错误处理机制**
2. **详细的日志系统**
3. **可配置参数管理**
4. **现代化用户界面**
5. **统计和报告功能**
6. **多URL支持**
7. **自动重试机制**

现在可以直接使用这个项目了！运行 `python simple_start.py` 开始体验增强版的GitHub访问检测工具。