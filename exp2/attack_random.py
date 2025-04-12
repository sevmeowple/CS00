#!/usr/bin/env python3

import subprocess
import re
import statistics
from collections import Counter

def get_stack_info(attempt=0):
    """Get stack information from the program"""
    try:
        gdb_commands = [
            "set args AAAA",
            "b welcome",  
            "r",
            "i r esp",    
            "x/16wx $esp", 
            "quit"
        ]

        gdb_output = subprocess.check_output(
            ["gdb", "-q", "-ex", " ".join(gdb_commands), "./vul"],
            stderr=subprocess.STDOUT,
            timeout=5          
        ).decode("utf-8")

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
        print(f"Attempt {attempt} timed out")
        return None
    except Exception as e:
        print(f"Attempt {attempt} error: {e}")
        return None

def analyze_addresses(addresses, num_runs):
    """Analyze collected addresses"""
    if not addresses:
        return
    
    esp_values = [info['esp'] for info in addresses if 'esp' in info]
    
    print(f"\n--- Stack Address Statistics (Success rate: {len(esp_values)}/{num_runs} = {len(esp_values)/num_runs*100:.2f}%) ---")
    print(f"Min value: 0x{min(esp_values):08x}")
    print(f"Max value: 0x{max(esp_values):08x}")
    print(f"Average: 0x{statistics.mean(esp_values):.0f}")
    print(f"Median: 0x{statistics.median(esp_values):.0f}")
    print(f"Std Dev: {statistics.stdev(esp_values):.2f}")
    print(f"Range size: {max(esp_values) - min(esp_values)} bytes")
    
    counter = Counter(esp_values)
    most_common = counter.most_common(5)
    print("\nMost common addresses:")
    for addr, count in most_common:
        print(f"0x{addr:08x}: occurs {count} times ({count/len(esp_values)*100:.2f}%)")
    
    return statistics.mean(esp_values)

def main():
    num_runs = 100  # Set number of runs
    print(f"Starting stack address analysis (attempts: {num_runs})")
    
    address_info_list = []
    for i in range(num_runs):
        if i % 10 == 0:
            print(f"Progress: {i}/{num_runs}")
        info = get_stack_info(i)
        if info:
            address_info_list.append(info)
    
    avg_addr = analyze_addresses(address_info_list, num_runs)
    
    # Generate attack vector reference info
    if avg_addr:
        print(f"\n--- Attack Vector Reference ---")
        print(f"Average stack address: 0x{int(avg_addr):08x}")
        print(f"Possible buffer offset: Needs experimental verification")
        print(f"Note: Due to ASLR, attack success rate will be low, requiring brute force approach")

if __name__ == "__main__":
    main()