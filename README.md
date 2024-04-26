<div align="center">

# clovers-setu-collection

</div>

使用的 API:

[Jitsu](https://image.anosu.top/) 简单好用的色图 api

[MirlKoi API](https://iw233.cn/) 可以避免 bot 被封的超安全（保证好看但是不怎么涩）色图 api

[Lolicon API](https://api.lolicon.app/) 使用这个的时候请注意身体

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
# 群聊图片限制（别关）
public_setu_limit = true
```

## 🎉 介绍

**指令**：`来N张xx色图` `来N张xx` `来N张r18xx色图`

**指令（仅私聊）**：切换 api

单次最多发送 5 张色图

群聊支持单个 tag，私聊支持 3 个 tag（因为私聊用 Lolicon），用空格隔开。

## 📞 联系

如有建议，bug 反馈等可以加群

机器人 bug 研究中心（闲聊群） 744751179

永恒之城（测试群） 724024810

![群号](https://github.com/clovers-project/clovers/blob/master/%E9%99%84%E4%BB%B6/qrcode_1676538742221.jpg)
