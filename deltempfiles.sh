#!/bin/bash
if [ ! -s features.log ]; then
    echo "usage: $0"
    echo 'Clear the file of temp data'
    echo 'the file feature.log doesnot exist!'
    exit 1
fi
for name in 'seg' 'splitpoint' 'corpora'; do
    for fname in data/$name*; do
        rm -f $fname
    done
done
while read line; do
    rm -f data/"$line"
    for fn in data/"$line"_*; do
        rm -f $fn
        # echo $fn
    done
done <features.log
rm -f features.log
echo DONE!