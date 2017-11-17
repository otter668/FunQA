#!/bin/bash
if [ ! -s features.log ]; then
    echo "usage: $0"
    echo 'Clear the file of temp data'
    echo 'the file feature.log doesnot exist!'
    exit 1
fi
while read line; do
rm -f data/"$line"
rm -f data/"$line"_fine_vec
rm -f data/"$line"_coarse_vec
rm -f data/"$line"_fine_vec_1
rm -f data/"$line"_coarse_vec_1
rm -f data/"$line"_fine_vec_2
rm -f data/"$line"_coarse_vec_2
rm -f data/"$line"_fine_line_model
rm -f data/"$line"_coarse_line_model
rm -f data/"$line"_fine_line_result
rm -f data/"$line"_coarse_line_result
done <features.log
rm -f features.log
echo DONE!