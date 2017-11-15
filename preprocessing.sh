#!/bin/bash
# 参数含义：
# 1. 测试集数据文件，如：test
# 2. 训练集数据文件，如：train
# 3. 训练集后缀符，如 ,+,-,+-
# 4. 合并后数据文件，如：corpora
# 5. 分割点文件，如：splitpoint
# 6. 分词后语料数据文件，如：seg
# 7. 分词器名，如：pyltp、jieba、pynlpir
# 合并测试集和训练集，后续统一处理
if [ ! -s data/$4$3 ] || [ ! -s data/$5$3 ]; then
    python merge.py -fs data/$1 data/$2$3 -o data/$4$3 > data/$5$3
fi
# 分词，词性标注，命名实体识别和依存句法分析
if [ ! -s data/$6$3 ]; then
    python tokenizer.py -s $7 -l -p < data/$4$3 | python nerecognizer.py | python parser.py > data/$6$3
fi
# 预处理结束，打印结果信息
echo Preprocessing $2$3 End!