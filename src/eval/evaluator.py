"""
评测框架 - 对 Pure Agent 和 RAG Agent 进行对比评测
"""
import json
import os
import time
from datetime import datetime
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 导入 agents
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from agents.pure_agent import PureAgent
from agents.rag_agent import RAGAgent


class Evaluator:
    """
    评测器：使用 LLM 作为评判来评估回答质量
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.judge_model = genai.GenerativeModel(model_name)
    
    def evaluate_single(self, question: str, answer: str, reference: str = None) -> Dict:
        """
        评估单个回答
        返回：准确性、完整性、相关性评分 (0-10)
        """
        eval_prompt = f"""你是一位专业的评测专家。请评估以下回答的质量。

问题: {question}

回答: {answer}

{f"参考答案/标准: {reference}" if reference else ""}

请从以下维度评分（0-10分），并给出简要理由：

1. **准确性 (Accuracy)**: 回答是否事实正确
2. **完整性 (Completeness)**: 回答是否涵盖了问题的所有方面  
3. **相关性 (Relevance)**: 回答是否紧扣问题主题
4. **清晰度 (Clarity)**: 回答是否清晰易懂

请用以下 JSON 格式返回（只返回 JSON，不要其他内容）：
{{
    "accuracy": <分数>,
    "completeness": <分数>,
    "relevance": <分数>,
    "clarity": <分数>,
    "overall": <总体评分>,
    "reasoning": "<简要评价>"
}}
"""
        
        try:
            response = self.judge_model.generate_content(eval_prompt)
            text = response.text
            
            # 解析 JSON
            # 找到 JSON 部分
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = text[start:end]
                scores = json.loads(json_str)
                return scores
            else:
                return {
                    "accuracy": 5,
                    "completeness": 5,
                    "relevance": 5,
                    "clarity": 5,
                    "overall": 5,
                    "reasoning": "无法解析评分"
                }
        except Exception as e:
            return {
                "accuracy": 0,
                "completeness": 0,
                "relevance": 0,
                "clarity": 0,
                "overall": 0,
                "reasoning": f"评估出错: {str(e)}"
            }
    
    def compare_agents(self, question: str, pure_answer: str, rag_answer: str, reference: str = None) -> Dict:
        """
        比较两个 Agent 的回答
        """
        compare_prompt = f"""你是一位专业的评测专家。请比较以下两个 AI 系统对同一问题的回答。

问题: {question}

{f"参考标准: {reference}" if reference else ""}

---
**Pure Agent 回答** (只依赖模型自身知识):
{pure_answer}

---
**RAG Agent 回答** (结合外部知识库):
{rag_answer}

---

请分析：
1. 哪个回答更准确？
2. 哪个回答更完整？
3. 各自的优势和不足
4. 总体哪个更好？

