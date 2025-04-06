# Obsidian Concierge アプリケーションフロー

このドキュメントでは、Obsidian Conciergeの主要な機能フローと操作シーケンスについて説明します。

## 1. 全体的なユーザーフロー

Obsidian Conciergeは、ユーザーがObsidian Vaultの管理を効率化するための支援ツールです。

```mermaid
graph TD
    A[開始] --> B[インストール・設定]
    B --> C[Vaultインデックス作成]
    C --> D{機能選択}
    
    D -->|検索| E[検索機能]
    D -->|質問応答| F[質問応答機能]
    D -->|ファイル移動| G[ファイル移動機能]
    D -->|MOC生成| H[MOC生成機能]
    D -->|タグ付け| I[タグ付け機能]
    D -->|リンク生成| J[リンク生成機能]
    
    E --> D
    F --> D
    G --> D
    H --> D
    I --> D
    J --> D
```

## 2. 初期セットアップフロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant App as アプリケーション
    participant Config as 設定ファイル
    participant Vault as Obsidian Vault
    participant DB as ChromaDB
    
    User->>App: アプリケーション起動
    App->>Config: 設定ファイル確認
    
    alt 初回起動
        App-->>User: 設定ファイルが見つかりません
        User->>App: Vaultパスと設定情報を提供
        App->>Config: 設定ファイル作成
    end
    
    App->>Vault: Vaultの存在確認
    Vault-->>App: 確認結果
    
    alt Vaultが見つからない
        App-->>User: Vaultが見つかりません
        User->>App: 正しいVaultパスを提供
        App->>Config: 設定を更新
    end
    
    App->>DB: インデックスの存在確認
    
    alt 初回インデックス作成
        App-->>User: インデックスが見つかりません。作成しますか？
        User->>App: 承認
        App->>Vault: すべてのMarkdownファイルを読み込み
        App->>DB: インデックス作成
        DB-->>App: 完了通知
    end
    
    App-->>User: セットアップ完了・メイン画面表示
```

## 3. 検索機能フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as 検索UI
    participant API as 検索API
    participant DB as ChromaDB
    
    User->>UI: 検索クエリ入力
    UI->>API: 検索リクエスト送信
    API->>DB: ベクトル検索実行
    DB-->>API: 検索結果返却
    API->>UI: 結果表示
    UI-->>User: 検索結果提示
    
    User->>UI: 結果選択
    UI-->>User: 選択したノートを表示
```

### 検索画面遷移

```mermaid
stateDiagram-v2
    [*] --> 検索フォーム
    検索フォーム --> 検索実行中: クエリ入力・検索
    検索実行中 --> 検索結果表示: 結果取得
    検索実行中 --> 検索エラー: エラー発生
    検索エラー --> 検索フォーム: 再試行
    検索結果表示 --> ノート詳細表示: 結果選択
    ノート詳細表示 --> 検索結果表示: 戻る
    検索結果表示 --> 検索フォーム: 新しい検索
```

### 検索フィルタリングオプション

ユーザーは以下の条件で検索結果をフィルタリングできます：

- **タグ**: 特定のタグを持つノートのみ表示
- **フォルダ**: 特定のフォルダ内のノートのみ表示
- **更新日時**: 特定の期間に更新されたノートのみ表示
- **タイトル**: タイトルに特定の文字列を含むノートのみ表示

## 4. 質問応答機能フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as 質問UI
    participant API as 質問API
    participant DB as ChromaDB
    participant LLM as Ollama
    
    User->>UI: 質問を入力
    UI->>API: 質問を送信
    API->>DB: 関連コンテキスト検索
    DB-->>API: 関連ノート
    API->>LLM: 質問とコンテキストを送信
    LLM-->>API: 回答生成
    API->>UI: 回答表示
    UI-->>User: 回答と参照ソースを提示
    
    opt フォローアップ質問
        User->>UI: フォローアップ質問入力
        UI->>API: 質問・会話履歴送信
        API->>DB: 追加コンテキスト検索
        API->>LLM: 会話履歴・コンテキスト送信
        LLM-->>API: 回答生成
        API->>UI: 回答表示
        UI-->>User: 更新された回答を提示
    end
