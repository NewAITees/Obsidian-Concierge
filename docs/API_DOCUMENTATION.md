# Obsidian Concierge API ドキュメント

このドキュメントでは、Obsidian ConciergeのAPI仕様と利用方法について説明します。

## 概要

Obsidian ConciergeのAPIはFastAPIを使用して実装されており、主にローカル環境で実行されることを想定しています。このAPIを通じて、Obsidian Vaultの検索、質問応答、ファイル操作などの機能にプログラムからアクセスできます。

## 認証

APIはローカル環境で動作するため、基本的に認証は必要ありません。ただし、セキュリティ強化のためにAPIキーを設定することも可能です。

```yaml
# config.yaml
api:
  enable_auth: true
  api_key: "your-secret-api-key"
```

認証が有効な場合、すべてのリクエストに `X-API-Key` ヘッダーを追加する必要があります。

```
X-API-Key: your-secret-api-key
```

## ベースURL

```
http://localhost:8000/api/v1
```

ポート番号はデフォルトで8000ですが、起動時に変更可能です。

## エンドポイント

```mermaid
graph LR
    A[API ルート] --> B[/search]
    A --> C[/question]
    A --> D[/vault]
    D --> E[/vault/files]
    D --> F[/vault/move]
    D --> G[/vault/tag]
    A --> H[/moc]
    A --> I[/links]
```

### 検索 API

#### 検索を実行する

```
GET /search
```

**パラメーター**:

| 名前 | 型 | 説明 |
|------|------|------|
| query | string | 検索クエリ |
| limit | integer | 返す結果の最大数（デフォルト: 10） |

**リクエスト例**:

```bash
curl -X GET "http://localhost:8000/api/v1/search?query=python&limit=5"
```

**レスポンス例**:

```json
{
  "results": [
    {
      "id": "f8a72b3e5c9d",
      "title": "Pythonプログラミング入門",
      "path": "Resources/Programming/Python/Pythonプログラミング入門.md",
      "excerpt": "Pythonは初心者にも扱いやすい汎用プログラミング言語です...",
      "relevance": 0.92
    },
    {
      "id": "a1b2c3d4e5f6",
      "title": "Pythonによるデータ分析",
      "path": "Projects/DataAnalysis/Pythonによるデータ分析.md",
      "excerpt": "PandasとNumPyを使用したデータ分析の基本手順...",
      "relevance": 0.85
    }
    // 他の結果...
  ],
  "total": 2,
  "query": "python"
}
```

### 質問応答 API

#### 質問に回答する

```
POST /question
```

**リクエストボディ**:

```json
{
  "question": "Pythonでリストの要素を逆順にするにはどうすればいいですか？",
  "max_context_items": 3
}
```

**レスポンス例**:

```json
{
  "answer": "Pythonでリストの要素を逆順にするには、以下の方法があります：\n\n1. スライシング構文を使用する: `reversed_list = my_list[::-1]`\n2. `reversed()`関数を使用する: `reversed_list = list(reversed(my_list))`\n3. `reverse()`メソッドを使用する: `my_list.reverse()`\n\nスライシング構文と`reversed()`は元のリストを変更せず新しいリストを返します。`reverse()`メソッドは元のリストを直接変更します。",
  "sources": [
    {
      "id": "f8a72b3e5c9d",
      "title": "Pythonプログラミング入門",
      "path": "Resources/Programming/Python/Pythonプログラミング入門.md"
    }
  ]
}
```

### Vault API

#### ファイル一覧を取得する

```
GET /vault/files
```

**パラメーター**:

| 名前 | 型 | 説明 |
|------|------|------|
| path | string | 相対パス（オプション） |
| pattern | string | ファイル名マッチングパターン（オプション） |

**リクエスト例**:

```bash
curl -X GET "http://localhost:8000/api/v1/vault/files?path=Projects&pattern=*.md"
```

**レスポンス例**:

```json
{
  "files": [
    {
      "name": "ProjectA.md",
      "path": "Projects/ProjectA.md",
      "size": 1024,
      "created": "2023-01-01T12:00:00Z",
      "modified": "2023-01-02T15:30:00Z",
      "tags": ["project", "active"]
    },
    // 他のファイル...
  ],
  "total": 10
}
```

#### ファイルを移動する

```
POST /vault/move
```

**リクエストボディ**:

```json
{
  "source": "移動前/メモ.md",
  "analyze": true
}
```

`analyze`が`true`の場合、システムはファイルの内容を分析して最適なフォルダを提案します。
特定の宛先を指定したい場合は、以下のようにします：

```json
{
  "source": "移動前/メモ.md",
  "destination": "Projects/Active",
  "analyze": false
}
```

