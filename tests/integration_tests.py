"""
Obsidian Concierge - Integration Tests

このモジュールは結合テストを自動実行するためのスクリプトを提供します。
テスト項目を順番に実行し、結果を記録します。
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
import subprocess
import httpx
import argparse
from typing import Dict, List, Optional, Any, Tuple, Callable


class TestResult:
    """テスト結果を格納するクラス"""
    
    def __init__(self, name: str):
        self.name = name
        self.success = False
        self.message = ""
        self.start_time = time.time()
        self.end_time = 0
        self.duration = 0
    
    def complete(self, success: bool, message: str) -> None:
        """テスト完了時に呼び出す"""
        self.success = success
        self.message = message
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
    
    def __str__(self) -> str:
        status = "PASS" if self.success else "FAIL"
        return f"{status} - {self.name} ({self.duration:.2f}s): {self.message}"


class IntegrationTester:
    """Obsidian Conciergeの結合テストを実行するクラス"""
    
    def __init__(
        self, 
        config_path: Optional[str] = None,
        vault_path: Optional[str] = None,
        api_port: int = 8000
    ):
        """
        結合テスターを初期化します。
        
        Args:
            config_path: 設定ファイルのパス
            vault_path: テスト用Obsidian Vaultのパス
            api_port: APIサーバーのポート番号
        """
        self.config_path = config_path
        self.vault_path = vault_path
        self.api_port = api_port
        self.api_url = f"http://localhost:{api_port}"
        self.server_process = None
        self.results = []
    
    async def setup(self) -> TestResult:
        """テスト環境をセットアップします"""
        result = TestResult("Setup")
        
        try:
            # Vaultパスが指定されていれば、テスト用の設定ファイルを作成
            if self.vault_path:
                # config.yamlを生成する
                config_content = f"""
app:
  name: "Obsidian Concierge Test"
  version: "0.1.0"