```

### 回答生成プロセス

1. ユーザーの質問を受け取る
2. 質問に関連するノートをベクトル検索で見つける
3. 見つかったノートから関連コンテキストを抽出
4. LLMに質問とコンテキストを提供
5. LLMが回答を生成
6. 回答と情報源となったノートへの参照を表示

## 5. ファイル移動機能フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as ファイル移動UI
    participant API as ファイル移動API
    participant LLM as Ollama
    participant FS as ファイルシステム
    
    User->>UI: 移動前フォルダのファイルリスト表示
    UI->>API: 移動前フォルダのファイル取得
    API->>FS: ディレクトリ内容取得
    FS-->>API: ファイルリスト
    API->>UI: ファイルリスト表示
    
    alt 自動分析による移動
        User->>UI: 自動分析・移動を選択
        UI->>API: ファイル移動リクエスト（分析モード）
        API->>FS: ファイル読み込み
        FS-->>API: ファイル内容
        API->>LLM: ファイル内容・フォルダ構造を送信
        LLM-->>API: 推奨フォルダを返却
        API->>UI: 移動先フォルダの提案表示
        UI-->>User: 提案を確認
        User->>UI: 提案を承認
        UI->>API: 移動実行リクエスト
        API->>FS: ファイル移動
        FS-->>API: 移動結果
        API->>UI: 完了通知
        UI-->>User: 移動完了メッセージ表示
    else 手動選択による移動
        User->>UI: ファイルと移動先を選択
        UI->>API: ファイル移動リクエスト（手動モード）
        API->>FS: ファイル移動
        FS-->>API: 移動結果
        API->>UI: 完了通知
        UI-->>User: 移動完了メッセージ表示
    end
```

### 移動先推論プロセス

LLMはノートの内容を分析し、以下の要素に基づいて最適なフォルダを推論します：

1. ノートのタイトルとタグ
2. ノートの内容における主要キーワード
3. ノートの構造とフォーマット
4. 設定ファイルで定義されたフォルダ構造との一致度

## 6. MOC生成機能フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as MOC生成UI
    participant API as MOC生成API
    participant DB as ChromaDB
    participant LLM as Ollama
    participant FS as ファイルシステム
    
    User->>UI: MOC生成フォーム表示
    UI-->>User: MOCタイプ選択フォーム表示
    
    alt トピックベースMOC
        User->>UI: トピックと出力ファイルパスを入力
        UI->>API: トピックベースMOC生成リクエスト
        API->>DB: トピック関連ノート検索
        DB-->>API: 関連ノートリスト
    else フォルダベースMOC
        User->>UI: フォルダと出力ファイルパスを選択
        UI->>API: フォルダベースMOC生成リクエスト
        API->>FS: フォルダ内のノート取得
        FS-->>API: フォルダ内ノートリスト
    else タグベースMOC
        User->>UI: タグと出力ファイルパスを選択
        UI->>API: タグベースMOC生成リクエスト
        API->>DB: 指定タグを持つノート検索
        DB-->>API: タグ付きノートリスト
    end
    
    API->>FS: 関連ノート読み込み
    FS-->>API: ノート内容
    API->>LLM: ノート内容・MOC生成指示を送信
    LLM-->>API: 生成されたMOC内容
    API->>UI: MOCプレビュー表示
    UI-->>User: MOCプレビュー確認
    
    User->>UI: 保存または編集
    
    alt 保存
        UI->>API: MOC保存リクエスト
        API->>FS: MOCファイル書き込み
        FS-->>API: 保存結果
        API->>UI: 完了通知
        UI-->>User: 保存完了メッセージ表示
    else 編集
        User->>UI: MOC内容を編集
        User->>UI: 保存
        UI->>API: 編集済みMOC保存リクエスト
        API->>FS: MOCファイル書き込み
        FS-->>API: 保存結果
        API->>UI: 完了通知
        UI-->>User: 保存完了メッセージ表示
    end
