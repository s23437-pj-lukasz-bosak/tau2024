import unittest
from unittest.mock import Mock, patch, call
from main import OrderService, PaymentService, InventoryService, NotificationService

class TestOrderService(unittest.TestCase):

    def setUp(self):
        # Tworzymy mocki dla zależności
        self.payment_service = Mock(spec=PaymentService)
        self.inventory_service = Mock(spec=InventoryService)
        self.notification_service = Mock(spec=NotificationService)

        # Tworzymy testowaną instancję OrderService z mockami
        self.order_service = OrderService(
            self.payment_service,
            self.inventory_service,
            self.notification_service
        )

    def test_order_placed_successfully(self):
        # Arrange
        order_id = "O001"
        product_id = "P001"
        quantity = 3
        payment_details = {"valid": True}

        # Konfiguracja mocków
        self.inventory_service.check_availability.return_value = True
        self.payment_service.process_payment.return_value = True


        result = self.order_service.place_order(order_id, product_id, quantity, payment_details)

        # Assert
        self.assertTrue(result)
        self.inventory_service.check_availability.assert_called_once_with(product_id, quantity)
        self.payment_service.process_payment.assert_called_once_with(order_id, payment_details)
        self.notification_service.notify.assert_called_once_with(order_id, "Order placed successfully.")

    def test_order_fails_when_product_not_available(self):

        order_id = "O002"
        product_id = "P002"
        quantity = 6
        payment_details = {"valid": True}

        # Konfiguracja mocków
        self.inventory_service.check_availability.return_value = False


        result = self.order_service.place_order(order_id, product_id, quantity, payment_details)

        # Assert
        self.assertFalse(result)
        self.inventory_service.check_availability.assert_called_once_with(product_id, quantity)
        self.notification_service.notify.assert_called_once_with(order_id, "Order failed: Product not available.")
        self.payment_service.process_payment.assert_not_called()

    def test_order_fails_when_payment_fails(self):

        order_id = "O003"
        product_id = "P003"
        quantity = 2
        payment_details = {"valid": False}

        # Konfiguracja mocków
        self.inventory_service.check_availability.return_value = True
        self.payment_service.process_payment.return_value = False

        # Act
        result = self.order_service.place_order(order_id, product_id, quantity, payment_details)

        # Assert
        self.assertFalse(result)
        self.inventory_service.check_availability.assert_called_once_with(product_id, quantity)
        self.payment_service.process_payment.assert_called_once_with(order_id, payment_details)
        self.notification_service.notify.assert_called_once_with(order_id, "Order failed: Payment issue.")

    def test_order_handles_payment_service_exception(self):

        order_id = "O004"
        product_id = "P004"
        quantity = 1
        payment_details = {"valid": True}

        # Konfiguracja mocków
        self.inventory_service.check_availability.return_value = True
        self.payment_service.process_payment.side_effect = Exception("Payment service error")


        result = self.order_service.place_order(order_id, product_id, quantity, payment_details)

        # Assert
        self.assertFalse(result)
        self.inventory_service.check_availability.assert_called_once_with(product_id, quantity)
        self.payment_service.process_payment.assert_called_once_with(order_id, payment_details)
        self.notification_service.notify.assert_called_once_with(order_id, "Order failed: Payment issue.")

if __name__ == '__main__':
    unittest.main()