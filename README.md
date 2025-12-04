# 🔐 Crypto RAG Experiment

## RAG vs Pure Agent Experiment | RAG 与纯 Agent 对比实验

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gemini 2.5](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange.svg)](https://ai.google.dev/)

[English](#english) | [中文](#中文)

---

## English

A reproducible experiment to evaluate the performance impact of **RAG (Retrieval-Augmented Generation)** on AI Agents in the cryptocurrency domain.

### 🎯 Project Goals

Compare two AI systems on information-intensive crypto tasks:

| System | Description |
|--------|-------------|
| **Pure Agent** | Relies solely on model's pre-trained knowledge + reasoning |
| **RAG + Agent** | Enhanced with vector database retrieval from real documents |

### 📁 Project Structure

```
crypto_rag_experiment/
├── 📂 data/                        # Data directory
│   └── bitcoin.pdf                 # Bitcoin whitepaper
├── 📂 src/
│   ├── 📂 agents/
│   │   ├── pure_agent.py           # Pure Agent (Gemini 2.5 Flash)
│   │   └── rag_agent.py            # RAG Agent (Gemini + ChromaDB)
│   ├── 📂 rag/
│   │   └── ingest.py               # Vector DB ingestion
│   └── 📂 eval/
│       ├── evaluator.py            # LLM-as-Judge evaluation
│       └── test_questions.json     # 10 test questions
├── 📂 chroma_db/                   # Vector database (auto-generated)
├── 📂 results/                     # Experiment results
├── run_experiment.py               # Main script
├── requirements.txt                # Dependencies
├── SECURITY.md                     # Security guidelines
└── README.md                       # This file
```

### 🚀 Quick Start

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Configure API Key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

> ⚠️ **Security Warning**: Never commit your API key to Git. See [SECURITY.md](SECURITY.md) for details.

#### 3. Build Vector Database

```bash
# Using py launcher (Windows)
py src/rag/ingest.py

# Or with ingest flag
py run_experiment.py --ingest
```

#### 4. Run Experiment

```bash
# Full experiment (10 questions)
py run_experiment.py

# Interactive mode - ask your own questions
py run_experiment.py --interactive

# Custom questions file
py run_experiment.py --questions path/to/questions.json
```

### 🧪 Experiment Design

#### Test Dataset

10 questions based on the **Bitcoin Whitepaper**, covering:

| Category | Examples |
|----------|----------|
| Mechanism | Proof of Work, Timestamp Server, SPV |
| Problem Solving | Double Spending Prevention |
| Tokenomics | Mining Incentives |
| Security | 51% Attack Prevention, Privacy |

#### Evaluation Metrics (LLM-as-Judge)

- **Accuracy** - Factual correctness
- **Completeness** - Coverage of all aspects
- **Relevance** - On-topic responses
- **Clarity** - Easy to understand

#### System Comparison

| Aspect | Pure Agent | RAG Agent |
|--------|------------|-----------|
| Knowledge | Pre-trained only | Retrieval + Pre-trained |
| Timeliness | Limited by training cutoff | Updatable knowledge base |
| Accuracy | May hallucinate | Document-grounded |
| Reasoning | Strong | Strong + Evidence-backed |
| Cost | Lower | Higher (retrieval overhead) |

### 📊 Expected Results

For **information-dense tasks** like crypto whitepaper Q&A:

- ✅ **RAG Agent** excels in accuracy and citation ability
- ✅ **Pure Agent** may be faster for general reasoning
- ✅ For **specific detail questions**, RAG advantage is more pronounced

---

## 中文

一个可复现的实验，用于评估 **RAG（检索增强生成）** 对加密货币领域 AI Agent 性能的影响。

### 🎯 项目目标

在信息密集型加密货币任务上比较两个 AI 系统：

| 系统 | 描述 |
|------|------|
| **纯 Agent** | 仅依赖模型预训练知识 + 推理 |
| **RAG + Agent** | 通过向量数据库检索增强 |

### 📁 项目结构

```
crypto_rag_experiment/
├── 📂 data/                        # 数据目录
│   └── bitcoin.pdf                 # 比特币白皮书
├── 📂 src/
│   ├── 📂 agents/
│   │   ├── pure_agent.py           # 纯 Agent (Gemini 2.5 Flash)
│   │   └── rag_agent.py            # RAG Agent (Gemini + ChromaDB)
│   ├── 📂 rag/
│   │   └── ingest.py               # 向量数据库摄入
│   └── 📂 eval/
│       ├── evaluator.py            # LLM 评测框架
│       └── test_questions.json     # 10 道测试题
├── 📂 chroma_db/                   # 向量数据库（自动生成）
├── 📂 results/                     # 实验结果
├── run_experiment.py               # 主脚本
├── requirements.txt                # 依赖
├── SECURITY.md                     # 安全指南
└── README.md                       # 本文件
```

### 🚀 快速开始

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置 API Key

在项目根目录创建 `.env` 文件：

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

> ⚠️ **安全警告**：切勿将 API Key 提交到 Git。详见 [SECURITY.md](SECURITY.md)。

#### 3. 构建向量数据库

```bash
# Windows 使用 py 启动器
py src/rag/ingest.py

# 或使用 --ingest 标志
py run_experiment.py --ingest
```

#### 4. 运行实验

```bash
# 完整实验（10 个问题）
py run_experiment.py

# 交互模式 - 提出自己的问题
py run_experiment.py --interactive

# 自定义问题文件
py run_experiment.py --questions path/to/questions.json
```

### 🧪 实验设计

#### 测试数据集

基于 **比特币白皮书** 的 10 个问题，涵盖：

| 类别 | 示例 |
|------|------|
| 机制 | 工作量证明、时间戳服务器、SPV |
| 问题解决 | 双重支付防范 |
| 代币经济 | 挖矿激励 |
| 安全 | 51% 攻击防范、隐私 |

#### 评测指标（LLM 评判法）

- **准确性** - 事实正确性
- **完整性** - 是否涵盖所有方面
- **相关性** - 是否紧扣主题
- **清晰度** - 是否易于理解

#### 系统对比

| 方面 | 纯 Agent | RAG Agent |
|------|----------|-----------|
| 知识来源 | 仅预训练 | 检索 + 预训练 |
| 实时性 | 受训练截止限制 | 可更新知识库 |
| 准确性 | 可能产生幻觉 | 基于文档 |
| 推理 | 强 | 强 + 有据可依 |
| 成本 | 较低 | 较高（检索开销） |

### 📊 预期结果

对于加密货币白皮书问答等**信息密集型任务**：

- ✅ **RAG Agent** 在准确性和引用能力上更优
- ✅ **纯 Agent** 在通用推理上可能更快
- ✅ 对于**具体细节问题**，RAG 优势更明显

---

## 🛠️ Tech Stack | 技术栈

- **LLM**: Google Gemini 2.5 Flash
- **Embeddings**: HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (local)
- **Vector DB**: ChromaDB
- **Framework**: LangChain

## 📄 License | 许可

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ for Crypto Research
</p>
