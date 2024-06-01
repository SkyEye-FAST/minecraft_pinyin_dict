# -*- encoding: utf-8 -*-
"""Minecraft拼音词库生成器"""

import json
from typing import TypeAlias, Dict

from pypinyin import lazy_pinyin, load_phrases_dict
from pypinyin_dict.phrase_pinyin_data import cc_cedict, di

from base import P, LANG_DIR_VALID

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

values = sorted(list(set(data.values())))
values.remove("TNT")
values.remove("TNT矿车")

with open(P / "dict.txt", "w", encoding="utf-8") as f:
    f.writelines(
        f"{element}\t{" ".join(lazy_pinyin(element))}\t1\n" for element in values
    )
