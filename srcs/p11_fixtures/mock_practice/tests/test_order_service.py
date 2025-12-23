"""
注文サービスのテスト
複数の外部依存（決済API、在庫管理、メール送信）をモック化してテストします。
"""

import pytest
from unittest.mock import Mock
from services.order_service import (
    OrderService,
    PaymentGateway,
    InventoryService,
    EmailService
)


@pytest.fixture
def mock_payment_gateway():
    """決済ゲートウェイのモックフィクスチャ"""
    return Mock(spec=PaymentGateway)


@pytest.fixture
def mock_inventory_service():
    """在庫管理サービスのモックフィクスチャ"""
    return Mock(spec=InventoryService)


@pytest.fixture
def mock_email_service():
    """メール送信サービスのモックフィクスチャ"""
    return Mock(spec=EmailService)


@pytest.fixture
def order_service(mock_payment_gateway, mock_inventory_service, mock_email_service):
    """注文サービスのフィクスチャ"""
    return OrderService(
        payment_gateway=mock_payment_gateway,
        inventory_service=mock_inventory_service,
        email_service=mock_email_service
    )


def test_create_order_success(
    order_service,
    mock_payment_gateway,
    mock_inventory_service,
    mock_email_service
):
    """注文作成が成功する場合のテスト"""
    # 各サービスのモックを設定
    mock_inventory_service.check_stock.return_value = True
    mock_payment_gateway.process_payment.return_value = {
        "success": True,
        "transaction_id": "txn_12345"
    }
    mock_email_service.send_email.return_value = True
    
    # テスト実行
    result = order_service.create_order(
        product_id="PROD001",
        quantity=2,
        amount=100.0,
        card_number="1234-5678-9012-3456",
        customer_email="customer@example.com"
    )
    
    # 結果を検証
    assert result["order_id"] == "ORD_txn_12345"
    assert result["product_id"] == "PROD001"
    assert result["quantity"] == 2
    assert result["amount"] == 100.0
    assert result["transaction_id"] == "txn_12345"
    assert result["email_sent"] is True
    
    # 各サービスが正しく呼ばれたことを確認
    mock_inventory_service.check_stock.assert_called_once_with("PROD001", 2)
    mock_payment_gateway.process_payment.assert_called_once_with(
        100.0, "1234-5678-9012-3456"
    )
    mock_inventory_service.reduce_stock.assert_called_once_with("PROD001", 2)
    mock_email_service.send_email.assert_called_once()
    
    # メール送信の引数を確認
    email_call_args = mock_email_service.send_email.call_args
    assert email_call_args[1]["to"] == "customer@example.com"
    assert email_call_args[1]["subject"] == "Order Confirmation"


def test_create_order_insufficient_stock(
    order_service,
    mock_inventory_service
):
    """在庫不足の場合のテスト"""
    # 在庫が不足している
    mock_inventory_service.check_stock.return_value = False
    
    # エラーが発生することを確認
    with pytest.raises(ValueError, match="Insufficient stock"):
        order_service.create_order(
            product_id="PROD001",
            quantity=100,  # 在庫不足
            amount=100.0,
            card_number="1234-5678-9012-3456",
            customer_email="customer@example.com"
        )
    
    # 決済や在庫減少は呼ばれないことを確認
    mock_inventory_service.reduce_stock.assert_not_called()


def test_create_order_payment_failed(
    order_service,
    mock_payment_gateway,
    mock_inventory_service
):
    """決済が失敗した場合のテスト"""
    # 在庫は十分
    mock_inventory_service.check_stock.return_value = True
    # 決済が失敗
    mock_payment_gateway.process_payment.return_value = {
        "success": False,
        "transaction_id": None
    }
    
    # エラーが発生することを確認
    with pytest.raises(ValueError, match="Payment failed"):
        order_service.create_order(
            product_id="PROD001",
            quantity=2,
            amount=100.0,
            card_number="invalid_card",
            customer_email="customer@example.com"
        )
    
    # 在庫減少は呼ばれないことを確認（決済失敗のため）
    mock_inventory_service.reduce_stock.assert_not_called()


def test_create_order_email_failed(
    order_service,
    mock_payment_gateway,
    mock_inventory_service,
    mock_email_service
):
    """メール送信が失敗した場合のテスト"""
    # 各サービスのモックを設定
    mock_inventory_service.check_stock.return_value = True
    mock_payment_gateway.process_payment.return_value = {
        "success": True,
        "transaction_id": "txn_12345"
    }
    mock_email_service.send_email.return_value = False  # メール送信失敗
    
    # テスト実行（注文は成功するが、メール送信は失敗）
    result = order_service.create_order(
        product_id="PROD001",
        quantity=2,
        amount=100.0,
        card_number="1234-5678-9012-3456",
        customer_email="customer@example.com"
    )
    
    # 注文は成功しているが、メール送信は失敗
    assert result["order_id"] == "ORD_txn_12345"
    assert result["email_sent"] is False
    
    # メール送信が呼ばれたことを確認
    mock_email_service.send_email.assert_called_once()

