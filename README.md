# RAG vs Pure Agent 实验

本项目复现与评测 RAG（Retrieval-Augmented Generation）对 AI Agent 的性能影响。

## 项目目标

比较两种系统在 Crypto 场景下完成信息密集任务的表现：

1. **纯 Agent 系统** - 依赖模型自身知识 + 推理链
2. **RAG + Agent 系统** - 加入向量数据库检索增强

## 项目结构

```
crypto_rag_experiment/
├── data/                       # 数据目录
│   └── bitcoin.pdf             # 比特币白皮书
├── src/
│   ├── agents/
│   │   ├── pure_agent.py       # 纯 Agent 实现
│   │   └── rag_agent.py        # RAG Agent 实现
│   ├── rag/
│   │   └── ingest.py           # 数据摄入脚本
│   └── eval/
│       ├── evaluator.py        # 评测框架
│       └── test_questions.json # 测试数据集
├── results/                    # 实验结果
├── run_experiment.py           # 主运行脚本
├── requirements.txt            # 依赖
└── README.md                   # 文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

在 `.env` 文件中配置：

```
GOOGLE_API_KEY=your_gemini_api_key
```

### 3. 数据摄入（构建向量数据库）

```bash
python run_experiment.py --ingest
```

或单独运行：

```bash
python src/rag/ingest.py
```

### 4. 运行实验

```bash
# 运行完整实验
python run_experiment.py

# 交互模式
python run_experiment.py --interactive

# 自定义问题文件
python run_experiment.py --questions path/to/questions.json
```

## 实验设计

### 测试任务

基于比特币白皮书的 10 个问题，涵盖：
- 机制理解（共识、时间戳服务器、工作量证明等）
- 问题解决（双重支付）
- 代币经济学分析
- 安全与隐私

### 评测指标

使用 LLM-as-Judge 方法评估：
- **准确性** (Accuracy): 回答是否正确
- **完整性** (Completeness): 是否涵盖所有方面
- **相关性** (Relevance): 是否紧扣主题
- **清晰度** (Clarity): 是否易于理解

### 方法对比

| 方面 | Pure Agent | RAG Agent |
|------|------------|-----------|
| 知识来源 | 模型预训练知识 | 向量检索 + 模型知识 |
| 实时性 | 受训练截止时间限制 | 可更新知识库 |
| 准确性 | 可能产生幻觉 | 基于真实文档，更准确 |
| 推理能力 | 强 | 强 + 有据可依 |
| 计算成本 | 低 | 较高（需要检索） |

## 预期结果

在 Crypto 白皮书问答这类**信息密集型任务**中：
- RAG Agent 预期在**准确性**和**引用能力**上更优
- Pure Agent 可能在**通用理解**和**推理速度**上有优势
- 对于白皮书中的**具体细节问题**，RAG 优势更明显

## 许可

MIT License
