#!/bin/bash

# 定义文件路径
finalOutputFileMSPY="output/Microsoft Pinyin.dat"
rimeOutputFile="output/Rime.txt"
imewlConverter="imewlconverter_linux/ImeWlConverterCmd"
tempFile="imewlconverter_linux/1.txt"
win10OutputFile="imewlconverter_linux/Win10微软拼音词库.dat"
sogouOutputFile="output/Sogou Pinyin.txt"

# 转换微软拼音
if [ -f "$finalOutputFileMSPY" ]; then
  rm -f "$finalOutputFileMSPY"
fi
$imewlConverter -i:rime "$rimeOutputFile" -o:win10mspy "$tempFile"
mv "$win10OutputFile" "$finalOutputFileMSPY"
rm -f "$tempFile"

# 转换搜狗拼音
$imewlConverter -i:rime "$rimeOutputFile" -o:sgpy "$sogouOutputFile"