```

### MOC生成プロセス

MOC（Map of Content）は、関連ノートを整理して概要を提供するメタノートです：

1. ユーザーがMOCのタイプ（トピック、フォルダ、タグ）を選択
2. 関連ノートの検索・収集
3. 関連ノートの内容を分析
4. ノート間の関係性を特定
5. 階層的な構造を持つMOCを生成
6. リンクと簡潔な説明を含めた内容を提供

### MOCの例

```markdown
# Python Programming MOC

## 概要
このMOCはPythonプログラミングに関する知識をまとめたものです。

## 基礎概念
- [[Python基本構文]] - 変数、ループ、条件分岐
- [[Python関数]] - 関数定義と使用方法
- [[Pythonクラス]] - オブジェクト指向プログラミング

## ライブラリとフレームワーク
- [[NumPy入門]] - 数値計算ライブラリ
- [[Pandas基礎]] - データ分析ライブラリ
- [[Djangoの基本]] - ウェブフレームワーク

## プロジェクト
- [[Pythonスクレイピングプロジェクト]] - Webスクレイピングの実践例
```

## 7. タグ付け機能フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as タグ付けUI
    participant API as タグ付けAPI
    participant LLM as Ollama
    participant FS as ファイルシステム
    
    User->>UI: ノート選択
    UI->>API: ノート情報取得リクエスト
    API->>FS: ノート読み込み
    FS-->>API: ノート内容
    API->>UI: ノート情報表示
    UI-->>User: 現在のタグ表示
    
    alt 自動タグ提案
        User->>UI: 自動タグ提案を選択
        UI->>API: タグ提案リクエスト
        API->>LLM: ノート内容・許可されたタグリストを送信
        LLM-->>API: 提案タグリスト
        API->>UI: タグ提案表示
        UI-->>User: 提案タグを確認
        User->>UI: 適用するタグを選択
    else 手動タグ編集
        User->>UI: タグを手動編集
    end
    
    User->>UI: 保存
    UI->>API: タグ更新リクエスト
    API->>FS: ノートファイル更新
    FS-->>API: 更新結果
    API->>UI: 完了通知
    UI-->>User: 保存完了メッセージ表示
```

### タグ提案ロジック

LLMを使用して、ノートの内容から適切なタグを提案します：

1. ノートの内容を分析
2. 設定ファイルで定義された許可タグリストを参照
3. ノートの主題、キーワード、構造に基づいてタグを推論
4. 既存のタグを考慮し、追加すべき新しいタグを提案
5. タグの階層（例: `project/active`）も適切に提案

## 8. リンク生成機能フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as リンクUI
    participant API as リンクAPI
    participant DB as ChromaDB
    participant LLM as Ollama
    participant FS as ファイルシステム
    
    User->>UI: ノート選択
    UI->>API: ノート情報取得リクエスト
    API->>FS: ノート読み込み
    FS-->>API: ノート内容
    API->>UI: ノート情報表示
    
    User->>UI: リンク候補生成を選択
    UI->>API: リンク候補リクエスト
    API->>DB: 関連ノート検索
    DB-->>API: 関連ノートリスト
    API->>LLM: ノート内容・関連ノート情報を送信
    LLM-->>API: リンク候補と挿入位置
    API->>UI: リンク候補表示
    UI-->>User: リンク候補を確認
    
    User->>UI: 適用するリンクを選択
    UI->>API: リンク適用リクエスト
    API->>FS: ノートファイル更新
    FS-->>API: 更新結果
    API->>UI: 完了通知
    UI-->>User: 適用完了メッセージ表示
```

### リンク候補生成ロジック

関連ノートへのリンクを提案するプロセス：

1. 対象ノートの内容を分析
2. ベクトル検索で意味的に関連するノートを見つける
3. キーフレーズを抽出し、一致するノートタイトルを検索
4. LLMを使用して最も適切な挿入位置を特定
5. リンクの重要度と関連性のスコアを計算
6. 可能な限り自然な形でリンクを挿入できる場所を提案

## 9. エラーハンドリングとリカバリー

### 一般的なエラーフロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as UI
    participant API as API
    participant System as システム
    
    User->>UI: アクション実行
    UI->>API: リクエスト送信
    
    alt エラー発生
        API-->>UI: エラーレスポンス
        UI-->>User: エラーメッセージ表示
        
        opt リトライ可能なエラー
            User->>UI: リトライを選択
            UI->>API: リクエスト再送信
        end
        
        opt リカバリーが必要
            User->>UI: リカバリーアクションを選択
            UI->>API: リカバリーリクエスト
            API->>System: リカバリー処理実行
            System-->>API: リカバリー結果
            API->>UI: 結果表示
            UI-->>User: 復旧状況を提示
        end
    end
```

