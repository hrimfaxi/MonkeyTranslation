# 使用方法

```shell
./xlsxtocsv.py aaa.xlsx #转化为csv
find . -iname "*.xlsx" -print0 -o -iname "*.xls" -print0 | xargs -P $(nproc) -I % -0 ../xlsxtocsv.py %
```

## 统计字数

凡是字数只包含汉字和日文平假名、片假名

```shell
find . -iname "*.csv" -print0 | xargs -P $(nproc) -I % -0 ../unpack.py % %.out > a
for file in *.csv; do ../unpack.py  "$file" "/tmp/$file"; done 
/tmp/a.导出.csv: 26306 entries exported. 336250 CJK charactors found.
/tmp/exported_Sheet1.csv: 53968 entries exported. 443568 CJK charactors found.
```

## 统计去重复字数:

```shell
find . -iname "*.csv" -print0 | xargs -P $(nproc) -I % -0 ../unpack.py -u % %.out > b
for file in *.csv; do ../unpack.py -u "$file" "/tmp/$file"; done 
Unique mode selected
/tmp/a.导出.csv: 26306 entries exported. 336250 CJK charactors found.
Unique mode selected
/tmp/exported_Sheet1.csv: 26306 entries exported. 336250 CJK charactors found.
```

## 总结 

```shell
find . -iname "*.xlsx" -print0 -o -iname "*.xls" -print0 | xargs -P $(nproc) -I % -0 ../xlsxtocsv.py %
find . -iname "*.csv" -print0 | xargs -P $(nproc) -I % -0 ../unpack.py % %.out > a
find . -iname "*.csv" -print0 | xargs -P $(nproc) -I % -0 ../unpack.py -u % %.out > b
../summary.sh
```
