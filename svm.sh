#!/bin/bash
# 参数含义：
# 1. 特征对应的存储文件名前缀，如：bow，baseline，b_q_r
# 训练model
if [ ! -s data/$1_fine_line_model ]; then
    train -q data/$1_fine_vec_2 data/$1_fine_line_model
fi
if [ ! -s data/$1_coarse_line_model ]; then
    train -q data/$1_coarse_vec_2 data/$1_coarse_line_model
fi
# 通过model预测结果
echo -n fine taxonomy:
predict data/$1_fine_vec_1 data/$1_fine_line_model data/$1_fine_line_result
echo -n coarse taxonomy:
predict data/$1_coarse_vec_1 data/$1_coarse_line_model data/$1_coarse_line_result