请用以下 JSON 格式返回（只返回 JSON，不要其他内容）：
{{
    "pure_agent_score": <0-10>,
    "rag_agent_score": <0-10>,
    "winner": "<pure_agent/rag_agent/tie>",
    "pure_agent_strengths": "<优势>",
    "pure_agent_weaknesses": "<不足>",
    "rag_agent_strengths": "<优势>",
    "rag_agent_weaknesses": "<不足>",
    "analysis": "<详细分析>"
}}
"""
        
        try:
            response = self.judge_model.generate_content(compare_prompt)
            text = response.text
            
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = text[start:end]
                result = json.loads(json_str)
                return result
        except Exception as e:
            pass
        
        return {
            "pure_agent_score": 5,
            "rag_agent_score": 5,
            "winner": "tie",
            "analysis": "无法完成比较"
        }


def run_experiment(questions: List[Dict], output_file: str = None) -> Dict:
    """
    运行完整实验
    
    Args:
        questions: 问题列表，每个问题包含 question 和可选的 reference
        output_file: 结果输出文件路径
    
    Returns:
        完整的实验结果
    """
    print("=" * 60)
    print("RAG vs Pure Agent 实验")
    print("=" * 60)
    
    # 初始化
    pure_agent = PureAgent()
    rag_agent = RAGAgent()
    evaluator = Evaluator()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "num_questions": len(questions),
        "questions": [],
        "summary": {}
    }
    
    pure_total = 0
    rag_total = 0
    rag_wins = 0
    pure_wins = 0
    ties = 0
    
    for i, q_data in enumerate(questions):
        question = q_data["question"]
        reference = q_data.get("reference", None)
        category = q_data.get("category", "general")
        
        print(f"\n[{i+1}/{len(questions)}] {question[:50]}...")
        
        # 获取两个 Agent 的回答
        print("  - Pure Agent 思考中...")
        pure_result = pure_agent.query_with_reasoning(question)
        time.sleep(1)  # 避免 API 限流
        
        print("  - RAG Agent 思考中...")
        rag_result = rag_agent.query_with_reasoning(question)
        time.sleep(1)
        
        # 评估
        print("  - 评估中...")
        comparison = evaluator.compare_agents(
            question, 
            pure_result["full_response"], 
            rag_result["full_response"],
            reference
        )
        
        # 统计
        pure_total += comparison.get("pure_agent_score", 5)
        rag_total += comparison.get("rag_agent_score", 5)
        
        winner = comparison.get("winner", "tie")
        if winner == "rag_agent":
            rag_wins += 1
        elif winner == "pure_agent":
            pure_wins += 1
        else:
            ties += 1
        
        print(f"  - 结果: Pure={comparison.get('pure_agent_score', 'N/A')}, RAG={comparison.get('rag_agent_score', 'N/A')}, Winner={winner}")
        
        # 记录结果
        results["questions"].append({
            "question": question,
            "category": category,
            "reference": reference,
            "pure_agent_response": pure_result["full_response"],
            "rag_agent_response": rag_result["full_response"],
            "rag_retrieved_docs": rag_result.get("retrieved_docs", []),
            "comparison": comparison
        })
    
    # 汇总
    n = len(questions)
    results["summary"] = {
        "pure_agent_avg_score": round(pure_total / n, 2) if n > 0 else 0,
        "rag_agent_avg_score": round(rag_total / n, 2) if n > 0 else 0,
        "rag_wins": rag_wins,
        "pure_wins": pure_wins,
        "ties": ties,
        "rag_win_rate": round(rag_wins / n * 100, 1) if n > 0 else 0,
        "pure_win_rate": round(pure_wins / n * 100, 1) if n > 0 else 0
    }
    
    print("\n" + "=" * 60)
    print("实验总结")
    print("=" * 60)
    print(f"Pure Agent 平均得分: {results['summary']['pure_agent_avg_score']}")
    print(f"RAG Agent 平均得分: {results['summary']['rag_agent_avg_score']}")
    print(f"RAG 获胜: {rag_wins} 次 ({results['summary']['rag_win_rate']}%)")
    print(f"Pure 获胜: {pure_wins} 次 ({results['summary']['pure_win_rate']}%)")
    print(f"平局: {ties} 次")
    
    # 保存结果
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {output_file}")
    
    return results


if __name__ == "__main__":
    # 加载测试问题
    test_file = os.path.join(os.path.dirname(__file__), "test_questions.json")
    
    if os.path.exists(test_file):
        with open(test_file, "r", encoding="utf-8") as f:
            test_data = json.load(f)
        questions = test_data["questions"]
    else:
        # 使用默认测试问题
        questions = [
            {"question": "比特币的共识机制是什么？", "category": "mechanism"},
            {"question": "解释比特币白皮书中如何解决双重支付问题", "category": "problem_solving"},
        ]
    
    # 运行实验
    output_path = os.path.join(os.path.dirname(__file__), "experiment_results.json")
    run_experiment(questions, output_path)
