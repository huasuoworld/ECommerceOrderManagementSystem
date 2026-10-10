from ..Models.ProductsModel import ProductsModel
from ..Models.FrontEndReponseModel import PageDataReponseModel
from ..DBConnects import ProductsDB

productDB = ProductsDB()

class ProductsService:

    # create a new product
    def createProduct(self, productModel: ProductsModel) -> ProductsModel:
        # 
        newProduct = productDB.create_product(productModel)
        return ProductsModel.model_validate(newProduct)

    #get a product by its ID
    def getProductById(self, productID: int) -> ProductsModel:
        product = productDB.getProductById(productID)
        return product

    # list all products with pagination
    def listProducts(self, product: ProductsModel) -> PageDataReponseModel:
        products = productDB.listProducts(product)
        #TODO get product inventory and product discount from data base and add to products list
        #TODO 1. get product inventory from database and add to products list
        #TODO 2. get product discount from database and add to products list
        #TODO 3. return products list with inventory and discount
        return PageDataReponseModel(data=products)
