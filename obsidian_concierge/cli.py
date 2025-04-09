"""
Obsidian Concierge - CLI Client

このモジュールはObsidian Conciergeのすべての機能にアクセスするための
コマンドラインインターフェースを提供します。
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
import yaml
import httpx
from typing import Dict, List, Optional, Any, Union
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

console = Console()

class ObsidianConciergeClient:
    """Obsidian Conciergeのクライアント"""

    def __init__(self, base_url: Optional[str] = None, config_path: Optional[str] = None):
        """
        クライアントを初期化します。
        
        Args:
            base_url: APIサーバーのベースURL
            config_path: 設定ファイルのパス
        """
        # .envから設定を読み込む
        host = os.getenv("API_HOST", "localhost")
        port = os.getenv("API_PORT", "8000")
        self.base_url = base_url or f"http://{host}:{port}"
        
        self.vault_path = os.getenv("VAULT_PATH")
        if not self.vault_path:
            console.print("[red]Error: VAULT_PATH not set in .env file[/red]")
            sys.exit(1)
        
        self.config = self._load_config(config_path) if config_path else {}
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """設定ファイルを読み込みます"""
        with open(config_path) as f:
            return yaml.safe_load(f)

    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """APIリクエストを実行します"""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )
                
                response.raise_for_status()
                return response.json()
            except httpx.ConnectError:
                console.print("[red]Error: Could not connect to the API server. Is it running?[/red]")
                sys.exit(1)
            except httpx.HTTPStatusError as e:
                console.print(f"[red]Error: {e}[/red]")
                if response.content:
                    console.print(f"Response: {response.text}")
                sys.exit(1)
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                sys.exit(1)

    # Vault管理コマンド
    async def index_vault(self, force: bool = False) -> None:
        """Vaultのインデックスを作成/更新します"""
        console.print("Indexing vault...", style="yellow")
        data = {"force": force}
        result = await self._make_request("POST", "/api/v1/index", data)
        console.print("Vault indexed successfully!", style="green")
        console.print(result)

    async def get_vault_stats(self) -> None:
        """Vaultの統計情報を取得します"""
        console.print("Fetching vault statistics...", style="yellow")
        result = await self._make_request("GET", "/api/v1/stats")
        
        table = Table(title="Vault Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        for key, value in result.items():
            table.add_row(key, str(value))
        
        console.print(table)

    # 検索コマンド
    async def search(
        self, 
        query: str, 
        limit: int = 10,
        include_content: bool = False
    ) -> None:
        """Vault内を検索します"""
        console.print(f"Searching for: {query}", style="yellow")
        
        data = {
            "query": query,
            "limit": limit,
            "include_content": include_content
        }
        
        result = await self._make_request("POST", "/api/v1/search", data)
        
        table = Table(title=f"Search Results ({result['total']} matches)")
        table.add_column("Title", style="cyan")
        table.add_column("Path", style="blue")
        table.add_column("Relevance", style="magenta")
        
        for item in result["results"]:
            table.add_row(
                item["title"],
                item["path"],
                f"{item['relevance']:.2f}"
            )
        
        console.print(table)
        
        if include_content:
            for item in result["results"]:
                console.print(f"\n[cyan]### {item['title']}[/cyan]")
                console.print(Markdown(item["excerpt"]))

    # 質問応答コマンド
    async def ask(
        self, 
        question: str,
        context_size: int = 3,
        temperature: float = 0.7
    ) -> None:
        """質問に回答します"""
        console.print(f"Question: {question}", style="yellow")
        
        data = {
            "question": question,
            "context_size": context_size,
            "temperature": temperature
        }
        
        result = await self._make_request("POST", "/api/v1/ask", data)
        
        console.print("\n[green]Answer:[/green]")
        console.print(Markdown(result["answer"]))
        
        if result.get("context"):
            console.print("\n[cyan]Context Sources:[/cyan]")
            for i, ctx in enumerate(result["context"], 1):
                console.print(f"{i}. {ctx['metadata']['title']}")

    # ノート管理コマンド
    async def create_note(
        self,
        title: str,
        content: str,
        folder: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> None:
        """新しいノートを作成します"""
        console.print(f"Creating note: {title}", style="yellow")
        
        data = {
            "title": title,
            "content": content,
            "folder": folder,
            "tags": tags or []
        }
        
        result = await self._make_request("POST", "/api/v1/notes", data)
        console.print(f"Note created: {result['path']}", style="green")

    async def update_note(
        self,
        path: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> None:
        """既存のノートを更新します"""
        console.print(f"Updating note: {path}", style="yellow")
        
        data = {
            "content": content,
            "tags": tags
        }
        
        result = await self._make_request("PUT", f"/api/v1/notes/{path}", data)
        console.print("Note updated successfully!", style="green")

    async def delete_note(self, path: str) -> None:
        """ノートを削除します"""
        console.print(f"Deleting note: {path}", style="yellow")
        await self._make_request("DELETE", f"/api/v1/notes/{path}")
        console.print("Note deleted successfully!", style="green")

    # タグ管理コマンド
    async def list_tags(self) -> None:
        """すべてのタグを一覧表示します"""
        console.print("Fetching tags...", style="yellow")
        result = await self._make_request("GET", "/api/v1/tags")
        
        table = Table(title="Tags")
        table.add_column("Tag", style="cyan")
        table.add_column("Count", style="magenta")
        
        for tag, count in result["tags"].items():
            table.add_row(tag, str(count))
        
        console.print(table)

    async def get_notes_by_tag(self, tag: str) -> None:
        """指定したタグが付いたノートを一覧表示します"""
        console.print(f"Fetching notes with tag: {tag}", style="yellow")
        result = await self._make_request("GET", f"/api/v1/tags/{tag}/notes")
        
        table = Table(title=f"Notes with tag: {tag}")
        table.add_column("Title", style="cyan")
        table.add_column("Path", style="blue")
        
        for note in result["notes"]:
            table.add_row(note["title"], note["path"])
        
        console.print(table)

    # 設定管理コマンド
    async def get_config(self) -> None:
        """現在の設定を表示します"""
        console.print("Current configuration:", style="yellow")
        result = await self._make_request("GET", "/api/v1/config")
        
        table = Table(title="Configuration")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="magenta")
        
        for key, value in result.items():
            table.add_row(key, str(value))
        
        console.print(table)

    async def update_config(self, updates: Dict[str, Any]) -> None:
        """設定を更新します"""
        console.print("Updating configuration...", style="yellow")
        result = await self._make_request("PUT", "/api/v1/config", updates)
        console.print("Configuration updated successfully!", style="green")
        
        table = Table(title="Updated Configuration")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="magenta")
        
        for key, value in result.items():
            table.add_row(key, str(value))
        
        console.print(table)


def setup_argparse() -> argparse.ArgumentParser:
    """コマンドライン引数のパーサーを設定します"""
    parser = argparse.ArgumentParser(
        description="Obsidian Concierge CLI Client",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--url",
        help="API server URL (overrides .env settings)"
    )
    parser.add_argument(
        "--config",
        help="Path to configuration file"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Vault管理コマンド
    index_parser = subparsers.add_parser("index", help="Index vault content")
    index_parser.add_argument(
        "--force",
        action="store_true",
        help="Force reindexing of all content"
    )
    
    stats_parser = subparsers.add_parser("stats", help="Show vault statistics")
    
    # 検索コマンド
    search_parser = subparsers.add_parser("search", help="Search vault content")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results"
    )
    search_parser.add_argument(
        "--content",
        action="store_true",
        help="Include content in results"
    )
    
    # 質問応答コマンド
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("question", help="Your question")
    ask_parser.add_argument(
        "--context-size",
        type=int,
        default=3,
        help="Number of context documents to use"
    )
    ask_parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for response generation"
    )
    
    # ノート管理コマンド
    note_parser = subparsers.add_parser("note", help="Note management commands")
    note_subparsers = note_parser.add_subparsers(dest="note_command")
    
    create_parser = note_subparsers.add_parser("create", help="Create a new note")
    create_parser.add_argument("title", help="Note title")
    create_parser.add_argument("content", help="Note content")
    create_parser.add_argument("--folder", help="Target folder")
    create_parser.add_argument("--tags", nargs="+", help="Tags to apply")
    
    update_parser = note_subparsers.add_parser("update", help="Update an existing note")
    update_parser.add_argument("path", help="Note path")
    update_parser.add_argument("--content", help="New content")
    update_parser.add_argument("--tags", nargs="+", help="New tags")
    
    delete_parser = note_subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("path", help="Note path")
    
    # タグ管理コマンド
    tag_parser = subparsers.add_parser("tag", help="Tag management commands")
    tag_subparsers = tag_parser.add_subparsers(dest="tag_command")
    
    tag_subparsers.add_parser("list", help="List all tags")
    
    notes_parser = tag_subparsers.add_parser("notes", help="List notes with tag")
    notes_parser.add_argument("tag", help="Tag to search for")
    
    # 設定管理コマンド
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    
    config_subparsers.add_parser("show", help="Show current configuration")
    
    update_config_parser = config_subparsers.add_parser("update", help="Update configuration")
    update_config_parser.add_argument(
        "updates",
        nargs="+",
        help="Configuration updates in key=value format"
    )
    
    return parser


async def _main():
    """非同期メイン関数"""
    parser = setup_argparse()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    client = ObsidianConciergeClient(args.url, args.config)
    
    try:
        if args.command == "index":
            await client.index_vault(args.force)
        
        elif args.command == "stats":
            await client.get_vault_stats()
        
        elif args.command == "search":
            await client.search(args.query, args.limit, args.content)
        
        elif args.command == "ask":
            await client.ask(args.question, args.context_size, args.temperature)
        
        elif args.command == "note":
            if args.note_command == "create":
                await client.create_note(args.title, args.content, args.folder, args.tags)
            elif args.note_command == "update":
                await client.update_note(args.path, args.content, args.tags)
            elif args.note_command == "delete":
                await client.delete_note(args.path)
            else:
                parser.print_help()
        
        elif args.command == "tag":
            if args.tag_command == "list":
                await client.list_tags()
            elif args.tag_command == "notes":
                await client.get_notes_by_tag(args.tag)
            else:
                parser.print_help()
        
        elif args.command == "config":
            if args.config_command == "show":
                await client.get_config()
            elif args.config_command == "update":
                updates = {}
                for update in args.updates:
                    key, value = update.split("=", 1)
                    updates[key] = value
                await client.update_config(updates)
            else:
                parser.print_help()
    
    except KeyboardInterrupt:
        console.print("\nOperation cancelled by user", style="yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)

def run_cli():
    """CLIエントリーポイント"""
    asyncio.run(_main())

if __name__ == "__main__":
    run_cli() 