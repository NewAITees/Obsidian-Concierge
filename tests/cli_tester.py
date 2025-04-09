"""
Obsidian Concierge - CLI Test Interface

このモジュールはObsidian Conciergeの機能をコマンドラインから
テストするためのインターフェースを提供します。
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
import httpx
from typing import Dict, List, Optional, Any, Union

# HTTPXクライアントを使ったAPIテスター
class ApiTester:
    """Obsidian Concierge APIをテストするためのクライアント"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        APIテスターを初期化します。
        
        Args:
            base_url: APIサーバーのベースURL
        """
        self.base_url = base_url
        print(f"API tester initialized with base URL: {base_url}")

    async def check_health(self) -> None:
        """APIのヘルスチェックエンドポイントをテストします"""
        endpoint = f"{self.base_url}/health"
        print(f"Checking API health at: {endpoint}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint)
                response.raise_for_status()
                data = response.json()
                
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(data, indent=2)}")
        except Exception as e:
            print(f"Health check failed: {e}")
            sys.exit(1)

    async def search(self, query: str, limit: int = 10) -> None:
        """
        検索APIをテストします
        
        Args:
            query: 検索クエリ
            limit: 結果の最大数
        """
        endpoint = f"{self.base_url}/api/v1/search"
        print(f"Testing search API at: {endpoint}")
        
        request_body = {
            "query": query,
            "limit": limit
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint, json=request_body)
                response.raise_for_status()
                data = response.json()
                
                print(f"Status: {response.status_code}")
                print(f"Total results: {data.get('total', 0)}")
                
                results = data.get("results", [])
                for i, result in enumerate(results, 1):
                    print(f"\n--- Result {i} ---")
                    print(f"Title: {result.get('title', 'Untitled')}")
                    print(f"Path: {result.get('path', 'Unknown')}")
                    print(f"Relevance: {result.get('relevance', 0):.2f}")
                    print(f"Excerpt: {result.get('excerpt', '')[:150]}...")
        except Exception as e:
            print(f"Search API test failed: {e}")
            sys.exit(1)

    async def ask_question(self, question: str, context_size: int = 3, temperature: float = 0.7) -> None:
        """
        質問応答APIをテストします
        
        Args:
            question: 質問文
            context_size: 使用するコンテキストドキュメントの数
            temperature: LLM生成の温度パラメータ
        """
        endpoint = f"{self.base_url}/api/v1/ask"
        print(f"Testing QA API at: {endpoint}")
        
        request_body = {
            "question": question,
            "context_size": context_size,
            "temperature": temperature
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint, json=request_body)
                response.raise_for_status()
                data = response.json()
                
                print(f"Status: {response.status_code}")
                
                print("\n--- Answer ---")
                print(data.get("answer", "No answer provided"))
                
                print("\n--- Context ---")
                for i, ctx in enumerate(data.get("context", []), 1):
                    title = ctx.get("metadata", {}).get("title", "Unknown")
                    print(f"{i}. {title}")
                
                print(f"\nConfidence: {data.get('confidence', 0):.2f}")
        except Exception as e:
            print(f"QA API test failed: {e}")
            sys.exit(1)

    async def index_vault(self, config_path: Optional[str] = None) -> None:
        """
        Vaultのインデックス作成をテストします
        
        Args:
            config_path: 設定ファイルのパス
        """
        endpoint = f"{self.base_url}/api/v1/index"
        print(f"Testing vault indexing at: {endpoint}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint)
                response.raise_for_status()
                data = response.json()
                
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(data, indent=2)}")
        except Exception as e:
            print(f"Vault indexing failed: {e}")
            sys.exit(1)

    async def interactive_mode(self) -> None:
        """対話モードを開始します"""
        print("\n=== Obsidian Concierge CLI Tester ===")
        print("Type 'help' for command list, 'exit' to quit")
        
        while True:
            try:
                command = input("\nCommand> ").strip()
                
                if command.lower() in ['exit', 'quit']:
                    break
                
                elif command.lower() == 'help':
                    self._print_help()
                
                elif command.lower() == 'health':
                    await self.check_health()
                
                elif command.lower().startswith('search '):
                    query = command[7:].strip()
                    limit_parts = query.split(' -limit ')
                    if len(limit_parts) > 1:
                        query = limit_parts[0].strip()
                        try:
                            limit = int(limit_parts[1].strip())
                        except ValueError:
                            limit = 10
                    else:
                        limit = 10
                    
                    await self.search(query, limit)
                
                elif command.lower().startswith('ask '):
                    question = command[4:].strip()
                    await self.ask_question(question)
                
                elif command.lower() == 'index':
                    await self.index_vault()
                
                else:
                    print("Unknown command. Type 'help' for command list.")
            
            except KeyboardInterrupt:
                print("\nInterrupted by user.")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _print_help(self) -> None:
        """ヘルプメッセージを表示します"""
        help_text = """
Available commands:
  help                          - Show this help message
  exit, quit                    - Exit the program
  health                        - Check API health
  search <query> [-limit N]     - Search for documents matching <query>
  ask <question>                - Ask a question about vault content
  index                         - Index the vault content
        """
        print(help_text)


async def run_cli_tests(args):
    """CLIテストを実行します"""
    tester = ApiTester(args.url)
    
    if args.health:
        await tester.check_health()
    
    if args.search:
        await tester.search(args.search, args.limit)
    
    if args.question:
        await tester.ask_question(args.question, args.context_size, args.temperature)
    
    if args.index:
        await tester.index_vault(args.config)
    
    if args.interactive:
        await tester.interactive_mode()


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="Obsidian Concierge CLI Test Client")
    
    parser.add_argument('--url', default="http://localhost:8000", help='API base URL')
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--health', action='store_true', help='Check API health')
    parser.add_argument('--search', help='Search for documents')
    parser.add_argument('--limit', type=int, default=10, help='Limit for search results')
    parser.add_argument('--question', help='Ask a question')
    parser.add_argument('--context-size', type=int, default=3, help='Context size for QA')
    parser.add_argument('--temperature', type=float, default=0.7, help='Temperature for LLM')
    parser.add_argument('--index', action='store_true', help='Index the vault')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    
    args = parser.parse_args()
    
    # もし引数が何も指定されていなければ対話モードを開始
    if not any([args.health, args.search, args.question, args.index]):
        args.interactive = True
    
    asyncio.run(run_cli_tests(args))


if __name__ == "__main__":
    main() 