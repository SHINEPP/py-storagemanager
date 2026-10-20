#!/usr/bin/env python3
"""
Android 签名证书 (keystore) 密码暴力破解脚本
------------------------------------------------
用途：恢复自己遗忘的 keystore 密码（store 密码与 key 密码相同）
前提：已知 alias 为 key0，密码疑似为日期格式，范围在 20260501 至 20260916 之前
依赖：Java keytool（随 JDK 安装，需确保已加入 PATH）

用法示例：
    python3 keystore_brute_force.py my.keystore
    python3 keystore_brute_force.py my.keystore --start 20260501 --end 20260916
    python3 keystore_brute_force.py my.keystore --formats %Y%m%d %Y-%m-%d %m%d%Y
"""

import argparse
import datetime
import subprocess
import sys


def try_password(keystore_path: str, alias: str, password: str) -> bool:
    """尝试用给定密码打开 keystore 并读取指定 alias 的证书信息"""
    cmd = [
        "keytool", "-list",
        "-keystore", keystore_path,
        "-alias", alias,
        "-storepass", password,
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def generate_date_candidates(start: str, end: str, fmt: str):
    """生成 [start, end) 区间内每一天按指定格式生成的候选密码"""
    start_date = datetime.datetime.strptime(start, "%Y%m%d").date()
    end_date = datetime.datetime.strptime(end, "%Y%m%d").date()
    current = start_date
    while current < end_date:
        yield current.strftime(fmt)
        current += datetime.timedelta(days=1)


def main():
    parser = argparse.ArgumentParser(description="Android keystore 密码（日期范围）暴力破解工具")
    parser.add_argument("keystore", help="keystore 文件路径 (.jks / .keystore)",
                        default="/Users/zhouzhenliang/source/gp-repackage/app-linklevelup/app/release-gp.keystore")
    parser.add_argument("--alias", default="key0", help="证书别名，默认 key0")
    parser.add_argument("--start", default="20250101", help="起始日期 YYYYMMDD（含）")
    parser.add_argument("--end", default="20270916", help="结束日期 YYYYMMDD（不含）")
    parser.add_argument(
        "--formats",
        nargs="*",
        default=["%Y%m%d"],
        help="要尝试的日期格式列表，默认只用 %%Y%%m%%d，"
             "可追加如 %%Y-%%m-%%d、%%m%%d%%Y、%%d%%m%%Y 等常见变体",
    )
    args = parser.parse_args()

    tried = 0
    for fmt in args.formats:
        for pwd in generate_date_candidates(args.start, args.end, fmt):
            tried += 1
            print(f"[{tried}] 尝试密码: {pwd}", end="\r", flush=True)
            if try_password(args.keystore, args.alias, pwd):
                print(f"\n[+] 找到密码: {pwd}  (格式: {fmt})")
                return
    print(f"\n[-] 未找到匹配密码，共尝试 {tried} 次")
    sys.exit(1)


if __name__ == "__main__":
    main()
