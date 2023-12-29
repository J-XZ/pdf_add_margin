#!/opt/homebrew/bin/fish

# 获取本文件路径
set current_path (dirname (status -f))

set input_file $argv[1]
set output_file1 (dirname $input_file)/(basename $input_file .pdf)_margin.pdf
set output_file2 (dirname $input_file)/(basename $input_file .pdf)_margin_compress.pdf

python3.11 $current_path/pdfm.py $input_file $output_file1
python3.11 $current_path/pdfc.py -c 4 -o $output_file2 $output_file1

# 比较文件大小，并删除较大的一个
set size1 (stat -f %z $output_file1)
set size2 (stat -f %z $output_file2)
if test $size1 -gt $size2
    rm $output_file1
else
    rm $output_file2
    mv $output_file1 $output_file2
end

