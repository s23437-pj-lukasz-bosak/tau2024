
class NotificationService:
    def notify(self, order_id, message):
        print(f"Notification for order {order_id}: {message}")


# class OrderService:
#     def __init__(self, payment_service, inventory_service, notification_service):
#         self.payment_service = payment_service
#         self.inventory_service = inventory_service
#         self.notification_service = notification_service
#
#     def place_order(self, order_id, product_id, quantity, payment_details):
#         print(f"Placing order {order_id} for product {product_id}, quantity {quantity}")
#         if not self.inventory_service.check_availability(product_id, quantity):
#             print("Product not available in requested quantity.")
#             self.notification_service.notify(order_id, "Order failed: Product not available.")
#             return False
#
#         if not self.payment_service.process_payment(order_id, payment_details):
#             print("Payment failed.")
#             self.notification_service.notify(order_id, "Order failed: Payment issue.")
#             return False
#
#         self.inventory_service.reserve_product(product_id, quantity)
#         self.notification_service.notify(order_id, "Order placed successfully.")
#         print(f"Order {order_id} placed successfully.")
#         return True
#
class OrderService:
    def __init__(self, payment_service, inventory_service, notification_service):
        self.payment_service = payment_service
        self.inventory_service = inventory_service
        self.notification_service = notification_service

    def place_order(self, order_id, product_id, quantity, payment_details):
        print(f"Placing order {order_id} for product {product_id}, quantity {quantity}")
        if not self.inventory_service.check_availability(product_id, quantity):
            print("Product not available in requested quantity.")
            self.notification_service.notify(order_id, "Order failed: Product not available.")
            return False

        try:
            if not self.payment_service.process_payment(order_id, payment_details):
                print("Payment failed.")
                self.notification_service.notify(order_id, "Order failed: Payment issue.")
                return False
        except Exception as e:
            print(f"Payment error: {e}")
            self.notification_service.notify(order_id, "Order failed: Payment issue.")
            return False

        self.inventory_service.reserve_product(product_id, quantity)
        self.notification_service.notify(order_id, "Order placed successfully.")
        print(f"Order {order_id} placed successfully.")
        return True
class InventoryService:
    def __init__(self):
        self.stock = {}

    def add_stock(self, product_id, quantity):
        self.stock[product_id] = self.stock.get(product_id, 0) + quantity
        print(f"Added {quantity} of product {product_id} to inventory.")

    def check_availability(self, product_id, quantity):
        available = self.stock.get(product_id, 0) >= quantity
        print(f"Checking availability for product {product_id}: {'Available' if available else 'Not available'}.")
        return available

    def reserve_product(self, product_id, quantity):
        if self.check_availability(product_id, quantity):
            self.stock[product_id] -= quantity
            print(f"Reserved {quantity} of product {product_id}.")


class PaymentService:
    def process_payment(self, order_id, payment_details):
        print(f"Processing payment for order {order_id}")
        if payment_details.get("valid", False):
            print("Payment successful.")
            return True
        else:
            print("Payment failed.")
            return False


if __name__ == "__main__":
    # 1. Utwórz instancje usług
    payment_service = PaymentService()
    inventory_service = InventoryService()
    notification_service = NotificationService()

    # 2. Utwórz instancję OrderService z zależnościami
    order_service = OrderService(payment_service, inventory_service, notification_service)

    # 3. Skonfiguruj magazyn
    inventory_service.add_stock("P001", 10)  # Dodaj 10 sztuk produktu P001
    inventory_service.add_stock("P002", 5)   # Dodaj 5 sztuk produktu P002

    # 4. Złóż zamówienia
    print("\n--- Zamówienie 1 ---")
    order_service.place_order("O001", "P001", 3, {"valid": True})

    print("\n--- Zamówienie 2 ---")
    order_service.place_order("O002", "P002", 6, {"valid": True})  # Próba przekroczenia stanu magazynowego

    print("\n--- Zamówienie 3 ---")
    order_service.place_order("O003", "P001", 2, {"valid": False})  # Nieprawidłowe dane płatności
