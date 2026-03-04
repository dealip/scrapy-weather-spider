#! /usr/bin/env python3
import os
import sys


def run_command(cmd, desc):
    """
    执行系统命令，并处理执行结果

    参数:
        cmd: 要执行的命令字符串
        desc: 命令描述，用于输出提示

    功能:
        - 执行命令并检查返回码
        - Windows系统下处理返回码的特殊性
        - 命令失败时退出脚本
    """
    print(f"\n==={desc}===")

    # 执行命令，获取返回码(0=成功，非0=失败)
    exit_code = os.system(cmd)

    # Windows系统特殊处理：os.system返回值为命令执行结果的高8位
    # 所以需要右移8位才能得到正确的返回码
    if os.name == "nt":  # nt 表示Windows系统
        exit_code >>= 8

    # 根据返回码判断命令执行结果
    if exit_code == 0:
        print(f"命令执行成功: {cmd}")
    else:
        print(f"命令执行失败({exit_code}): {cmd}")
        sys.exit(exit_code)  # 失败时退出整个脚本


if __name__ == "__main__":
    # Windows系统设置：解决中文显示问题
    if os.name == "nt":
        # 将终端编码设置为UTF-8，避免中文乱码
        # > nul 用于隐藏命令输出信息
        os.system("chcp 65001 > nul")

    # 第一步：执行flake8检查（初始检查）
    run_command("flake8 .", "运行flake8检查")

    try:
        # 1. autoflake自动清理工具
        # 合并成一条命令，添加--expand-star-imports（可选，处理*导入）、--verbose（看清理日志）
        run_command(
            "autoflake --in-place --remove-all-unused-imports --remove-unused-variables --expand-star-imports --verbose .",
            "自动清理未使用的导入/变量",
        )

        # 2. black代码格式化工具
        # 自动格式化代码为统一风格
        run_command("black .", "代码格式化(black)")

        # 3. 再次执行flake8检查（验证格式化后的代码）
        run_command("flake8 .", "代码风格检查(flake8)")

        # 所有检查通过
        print("\n === 所有检查通过 ===\n")

    except Exception as e:
        # 捕获并处理可能出现的异常
        print(f"\n === 检查过程中出现错误: {str(e)} ===\n")
        sys.exit(1)
