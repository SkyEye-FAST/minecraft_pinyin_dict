@echo off
chcp 65001
setlocal

REM 定义路径
set scriptPath=%~dp0
cd /d %scriptPath%

set inputFile=output\Rime.txt
set outputFileMSPY="imewlconverter_windows\Win10微软拼音词库.dat"
set tempFile=imewlconverter_windows\1.txt
set finalOutputFileMSPY="output\Microsoft Pinyin.dat"
set outputFileSGPY="output\Sogou Pinyin.txt"
set converterExe="imewlconverter_windows\深蓝词库转换.exe"

REM 转换微软拼音
if exist %finalOutputFileMSPY% (
    del %finalOutputFileMSPY%
)
%converterExe% -i:rime %inputFile% -o:win10mspy %tempFile%
move %outputFileMSPY% %finalOutputFileMSPY%
del %tempFile%

REM 转换搜狗拼音
%converterExe% -i:rime %inputFile% -o:sgpy %outputFileSGPY%

endlocal
