#!/bin/bash

# This script builds the vulnerable program with the necessary flags
gcc -fno-stack-protector -z execstack -o vul ../vul.c;
sudo chown root ./vul;
sudo chmod 4755 ./vul;