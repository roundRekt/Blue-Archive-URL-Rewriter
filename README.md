# Blue-Archive-URL-Rewriter

<div align="center">
自动解密、获取并修改「ブルーアーカイブ」APK 中的 ServerInfoDataUrl，以实现汉化等目的。</div>


## 用途 / Usage

```python
from rewrite_url import ServerInfoUrlRewriter

ServerInfoUrlRewriter().fast_rewrite("/path/to/your/directory", "example.com") # 根据路径和目标 URL 自动修改文件

#rewriter = ServerInfoUrlRewriter()

#rewriter.get_gamemainconfig(path) # 获取 GameMainConfig 并保存到 self.original_config

#rewriter.get_serverinfo_url() # 根据 GameMainConfig 解析 ServerInfo URL 并保存到 self.original_url
#rewriter.get_serverinfo_url(original_config) # 可输入字符串类型的 Base64 编码的加密 GameMainConfig

#rewriter.modify_serverinfo_url(target_url) # 修改 ServerInfo URL 并保存到 self.modified_url
#rewriter.modify_serverinfo_url(target_url, original_url) # 可输入自定义原始 ServerInfo URL

#rewriter.modify_config() # 根据修改后的 ServerInfo URL 修改 GameMainConfig 并保存到 self.modified_config
#rewriter.modify_config(original_config, modified_url) # 可选输入字符串类型的 Base64 编码的加密 GameMainConfig 和修改后的 ServerInfo URL

#rewriter.rewrite_config(path) # 根据修改后的 GameMainConfig 写回文件
#rewriter.rewrite_config(path, modified_config) # 可选输入字符串类型的 Base64 编码的加密 GameMainConfig
```


## 关于 / About

- `lib.encryption` 库来自 [Blue-Archive-Asset-Downloader](https://github.com/ZM-Kimu/Blue-Archive-Asset-Downloader)