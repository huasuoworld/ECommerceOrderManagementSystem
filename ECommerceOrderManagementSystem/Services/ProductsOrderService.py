from ..DBConnects.SQLiteDB import getDB
from ..DBConnects.ProductsOrderDB import ProductsOrderDB
from ..DBConnects.ProductsShoppingCartDB import ProductsShoppingCartDB
from ..DBConnects.ProductsOrderItemsDB import ProductsOrderItemsDB
from ..DBConnects.ProductsInventoryDB import ProductsInventoryDB
from ..Models.ProductsOrderModel import ProductsOrderModel
from ..Models.ProductsOrderItemsModel import ProductsOrderItemsModel
from ..CommonUtils.ConstantUtil import PaymentStatusUnpaid, OrderStatusUnpaid, getOrderNumber, DBExcludeColumnsWithoutId, getCurrentTime

class ProductsOrderService:
    def __init__(self):
        self.productsOrderDB = ProductsOrderDB()
        self.productsOrderItemsDB = ProductsOrderItemsDB()
        self.productsShoppingCartDB = ProductsShoppingCartDB()
        self.productsInventoryDB = ProductsInventoryDB()

    def confirmOrderByUserShoppingCart(self, userId: int):
        with getDB() as db:
            #1. get products from shopping cart
            cartItems = self.productsShoppingCartDB.queryProductsShoppingCartByUserIdWithSession(userId, db)
            if not cartItems:
                raise ValueError("Your shopping cart is empty.")

            orderNumber = str(getOrderNumber())

            #2.1 Build productsOrderModel
            orderModel = ProductsOrderModel(
                users_id = userId,
                order_number = orderNumber,
                # order_amount = sum(orderAmountList),
                # order_discount_price = sum(orderDiscountPriceList),
                # order_product_price = sum(orderProductPriceList),
                order_freight_price = 0,
                order_status = OrderStatusUnpaid,
                payment_status = PaymentStatusUnpaid
            )
            #2.1 save productsOrder info, and get productsOrderId
            order = self.productsOrderDB.createProductsOrder(db, orderModel)

            #3. collect the product ids; calculate the product price,discount price and amount
            #3. Build productsOrderItemsModel and lock inventory stock
            productsIDs = []
            orderProductPriceList = []
            orderDiscountPriceList = []
            orderAmountList = []
            orderItems = []
            for item in cartItems:
                #3.1 collect the product ids
                productsIDs.append(item.product_id)
                #3.2 calculate the product price
                orderProductPriceList.append(item.product_price * item.products_quantity)
                #3.3 calculate the discount price
                orderDiscountPriceList.append(item.discount_price * item.products_quantity)
                #3.4 calculate the amount
                orderAmountList.append(max(0, item.product_price - item.discount_price) * item.products_quantity)
                currentTime = getCurrentTime()
                #3.5 Build productsOrderItemsModel
                productsOrderItemsModel = ProductsOrderItemsModel(
                    products_order_id = order.id,
                    users_id = userId,
                    products_id = item.product_id,
                    products_discount_id = item.products_discount_id,
                    products_inventory_id = item.products_inventory_id,
                    product_name = item.product_name,
                    product_code = item.product_code,
                    item_quantity = item.products_quantity,
                    item_ordder_number = orderNumber,
                    item_product_price = item.product_price,
                    item_discount_price = item.discount_price,
                    item_unit_price = max(0, item.product_price - item.discount_price),
                    created_at = currentTime,
                    updated_at = currentTime)
                orderItems.append(productsOrderItemsModel)
                #3.6 lock inventory stock
                self.productsInventoryDB.lockStockWithSession(db, item.product_id, item.products_quantity)
            #4. after calculate the price then update the order's amount,discount_price and product_price
            order.order_amount = sum(orderAmountList),
            order.order_discount_price = sum(orderDiscountPriceList),
            order.order_product_price = sum(orderProductPriceList),
            #5. save productsOrderItems
            productsOrderItems = self.productsOrderItemsDB.createProductsOrderItems(db, orderItems)
            #6. delete ProductsShoppingCart from db
            self.productsShoppingCartDB.delProductsShoppingCartByUserIdWithSession(db, userId)
            db.commit()
            db.refresh(order)
            return order

    def getOrderByUserId(self, userId: int):
        return self.productsOrderDB.getOrderByUserId(userId)