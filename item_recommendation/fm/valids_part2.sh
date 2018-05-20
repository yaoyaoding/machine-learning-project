#!/bin/bash

echo "iter 200 dim 4"
make valid iter=200 dim=1,1,4 > iter200_dim4.log
echo "iter 200 dim 8"
make valid iter=200 dim=1,1,8 > iter200_dim8.log
echo "iter 200 dim 16"
make valid iter=200 dim=1,1,16 > iter200_dim16.log

