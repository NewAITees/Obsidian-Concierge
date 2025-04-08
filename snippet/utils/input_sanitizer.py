import re
import html
from typing import Any, Dict, List, Optional, Union


class InputSanitizer:
    """
    入力値のサニタイズを行うユーティリティクラス
    HTMLエスケープやSQLインジェクション対策を提供
    """
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """
        HTMLタグをエスケープ
        
        Args:
            text: 処理対象のテキスト
            
        Returns:
            エスケープされたテキスト
        """
        if text is None:
            return ""
        # シングルクォートを特別に処理
        text = str(text).replace("'", "'")
        return html.escape(text, quote=False)
    
    @staticmethod
    def strip_tags(text: str) -> str:
        """
        HTMLタグを削除
        
        Args:
            text: 処理対象のテキスト
            
        Returns:
            タグが削除されたテキスト
        """
        if text is None:
            return ""
        return re.sub(r'<[^>]*>', '', str(text))
    
    @staticmethod
    def sanitize_sql(text: str) -> str:
        """
        SQLインジェクション対策のためのエスケープ
        
        注意: これはパラメータ化クエリの代わりにはなりません。
        常にプリペアドステートメントを使用してください。
        
        Args:
            text: 処理対象のテキスト
            
        Returns:
            エスケープされたテキスト
        """
        if text is None:
            return ""
        
        # SQLキーワードと特殊文字を削除
        sql_keywords = [
            "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE",
            "UNION", "JOIN", "WHERE", "FROM", "INTO", "SET", "VALUES", "--", "/*", "*/"
        ]
        # 特殊文字のリスト
        special_chars = [";", "'", "\"", "\\", "/", "*", "%", "_"]
        
        result = str(text).upper()
        # SQLキーワードを削除
        for keyword in sql_keywords:
            result = result.replace(keyword, "")
        # 特殊文字を削除
        for char in special_chars:
            result = result.replace(char, "")
        
        return result.lower().strip()
    
    @staticmethod
    def sanitize_filename(text: str) -> str:
        """
        ファイル名から危険な文字を削除
        
        Args:
            text: 処理対象のテキスト
            
        Returns:
            安全なファイル名
        """
        if text is None:
            return ""
        
        # 危険な文字やパターンを削除
        text = str(text)
        text = re.sub(r'[.]{2,}', '', text)  # 連続したドットを削除
        text = re.sub(r'[/\\?%*:|"<>]', '_', text)  # 危険な文字を_に置換
        text = text.lstrip('.')  # 先頭のドットを削除
        return text
    
    @staticmethod
    def sanitize_integer(value: Any, default: int = 0, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
        """
        整数値をサニタイズ
        
        Args:
            value: 処理対象の値
            default: 変換できない場合のデフォルト値
            min_value: 最小値
            max_value: 最大値
            
        Returns:
            サニタイズされた整数値
        """
        try:
            result = int(value)
            
            if min_value is not None and result < min_value:
                return min_value
            
            if max_value is not None and result > max_value:
                return max_value
            
            return result
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """
        メールアドレスをサニタイズ
        
        Args:
            email: メールアドレス
            
        Returns:
            サニタイズされたメールアドレス（無効な場合は空文字）
        """
        if not email:
            return ""
        
        # 簡易的なメールアドレスの正規表現
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return email
        return ""
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
        """
        辞書から許可されたキーのみを抽出
        
        Args:
            data: 処理対象の辞書
            allowed_keys: 許可するキーのリスト
            
        Returns:
            サニタイズされた辞書
        """
        if not data:
            return {}
        
        return {k: data[k] for k in allowed_keys if k in data}
    
    @staticmethod
    def sanitize_all_dict_values(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        辞書のすべての文字列値をHTMLエスケープ
        
        Args:
            data: 処理対象の辞書
            
        Returns:
            サニタイズされた辞書
        """
        if not data:
            return {}
        
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = InputSanitizer.sanitize_html(value)
            elif isinstance(value, dict):
                result[key] = InputSanitizer.sanitize_all_dict_values(value)
            elif isinstance(value, list):
                result[key] = InputSanitizer.sanitize_all_list_values(value)
            else:
                result[key] = value
        return result
    
    @staticmethod
    def sanitize_all_list_values(data: List[Any]) -> List[Any]:
        """
        リストのすべての文字列値をHTMLエスケープ
        
        Args:
            data: 処理対象のリスト
            
        Returns:
            サニタイズされたリスト
        """
        if not data:
            return []
        
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(InputSanitizer.sanitize_html(item))
            elif isinstance(item, dict):
                result.append(InputSanitizer.sanitize_all_dict_values(item))
            elif isinstance(item, list):
                result.append(InputSanitizer.sanitize_all_list_values(item))
            else:
                result.append(item)
        return result


# 使用例
if __name__ == "__main__":
    # HTMLエスケープ
    html_input = "<script>alert('XSS');</script>"
    print(f"元のHTML: {html_input}")
    print(f"サニタイズ後: {InputSanitizer.sanitize_html(html_input)}")
    print(f"タグ削除後: {InputSanitizer.strip_tags(html_input)}")
    
    # SQLインジェクション対策
    sql_input = "1; DROP TABLE users; --"
    print(f"\n元のSQL入力: {sql_input}")
    print(f"サニタイズ後: {InputSanitizer.sanitize_sql(sql_input)}")
    
    # ファイル名のサニタイズ
    filename_input = "../../../etc/passwd"
    print(f"\n元のファイル名: {filename_input}")
    print(f"サニタイズ後: {InputSanitizer.sanitize_filename(filename_input)}")
    
    # 整数値のサニタイズ
    int_inputs = ["123", "abc", "456", "-10"]
    print("\n整数値のサニタイズ:")
    for val in int_inputs:
        sanitized = InputSanitizer.sanitize_integer(val, default=0, min_value=0, max_value=100)
        print(f"  {val} -> {sanitized}")
    
    # メールアドレスのサニタイズ
    email_inputs = ["user@example.com", "invalid-email", "admin@test.org"]
    print("\nメールアドレスのサニタイズ:")
    for email in email_inputs:
        sanitized = InputSanitizer.sanitize_email(email)
        print(f"  {email} -> {sanitized}")
    
    # 辞書のサニタイズ
    user_input = {
        "name": "<b>Test User</b>",
        "email": "user@example.com",
        "password": "secret123",
        "role": "admin"
    }
    print("\n辞書のサニタイズ:")
    allowed_keys = ["name", "email", "role"]
    filtered_dict = InputSanitizer.sanitize_dict(user_input, allowed_keys)
    print(f"  フィルタリング後: {filtered_dict}")
    
    sanitized_dict = InputSanitizer.sanitize_all_dict_values(filtered_dict)
    print(f"  値のサニタイズ後: {sanitized_dict}")