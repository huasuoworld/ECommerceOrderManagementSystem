from fastapi import Query, Depends
from ..CommonUtils import LoggingUtil
from ..Models.ProductsModel import ProductsModel
from ..Models.FrontEndReponseModel import SuccessResponseModel, ErrorResponseException
from .APIGatewayDefine import app, getCurrentUser
from ..Services.ProductsService import ProductsService
from ..Models.UsersModel import UsersModel

productService = ProductsService()

@app.post("/products/createProduct")
async def createProduct(product: ProductsModel):
    LoggingUtil.logger.info(f"Creating product: {product}")
    created_product = productService.create_product(product)
    # Here you can implement your product creation logic, e.g., save the product to a database
    return SuccessResponseModel(data=created_product)

@app.get("/products/listProducts")
async def listProducts(
    page_number: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
):
    LoggingUtil.logger.info("Listing all products")
    product = ProductsModel.model_construct(page_number=page_number, page_size=page_size)
    products = productService.listProducts(product)
    return products

@app.get("/products/listProductsBySellerId")
async def listProductsBySellerId(
    page_number: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1), user: UsersModel = Depends(getCurrentUser)):
    LoggingUtil.logger.info("Listing all products")
    product = ProductsModel.model_construct(page_number=page_number, page_size=page_size, seller_id = user.id)
    products = productService.listProducts(product)
    return products

@app.get("/products/{productID}")
async def getProduct(productID: int):
    LoggingUtil.logger.info(f"Fetching product with ID: {productID}")
    # Validate the productID
    if productID <= 0 or productID > 1000000 or productID is None:
        raise ErrorResponseException(message="Invalid product ID", status=400)
    # Here you can implement your logic to fetch the product from a database
    # For demonstration, let's assume we have a function `get_product_by_id`
    product = productService.getProductById(productID)
    if product:
        return SuccessResponseModel(data=product)
    else:
        raise ErrorResponseException(message="Product not found", status=404)