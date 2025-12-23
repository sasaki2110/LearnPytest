"""
ユーザー管理サービス
データベースにユーザー情報を保存・取得します。
"""


class Database:
    """データベース操作を模擬するクラス"""
    
    def connect(self):
        """データベースに接続"""
        # 実際の実装では、データベース接続処理
        pass
    
    def execute_query(self, query: str, params: dict = None):
        """
        クエリを実行
        
        Args:
            query: SQLクエリ
            params: パラメータ
            
        Returns:
            クエリ結果
        """
        # 実際の実装では、データベースクエリ実行
        pass
    
    def insert(self, table: str, data: dict) -> int:
        """
        データを挿入
        
        Args:
            table: テーブル名
            data: 挿入するデータ
            
        Returns:
            挿入されたレコードのID
        """
        # 実際の実装では、INSERT文を実行
        pass
    
    def select(self, table: str, conditions: dict = None) -> list:
        """
        データを取得
        
        Args:
            table: テーブル名
            conditions: 検索条件
            
        Returns:
            取得したレコードのリスト
        """
        # 実際の実装では、SELECT文を実行
        pass


class UserService:
    """ユーザー管理サービスクラス"""
    
    def __init__(self, database: Database):
        """
        初期化
        
        Args:
            database: データベースインスタンス
        """
        self.db = database
        self.db.connect()
    
    def create_user(self, name: str, email: str) -> dict:
        """
        ユーザーを作成
        
        Args:
            name: ユーザー名
            email: メールアドレス
            
        Returns:
            作成されたユーザー情報
        """
        user_data = {
            "name": name,
            "email": email
        }
        
        user_id = self.db.insert("users", user_data)
        
        return {
            "id": user_id,
            "name": name,
            "email": email
        }
    
    def get_user(self, user_id: int) -> dict:
        """
        ユーザー情報を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            ユーザー情報
        """
        results = self.db.select("users", {"id": user_id})
        
        if not results:
            raise ValueError(f"User with id {user_id} not found")
        
        return results[0]
    
    def get_user_by_email(self, email: str) -> dict:
        """
        メールアドレスでユーザーを検索
        
        Args:
            email: メールアドレス
            
        Returns:
            ユーザー情報（見つからない場合はNone）
        """
        results = self.db.select("users", {"email": email})
        
        if not results:
            return None
        
        return results[0]

