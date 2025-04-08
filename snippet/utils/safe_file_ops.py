import os
import tempfile
import shutil
import json
import csv
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable


class FileOperationError(Exception):
    """ファイル操作に関するエラー"""
    pass


class SafeFileOps:
    """
    安全なファイル操作を提供するユーティリティクラス
    一時ファイルを使った安全な書き込み処理とエラーハンドリングを提供
    """
    
    @staticmethod
    def safe_read(file_path: Union[str, Path], encoding: str = 'utf-8', default: Any = None) -> str:
        """
        安全にファイルを読み込む
        
        Args:
            file_path: 読み込むファイルのパス
            encoding: 文字エンコーディング
            default: エラー時のデフォルト値
            
        Returns:
            ファイルの内容
            
        Raises:
            FileOperationError: デフォルト値が指定されておらず、ファイル読み込みに失敗した場合
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (IOError, OSError, UnicodeDecodeError) as e:
            if default is not None:
                return default
            raise FileOperationError(f"ファイル読み込みエラー: {file_path} - {str(e)}")
    
    @staticmethod
    def safe_write(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """
        安全にファイルに書き込む（一時ファイルを使用）
        
        Args:
            file_path: 書き込み先ファイルのパス
            content: 書き込む内容
            encoding: 文字エンコーディング
            
        Raises:
            FileOperationError: ファイル書き込みに失敗した場合
        """
        file_path = Path(file_path)
        
        # 親ディレクトリが存在しない場合は作成
        os.makedirs(file_path.parent, exist_ok=True)
        
        # 同じディレクトリに一時ファイルを作成
        temp_dir = file_path.parent
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding=encoding, dir=temp_dir, delete=False) as tmp:
                tmp_path = tmp.name
                tmp.write(content)
            
            # 一時ファイルを本来のファイルに置き換え（アトミック操作）
            shutil.move(tmp_path, file_path)
        except (IOError, OSError, UnicodeEncodeError) as e:
            # エラーが発生した場合、一時ファイルを削除
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass  # 一時ファイル削除のエラーは無視
            raise FileOperationError(f"ファイル書き込みエラー: {file_path} - {str(e)}")
    
    @staticmethod
    def safe_append(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """
        安全にファイルに追記する
        
        Args:
            file_path: 追記先ファイルのパス
            content: 追記する内容
            encoding: 文字エンコーディング
            
        Raises:
            FileOperationError: ファイル追記に失敗した場合
        """
        file_path = Path(file_path)
        
        # 親ディレクトリが存在しない場合は作成
        os.makedirs(file_path.parent, exist_ok=True)
        
        try:
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)
        except (IOError, OSError, UnicodeEncodeError) as e:
            raise FileOperationError(f"ファイル追記エラー: {file_path} - {str(e)}")
    
    @staticmethod
    def safe_delete(file_path: Union[str, Path]) -> bool:
        """
        安全にファイルを削除する
        
        Args:
            file_path: 削除するファイルのパス
            
        Returns:
            削除が成功したかどうか
            
        Raises:
            FileOperationError: ファイル削除に失敗した場合
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except (IOError, OSError) as e:
            raise FileOperationError(f"ファイル削除エラー: {file_path} - {str(e)}")
    
    @staticmethod
    def safe_rename(src_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
        """
        安全にファイルをリネーム/移動する
        
        Args:
            src_path: 元のファイルパス
            dst_path: 移動先のファイルパス
            
        Raises:
            FileOperationError: ファイル移動に失敗した場合
        """
        try:
            # 移動先の親ディレクトリが存在しない場合は作成
            dst_path = Path(dst_path)
            os.makedirs(dst_path.parent, exist_ok=True)
            
            shutil.move(src_path, dst_path)
        except (IOError, OSError) as e:
            raise FileOperationError(f"ファイル移動エラー: {src_path} → {dst_path} - {str(e)}")
    
    @staticmethod
    def safe_copy(src_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
        """
        安全にファイルをコピーする
        
        Args:
            src_path: コピー元のファイルパス
            dst_path: コピー先のファイルパス
            
        Raises:
            FileOperationError: ファイルコピーに失敗した場合
        """
        try:
            # コピー先の親ディレクトリが存在しない場合は作成
            dst_path = Path(dst_path)
            os.makedirs(dst_path.parent, exist_ok=True)
            
            shutil.copy2(src_path, dst_path)
        except (IOError, OSError) as e:
            raise FileOperationError(f"ファイルコピーエラー: {src_path} → {dst_path} - {str(e)}")
    
    @staticmethod
    def read_json(file_path: Union[str, Path], encoding: str = 'utf-8', default: Optional[Any] = None) -> Dict[str, Any]:
        """
        JSONファイルを読み込む
        
        Args:
            file_path: 読み込むJSONファイルのパス
            encoding: 文字エンコーディング
            default: ファイルが存在しない場合のデフォルト値
            
        Returns:
            JSONデータ（辞書）
            
        Raises:
            FileOperationError: デフォルト値が指定されておらず、ファイル読み込みに失敗した場合
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return json.load(f)
        except (IOError, OSError, json.JSONDecodeError) as e:
            if default is not None:
                return default
            raise FileOperationError(f"JSONファイル読み込みエラー: {file_path} - {str(e)}")
    
    @staticmethod
    def write_json(file_path: Union[str, Path], data: Dict[str, Any], encoding: str = 'utf-8', indent: int = 4) -> None:
        """
        JSONファイルに書き込む
        
        Args:
            file_path: 書き込み先JSONファイルのパス
            data: 書き込むデータ（辞書）
            encoding: 文字エンコーディング
            indent: JSONのインデントスペース数
            
        Raises:
            FileOperationError: ファイル書き込みに失敗した場合
        """
        try:
            content = json.dumps(data, ensure_ascii=False, indent=indent)
            SafeFileOps.safe_write(file_path, content, encoding=encoding)
        except (IOError, OSError, TypeError) as e:
            raise FileOperationError(f"JSONファイル書き込みエラー: {file_path} - {str(e)}")
    
    @staticmethod
    def read_csv(file_path: Union[str, Path], encoding: str = 'utf-8', delimiter: str = ',', has_header: bool = True) -> List[Dict[str, str]]:
        """
        CSVファイルを読み込む
        
        Args:
            file_path: 読み込むCSVファイルのパス
            encoding: 文字エンコーディング
            delimiter: 区切り文字
            has_header: ヘッダー行があるかどうか
            
        Returns:
            CSVデータ（辞書のリスト）
            
        Raises:
            FileOperationError: ファイル読み込みに失敗した場合
        """
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                if has_header:
                    reader = csv.DictReader(f, delimiter=delimiter)
                    return list(reader)
                else:
                    reader = csv.reader(f, delimiter=delimiter)
                    data = list(reader)
                    return [dict(zip([f"column_{i}" for i in range(len(row))], row)) for row in data]
        except (IOError, OSError, csv.Error) as e:
            raise FileOperationError(f"CSVファイル読み込みエラー: {file_path} - {str(e)}")
    
    @staticmethod
    def write_csv(file_path: Union[str, Path], data: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None, 
                  encoding: str = 'utf-8', delimiter: str = ',') -> None:
        """
        CSVファイルに書き込む
        
        Args:
            file_path: 書き込み先CSVファイルのパス
            data: 書き込むデータ（辞書のリスト）
            fieldnames: 列名のリスト（None の場合は最初の辞書のキーを使用）
            encoding: 文字エンコーディング
            delimiter: 区切り文字
            
        Raises:
            FileOperationError: ファイル書き込みに失敗した場合
        """
        if not data:
            # 空のデータの場合は空のCSVを作成
            SafeFileOps.safe_write(file_path, "", encoding=encoding)
            return
            
        if fieldnames is None:
            # 最初の辞書のキーを列名として使用
            fieldnames = list(data[0].keys())
        
        try:
            # 一時ファイルに書き込む
            file_path = Path(file_path)
            temp_dir = file_path.parent
            os.makedirs(temp_dir, exist_ok=True)
            
            with tempfile.NamedTemporaryFile(mode='w', encoding=encoding, newline='', dir=temp_dir, delete=False) as tmp:
                tmp_path = tmp.name
                writer = csv.DictWriter(tmp, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            
            # 一時ファイルを本来のファイルに置き換え
            shutil.move(tmp_path, file_path)
        except (IOError, OSError, csv.Error) as e:
            # エラーが発生した場合、一時ファイルを削除
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass  # 一時ファイル削除のエラーは無視
            raise FileOperationError(f"CSVファイル書き込みエラー: {file_path} - {str(e)}")
    
    @staticmethod
    def get_file_hash(file_path: Union[str, Path], algorithm: str = 'sha256', chunk_size: int = 4096) -> str:
        """
        ファイルのハッシュ値を計算
        
        Args:
            file_path: ハッシュ値を計算するファイルのパス
            algorithm: ハッシュアルゴリズム（md5, sha1, sha256 など）
            chunk_size: 一度に読み込むバイト数
            
        Returns:
            ハッシュ値（16進数文字列）
            
        Raises:
            FileOperationError: ファイル読み込みに失敗した場合
        """
        try:
            hasher = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            
            return hasher.hexdigest()
        except (IOError, OSError) as e:
            raise FileOperationError(f"ファイルハッシュ計算エラー: {file_path} - {str(e)}")
    
    @staticmethod
    def process_file_safely(file_path: Union[str, Path], processor: Callable[[str], str], encoding: str = 'utf-8') -> None:
        """
        ファイルを安全に処理する
        
        Args:
            file_path: 処理するファイルのパス
            processor: ファイルの内容を処理する関数
            encoding: 文字エンコーディング
            
        Raises:
            FileOperationError: ファイル処理に失敗した場合
        """
        try:
            # ファイル読み込み
            content = SafeFileOps.safe_read(file_path, encoding=encoding)
            
            # コンテンツ処理
            processed_content = processor(content)
            
            # 安全に書き戻し
            SafeFileOps.safe_write(file_path, processed_content, encoding=encoding)
            
        except Exception as e:
            raise FileOperationError(f"ファイル処理エラー: {file_path} - {str(e)}")


# 使用例
if __name__ == "__main__":
    # テスト用の一時ディレクトリを作成
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        print(f"==== 安全なファイル操作テスト ({temp_dir}) ====")
        
        # 1. テキストファイルの書き込みと読み込み
        text_file = temp_dir_path / "test.txt"
        original_content = "これはテストファイルです。\n安全に書き込まれました。"
        
        print("1. テキストファイル書き込み...")
        SafeFileOps.safe_write(text_file, original_content)
        
        print("   テキストファイル読み込み...")
        content = SafeFileOps.safe_read(text_file)
        print(f"   読み込まれた内容: {content}")
        assert content == original_content
        
        # 2. JSONファイルの書き込みと読み込み
        json_file = temp_dir_path / "test.json"
        json_data = {
            "name": "テストユーザー",
            "age": 30,
            "items": ["アイテム1", "アイテム2", "アイテム3"]
        }
        
        print("\n2. JSONファイル書き込み...")
        SafeFileOps.write_json(json_file, json_data)
        
        print("   JSONファイル読み込み...")
        loaded_data = SafeFileOps.read_json(json_file)
        print(f"   読み込まれたJSON: {loaded_data}")
        assert loaded_data == json_data
        
        # 3. CSVファイルの書き込みと読み込み
        csv_file = temp_dir_path / "test.csv"
        csv_data = [
            {"名前": "山田太郎", "年齢": "30", "職業": "エンジニア"},
            {"名前": "鈴木花子", "年齢": "25", "職業": "デザイナー"},
            {"名前": "佐藤次郎", "年齢": "40", "職業": "マネージャー"}
        ]
        
        print("\n3. CSVファイル書き込み...")
        SafeFileOps.write_csv(csv_file, csv_data)
        
        print("   CSVファイル読み込み...")
        loaded_csv = SafeFileOps.read_csv(csv_file)
        print(f"   読み込まれたCSV: {loaded_csv}")
        
        # 4. ファイル操作
        copy_file = temp_dir_path / "copy.txt"
        
        print("\n4. ファイルコピー...")
        SafeFileOps.safe_copy(text_file, copy_file)
        
        print("   ファイルハッシュ計算...")
        original_hash = SafeFileOps.get_file_hash(text_file)
        copy_hash = SafeFileOps.get_file_hash(copy_file)
        print(f"   元ファイルハッシュ: {original_hash}")
        print(f"   コピーファイルハッシュ: {copy_hash}")
        assert original_hash == copy_hash
        
        # 5. ファイル処理
        print("\n5. ファイル処理...")
        def uppercase_processor(content):
            return content.upper()
        
        SafeFileOps.process_file_safely(text_file, uppercase_processor)
        processed_content = SafeFileOps.safe_read(text_file)
        print(f"   処理後の内容: {processed_content}")
        assert processed_content == original_content.upper()
        
        print("\nすべてのテストが成功しました！")