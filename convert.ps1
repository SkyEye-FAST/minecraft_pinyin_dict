$scriptPath = $PSScriptRoot
Set-Location -Path $scriptPath

# 定义路径
$inputFile = "output\Rime.txt"
$outputFileMSPY = "imewlconverter_windows\Win10微软拼音词库.dat"
$tempFile = "imewlconverter_windows\1.txt"
$finalOutputFileMSPY = "output\Microsoft Pinyin.dat"
$outputFileSGPY = "output\Sogou Pinyin.txt"
$converterExe = "imewlconverter_windows\深蓝词库转换.exe"

# 转换微软拼音
if (Test-Path -Path $finalOutputFileMSPY) {
    Remove-Item -Path $finalOutputFileMSPY
}
& $converterExe -i:rime $inputFile -o:win10mspy $tempFIle
Start-Sleep -Seconds 3
Move-Item -Path $outputFileMSPY -Destination $finalOutputFileMSPY
Remove-Item -Path $tempFile

# 转换搜狗拼音
& $converterExe -i:rime $inputFile -o:sgpy $outputFileSGPY