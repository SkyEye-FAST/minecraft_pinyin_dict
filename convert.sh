#!/bin/bash

# 获取转换器
TARGET_DIR="imewlconverter_linux"
DOWNLOAD_URL="https://github.com/studyzy/imewlconverter/releases/download/v3.1.0/imewlconverter_Linux.tar.gz"
ARCHIVE_NAME="imewlconverter_Linux.tar.gz"
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

if [ ! -d "$SCRIPT_DIR/$TARGET_DIR" ] || [ -z "$(ls -A "$SCRIPT_DIR/$TARGET_DIR")" ]; then
    mkdir -p "$SCRIPT_DIR/$TARGET_DIR"
    if ! wget -O "$SCRIPT_DIR/$ARCHIVE_NAME" "$DOWNLOAD_URL"; then
        echo "下载失败，请检查网络连接或URL"
        exit 1
    fi

    if ! tar --strip-components=1 -xzvf "$SCRIPT_DIR/$ARCHIVE_NAME" -C "$SCRIPT_DIR/$TARGET_DIR"; then
        echo "解压失败"
        rm -f "$SCRIPT_DIR/$ARCHIVE_NAME"
        exit 1
    fi

    rm -f "$SCRIPT_DIR/$ARCHIVE_NAME"
fi

FINAL_OUTPUT_FILE_MSPY="$SCRIPT_DIR/output/Microsoft Pinyin.dat"
RIME_OUTPUT_FILE="$SCRIPT_DIR/output/Rime.txt"
CONVERTER="$SCRIPT_DIR/$TARGET_DIR/ImeWlConverterCmd"
TEMP_FILE="$SCRIPT_DIR/$TARGET_DIR/1.txt"
WIN10_OUTPUT_FILE="$SCRIPT_DIR/$TARGET_DIR/Win10微软拼音词库.dat"
SOGOU_OUTPUT_FILE="$SCRIPT_DIR/output/Sogou Pinyin.txt"

mkdir -p "$SCRIPT_DIR/output"

# 转换微软拼音
if [ -f "$FINAL_OUTPUT_FILE_MSPY" ]; then
    rm -f "$FINAL_OUTPUT_FILE_MSPY"
fi
if ! "$CONVERTER" -i:rime "$RIME_OUTPUT_FILE" -o:win10mspy "$TEMP_FILE"; then
    echo "微软拼音词库转换失败"
    exit 1
fi
mv "$WIN10_OUTPUT_FILE" "$FINAL_OUTPUT_FILE_MSPY"
rm -f "$TEMP_FILE"

# 转换搜狗拼音
if ! "$CONVERTER" -i:rime "$RIME_OUTPUT_FILE" -o:sgpy "$SOGOU_OUTPUT_FILE"; then
    echo "搜狗拼音词库转换失败"
    exit 1
fi

echo "转换完成"