HOST: "127.0.0.1"
PORT: {self.api_port}
LOG_LEVEL: "INFO"
LOG_FILE: "test_app.log"
CHROMA_DB_DIR: "test_data/chromadb"
CHROMA_COLLECTION_NAME: "test_obsidian_notes"
VAULT_PATH: "{self.vault_path}"
VAULT_INDEX_BATCH_SIZE: 50
"""
                test_config_path = "test_config.yaml"
                with open(test_config_path, "w") as f:
                    f.write(config_content)
                self.config_path = test_config_path
            
            # ディレクトリが存在しなければ作成
            os.makedirs("test_data/chromadb", exist_ok=True)
            
            result.complete(True, "Test environment setup successfully")
        except Exception as e:
            result.complete(False, f"Setup failed: {e}")
        
        self.results.append(result)
        return result
    
    async def start_server(self) -> TestResult:
        """APIサーバーを起動します"""
        result = TestResult("Start API Server")
        
        try:
            # サーバー起動コマンド
            cmd = [sys.executable, "-m", "obsidian_concierge.main"]
            
            if self.config_path:
                cmd.extend(["--config", self.config_path])
            
            # サーバープロセスを起動
            self.server_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # サーバーが起動するまで少し待つ
            await asyncio.sleep(2)
            
            # ヘルスチェックを実行してサーバーが起動したことを確認
            max_retries = 5
            for i in range(max_retries):
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"{self.api_url}/health")
                        if response.status_code == 200:
                            result.complete(True, "API server started successfully")
                            break
                except Exception:
                    if i == max_retries - 1:
                        raise
                    await asyncio.sleep(2)
            else:
                raise Exception("Server health check failed after multiple retries")
            
        except Exception as e:
            if self.server_process:
                self.server_process.terminate()
                self.server_process = None
            result.complete(False, f"Failed to start API server: {e}")
        
        self.results.append(result)
        return result
    
    async def index_vault(self) -> TestResult:
        """Vaultのインデックス作成をテストします"""
        result = TestResult("Index Vault")
        
        try:
            # CLIインデクサーを使用
            cmd = [
                sys.executable, 
                "tests/cli_tester.py", 
                "--index"
            ]
            
            if self.config_path:
                cmd.extend(["--config", self.config_path])
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                result.complete(True, "Vault indexed successfully")
            else:
                error_msg = stderr.decode('utf-8') if stderr else "Unknown error"
                result.complete(False, f"Vault indexing failed: {error_msg}")
        except Exception as e:
            result.complete(False, f"Vault indexing exception: {e}")
        
        self.results.append(result)
        return result
    
    async def test_search_api(self) -> TestResult:
        """検索APIをテストします"""
        result = TestResult("Search API")
        
        try:
            query = "Obsidian knowledge management"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/v1/search",
                    json={"query": query, "limit": 5}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "results" in data and "total" in data:
                        result.complete(True, f"Search API returned {data['total']} results")
                    else:
                        result.complete(False, "Search API response missing expected fields")
                else:
                    result.complete(False, f"Search API returned status code {response.status_code}")
        except Exception as e:
            result.complete(False, f"Search API test failed: {e}")
        
        self.results.append(result)
        return result
    
    async def test_qa_api(self) -> TestResult:
        """質問応答APIをテストします"""
        result = TestResult("Question Answering API")
        
        try:
            question = "What is the Obsidian Concierge project about?"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/v1/ask",
                    json={
                        "question": question,
                        "context_size": 3,
                        "temperature": 0.7
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "answer" in data and "context" in data:
                        result.complete(True, "QA API returned valid response")
                    else:
                        result.complete(False, "QA API response missing expected fields")
                else:
                    result.complete(False, f"QA API returned status code {response.status_code}")
        except Exception as e:
            result.complete(False, f"QA API test failed: {e}")
        
        self.results.append(result)
        return result

    async def cleanup(self) -> TestResult:
        """テスト環境をクリーンアップします"""
        result = TestResult("Cleanup")
        
        try:
            # サーバープロセスの終了
            if self.server_process:
                self.server_process.terminate()
                try:
                    self.server_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.server_process.kill()
                self.server_process = None
            
            # テスト用設定ファイルの削除
            if self.config_path and self.config_path == "test_config.yaml":
                try:
                    os.remove(self.config_path)
                except FileNotFoundError:
                    pass
            
            # テストデータディレクトリの削除
            import shutil
            try:
                shutil.rmtree("test_data", ignore_errors=True)
            except Exception:
                pass
            
            result.complete(True, "Test environment cleaned up successfully")
        except Exception as e:
            result.complete(False, f"Cleanup failed: {e}")
        
        self.results.append(result)
        return result
    
    def generate_report(self) -> str:
        """テスト結果のレポートを生成します"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        total_duration = sum(r.duration for r in self.results)
        
        report = [
            "\n=== Obsidian Concierge Integration Test Report ===\n",
            f"Total Tests: {total_tests}",
            f"Passed: {passed_tests}",
            f"Failed: {total_tests - passed_tests}",
            f"Total Duration: {total_duration:.2f}s\n",
            "Detailed Results:"
        ]
        
        for result in self.results:
            report.append(str(result))
        
        return "\n".join(report)
    
    async def run_all_tests(self) -> bool:
        """すべてのテストを実行します"""
        try:
            # セットアップ
            setup_result = await self.setup()
            if not setup_result.success:
                print(self.generate_report())
                return False
            
            # サーバー起動
            server_result = await self.start_server()
            if not server_result.success:
                await self.cleanup()
                print(self.generate_report())
                return False
            
            # Vaultインデックス作成
            index_result = await self.index_vault()
            if not index_result.success:
                await self.cleanup()
                print(self.generate_report())
                return False
            
            # 各APIテスト実行
            await self.test_search_api()
            await self.test_qa_api()
            
            # クリーンアップ
            await self.cleanup()
            
            # レポート生成と表示
            print(self.generate_report())
            
            # すべてのテストが成功したかチェック
            return all(result.success for result in self.results)
            
        except Exception as e:
            print(f"Test execution failed: {e}")
            await self.cleanup()
            return False


async def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="Obsidian Concierge Integration Tests")
    
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--vault', help='Path to test vault')
    parser.add_argument('--port', type=int, default=8000, help='API server port')
    
    args = parser.parse_args()
    
    tester = IntegrationTester(
        config_path=args.config,
        vault_path=args.vault,
        api_port=args.port
    )
    
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main()) 