# -*- encoding: utf-8 -*-
"""Minecraft拼音词库生成器"""

import json
import csv
from pathlib import Path
from typing import TypeAlias, Dict, List

from pypinyin import lazy_pinyin, load_phrases_dict
from pypinyin_dict.phrase_pinyin_data import cc_cedict, di

# 当前绝对路径
P = Path(__file__).resolve().parent

# 文件夹
LANG_DIR = P / "mc_lang"
LANG_DIR_FULL = LANG_DIR / "full"
LANG_DIR_VALID = LANG_DIR / "valid"
OUTPUT_DIR = P / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# 类型别名
Ldata: TypeAlias = Dict[str, str]

# 初始化pypinyin
cc_cedict.load()
di.load()
with open(P / "data" / "phrases.json", "r", encoding="utf-8") as f:
    phrases: Ldata = json.load(f)
load_phrases_dict({k: [[_] for _ in v.split()] for k, v in phrases.items()})

# 读取语言文件
with open(LANG_DIR_VALID / "zh_cn.json", "r", encoding="utf-8") as f:
    data: Ldata = json.load(f)

# 处理语言文件数据
data_list: List[str] = [
    v
    for v in data.values()
    if all(_ not in v for _ in "？！。，、；：“”‘’《》0123456789")
]
exclude_values = {"TNT", "TNT矿车", "Minecraft"}
values: List[str] = [v for v in sorted(set(data_list)) if v not in exclude_values]

# 写入拼音词库文件
with open(OUTPUT_DIR / "Rime.txt", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    for element in values:
        writer.writerow([element, " ".join(lazy_pinyin(element)), 1])
