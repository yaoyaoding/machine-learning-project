#!/bin/bash

echo "train iter 800 dim 8"
make train iter=600 dim=1,1,8 index=i600_d8
echo "train iter 300 dim 12"
make train iter=300 dim=1,1,12 index=i300_d12
