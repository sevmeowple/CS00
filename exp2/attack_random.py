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
        print("Attempt {0} timed out".format(attempt))
        return None
    except Exception as e:
        print("Attempt {0} error: {1}".format(attempt, e))
        return None

def analyze_addresses(addresses, num_runs):
    """Analyze collected addresses"""
    if not addresses:
        return
    
    esp_values = [info['esp'] for info in addresses if 'esp' in info]
    
    success_rate = len(esp_values)/num_runs*100
    print("\n--- Stack Address Statistics (Success rate: {0}/{1} = {2:.2f}%) ---".format(
        len(esp_values), num_runs, success_rate))
    print("Min value: 0x{0:08x}".format(min(esp_values)))
    print("Max value: 0x{0:08x}".format(max(esp_values)))
    print("Average: 0x{0:.0f}".format(statistics.mean(esp_values)))
    print("Median: 0x{0:.0f}".format(statistics.median(esp_values)))
    print("Std Dev: {0:.2f}".format(statistics.stdev(esp_values)))
    print("Range size: {0} bytes".format(max(esp_values) - min(esp_values)))
    
    counter = Counter(esp_values)
    most_common = counter.most_common(5)
    print("\nMost common addresses:")
    for addr, count in most_common:
        print("0x{0:08x}: occurs {1} times ({2:.2f}%)".format(
            addr, count, count/len(esp_values)*100))
    
    return statistics.mean(esp_values)

def main():
    num_runs = 100  # Set number of runs
    print("Starting stack address analysis (attempts: {0})".format(num_runs))
    
    address_info_list = []
    for i in range(num_runs):
        if i % 10 == 0:
            print("Progress: {0}/{1}".format(i, num_runs))
        info = get_stack_info(i)
        if info:
            address_info_list.append(info)
    
    avg_addr = analyze_addresses(address_info_list, num_runs)
    
    # Generate attack vector reference info
    if avg_addr:
        print("\n--- Attack Vector Reference ---")
        print("Average stack address: 0x{0:08x}".format(int(avg_addr)))
        print("Possible buffer offset: Needs experimental verification")
        print("Note: Due to ASLR, attack success rate will be low, requiring brute force approach")

if __name__ == "__main__":
    main()