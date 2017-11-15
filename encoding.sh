#!/bin/bash
# 参数含义：
# 1. 输入经分词过的语料数据文件，如：seg
# 2. 分割点文件，如：splitpoint
# 3. 特征名称，如：bow，baseline，b+q+r
# 4. 特征对应的存储文件名前缀，如：bow，baseline，b_q_r
# 5. 分割方式，如：seq、ran、tag
# 抽取特征模版
if [ ! -s data/$4 ]; then
    python extfeatures.py -f $3 < data/$1 > data/$4
fi
# 分小类和大类编码
if [ ! -s data/$4_fine_vec ]; then
    python wordset_encoding.py -f $3 < data/$4 > data/$4_fine_vec
fi
if [ ! -s data/$4_coarse_vec ]; then
    python wordset_encoding.py -t -f $3 < data/$4 > data/$4_coarse_vec
fi
# 分割为测试集和训练集
if [ ! -s data/$4_fine_vec_1 ] || [ ! -s data/$4_fine_vec_2 ]; then
    python split.py -f data/$4_fine_vec -sp data/$2 -s $5
fi
if [ ! -s data/$4_coarse_vec_1 ] || [ ! -s data/$4_coarse_vec_2 ]; then
    python split.py -f data/$4_coarse_vec -sp data/$2 -s $5
fi
# 特征抽取并编码完成，打印结果信息
echo Encoding with feature of $3 End!