# -*- encoding: utf-8 -*-
"""Minecraft语言文件更新器"""

import hashlib
import sys
import requests as r
from base import P, LANG_DIR_FULL


def get_response(url: str):
    """获取响应"""
    try:
        resp = r.get(url, timeout=60)
        resp.raise_for_status()
        return resp
    except r.exceptions.RequestException as ex:
        print(f"请求发生错误: {ex}")
        sys.exit()


def get_file(url: str, file_name: str, file_path: str, sha1: str):
    """下载文件"""
    for _ in range(3):
        with open(file_path, "wb") as f:
            f.write(get_response(url).content)
        size_in_bytes = file_path.stat().st_size
        if size_in_bytes > 1048576:
            size = f"{round(size_in_bytes / 1048576, 2)} MB"
        else:
            size = f"{round(size_in_bytes / 1024, 2)} KB"
        with open(file_path, "rb") as f:
            if hashlib.file_digest(f, "sha1").hexdigest() == sha1:
                print(f"文件SHA1校验一致。文件大小：{size_in_bytes} B（{size}）\n")
                break
            print("文件SHA1校验不一致，重新尝试下载。\n")
    else:
        print(f"无法下载文件“{file_name}”。\n")


# 文件夹
LANG_DIR_FULL.mkdir(exist_ok=True)

# 获取version_manifest_v2.json
version_manifest_path = P / "version_manifest_v2.json"
try:
    print("正在获取版本清单“version_manifest_v2.json”的内容……\n")
    version_manifest = r.get(
        "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json",
        timeout=60,
    )
    version_manifest.raise_for_status()
    version_manifest_json = version_manifest.json()
except r.exceptions.RequestException as e:
    print("无法获取版本清单，请检查网络连接。")
    sys.exit()
V = version_manifest_json["latest"]["snapshot"]

# 获取client.json
client_manifest_url = next(
    (i["url"] for i in version_manifest_json["versions"] if i["id"] == V), None
)

print(f"正在获取客户端索引文件“{client_manifest_url.rsplit('/', 1)[-1]}”的内容……")
client_manifest = get_response(client_manifest_url).json()

# 获取资产索引文件
asset_index_url = client_manifest["assetIndex"]["url"]
print(f"正在获取资产索引文件“{asset_index_url.rsplit('/', 1)[-1]}”的内容……\n")
asset_index = get_response(asset_index_url).json()["objects"]

# 获取语言文件
lang_asset = asset_index.get("minecraft/lang/zh_cn.json")
if lang_asset:
    file_hash = lang_asset["hash"]
    print(f"正在下载语言文件“zh_cn.json”（{file_hash}）……")
    get_file(
        f"https://resources.download.minecraft.net/{file_hash[:2]}/{file_hash}",
        "zh_cn.json",
        LANG_DIR_FULL / "zh_cn.json",
        file_hash,
    )
else:
    print("zh_cn.json不存在。\n")

print("已完成。")
