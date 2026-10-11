from .UsersBaseModel import UsersBaseModel

class ProductsOrderPaymentModel(UsersBaseModel):
    products_order_id = int
    users_id = int
    payment_number = str
    payment_channel = str
    payment_type = str
    payment_amount = int
    payment_order_number = str
    payment_status = str
    
    class Config:
                from_attributes = True