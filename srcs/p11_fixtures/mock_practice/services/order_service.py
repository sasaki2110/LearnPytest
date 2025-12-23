"""
注文処理サービス
複数の外部依存（決済API、在庫管理、メール送信）を使用します。
"""


class PaymentGateway:
    """決済ゲートウェイ（外部サービス）"""
    
    def process_payment(self, amount: float, card_number: str) -> dict:
        """
        決済を処理
        
        Args:
            amount: 金額
            card_number: カード番号
            
        Returns:
            決済結果
            {
                "success": True,
                "transaction_id": "txn_12345"
            }
        """
        # 実際の実装では、外部の決済APIを呼び出す
        pass


class InventoryService:
    """在庫管理サービス（外部サービス）"""
    
    def check_stock(self, product_id: str, quantity: int) -> bool:
        """
        在庫を確認
        
        Args:
            product_id: 商品ID
            quantity: 数量
            
        Returns:
            在庫が十分な場合はTrue
        """
        # 実際の実装では、在庫管理システムに問い合わせ
        pass
    
    def reduce_stock(self, product_id: str, quantity: int) -> None:
        """
        在庫を減らす
        
        Args:
            product_id: 商品ID
            quantity: 減らす数量
        """
        # 実際の実装では、在庫管理システムで在庫を更新
        pass


class EmailService:
    """メール送信サービス（外部サービス）"""
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        メールを送信
        
        Args:
            to: 送信先メールアドレス
            subject: 件名
            body: 本文
            
        Returns:
            送信成功した場合はTrue
        """
        # 実際の実装では、メール送信サービスを呼び出す
        pass


class OrderService:
    """注文処理サービスクラス"""
    
    def __init__(
        self,
        payment_gateway: PaymentGateway,
        inventory_service: InventoryService,
        email_service: EmailService
    ):
        """
        初期化
        
        Args:
            payment_gateway: 決済ゲートウェイ
            inventory_service: 在庫管理サービス
            email_service: メール送信サービス
        """
        self.payment = payment_gateway
        self.inventory = inventory_service
        self.email = email_service
    
    def create_order(
        self,
        product_id: str,
        quantity: int,
        amount: float,
        card_number: str,
        customer_email: str
    ) -> dict:
        """
        注文を作成
        
        Args:
            product_id: 商品ID
            quantity: 数量
            amount: 金額
            card_number: カード番号
            customer_email: 顧客のメールアドレス
            
        Returns:
            注文情報
        """
        # 1. 在庫を確認
        if not self.inventory.check_stock(product_id, quantity):
            raise ValueError("Insufficient stock")
        
        # 2. 決済を処理
        payment_result = self.payment.process_payment(amount, card_number)
        
        if not payment_result.get("success"):
            raise ValueError("Payment failed")
        
        # 3. 在庫を減らす
        self.inventory.reduce_stock(product_id, quantity)
        
        # 4. 確認メールを送信
        email_sent = self.email.send_email(
            to=customer_email,
            subject="Order Confirmation",
            body=f"Your order for {quantity} x {product_id} has been confirmed."
        )
        
        return {
            "order_id": f"ORD_{payment_result['transaction_id']}",
            "product_id": product_id,
            "quantity": quantity,
            "amount": amount,
            "transaction_id": payment_result["transaction_id"],
            "email_sent": email_sent
        }

