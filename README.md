<div align="center">

# clovers-setu-collection

_✨ 从多个 api 获取色图并根据场景整合的色图插件 ✨_

<img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="python">
<a href="./LICENSE"><img src="https://img.shields.io/github/license/KarisAya/clovers_setu_collection.svg" alt="license"></a>
<a href="https://pypi.python.org/pypi/clovers_setu_collection"><img src="https://img.shields.io/pypi/v/clovers_setu_collection.svg" alt="pypi"></a>
<a href="https://pypi.python.org/pypi/clovers_setu_collection"><img src="https://img.shields.io/pypi/dm/clovers_setu_collection" alt="pypi download"></a>

</div>

## 💿 安装

```bash
pip install clovers-setu-collection
```

## ⚙️ 配置

```toml
[clovers_setu_collection]
# 是否保存从api获取的图片
save_image = true
# 主路径
path = "data\\setu_collection"
# 私聊图片限制
private_setu_limit = false
# 私聊使用的图片api
private_setu_api  = "Lolicon API"
# 群聊图片限制（别关）
public_setu_limit = true
# 群聊使用的图片api
public_setu_api = "Jitsu/MirlKoi API"
```

## 🎉 介绍

**指令**：`来N张xx色图` `来N张xx` `来N张r18xx色图`

**指令**：切换 api

单次最多发送 5 张色图

群聊支持单个 tag，私聊支持 3 个 tag（因为私聊用 Lolicon），用空格隔开。

## 📞 联系

如有建议，bug 反馈等可以加群

机器人 bug 研究中心（闲聊群） 744751179

永恒之城（测试群） 724024810

![群号](https://github.com/clovers-project/clovers/blob/master/%E9%99%84%E4%BB%B6/qrcode_1676538742221.jpg)

## 💡 使用的 API

[Jitsu](https://image.anosu.top/) 简单好用的色图 api

[MirlKoi API](https://iw233.cn/) 可以避免 bot 被封的超安全（好看但是不涩）色图 api

[Lolicon API](https://api.lolicon.app/) 使用这个的时候请注意身体
