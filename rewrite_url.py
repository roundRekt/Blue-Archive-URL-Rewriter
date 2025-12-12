import base64, json, os, UnityPy
from urllib.parse import urlparse
from lib.encryption import create_key, convert_string, encrypt_string

class ServerInfoUrlRewriter:
    def get_gamemainconfig(self, path): # 获取 GameMainConfig 并保存到 self.original_config
        files = []
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath) and "." not in filename:
                files.append(filepath)
        for file in files:
            env = UnityPy.load(file)
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    txt = obj.parse_as_object()
                    if txt.m_Name != "GameMainConfig":
                        continue
                    original_config = txt.m_Script.encode("utf-8", "surrogateescape")
                    self.original_config = base64.b64encode(original_config).decode("utf-8", "surrogateescape")
                    return original_config
        
    def get_serverinfo_url(self, original_config = None): # 根据 GameMainConfig 解析 ServerInfo URL 并保存到 self.original_url
        if original_config is None: original_config = self.original_config
        decrypted_config = convert_string(original_config, create_key("GameMainConfig")) # 解密 GameMainConfig
        config_json = json.loads(decrypted_config)
        encrypted_url = config_json["X04YXBFqd3ZpTg9cKmpvdmpOElwnamB2eE4cXDZqc3ZgTg=="] # 从键值对获取加密的 ServerInfo URL
        decrypted_url = convert_string(encrypted_url, create_key("ServerInfoDataUrl")) # 解密 ServerInfo URL
        self.original_url = decrypted_url
        print(f"已获取的 ServerInfo URL: {decrypted_url}")
        return decrypted_url

    def modify_serverinfo_url(self, target_url, original_url = None): # 修改 ServerInfo URL 并保存到 self.modified_url
        if original_url is None: original_url = self.original_url
        filename = os.path.basename(urlparse(original_url).path) # 获取文件名
        if not urlparse(target_url).scheme: # 补全协议，默认https
            target_url = "https://" + target_url
        if not target_url.endswith("/"): # 补全斜杠
            target_url += "/"
        modified_url = target_url + filename
        self.modified_url = modified_url
        print(f"修改后的 ServerInfo URL: {modified_url}")
        return modified_url

    def modify_config(self, original_config = None, modified_url = None): # 根据修改后的 ServerInfo URL 修改 GameMainConfig 并保存到 self.modified_config
        if original_config is None: original_config = self.original_config
        if modified_url is None: modified_url = self.modified_url
        decrypted_config = convert_string(original_config, create_key("GameMainConfig")) # 解密 GameMainConfig
        encrypted_url = encrypt_string(modified_url, create_key("ServerInfoDataUrl")) # 加密修改后的 ServerInfo URL
        config_json = json.loads(decrypted_config)
        config_json["X04YXBFqd3ZpTg9cKmpvdmpOElwnamB2eE4cXDZqc3ZgTg=="] = encrypted_url
        encrypted_config = encrypt_string(json.dumps(config_json, separators=(',', ':')), create_key("GameMainConfig"))
        self.modified_config = encrypted_config
        print("已生成修改后的 GameMainConfig")
        return encrypted_config

    def rewrite_config(self, path, modified_config = None): # 根据修改后的 GameMainConfig 写回文件
        if modified_config is None: modified_config = self.modified_config
        files = []
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath) and "." not in filename:
                files.append(filepath)
        for file in files:
            env = UnityPy.load(file)
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    txt = obj.parse_as_object()
                    if txt.m_Name != "GameMainConfig":
                        continue
                    txt.m_Script = base64.b64decode(modified_config).decode("utf-8", "surrogateescape")
                    txt.save()
                    with open(file, "wb") as f:
                        f.write(env.file.save())
        print(f"已写入修改后的 GameMainConfig")

    def fast_rewrite(self, path, target_url): # 根据路径和目标 URL 自动修改文件
        self.get_gamemainconfig(path)
        self.get_serverinfo_url()
        self.modify_serverinfo_url(target_url)
        self.modify_config()
        self.rewrite_config(path)

class SdkUrlRewriter:
    def get_sdkconfigsettings(self, path): # 获取 SDKConfigSettings 并保存到 self.original_config
        files = []
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath) and "." not in filename:
                files.append(filepath)
        for file in files:
            env = UnityPy.load(file)
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    txt = obj.parse_as_object()
                    if txt.m_Name != "SDKConfigSettings":
                        continue
                    original_config = txt.m_Script.encode("utf-8", "surrogateescape")
                    self.original_config = original_config.decode("utf-8", "surrogateescape")
                    return original_config
        
    def get_sdk_url(self, original_config = None): # 根据 SDKConfigSettings 解析 SDK URL 并保存到 self.original_url
        if original_config is None: original_config = self.original_config
        config_json = json.loads(original_config)
        original_url = config_json["Regions"]["Jp"]["Sdk_Url"]
        self.original_url = original_url
        print(f"已获取的 SDK URL: {original_url}")
        return original_url

    def modify_sdk_url(self, target_url): # 修改 SDK URL 并保存到 self.modified_url
        modified_url = target_url
        if not urlparse(target_url).scheme: # 补全协议，默认https
            modified_url= "https://" + modified_url
        self.modified_url = modified_url
        print(f"修改后的 SDK URL: {modified_url}")
        return modified_url

    def modify_config(self, original_config = None, modified_url = None): # 根据修改后的 SDK URL 修改 SDKConfigSettings 并保存到 self.modified_config
        if original_config is None: original_config = self.original_config
        if modified_url is None: modified_url = self.modified_url
        config_json = json.loads(original_config)
        config_json["Regions"]["Jp"]["Sdk_Url"] = modified_url
        modified_config = json.dumps(config_json, indent=1, ensure_ascii=False)
        self.modified_config = modified_config
        print("已生成修改后的 SDKConfigSettings")
        return modified_config

    def rewrite_config(self, path, modified_config = None): # 根据修改后的 SDKConfigSettings 写回文件
        if modified_config is None: modified_config = self.modified_config
        files = []
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath) and "." not in filename:
                files.append(filepath)
        for file in files:
            env = UnityPy.load(file)
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    txt = obj.parse_as_object()
                    if txt.m_Name != "SDKConfigSettings":
                        continue
                    txt.m_Script = modified_config
                    txt.save()
                    with open(file, "wb") as f:
                        f.write(env.file.save())
        print(f"已写入修改后的 SDKConfigSettings")

    def fast_rewrite(self, path, target_url): # 根据路径和目标 URL 自动修改文件
        self.get_sdkconfigsettings(path)
        self.get_sdk_url()
        self.modify_sdk_url(target_url)
        self.modify_config()
        self.rewrite_config(path)
        
if __name__ == "__main__":
    ServerInfoUrlRewriter().fast_rewrite("/path/to/your/directory", "example.com") # 根据路径和目标 URL 自动修改文件
    SdkUrlRewriter().fast_rewrite("/path/to/your/directory", "example.com") # 根据路径和目标 URL 自动修改文件

    #path = "/path/to/your/directory" # 二进制文件所在目录
    #target_url = "https://example.com/" # 目标 URL，可省略协议和末尾斜杠，如example.com

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