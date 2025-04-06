import unittest
import os
import tempfile
import json
import yaml
from pathlib import Path
from datetime import datetime, date

from snippet.utils.logger.config_manage import ConfigManager
from snippet.utils.input_sanitizer import InputSanitizer
from snippet.utils.env_loader import EnvLoader
from validator import Validator, ValidationError
from test_data_generator import TestDataGenerator, Factory
from scripts.code_complexity_checker import CodeComplexityChecker
from snippet.utils.exception_handler import exception_handler
from logger.contextual_logger import ContextualLogger, get_logger


class TestInputSanitizer(unittest.TestCase):
    def setUp(self):
        self.sanitizer = InputSanitizer()

    def test_sanitize_html(self):
        html = "<script>alert('XSS');</script>"
        sanitized = self.sanitizer.sanitize_html(html)
        self.assertEqual(sanitized, "&lt;script&gt;alert('XSS');&lt;/script&gt;")

    def test_strip_tags(self):
        html = "<p>Hello <b>World</b>!</p>"
        stripped = self.sanitizer.strip_tags(html)
        self.assertEqual(stripped, "Hello World!")

    def test_sanitize_sql(self):
        sql = "1; DROP TABLE users; --"
        sanitized = self.sanitizer.sanitize_sql(sql)
        self.assertNotIn(";", sanitized)
        self.assertNotIn("DROP", sanitized)

    def test_sanitize_filename(self):
        filename = "../../../etc/passwd"
        sanitized = self.sanitizer.sanitize_filename(filename)
        self.assertNotIn("/", sanitized)
        self.assertNotIn("..", sanitized)

    def test_sanitize_email(self):
        valid_email = "test@example.com"
        invalid_email = "not-an-email"
        self.assertEqual(self.sanitizer.sanitize_email(valid_email), valid_email)
        self.assertEqual(self.sanitizer.sanitize_email(invalid_email), "")


class TestEnvLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.env_loader = EnvLoader(base_dir=self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_env_file(self):
        # テスト用の.envファイルを作成
        env_content = """
DB_HOST=localhost
DB_PORT=5432
DB_USER=test
DB_PASSWORD=password
"""
        with open(os.path.join(self.temp_dir, '.env'), 'w') as f:
            f.write(env_content)

        # 環境変数をロード
        loaded_vars = self.env_loader.load()

        # 検証
        self.assertEqual(loaded_vars['DB_HOST'], 'localhost')
        self.assertEqual(loaded_vars['DB_PORT'], '5432')
        self.assertEqual(loaded_vars['DB_USER'], 'test')
        self.assertEqual(loaded_vars['DB_PASSWORD'], 'password')


class TestValidator(unittest.TestCase):
    def test_validate_type(self):
        Validator.validate_type("test", str)
        Validator.validate_type(123, int)
        with self.assertRaises(ValidationError):
            Validator.validate_type("test", int)

    def test_validate_length(self):
        Validator.validate_length("test", min_length=2, max_length=10)
        with self.assertRaises(ValidationError):
            Validator.validate_length("test", min_length=5)
        with self.assertRaises(ValidationError):
            Validator.validate_length("test", max_length=3)

    def test_validate_range(self):
        Validator.validate_range(5, min_value=0, max_value=10)
        with self.assertRaises(ValidationError):
            Validator.validate_range(5, max_value=4)
        with self.assertRaises(ValidationError):
            Validator.validate_range(5, min_value=6)

    def test_validate_email(self):
        Validator.validate_email("test@example.com")
        with self.assertRaises(ValidationError):
            Validator.validate_email("not-an-email")


class TestDataGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.generator = TestDataGenerator()

    def test_random_string(self):
        string1 = self.generator.random_string()
        string2 = self.generator.random_string()
        self.assertNotEqual(string1, string2)
        self.assertEqual(len(string1), 10)  # デフォルトの長さ

    def test_random_email(self):
        email = self.generator.random_email()
        self.assertIn("@", email)
        self.assertTrue(email.endswith(('.com', '.org', '.net', '.io')))

    def test_random_date(self):
        date_obj = self.generator.random_date()
        self.assertIsInstance(date_obj, date)

    def test_random_phone(self):
        phone = self.generator.random_phone()
        self.assertTrue(phone.startswith('0'))
        self.assertEqual(len(phone.split('-')), 3)


class TestCodeComplexityChecker(unittest.TestCase):
    def setUp(self):
        self.checker = CodeComplexityChecker(max_lines=10, max_nest_level=2)

    def test_simple_code(self):
        code = """
def simple_function():
    return "Hello"
"""
        self.assertTrue(self.checker.check_code(code))
        self.assertEqual(len(self.checker.issues), 0)

    def test_complex_code(self):
        code = """
def complex_function():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                print(i, j, k)
"""
        self.assertFalse(self.checker.check_code(code))
        self.assertTrue(any(issue['issue'] == 'too_nested' for issue in self.checker.issues))


class TestExceptionHandler(unittest.TestCase):
    def test_exception_handling(self):
        @exception_handler(reraise=False, default_return=0)
        def divide(a, b):
            return a / b

        result = divide(10, 0)
        self.assertEqual(result, 0)  # デフォルト値が返される

    def test_exception_reraising(self):
        @exception_handler(reraise=True)
        def divide(a, b):
            return a / b

        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)


