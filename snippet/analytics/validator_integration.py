"""
関数の入出力検証モジュール

validatorとtest_data_generatorを統合して、
関数の入出力形式を検証し、テストデータを自動生成します。
"""
import ast
import inspect
import typing
import sys
import os
from typing import Any, Dict, List, Optional, Set, Tuple, Union, get_type_hints
from pathlib import Path

# 既存のツールをインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snippet.validator import Validator, ValidationError
from snippet.test_data_generator import TestDataGenerator

# 型ヒントの解決に必要なモジュール
try:
    from typing import _GenericAlias  # Python 3.7-3.8
except ImportError:
    try:
        from typing import _SpecialGenericAlias as _GenericAlias  # Python 3.9+
    except ImportError:
        # フォールバック
        _GenericAlias = type(List[int])


class FunctionValidator:
    """
    関数の入出力形式を検証するバリデータ
    """
    
    def __init__(self, test_data_count: int = 5):
        """
        初期化
        
        Args:
            test_data_count: 生成するテストデータの数
        """
        self.data_generator = TestDataGenerator()
        self.validator = Validator()
        self.test_data_count = test_data_count
        self.issues = []
    
    def _generate_test_value(self, type_hint: Any) -> Any:
        """
        型ヒントに基づいてテスト値を生成
        
        Args:
            type_hint: 型ヒント
            
        Returns:
            生成された値
        """
        if type_hint == str:
            return self.data_generator.random_string()
        elif type_hint == int:
            return 42
        elif type_hint == float:
            return 3.14
        elif type_hint == bool:
            return self.data_generator.random_bool()
        elif type_hint == list or (hasattr(type_hint, "__origin__") and type_hint.__origin__ == list):
            # List[T] の場合、要素の型を取得
            if hasattr(type_hint, "__args__") and type_hint.__args__:
                element_type = type_hint.__args__[0]
                return [self._generate_test_value(element_type) for _ in range(3)]
            return [1, 2, 3]
        elif type_hint == dict or (hasattr(type_hint, "__origin__") and type_hint.__origin__ == dict):
            # Dict[K, V] の場合
            if hasattr(type_hint, "__args__") and len(type_hint.__args__) >= 2:
                key_type, value_type = type_hint.__args__[:2]
                return {
                    self._generate_test_value(key_type): self._generate_test_value(value_type)
                    for _ in range(2)
                }
            return {"key": "value"}
        elif type_hint == set or (hasattr(type_hint, "__origin__") and type_hint.__origin__ == set):
            # Set[T] の場合
            if hasattr(type_hint, "__args__") and type_hint.__args__:
                element_type = type_hint.__args__[0]
                return {self._generate_test_value(element_type) for _ in range(3)}
            return {1, 2, 3}
        elif type_hint == tuple or (hasattr(type_hint, "__origin__") and type_hint.__origin__ == tuple):
            # Tuple[T1, T2, ...] の場合
            if hasattr(type_hint, "__args__") and type_hint.__args__:
                return tuple(self._generate_test_value(t) for t in type_hint.__args__)
            return (1, "test")
        elif type_hint == Any or type_hint is None:
            return "test_value"
        elif isinstance(type_hint, type):
            # クラスの場合、デフォルトコンストラクタを呼び出し
            try:
                return type_hint()
            except:
                return None
        # 他の型や複雑な型は未対応
        return None
    
    def generate_test_data(self, func) -> List[Dict[str, Any]]:
        """
        関数のテストデータを生成
        
        Args:
            func: 対象の関数
            
        Returns:
            生成されたテストデータのリスト
        """
        test_data = []
        
        # 型ヒントを取得
        try:
            type_hints = get_type_hints(func)
        except Exception:
            type_hints = {}
        
        # 引数情報を取得
        sig = inspect.signature(func)
        parameters = sig.parameters
        
        for _ in range(self.test_data_count):
            args_data = {}
            
            for name, param in parameters.items():
                if name == 'self' or name == 'cls':
                    continue
                
                # 型ヒントがある場合
                if name in type_hints:
                    args_data[name] = self._generate_test_value(type_hints[name])
                # デフォルト値がある場合
                elif param.default != inspect.Parameter.empty:
                    args_data[name] = param.default
                # ヒントがない場合
                else:
                    args_data[name] = f"test_{name}"
            
            test_data.append(args_data)
        
        return test_data
    
    def validate_function_types(self, func) -> List[Dict[str, Any]]:
        """
        関数の型ヒントを検証
        
        Args:
            func: 対象の関数
            
        Returns:
            検出された問題のリスト
        """
        issues = []
        
        try:
            # 型ヒントを取得
            type_hints = get_type_hints(func)
            
            # 引数情報を取得
            sig = inspect.signature(func)
            parameters = sig.parameters
            
            # 各パラメータに型ヒントがあるか確認
            for name, param in parameters.items():
                if name == 'self' or name == 'cls':
                    continue
                
                if name not in type_hints:
                    issues.append({
                        'type': 'missing_type_hint',
                        'name': name,
                        'message': f"パラメータ '{name}' に型ヒントがありません"
                    })
            
            # 戻り値の型ヒントがあるか確認
            if 'return' not in type_hints:
                issues.append({
                    'type': 'missing_return_type',
                    'message': "戻り値の型ヒントがありません"
                })
            
        except Exception as e:
            issues.append({
                'type': 'type_hint_error',
                'message': f"型ヒントの検証中にエラーが発生しました: {str(e)}"
            })
        
        return issues
    
    def validate_function_behavior(self, func, instance=None) -> List[Dict[str, Any]]:
        """
        関数の動作を検証
        
        Args:
            func: 対象の関数
            instance: クラスメソッドの場合のインスタンス
            
        Returns:
            検出された問題のリスト
        """
        issues = []
        
        # テストデータを生成
        test_data_list = self.generate_test_data(func)
        
        # 型ヒントを取得
        try:
            type_hints = get_type_hints(func)
            return_type = type_hints.get('return')
        except Exception:
            type_hints = {}
            return_type = None
        
        # テストデータで関数を実行
        for i, test_data in enumerate(test_data_list):
            try:
                # 関数を呼び出し
                if instance:
                    result = func.__get__(instance)(
                        **{k: v for k, v in test_data.items() if k in inspect.signature(func).parameters}
                    )
                else:
                    result = func(
                        **{k: v for k, v in test_data.items() if k in inspect.signature(func).parameters}
                    )
                
                # 戻り値の型をチェック
                if return_type and result is not None:
                    try:
                        self._validate_type(result, return_type)
                    except ValidationError:
                        issues.append({
                            'type': 'return_type_mismatch',
                            'test_case': i + 1,
                            'expected_type': str(return_type),
                            'actual_type': type(result).__name__,
                            'message': f"テストケース {i+1}: 戻り値の型が一致しません。期待: {return_type}, 実際: {type(result).__name__}"
                        })
                
            except Exception as e:
                issues.append({
                    'type': 'function_error',
                    'test_case': i + 1,
                    'error': str(e),
                    'test_data': test_data,
                    'message': f"テストケース {i+1}: 関数の実行中にエラーが発生しました: {str(e)}"
                })
        
        return issues
    
    def _validate_type(self, value: Any, expected_type: Any) -> None:
        """
        値の型を検証
        
        Args:
            value: 検証する値
            expected_type: 期待される型
            
        Raises:
            ValidationError: 型が一致しない場合
        """
        # 単純な型チェック
        if expected_type in (str, int, float, bool):
            Validator.validate_type(value, expected_type)
        
        # リストのチェック
        elif expected_type == list or (hasattr(expected_type, "__origin__") and expected_type.__origin__ == list):
            Validator.validate_type(value, list)
            
            # 要素の型をチェック
            if hasattr(expected_type, "__args__") and expected_type.__args__ and value:
                element_type = expected_type.__args__[0]
                for item in value:
                    self._validate_type(item, element_type)
        
        # 辞書のチェック
        elif expected_type == dict or (hasattr(expected_type, "__origin__") and expected_type.__origin__ == dict):
            Validator.validate_type(value, dict)
            
            # キーと値の型をチェック
            if hasattr(expected_type, "__args__") and len(expected_type.__args__) >= 2 and value:
                key_type, value_type = expected_type.__args__[:2]
                for k, v in value.items():
                    self._validate_type(k, key_type)
                    self._validate_type(v, value_type)
        
        # その他の複合型は簡易チェック
        elif isinstance(value, expected_type):
            pass
        
        # Union, Optional, Any などは単純に通過
        elif expected_type == Any:
            pass
        
        # 複雑な型は単純に通過
        elif hasattr(expected_type, "__origin__"):
            pass
        
        # それ以外はエラー
        else:
            Validator.validate_type(value, expected_type)
    
    def get_function_signature(self, func) -> str:
        """
        関数のシグネチャを取得
        
        Args:
            func: 対象の関数
            
        Returns:
            関数のシグネチャ文字列
        """
        try:
            # 型ヒントを取得
            type_hints = get_type_hints(func)
            
            # 引数情報を取得
            sig = inspect.signature(func)
            
            # パラメータ文字列を構築
            params = []
            for name, param in sig.parameters.items():
                if name == 'self' or name == 'cls':
                    params.append(name)
                    continue
                
                # 型ヒントを追加
                type_str = str(type_hints.get(name, 'Any')).replace('typing.', '')
                
                # デフォルト値を追加
                if param.default != inspect.Parameter.empty:
                    default_str = f" = {repr(param.default)}"
                else:
                    default_str = ""
                
                params.append(f"{name}: {type_str}{default_str}")
            
            # 戻り値の型を追加
            return_type = type_hints.get('return', 'None')
            return_type_str = str(return_type).replace('typing.', '')
            
            return f"{func.__name__}({', '.join(params)}) -> {return_type_str}"
            
        except Exception:
            # エラーが発生した場合は簡易表示
            return f"{func.__name__}{str(inspect.signature(func))}"
    
    def validate_module_functions(self, module_or_path) -> Dict[str, Any]:
        """
        モジュール内のすべての関数を検証
        
        Args:
            module_or_path: モジュールまたはファイルパス
            
        Returns:
            検証結果
        """
        self.issues = []
        results = {
            'functions': [],
            'classes': [],
            'stats': {
                'function_count': 0,
                'function_with_issues': 0,
                'method_count': 0,
                'method_with_issues': 0,
                'missing_type_hints': 0,
                'runtime_errors': 0
            }
        }
        
        # モジュールを取得
        if isinstance(module_or_path, str):
            # ファイルパスからモジュールをインポート
            try:
                module_name = Path(module_or_path).stem
                spec = importlib.util.spec_from_file_location(module_name, module_or_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                results['file_path'] = module_or_path
            except Exception as e:
                self.issues.append({
                    'type': 'module_import_error',
                    'message': f"モジュールのインポート中にエラーが発生しました: {str(e)}"
                })
                return results
        else:
            # モジュールオブジェクトを直接使用
            module = module_or_path
            results['module_name'] = module.__name__
        
        # グローバル関数を検証
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            # 外部モジュールの関数は除外
            if obj.__module__ != module.__name__:
                continue
                
            results['stats']['function_count'] += 1
            
            # 関数情報
            func_info = {
                'name': name,
                'signature': self.get_function_signature(obj),
                'docstring': inspect.getdoc(obj) or "",
                'issues': []
            }
            
            # 型ヒント検証
            type_issues = self.validate_function_types(obj)
            if type_issues:
                func_info['issues'].extend(type_issues)
                results['stats']['missing_type_hints'] += len(type_issues)
            
            # 動作検証
            try:
                behavior_issues = self.validate_function_behavior(obj)
                if behavior_issues:
                    func_info['issues'].extend(behavior_issues)
                    results['stats']['runtime_errors'] += len(behavior_issues)
            except Exception as e:
                func_info['issues'].append({
                    'type': 'validator_error',
                    'message': f"関数の検証中にエラーが発生しました: {str(e)}"
                })
            
            # 問題があれば統計を更新
            if func_info['issues']:
                results['stats']['function_with_issues'] += 1
            
            # 結果に追加
            results['functions'].append(func_info)
        
        # クラスを検証
        for class_name, cls in inspect.getmembers(module, inspect.isclass):
            # 外部モジュールのクラスは除外
            if cls.__module__ != module.__name__:
                continue
            
            # クラス情報
            class_info = {
                'name': class_name,
                'docstring': inspect.getdoc(cls) or "",
                'methods': [],
                'issues': []
            }
            
            # インスタンス作成を試みる
            instance = None
            try:
                instance = cls()
            except:
                class_info['issues'].append({
                    'type': 'instance_creation_error',
                    'message': f"クラスのインスタンス作成に失敗しました"
                })
            
            # メソッドを検証
            for method_name, method in inspect.getmembers(cls, inspect.isfunction):
                # 特殊メソッドとプライベートメソッドは除外
                if method_name.startswith('__') or method_name.startswith('_'):
                    continue
                
                results['stats']['method_count'] += 1
                
                # メソッド情報
                method_info = {
                    'name': method_name,
                    'signature': self.get_function_signature(method),
                    'docstring': inspect.getdoc(method) or "",
                    'issues': []
                }
                
                # 型ヒント検証
                type_issues = self.validate_function_types(method)
                if type_issues:
                    method_info['issues'].extend(type_issues)
                    results['stats']['missing_type_hints'] += len(type_issues)
                
                # 動作検証 (インスタンスがある場合のみ)
                if instance:
                    try:
                        behavior_issues = self.validate_function_behavior(method, instance)
                        if behavior_issues:
                            method_info['issues'].extend(behavior_issues)
                            results['stats']['runtime_errors'] += len(behavior_issues)
                    except Exception as e:
                        method_info['issues'].append({
                            'type': 'validator_error',
                            'message': f"メソッドの検証中にエラーが発生しました: {str(e)}"
                        })
                
                # 問題があれば統計を更新
                if method_info['issues']:
                    results['stats']['method_with_issues'] += 1
                
                # 結果に追加
                class_info['methods'].append(method_info)
            
            # 結果に追加
            results['classes'].append(class_info)
        
        return results


def validate_functions(module_or_path, test_data_count: int = 5) -> Dict[str, Any]:
    """
    モジュール内の関数を検証するヘルパー関数
    
    Args:
        module_or_path: モジュールまたはファイルパス
        test_data_count: 生成するテストデータの数
        
    Returns:
        検証結果
    """
    validator = FunctionValidator(test_data_count=test_data_count)
    return validator.validate_module_functions(module_or_path)


# テスト用モジュール
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="関数の入出力検証ツール")
    parser.add_argument("path", help="検証するPythonファイル")
    parser.add_argument("--test-count", "-t", type=int, default=3, help="生成するテストケース数")
    parser.add_argument("--output", "-o", help="結果を保存するJSONファイル")
    
    args = parser.parse_args()
    
    # 検証実行
    validator = FunctionValidator(test_data_count=args.test_count)
    results = validator.validate_module_functions(args.path)
    
    # 結果を表示
    print(f"\n=== 関数検証結果 ===")
    print(f"関数数: {results['stats']['function_count']}")
    print(f"問題のある関数数: {results['stats']['function_with_issues']}")
    print(f"メソッド数: {results['stats']['method_count']}")
    print(f"問題のあるメソッド数: {results['stats']['method_with_issues']}")
    print(f"型ヒント不足: {results['stats']['missing_type_hints']}")
    print(f"実行時エラー: {results['stats']['runtime_errors']}")
    
    # ファイルに保存（オプション）
    if args.output:
        import json
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"検証結果を保存しました: {args.output}")