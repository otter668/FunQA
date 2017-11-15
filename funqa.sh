#!/bin/bash
# 参数含义：
# 1. 特征模版所在文件，或者特征模版对。
#    特征模版文件内包括两行，第一行是特征名称数组，以空格分割；第二行是特征前缀名称数组，以空格分割。
#    特征模版对是一个数组，分别是特征名称1 特征前缀1 特征名称2 特征前缀2 …… 这样的形式。
# 处理入口参数，若无参数则打印帮助信息
if [ -z $1 ]; then
    echo "usage: $0 <features.in>|[feature_name1 feature_prefix1[ feature_name2 feature_prefix2...]]"
    echo "Integrated testing tools for SVM. V1.0"
    echo "The file of features.in contains 2 lines of feature_name and feature_prefix."
    echo "Or input pair of feature_names and feature_prefixs at here."
    exit 1
fi
# 处理特征模版文件参数和特征对参数
if [ "$#" == '1' ]; then
    if [ -s $1 ]; then
        features=$(sed -n '1p' $1)
        prefixs=$(sed -n '2p' $1)
    else
        echo "File of $1 not exists!"
        exit -1
    fi
else
    argv=("$@")
    for ((i=0;i<${#argv[@]};i+=2)); do
        features[i]=${argv[i]}
        prefixs[i]=${argv[i+1]}
    done
fi
# 根据后缀进行SVM分类
for suffix in "" + - +-; do
    if [ ! -s data/seg$suffix ] || [ ! -s data/splitpoint$suffix ]; then
        if [ -z $suffix ]; then 
            bash preprocessing.sh test train "" corpora splitpoint seg pyltp
        else
            bash preprocessing.sh test train "$suffix" corpora splitpoint seg pyltp
        fi
    fi
    echo training set of "train$suffix"
    paste <(for feature in ${features[@]}; do echo $feature; done) \
    <(for prefix in ${prefixs[@]}; do echo $prefix; done) | \
    while read feature prefix; do
        # 编码
        bash encoding.sh "seg$suffix" "splitpoint$suffix" "$feature" "$prefix$suffix" seq
        # 使用SVM训练并预测
        bash svm.sh "$prefix$suffix"
        echo "$prefix$suffix" >> features.log
    done
done