**レスポンス例**:

```json
{
  "success": true,
  "source": "移動前/メモ.md",
  "destination": "Projects/Active/メモ.md",
  "message": "ファイルを正常に移動しました"
}
```

#### ファイルにタグを追加する

```
POST /vault/tag
```

**リクエストボディ**:

```json
{
  "path": "Projects/Active/メモ.md",
  "tags": ["project", "research"],
  "analyze": false
}
```

`analyze`が`true`の場合、システムはファイルの内容を分析して適切なタグを提案します：

```json
{
  "path": "Projects/Active/メモ.md",
  "analyze": true
}
```

**レスポンス例**:

```json
{
  "success": true,
  "path": "Projects/Active/メモ.md",
  "tags": ["project", "research", "python"],
  "message": "タグを正常に追加しました"
}
```

### MOC API

#### MOCを生成する

```
POST /moc
```

**リクエストボディ**:

```json
{
  "type": "topic",
  "topic": "Python",
  "file_path": "Maps/Python MOC.md"
}
```

MOCタイプは以下から選択できます：
- `topic`: トピックベースのMOC
- `folder`: フォルダベースのMOC
- `tag`: タグベースのMOC

フォルダベースの場合：

```json
{
  "type": "folder",
  "folder": "Projects/Python",
  "file_path": "Maps/Python Projects MOC.md"
}
```

タグベースの場合：

```json
{
  "type": "tag",
  "tag": "python",
  "file_path": "Maps/Python Tag MOC.md"
}
```

**レスポンス例**:

```json
{
  "success": true,
  "file_path": "Maps/Python MOC.md",
  "moc_content": "# Python MOC\n\n## 概要\n\nPythonは...",
  "included_files": 15,
  "message": "MOCを正常に生成しました"
}
```

### リンク API

#### リンク候補を生成する

```
POST /links/suggest
```

**リクエストボディ**:

```json
{
  "file_path": "Projects/Active/メモ.md",
  "max_suggestions": 5
}
```

**レスポンス例**:

```json
{
  "suggestions": [
    {
      "target": "Resources/Programming/Python/Pythonプログラミング入門.md",
      "title": "Pythonプログラミング入門",
      "confidence": 0.92,
      "context": "...Pythonを使った自動化スクリプトについて...",
      "position": 1250
    },
    // 他の提案...
  ],
  "file_path": "Projects/Active/メモ.md",
  "total": 3
}
```

#### リンク提案を適用する

```
POST /links/apply
```

**リクエストボディ**:

```json
{
  "file_path": "Projects/Active/メモ.md",
  "selected_links": [
    {
      "target": "Resources/Programming/Python/Pythonプログラミング入門.md",
      "position": 1250
    }
  ]
}
```

**レスポンス例**:

```json
{
  "success": true,
  "file_path": "Projects/Active/メモ.md",
  "applied_links": 1,
  "message": "リンクを正常に適用しました"
}
```

## エラーレスポンス

APIはエラーが発生した場合、適切なHTTPステータスコードと詳細なエラーメッセージを返します。

```json
{
  "error": {
    "code": "file_not_found",
    "message": "指定されたファイルが見つかりません",
    "details": "Projects/NonExistent.md"
  }
}
```

## 一般的なエラーコード

| コード | HTTP ステータス | 説明 |
|------|------|------|
| `invalid_request` | 400 | リクエストデータが無効です |
| `unauthorized` | 401 | 認証が必要です |
| `forbidden` | 403 | アクションが禁止されています |
| `file_not_found` | 404 | 指定されたファイルが見つかりません |
| `folder_not_found` | 404 | 指定されたフォルダが見つかりません |
| `conflict` | 409 | リソースの競合が発生しました |
| `server_error` | 500 | サーバー内部エラーが発生しました |

## APIクライアントの例

### Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

def search(query, limit=10):
    response = requests.get(f"{BASE_URL}/search", params={
        "query": query,
        "limit": limit
    })
    return response.json()

def ask_question(question):
    response = requests.post(f"{BASE_URL}/question", json={
        "question": question
    })
    return response.json()

# 使用例
results = search("python")
print(f"検索結果: {results}")

answer = ask_question("マークダウンとは何ですか？")
print(f"回答: {answer['answer']}")
```

## レート制限

APIには以下のレート制限があります：

- 1分あたり60リクエスト
- 1時間あたり1000リクエスト

制限を超えた場合、429 Too Many Requestsステータスコードが返されます。

## API拡張の予定

将来のバージョンでは以下の機能が追加される予定です：

1. WebSocket接続によるリアルタイム更新
2. バルク操作のサポート
3. Vault統計情報API
4. プラグインAPIエンドポイント