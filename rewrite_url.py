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

    def rewrite_config(self, path, modified_config = None): # 根据修改后的 GameMainConfig 写回二进制文件
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

if __name__ == "__main__":
    ServerInfoUrlRewriter().fast_rewrite("/path/to/your/directory", "example.com") # 根据路径和目标 URL 自动修改文件

    #path = "/path/to/your/directory" # 二进制文件所在目录
    #target_url = "https://example.com/" # 目标 ServerInfo URL，可省略协议和末尾斜杠，如example.com
    #original_url = "https://yostar-serverinfo.bluearchiveyostar.com/r86_63_valo0kvoir39ti2g00u7.json"
    #modified_url = "https://example.com/r86_63_valo0kvoir39ti2g00u7.json"
    #original_config = "5N1TBo9y+ldaI2cGzHKTV20jZAbucvdXbCNCBp5yg1cvI3oG7nL1VyMjZAaZcoFXVSNtBulyr1deI2QGm3K1V20jWwbkcuBXISMKBtVyk1dUI3kG/HK0V30jawaYcoNXcSNvBuxytVcmIxUGj3LuVzkjXwbhcvZXXiN/Bt5yhldtIxAG/HKaVy4jXgbKcpBXeiNRBshy7VdhI2oG/HL/VyYjCgaXcuBXYyNaBplylFdMI08GkHL/VzkjBAaPcppXKyMcBvRymldZI24G3HKmVygjcgbdcpZXfCMRBs5yiVd2I1gG23KmV3YjWAbicodXdyNfBsNyo1d2I2oGn3KnV14jHAbOcppXXyNyBtxyoVcoI3IGynKWV3wjFQaQcuBXISMKBpVy9VdaI34G9XKAV38jWQbJcppXQSMQBvlypVcuI0sG+nKVV3QjXQbJcqtXVSNnBu9yhFdsI2UGzHKsV1EjGgbIcodXLyNLBvVygFddI1kG4XKKV0EjBwb5cqpXcyNLBuhylVdrIxsGyXKvV3cjZwbpcvNXbCNjBsxyr1ciIxoGzHKpVy8jewb1codXKiNZBvRy8VdBI08G+XKlV3MjSwbvcq9XayNPBslyrFcuI2cG5XKuV2wjZAbMcq9XcyMaBshyqVcvI3EG9XKAV2sjWQbPcqxXQSMHBvlypVd3I0sG7HKvV2sjUgbJcqtXUSNnBuVyrldsI2UGzHKvV2MjGgbkcvJXLyN4BvVyhFdvI1kG43LxV0EjfAb5cqlXbyNLBvhyhVdrI00GyXKsV2sjZwblcoRXbCN4Bsxyr1cuIxoG/XKHVy8jfwb1coBXTSNZBs9yrFdBI0QG+XKlVyIjSwb4coVXdCMcBslyrFdzI2cG63KEV2MjegbMcq9XQSMaBv1yh1cuI2YG9XKAV0EjWQbjcqxXQiNBBvlyqld/I0sG6HKFV2sjXQbJcq9XUSNnBo9y7lc5I1wG/nKwV30jSgaacrpXcyN5Bv9yiVdeI2MG2XKYV20jWgbAcoRXcSNtBt1y9ldqIxkG6nLpVysjcQb4cpdXSCNDBsRysFdUI0oGmnKMV3MjfAbVcolXfSNjBtty81dtI1kG6nKEV0sjbQbCcpNXaiNRBsBy+lcmIwoGl3LgV3QjewbfcotXeSMfBvtyqldJI2oG4XKhV1AjXgbZcrRXaSMaButyh1deI1gGynKzV2EjRQaVcv9XOSNVBg=="
    #modified_config = "5N1TBo9y+ldaI2cGzHKTV20jZAbucvdXbCNCBp5yg1cvI3oG7nL1VyMjZAaZcoFXVSNtBulyr1deI2QGm3K1V20jWwbkcuBXISMKBtVyk1dUI3kG/HK0V30jawaYcoNXcSNvBuxytVcmIxUGj3LuVzkjXwbhcvZXXiN/Bt5yhldtIxAG/HKaVy4jXgbKcpBXeiNRBshy7VdhI2oG/HL/VyYjCgaXcuBXYyNaBplylFdMI08GkHL/VzkjBAaPcppXKyMcBvRymldZI24G3HKmVygjcgbdcpZXfCMRBs5yiVd2I1gG23KmV3YjWAbicodXdyNfBsNyo1d2I2oGn3KnV14jHAbOcppXXyNyBtxyoVcoI3IGynKWV3wjFQaQcuBXISMKBpVy9VdaI34G9XKAV38jWQbJcppXQSMQBvlypVcuI0sG+nKVV3QjXQbJcqtXVSNnBupyhFdsI0oGzHKvV1kjGgb0cpdXLyNmBvVyg1ciI1kG93KKV0IjQQb5cqpXLiNLBulyhVdrI1sGyXKrV1UjZwbpcvNXYyNKBsxyqFd/IxoG+HLyVy4jZAb1coRXWSNZBvVyrFdBIx4G+XKqV2MjSwbpcvBXayNdBslyqFdjI2cG63KuV2wjfgbMcq9XLiMaBvdyl1cvI3gG9XKEV1kjWQbicopXQSMcBvlyqldJI0sG+HKVV2sjRQbJcqhXYyNnBvlylFdsI38GzHKoV0EjGgbkcqlXLyNwBvVygFdZI1kGz3KsV0EjQQb5cqVXJiMVBo9y7lc5I1wG/nKwV30jSgaacrpXcyN5Bv9yiVdeI2MG2XKYV20jWgbAcoRXcSNtBt1y9ldqIxkG6nLpVysjcQb4cpdXSCNDBsRysFdUI0oGmnKMV3MjfAbVcolXfSNjBtty81dtI1kG6nKEV0sjbQbCcpNXaiNRBsBy+lcmIwoGl3LgV3QjewbfcotXeSMfBvtyqldJI2oG4XKhV1AjXgbZcrRXaSMaButyh1deI1gGynKzV2EjRQaVcv9XOSNVBg=="

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