### バックアップとロールバック

重要な操作（ファイル移動、MOC生成、タグ編集など）の前に自動的にバックアップを作成し、問題が発生した場合に復元できるようにします：

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as UI
    participant API as API
    participant FS as ファイルシステム
    participant Backup as バックアップシステム
    
    User->>UI: 重要な操作を実行
    UI->>API: 操作リクエスト
    API->>Backup: バックアップ作成
    Backup->>FS: ファイルコピー
    Backup-->>API: バックアップID
    
    alt 操作成功
        API->>FS: 操作実行
        FS-->>API: 操作結果
        API->>UI: 完了通知
        UI-->>User: 操作完了メッセージ
    else 操作失敗
        API->>UI: エラー通知
        UI-->>User: エラーメッセージと復元オプション表示
        User->>UI: 復元を選択
        UI->>API: 復元リクエスト
        API->>Backup: 復元処理
        Backup->>FS: バックアップから復元
        FS-->>API: 復元結果
        API->>UI: 復元完了通知
        UI-->>User: 復元完了メッセージ
    end
```

## 10. アプリケーション設定フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as 設定UI
    participant API as 設定API
    participant Config as 設定ファイル
    
    User->>UI: 設定画面を開く
    UI->>API: 現在の設定取得
    API->>Config: 設定読み込み
    Config-->>API: 設定データ
    API->>UI: 設定表示
    UI-->>User: 現在の設定を表示
    
    User->>UI: 設定を変更
    UI->>API: 設定更新リクエスト
    API->>Config: 設定更新
    Config-->>API: 更新結果
    
    alt 変更が即時反映が必要
        API->>API: 関連システム再初期化
    end
    
    API->>UI: 完了通知
    UI-->>User: 設定保存完了メッセージ
```

### 設定可能な項目

Obsidian Conciergeでは、以下の設定が可能です：

- **基本設定**
  - Vaultパス
  - UIテーマ（ライト/ダーク）
  - ログレベル

- **フォルダ構造**
  - フォルダ階層の定義
  - 自動生成されるフォルダ

- **タグ管理**
  - 許可されたタグのリスト
  - 自動タグ付けルール

- **LLM設定**
  - 使用するモデル
  - 温度（創造性）パラメーター
  - コンテキスト長
  - API設定

- **インデックス設定**
  - 自動インデックス更新
  - インデックス除外フォルダ
  - 差分更新頻度

## 11. トラブルシューティングガイド

一般的な問題と解決策のフローチャート：

```mermaid
graph TD
    A[問題発生] --> B{問題タイプ}
    
    B -->|インデックスエラー| C[インデックス問題]
    B -->|LLM接続エラー| D[LLM問題]
    B -->|ファイル操作エラー| E[ファイルシステム問題]
    B -->|UI表示問題| F[UI問題]
    
    C --> C1{原因}
    C1 -->|インデックス破損| C2[インデックス再構築]
    C1 -->|アクセス権限| C3[権限確認]
    C1 -->|不完全なインデックス| C4[差分更新実行]
    
    D --> D1{原因}
    D1 -->|Ollama未起動| D2[Ollama起動]
    D1 -->|モデル未ダウンロード| D3[モデルダウンロード]
    D1 -->|API設定誤り| D4[設定確認]
    
    E --> E1{原因}
    E1 -->|アクセス権限| E2[権限確認]
    E1 -->|パス不正| E3[パス検証]
    E1 -->|ファイルロック| E4[ロック解除]
    
    F --> F1{原因}
    F1 -->|ブラウザ問題| F2[ブラウザキャッシュクリア]
    F1 -->|リソース不足| F3[リソース確認]
    F1 -->|レンダリングエラー| F4[UIリロード]
```