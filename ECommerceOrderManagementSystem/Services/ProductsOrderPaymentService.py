from ..DBConnects.ProductsOrderDB import ProductsOrderDB
from ..DBConnects.ProductsInventoryDB import ProductsInventoryDB
from ..DBConnects.ProductsOrderItemsDB import ProductsOrderItemsDB
from ..DBConnects.ProductsOrderPaymentDB import ProductsOrderPaymentDB
from ..DBConnects.SQLiteDB import getDB
from ..CommonUtils.ConstantUtil import getCurrentTime, getPaymentNumber, PaymentStatusPaid, OrderStatusPaid
from ..CommonUtils.LoggingUtil import logger
from ..Models.ProductsOrderPaymentModel import ProductsOrderPaymentModel
from ..Services.NotificationMessagesService import NotificationMessagesService

class ProductsOrderPaymentService:
    def __init__(self):
        self.productsOrderDB = ProductsOrderDB()
        self.productsInventoryDB = ProductsInventoryDB()
        self.productsOrderItemsDB = ProductsOrderItemsDB()
        self.productsOrderPaymentDB = ProductsOrderPaymentDB()
        self.notificationMessagesService = NotificationMessagesService()

    #get a product by its ID
    def orderPayment(self, orderId: int, userId: int):
        with getDB() as db:
            #1. get order information
            order = self.productsOrderDB.getOrderByIdAndUserIdWithSession(db, orderId, userId)
            #2. get order item information
            orderItems = self.productsOrderItemsDB.getProductsOrderItemsWithSession(db, order.id, userId)
            currentTime = getCurrentTime()
            paymentNumber = getPaymentNumber()
            for orderItem in orderItems:
                #3. update inventory
                self.productsInventoryDB.releaseReservedStockWithSession(db, orderItem.products_id, orderItem.item_quantity)
                #4. update products_order_items updated_at
                orderItem.updated_at = currentTime

            #5. create order payment
            productsOrderPaymentModel = ProductsOrderPaymentModel(
                products_order_id = order.id,
                users_id = order.users_id,
                payment_number = paymentNumber,
                payment_channel = "CIBC",
                payment_type = "ONLINE",
                payment_amount = order.order_amount,
                payment_order_number = order.order_number,
                payment_status = PaymentStatusPaid,
                created_at = currentTime,
                updated_at = currentTime)
            self.productsOrderPaymentDB.createProductsOrderPaymentWithSession(db, productsOrderPaymentModel)
            #6. update order status
            order.order_status = OrderStatusPaid
            order.payment_status = PaymentStatusPaid
            order.updated_at = currentTime
            try:
                #add a notification message for order payment
                self.notificationMessagesService.addNotificationMessagesWithSession(db,f"Order {order.order_number} has been paid successfully.")
            except Exception as e:
                logger.error(f"Failed to add notification message for order payment: {e}")
            #7. commit data
            db.commit()
           