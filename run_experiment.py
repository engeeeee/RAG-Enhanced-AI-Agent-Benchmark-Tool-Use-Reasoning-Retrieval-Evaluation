#!/usr/bin/env python
"""
RAG vs Pure Agent 实验主程序
用于 Crypto 场景下比较两种 AI 系统的表现
"""
import os
import sys
import json
import argparse

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from agents.pure_agent import PureAgent
from agents.rag_agent import RAGAgent
from eval.evaluator import run_experiment


def main():
    parser = argparse.ArgumentParser(description="RAG vs Pure Agent 实验")
    parser.add_argument("--ingest", action="store_true", help="先执行数据摄入")
    parser.add_argument("--questions", type=str, help="自定义问题文件路径")
    parser.add_argument("--output", type=str, default="results/experiment_results.json", help="结果输出路径")
    parser.add_argument("--interactive", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    # 数据摄入
    if args.ingest:
        print("正在执行数据摄入...")
        from rag.ingest import ingest_data
        ingest_data()
        print("数据摄入完成！")
    
    # 交互模式
    if args.interactive:
        interactive_mode()
        return
    
    # 加载问题
    if args.questions:
        with open(args.questions, "r", encoding="utf-8") as f:
            test_data = json.load(f)
        questions = test_data["questions"]
    else:
        default_path = os.path.join(PROJECT_ROOT, "src", "eval", "test_questions.json")
        with open(default_path, "r", encoding="utf-8") as f:
            test_data = json.load(f)
        questions = test_data["questions"]
    
    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 运行实验
    run_experiment(questions, args.output)


def interactive_mode():
    """交互式问答模式，可以实时比较两个 Agent"""
    print("\n" + "=" * 60)
    print("RAG vs Pure Agent 交互模式")
    print("=" * 60)
    print("输入问题进行测试，输入 'quit' 退出")
    print()
    
    pure_agent = PureAgent()
    rag_agent = RAGAgent()
    
    while True:
        question = input("问题: ").strip()
        if question.lower() in ["quit", "exit", "q"]:
            print("再见！")
            break
        
        if not question:
            continue
        
        print("\n" + "-" * 40)
        print("【Pure Agent 回答】")
        print("-" * 40)
        pure_answer = pure_agent.query(question)
        print(pure_answer)
        
        print("\n" + "-" * 40)
        print("【RAG Agent 回答】")
        print("-" * 40)
        rag_result = rag_agent.query_with_reasoning(question)
        print(f"(检索到 {len(rag_result['retrieved_docs'])} 个相关片段)")
        print(rag_result["full_response"])
        
        print("\n")


if __name__ == "__main__":
    main()
