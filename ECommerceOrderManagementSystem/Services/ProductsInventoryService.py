from ..DBConnects.ProductsInventoryDB import ProductsInventoryDB

class ProductsInventoryService:
    def __init__(self):
        self.productsInventoryDB = ProductsInventoryDB()