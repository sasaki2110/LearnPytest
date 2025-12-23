"""
ファイル操作サービス
ファイルの読み書きを行います。
"""

from pathlib import Path


class FileService:
    """ファイル操作サービスクラス"""
    
    def read_file(self, file_path: str) -> str:
        """
        ファイルを読み込む
        
        Args:
            file_path: ファイルパス
            
        Returns:
            ファイルの内容
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return path.read_text(encoding="utf-8")
    
    def write_file(self, file_path: str, content: str) -> None:
        """
        ファイルに書き込む
        
        Args:
            file_path: ファイルパス
            content: 書き込む内容
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    
    def append_file(self, file_path: str, content: str) -> None:
        """
        ファイルに追記する
        
        Args:
            file_path: ファイルパス
            content: 追記する内容
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        current_content = path.read_text(encoding="utf-8")
        path.write_text(current_content + content, encoding="utf-8")
    
    def file_exists(self, file_path: str) -> bool:
        """
        ファイルが存在するか確認
        
        Args:
            file_path: ファイルパス
            
        Returns:
            存在する場合はTrue
        """
        return Path(file_path).exists()

