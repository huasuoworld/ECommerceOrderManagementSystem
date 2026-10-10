from ..CommonUtils import LoggingUtil
from ..Models.ProductsModel import ProductsModel
from ..Models.FrontEndReponseModel import SuccessResponseModel, ErrorResponseModel
from .APIGatewayDefine import app
from ..Services import ProductsService

productService = ProductsService()

@app.post("/products/createProduct")
async def createProduct(product: ProductsModel):
    LoggingUtil.logger.info(f"Creating product: {product}")
    created_product = productService.create_product(product)
    # Here you can implement your product creation logic, e.g., save the product to a database
    return SuccessResponseModel(data=created_product)

@app.get("/products/{productID}")
async def getProduct(productID: int):
    LoggingUtil.logger.info(f"Fetching product with ID: {productID}")
    # Validate the productID
    if productID <= 0 or productID > 1000000 or productID is None:
        return ErrorResponseModel(message="Invalid product ID", error_code=400)
    # Here you can implement your logic to fetch the product from a database
    # For demonstration, let's assume we have a function `get_product_by_id`
    product = productService.getProductById(productID)
    if product:
        return SuccessResponseModel(data=product)
    else:
        return ErrorResponseModel(message="Product not found", error_code=404)

@app.get("/products/listProducts")
async def listProducts(product: ProductsModel):
    LoggingUtil.logger.info("Listing all products")
    # Here you can implement your logic to list all products from a database
    # For demonstration, let's assume we have a function `list_all_products`
    products = productService.listProducts(product)
    return products