class TestContextualLogger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.logger = ContextualLogger(name="test", log_dir=self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_logging_levels(self):
        self.logger.info("Test info message")
        self.logger.warning("Test warning message")
        self.logger.error("Test error message")
        
        # ログファイルが作成されていることを確認
        app_log_dir = os.path.join(self.temp_dir, 'application')
        error_log_dir = os.path.join(self.temp_dir, 'error')
        self.assertTrue(os.path.exists(app_log_dir))
        self.assertTrue(os.path.exists(error_log_dir))


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir)
        
        # テスト用の設定ファイルを作成
        self.base_config = {
            'app': {
                'name': 'TestApp',
                'version': '1.0.0'
            },
            'database': {
                'host': 'localhost',
                'port': 5432
            }
        }
        
        self.dev_config = {
            'app': {
                'debug': True
            },
            'database': {
                'port': 5433
            }
        }
        
        # base.yaml を作成
        with open(self.config_dir / 'base.yaml', 'w') as f:
            yaml.dump(self.base_config, f)
            
        # development.yaml を作成
        with open(self.config_dir / 'development.yaml', 'w') as f:
            yaml.dump(self.dev_config, f)
            
        self.config_manager = ConfigManager(config_dir=self.config_dir, env='development')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_config(self):
        config = self.config_manager.load()
        
        # ベース設定が読み込まれていることを確認
        self.assertEqual(config['app']['name'], 'TestApp')
        self.assertEqual(config['app']['version'], '1.0.0')
        
        # 環境固有の設定で上書きされていることを確認
        self.assertEqual(config['database']['port'], 5433)
        self.assertTrue(config['app']['debug'])

    def test_get_config_value(self):
        self.config_manager.load()
        
        # ドット記法でのアクセス
        self.assertEqual(self.config_manager.get('app.name'), 'TestApp')
        self.assertEqual(self.config_manager.get('database.port'), 5433)
        
        # 存在しないキー
        self.assertIsNone(self.config_manager.get('nonexistent.key'))
        self.assertEqual(self.config_manager.get('nonexistent.key', 'default'), 'default')

    def test_set_config_value(self):
        self.config_manager.load()
        
        # 値を設定
        self.config_manager.set('app.new_setting', 'test_value')
        self.assertEqual(self.config_manager.get('app.new_setting'), 'test_value')
        
        # ネストされた値を設定
        self.config_manager.set('database.credentials.username', 'admin')
        self.assertEqual(self.config_manager.get('database.credentials.username'), 'admin')


class TestSaveFileStructure(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        # テスト用のファイル構造を作成
        os.makedirs('src/components', exist_ok=True)
        os.makedirs('docs', exist_ok=True)
        os.makedirs('tests', exist_ok=True)
        
        # テストファイルを作成
        with open('src/components/app.py', 'w') as f:
            f.write('# Test file')
        with open('docs/readme.md', 'w') as f:
            f.write('# Documentation')
        with open('tests/test_app.py', 'w') as f:
            f.write('# Test cases')
            
        # .gitignoreファイルを作成
        with open('.gitignore', 'w') as f:
            f.write('*.pyc\n__pycache__\n')

    def tearDown(self):
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_format_file_structure(self):
        from save_file_structure import format_file_structure
        
        files = [
            'src/components/app.py',
            'docs/readme.md',
            'tests/test_app.py'
        ]
        
        structure = format_file_structure(files)
        
        # 基本的な構造の確認
        self.assertIn('📁 src/', structure)
        self.assertIn('📁 components/', structure)
        self.assertIn('📁 docs/', structure)
        self.assertIn('📁 tests/', structure)
        
        # ファイルの確認
        self.assertIn('🔧 app.py', structure)
        self.assertIn('📝 readme.md', structure)
        self.assertIn('🔧 test_app.py', structure)

    def test_save_file_structure(self):
        from save_file_structure import save_file_structure
        
        # ファイル構造を保存
        save_file_structure()
        
        # 出力ファイルの確認
        output_file = Path('docs/file_structure.md')
        self.assertTrue(output_file.exists())
        
        # ファイルの内容を確認
        content = output_file.read_text()
        self.assertIn('File Structure Generated at:', content)
        self.assertIn('📁 src/', content)
        self.assertIn('Legend:', content)


if __name__ == '__main__':
    unittest.main() 