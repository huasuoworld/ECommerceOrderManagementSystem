from ..DBConnects.ProductsDB import ProductsDB
from ..DBConnects.ProductsDiscountDB import ProductsDiscountDB
from ..DBConnects.ProductsInventoryDB import ProductsInventoryDB
from ..DBConnects.ProductsShoppingCartDB import ProductsShoppingCartDB
from ..Models.FrontEndReponseModel import PageDataReponseModel
from ..Models.ProductsShoppingCartModel import ProductsShoppingCartModel

productsShoppingCartDB = ProductsShoppingCartDB()
productsDB = ProductsDB()
productsInventoryDB = ProductsInventoryDB()
productsDiscountDB = ProductsDiscountDB()


class ShoppingCartService:
    #get shopping cart's all items by userId
    def getCart(self, userId: int) -> PageDataReponseModel[ProductsShoppingCartModel]:
        cartItems = productsShoppingCartDB.queryProductsShoppingCartByUserId(userId)
        items = []
        for cartItem in cartItems:
            unitPrice = max(0, (cartItem.product_price or 0) - (cartItem.discount_price or 0))
            quantity = cartItem.products_quantity or 0
            items.append(ProductsShoppingCartModel(
                product_id=cartItem.product_id,
                products_discount_id=cartItem.products_discount_id,
                products_inventory_id=cartItem.products_inventory_id,
                product_name=cartItem.product_name,
                product_code=cartItem.product_code,
                product_price=cartItem.product_price,
                discount_price=cartItem.discount_price,
                product_img_url=cartItem.product_img_url,
                products_quantity=quantity,
                unit_price=unitPrice,
                products_total_price=unitPrice * quantity,
            ))

        return PageDataReponseModel[ProductsShoppingCartModel](
            items=items,
            total_items=len(items),
            total_pages=1 if items else 0,
            page_number=1,
            page_size=max(len(items), 1),
        )

    #add shopping cart's items
    def addItem(
        self,
        userId: int,
        productId: int,
        quantity: int = 1,
    ) -> PageDataReponseModel[ProductsShoppingCartModel]:
        product = productsDB.getProductById(productId)
        if product is None:
            raise KeyError(productId)
        #get products inventory info
        inventory = productsInventoryDB.getProductInventoryByProductId(productId)
        if inventory is None:
            raise KeyError(productId)
         #get products discount info
        discount = productsDiscountDB.getProductDiscountByProductId(productId)
        discountPrice = discount.discount_price if discount else 0
        unitPrice = max(0, product.product_price - discountPrice)
        productData = ProductsShoppingCartModel(
            product_id=product.id,
            products_discount_id=discount.id if discount else 0,
            products_inventory_id=inventory.id,
            product_name=product.product_name,
            product_code=product.product_code,
            product_price=product.product_price,
            discount_price=discountPrice,
            product_img_url=product.product_img_url,
            products_quantity=quantity,
            unit_price=unitPrice,
            products_total_price=unitPrice * quantity,
        )
        productsShoppingCartDB.addProductsShoppingCartByProductId(userId, productData)
        return self.getCart(userId)

    #update shopping cart's items quantity
    def updateQuantity(
        self,
        userId: int,
        productId: int,
        quantity: int,
    ) -> PageDataReponseModel[ProductsShoppingCartModel]:
        productsShoppingCartDB.updateProductsShoppingCartQuantity(userId, productId, quantity)
        return self.getCart(userId)
    #remove shopping cart's items
    def removeItem(
        self,
        userId: int,
        productId: int,
    ) -> PageDataReponseModel[ProductsShoppingCartModel]:
        productsShoppingCartDB.delProductsShoppingCartByProductId(userId, productId)
        return self.getCart(userId)
