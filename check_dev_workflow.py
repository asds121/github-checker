#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发工作流程检查脚本
按照 dev-workflow.md 进行逐项检查
"""

import subprocess
import sys
from pathlib import Path

class Colors:
    """终端颜色常量"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text):
    """打印标题"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def run_command(cmd, description):
    """运行命令并返回结果"""
    print(f"🔍 {description}...")
    try:
        # Windows 系统使用 gbk 编码
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='gbk',
            errors='ignore'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_flake8():
    """检查代码规范"""
    print_header("1. 代码规范检查 (Flake8)")
    
    success, stdout, stderr = run_command(
        "flake8 github_checker.py",
        "运行 flake8 检查"
    )
    
    if success:
        print_success("Flake8 检查通过")
        return True
    else:
        print_error(f"Flake8 检查失败:\n{stdout}")
        return False

def check_tests():
    """检查测试"""
    print_header("2. 测试验证 (Pytest)")
    
    success, stdout, stderr = run_command(
        "python -m pytest tests/test_github_checker.py -v",
        "运行单元测试"
    )
    
    if success:
        # 统计测试数量
        if "passed" in stdout:
            print_success("所有测试通过")
            return True
        else:
            print_warning("测试运行完成，但未找到通过标记")
            return True
    else:
        print_error(f"测试失败:\n{stdout}")
        return False

def check_module_import():
    """检查模块导入"""
    print_header("3. 模块导入检查")
    
    success, stdout, stderr = run_command(
        'python -c "import github_checker; print(\'模块导入成功\')"',
        "测试模块导入"
    )
    
    if success:
        print_success("模块导入成功")
        return True
    else:
        print_error(f"模块导入失败:\n{stderr}")
        return False

def check_project_structure():
    """检查项目结构"""
    print_header("4. 项目结构检查")
    
    required_files = [
        "github_checker.py",
        "requirements.txt",
        "README.md",
        ".flake8",
        ".gitignore",
        "tests/test_github_checker.py"
    ]
    
    required_dirs = [
        "docs",
        "tools"
    ]
    
    all_ok = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"文件存在: {file_path}")
        else:
            print_error(f"文件缺失: {file_path}")
            all_ok = False
    
    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print_success(f"目录存在: {dir_path}")
        else:
            print_error(f"目录缺失: {dir_path}")
            all_ok = False
    
    return all_ok

def check_documentation():
    """检查文档"""
    print_header("5. 文档检查")
    
    docs_dir = Path("docs")
    if not docs_dir.is_dir():
        print_error("docs 目录不存在")
        return False
    
    required_docs = [
        "01-需求分析.md",
        "02-系统设计.md",
        "03-详细设计.md",
        "13-代码提交检查清单.md",
        "14-设计决策记录.md"
    ]
    
    all_ok = True
    for doc in required_docs:
        doc_path = docs_dir / doc
        if doc_path.exists():
            print_success(f"文档存在: {doc}")
        else:
            print_warning(f"文档缺失: {doc}")
            # 不影响整体结果，因为某些文档可能不是必需的
    
    return all_ok

def check_git_status():
    """检查 Git 状态"""
    print_header("6. Git 状态检查")
    
    success, stdout, stderr = run_command(
        "git status --short",
        "检查 Git 状态"
    )
    
    if success:
        if stdout.strip():
            print_warning("存在未提交的更改:")
            print(stdout)
        else:
            print_success("工作区干净，无未提交更改")
        return True
    else:
        print_warning("无法检查 Git 状态（可能不是 Git 仓库）")
        return True  # 不影响整体结果

def main():
    """主函数"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}开发工作流程检查{Colors.RESET}")
    print(f"{Colors.BLUE}按照 dev-workflow.md 进行逐项检查{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    results = {
        "代码规范检查": check_flake8(),
        "测试验证": check_tests(),
        "模块导入": check_module_import(),
        "项目结构": check_project_structure(),
        "文档检查": check_documentation(),
        "Git 状态": check_git_status()
    }
    
    # 打印总结
    print_header("检查总结")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        if result:
            print_success(f"{check_name}: 通过")
        else:
            print_error(f"{check_name}: 失败")
    
    print(f"\n{Colors.BLUE}总计: {passed}/{total} 项检查通过{Colors.RESET}\n")
    
    if passed == total:
        print_success("🎉 所有检查通过！项目符合开发工作流程要求。")
        return 0
    else:
        print_warning(f"⚠️  有 {total - passed} 项检查未通过，请修复后重试。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
