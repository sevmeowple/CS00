#!/usr/bin/env python3
# improved_stack_analyzer.py - 多次尝试分析栈地址分布

import subprocess
import re
import sys
import statistics
import matplotlib.pyplot as plt
from collections import Counter

def get_stack_info(attempt=0):
    """获取程序的栈信息"""
    try:
        # 使用更可靠的方式获取栈地址信息
        gdb_commands = [
            "set args AAAA",
            "b welcome",  # 在welcome函数设置断点
            "r",
            "i r esp",    # 查看ESP寄存器
            "x/16wx $esp", # 查看栈内容
            "quit"
        ]

        gdb_output = subprocess.check_output(
            ["gdb", "-q", "-ex", " ".join(gdb_commands), "./vul"],
            stderr=subprocess.STDOUT,
            timeout=5  # 添加超时防止挂起
        ).decode("utf-8")

        # 匹配ESP值
        esp_pattern = re.compile(r"esp\s+0x([0-9a-f]+)")
        esp_match = esp_pattern.search(gdb_output)
        
        if esp_match:
            esp_addr = int(esp_match.group(1), 16)
            return {
                'attempt': attempt,
                'esp': esp_addr,
                'output': gdb_output
            }
        return None
    except subprocess.TimeoutExpired:
        print(f"尝试 {attempt} 超时")
        return None
    except Exception as e:
        print(f"尝试 {attempt} 出错: {e}")
        return None

def analyze_addresses(addresses, num_runs):
    """分析收集到的地址"""
    if not addresses:
        print("未收集到任何有效地址")
        return
    
    # 提取ESP值进行统计
    esp_values = [info['esp'] for info in addresses if 'esp' in info]
    
    # 基本统计
    print(f"\n--- 栈地址统计分析 (成功率: {len(esp_values)}/{num_runs} = {len(esp_values)/num_runs*100:.2f}%) ---")
    print(f"最小值: 0x{min(esp_values):08x}")
    print(f"最大值: 0x{max(esp_values):08x}")
    print(f"平均值: 0x{statistics.mean(esp_values):.0f}")
    print(f"中位数: 0x{statistics.median(esp_values):.0f}")
    print(f"标准差: {statistics.stdev(esp_values):.2f}")
    print(f"范围大小: {max(esp_values) - min(esp_values)} 字节")
    
    # 统计最常见的地址
    counter = Counter(esp_values)
    most_common = counter.most_common(5)
    print("\n最常见的地址:")
    for addr, count in most_common:
        print(f"0x{addr:08x}: 出现 {count} 次 ({count/len(esp_values)*100:.2f}%)")
    
    # 绘制分布图
    plt.figure(figsize=(10, 6))
    plt.hist(esp_values, bins=30)
    plt.title(f'栈地址分布 (ASLR Level=2, {len(esp_values)}次运行)')
    plt.xlabel('内存地址')
    plt.ylabel('频率')
    plt.grid(True)
    plt.savefig('stack_address_distribution.png')
    print("\n地址分布图已保存为 stack_address_distribution.png")
    
    return statistics.mean(esp_values)

def main():
    num_runs = 100  # 设置运行次数
    print(f"开始分析栈地址 (尝试次数: {num_runs})")
    
    address_info_list = []
    for i in range(num_runs):
        if i % 10 == 0:
            print(f"进度: {i}/{num_runs}")
        info = get_stack_info(i)
        if info:
            address_info_list.append(info)
    
    avg_addr = analyze_addresses(address_info_list, num_runs)
    
    # 生成攻击向量的参考信息
    if avg_addr:
        print(f"\n--- 攻击向量参考 ---")
        print(f"平均栈地址: 0x{int(avg_addr):08x}")
        print(f"可能的缓冲区偏移量: 推测需要实验确定")
        print(f"注意: 由于ASLR，攻击成功率将较低，需要使用暴力尝试方法")

if __name__ == "__main__":
    main()