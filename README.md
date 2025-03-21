# 🌐 DeepLX 本地部署与调用指南

本项目说明如何：

1. 获取 DeepLX 的必要 Cookie 信息（`TOKEN` 和 `DL_SESSION`）
2. 使用 Docker 快速部署 DeepLX 本地翻译服务
3. 调用本地部署的 API 进行翻译
4. 参考文档地址：[https://deeplx.owo.network/install/](https://deeplx.owo.network/install/)

---

## 🔐 1. 获取 TOKEN 和 DL_SESSION

DeepLX 模拟 DeepL 网页翻译，需要携带你的浏览器 Cookie 信息。

### 获取方式：

1. 打开网页：[https://www.deepl.com/translator](https://www.deepl.com/translator)
2. 提取 Cookie 中的：
   - `DL_SESSION`
   - `cf_clearance`，作为 `TOKEN` 使用

⚠️ 这些字段定期会过期，需要定期更新。

---

## 🐳 2. 使用 Docker 部署 DeepLX

### 使用 `docker run` 快速启动

```bash
docker run -itd -p 1188:1188 \
  -e TOKEN=你的_token \
  -e DL_SESSION=你的_dl_session \
  missuo/deeplx:latest
```

### 启动成功后服务地址为：
```bash
http://localhost:1188/translate
```

## 📡 3. 在代码中调用 DeepLX API

在你的程序中，只需要设置好 API 地址，即可通过 POST 请求发送文本并获取翻译结果。
