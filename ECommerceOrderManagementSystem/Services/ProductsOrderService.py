from ..DBConnects.SQLiteDB import getDB
from ..DBConnects.ProductsOrderDB import ProductsOrderDB
from ..DBConnects.ProductsShoppingCartDB import ProductsShoppingCartDB
from ..DBConnects.ProductsOrderItemsDB import ProductsOrderItemsDB
from ..Models.ProductsOrderModel import ProductsOrderModel
from ..Models.ProductsOrderItemsModel import ProductsOrderItemsModel
from ..CommonUtils.ConstantUtil import PaymentStatusUnpaid, OrderStatusUnpaid, getOrderNumber

productsOrderDB = ProductsOrderDB()
productsOrderItemsDB = ProductsOrderItemsDB()
productsShoppingCartDB = ProductsShoppingCartDB()

class ProductsOrderService:

    def confirmOrderByUserShoppingCart(self, userId: int):
        with getDB() as db:
            #1. get products from shopping cart
            cartItems = productsShoppingCartDB.queryProductsShoppingCartByUserIdWithSession(userId, db)
            if not cartItems:
                raise ValueError("Your shopping cart is empty.")

            orderNumber = str(getOrderNumber())
            orderProductPrice = sum(
                item.product_price * item.products_quantity for item in cartItems
            )
            orderDiscountPrice = sum(
                item.discount_price * item.products_quantity for item in cartItems
            )
            orderAmount = sum(
                max(0, item.product_price - item.discount_price) * item.products_quantity
                for item in cartItems
            )
            #2. Build productsOrderModel
            orderModel = ProductsOrderModel(
                users_id=userId,
                order_number=orderNumber,
                order_amount=orderAmount,
                order_discount_price=orderDiscountPrice,
                order_product_price=orderProductPrice,
                order_freight_price=0,
                order_status=OrderStatusUnpaid,
                payment_status=PaymentStatusUnpaid
            )
            #3. save productsOrder info, and get productsOrderId
            order = productsOrderDB.createProductsOrder(db, orderModel)
            #4. Build productsOrderItemsModel
            orderItems = [
                ProductsOrderItemsModel(
                    products_order_id=order.id,
                    users_id=userId,
                    products_id=item.product_id,
                    products_discount_id=item.products_discount_id,
                    products_inventory_id=item.products_inventory_id,
                    product_name=item.product_name,
                    product_code=item.product_code,
                    item_quantity=item.products_quantity,
                    item_ordder_number=orderNumber,
                    item_product_price=item.product_price,
                    item_discount_price=item.discount_price,
                    item_unit_price=max(0, item.product_price - item.discount_price)
                )
                for item in cartItems
            ]
            #5. save productsOrderItems
            productsOrderItemsDB.createProductsOrderItems(db, orderItems)
            #5. delete ProductsShoppingCart from db
            productsShoppingCartDB.delProductsShoppingCartByUserIdWithSession(db, userId)
            db.commit()
            db.refresh(order)
            return order

    def getOrderByUserId(self, userId: int):
        return productsOrderDB.getOrderByUserId(userId)