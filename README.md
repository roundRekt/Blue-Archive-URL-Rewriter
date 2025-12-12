# Blue-Archive-URL-Rewriter

<div align="center">
自动解密、获取并修改「ブルーアーカイブ」APK 中的 ServerInfoDataUrl 和 Sdk_Url，以实现汉化、加速等目的。</div>

## 用途 / Usage

```python
from rewrite_url import ServerInfoUrlRewriter
from rewrite_url import SdkUrlRewriter

ServerInfoUrlRewriter().fast_rewrite("/path/to/your/directory", "example.com") # 根据路径和目标 URL 自动修改文件
SdkUrlRewriter().fast_rewrite("/path/to/your/directory", "example.com") # 根据路径和目标 URL 自动修改文件

#serverinfourlrewriter = ServerInfoUrlRewriter()

#serverinfourlrewriter.get_gamemainconfig(path) # 获取 GameMainConfig 并保存到 self.original_config

#serverinfourlrewriter.get_serverinfo_url() # 根据 GameMainConfig 解析 ServerInfo URL 并保存到 self.original_url
#serverinfourlrewriter.get_serverinfo_url(original_config) # 可输入字符串类型的 Base64 编码的加密 GameMainConfig

#serverinfourlrewriter.modify_serverinfo_url(target_url) # 修改 ServerInfo URL 并保存到 self.modified_url
#serverinfourlrewriter.modify_serverinfo_url(target_url, original_url) # 可输入自定义原始 ServerInfo URL

#serverinfourlrewriter.modify_config() # 根据修改后的 ServerInfo URL 修改 GameMainConfig 并保存到 self.modified_config
#serverinfourlrewriter.modify_config(original_config, modified_url) # 可选输入字符串类型的 Base64 编码的加密 GameMainConfig 和修改后的 ServerInfo URL

#serverinfourlrewriter.rewrite_config(path) # 根据修改后的 GameMainConfig 写回文件
#serverinfourlrewriter.rewrite_config(path, modified_config) # 可选输入字符串类型的 Base64 编码的加密 GameMainConfig

#sdkurlrewriter = SdkUrlRewriter()

#sdkurlrewriter.get_sdkconfigsettings(path) # 获取 SDKConfigSettings 并保存到 self.original_config

#sdkurlrewriter.get_sdk_url() # 根据 SDKConfigSettings 解析 SDK URL 并保存到 self.original_url
#sdkurlrewriter.get_sdk_url(original_config) # 可输入字符串类型的 SDKConfigSettings

#sdkurlrewriter.modify_sdk_url(target_url) # 修改 SDK URL 并保存到 self.modified_url

#sdkurlrewriter.modify_config() # 根据修改后的 SDK URL 修改 SDKConfigSettings 并保存到 self.modified_config
#sdkurlrewriter.modify_config(original_config, modified_url) # 可选输入字符串类型的 SDKConfigSettings 和修改后的 SDK URL

#sdkurlrewriter.rewrite_config(path) # 根据修改后的 SDKConfigSettings 写回文件
#sdkurlrewriter.rewrite_config(path, modified_config) # 可选输入字符串类型的 SDKConfigSettings
```

## 关于 / About

- `lib.encryption` 库来自 [Blue-Archive-Asset-Downloader](https://github.com/ZM-Kimu/Blue-Archive-Asset-Downloader)
