from ..Models.ProductsModel import ProductsModel
from ..Models.ProductsDiscountInventoryModel import ProductsDiscountInventoryModel
from ..Models.FrontEndReponseModel import PageDataReponseModel
from ..DBConnects.ProductsDB import ProductsDB
from ..DBConnects.ProductsDiscountDB import ProductsDiscountDB
from ..DBConnects.ProductsInventoryDB import ProductsInventoryDB

productsDB = ProductsDB()
productsDiscountDB = ProductsDiscountDB()
productsInventoryDB = ProductsInventoryDB()

class ProductsService:

    # create a new product
    def createProduct(self, productModel: ProductsModel) -> ProductsModel:
        # 
        newProduct = productsDB.create_product(productModel)
        return ProductsModel.model_validate(newProduct)

    #get a product by its ID
    def getProductById(self, productID: int) -> ProductsModel:
        product = productsDB.getProductById(productID)
        return product

    # list all products with pagination
    def listProducts(self, product: ProductsModel) -> PageDataReponseModel:
        productsPageList = productsDB.listProducts(product)
        if not productsPageList.items:
            return productsPageList
        #get products IDs
        productsIDs = ProductsModel.getProductsIDList(productsPageList)
        #get product inventory from data base 
        productsInventoryPageList = productsInventoryDB.listProductsInventoryByIDs(productsIDs)
        #get product discount from data base 
        productsDiscountPageList = productsDiscountDB.listProductsDiscountByProductsIDs(productsIDs)
        for productsDiscountInventory in productsPageList.items:
            #add productsInventory to productsDiscountInventory list
            for productsInventory in productsInventoryPageList.items:
                if productsDiscountInventory.id == productsInventory.product_id:
                    productsDiscountInventory = productsDiscountInventory.copyProductsInventoryToThisModel(productsInventory, productsDiscountInventory)
            #add productsDiscount to productsDiscountInventory list
            for productsDiscount in productsDiscountPageList.items:
                if productsDiscountInventory.id == productsDiscount.product_id:
                    productsDiscountInventory = productsDiscountInventory.copyProductsDiscountToThisModel(productsDiscount, productsDiscountInventory)

        return productsPageList