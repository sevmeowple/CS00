#!/bin/bash

gcc -z execstack -o fmtstr ../fmtstr.c;
sudo chown root:root ./fmtstr;
sudo chmod 4755 ./fmtstr;
