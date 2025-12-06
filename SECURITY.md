# Security Policy | 安全政策

[English](#english) | [中文](#中文)

---

## English

### 🔐 API Key Security

This project requires a Google Gemini API key. **Improper handling of API keys can lead to security breaches and unexpected charges.**

#### ⚠️ Critical Rules

1. **NEVER commit your `.env` file to Git**
   - The `.env` file is already in `.gitignore`
   - Always verify before pushing

2. **NEVER share your API key in:**
   - Chat messages (including AI assistants)
   - Public repositories
   - Screenshots or screen recordings
   - Log files

3. **If your key is exposed:**
   - Immediately revoke it at [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Generate a new key
   - Update your `.env` file

### 📋 Secure Setup Checklist

- [ ] Create `.env` file in project root
- [ ] Add `GOOGLE_API_KEY=your_key_here`
- [ ] Verify `.env` is in `.gitignore`
- [ ] Never paste key in chat/AI tools

### 🛡️ Best Practices

| Do ✅ | Don't ❌ |
|-------|---------|
| Store keys in `.env` files | Hardcode keys in source code |
| Use environment variables | Commit `.env` to Git |
| Rotate keys regularly | Share keys via chat/email |
| Restrict key permissions | Use same key across projects |

### 🔄 Key Rotation

Rotate your API key periodically:

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Update your local `.env` file
4. Delete the old key

---

## 中文

### 🔐 API Key 安全

本项目需要 Google Gemini API 密钥。**不当处理 API 密钥可能导致安全漏洞和意外费用。**

#### ⚠️ 关键规则

1. **永远不要将 `.env` 文件提交到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 推送前务必检查

2. **永远不要在以下地方分享 API 密钥：**
   - 聊天消息（包括 AI 助手）
   - 公开代码库
   - 截图或录屏
   - 日志文件

3. **如果密钥泄露：**
   - 立即在 [Google AI Studio](https://aistudio.google.com/app/apikey) 撤销
   - 生成新密钥
   - 更新 `.env` 文件

### 📋 安全配置清单

- [ ] 在项目根目录创建 `.env` 文件
- [ ] 添加 `GOOGLE_API_KEY=your_key_here`
- [ ] 确认 `.env` 在 `.gitignore` 中
- [ ] 切勿在聊天/AI 工具中粘贴密钥

### 🛡️ 最佳实践

| 应该 ✅ | 不应该 ❌ |
|---------|----------|
| 在 `.env` 文件中存储密钥 | 在源代码中硬编码密钥 |
| 使用环境变量 | 将 `.env` 提交到 Git |
| 定期轮换密钥 | 通过聊天/邮件分享密钥 |
| 限制密钥权限 | 跨项目使用同一密钥 |

### 🔄 密钥轮换

定期轮换 API 密钥：

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 创建新的 API 密钥
3. 更新本地 `.env` 文件
4. 删除旧密钥

---

## 📧 Reporting Security Issues | 报告安全问题

If you discover a security vulnerability, please report it responsibly.

如果您发现安全漏洞，请负责任地报告。

---

<p align="center">
  🔒 Stay Secure | 保持安全 🔒
</p>
